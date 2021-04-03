import logging
import os
import re
from typing import List, Tuple, Optional

import aiohttp
from bs4 import BeautifulSoup
from sciolyid.util import cache
from sentry_sdk import capture_exception

IMAGES_PER_DOWNLOAD = 5  # probably don't change this over 15, only tested with 5
BASE_URL = "https://www.mindat.org"
CONTENT_TYPE_LOOKUP = {"image/png": "png", "image/jpeg": "jpg"}

# extract mineral id from /min-##.html
mineral_id_regex = re.compile(r"\/min-(\d+)\.html")
# extract page numbers
page_number_regex = re.compile(r"Page (\d+) of (\d+)")

logger = logging.getLogger("minerobo")


async def get_images(data, category, item):
    logger.info(f"downloading images for {item}")
    if category is None or item is None:
        return
    directory = f"bot_files/images/{category}/{item}/"
    os.makedirs(directory, exist_ok=True)
    if len(os.listdir(directory)) != 0:
        logger.info("images already exist!")
    index = int(data.database.zscore("image.index:global", item) or 0)
    async with aiohttp.ClientSession() as session:
        mineral_id = await get_mineral_id(item, session)
        if mineral_id:
            if mineral_id == 8573:  # hardcode alternate satin spar images for now
                index, urls = await satin_spar()
            else:
                index, urls = await get_urls_by_mineral_id(session, mineral_id, index)
        else:
            index, urls = await get_urls_by_photoscroll(session, item, index)
        await download_images(session, urls, directory)
    data.database.zadd("image.index:global", {item: index})


@cache()
async def get_mineral_id(item: str, session: aiohttp.ClientSession) -> Optional[int]:
    """Return Mindat's ID for the specimen."""

    async with session.head(f"{BASE_URL}/search.php?name={item}") as resp:
        match = mineral_id_regex.match(resp.headers.get("location", ""))
        if match:
            return int(match.group(1))
        return None


async def satin_spar():
    return (
        0,
        (
            "https://www.minerals.net/MineralImages/gypsum7.jpg",
            "https://www.minerals.net/MineralImages/gypsum-satin-spar-france.jpg",
        ),
    )


async def get_urls_by_mineral_id(
    session: aiohttp.ClientSession, mineral_id: int, index: int
) -> Tuple[int, Tuple[str, ...]]:
    """Return URLS of images of the specimen to download.

    This method uses mindat.org's "gallery" page to download images.
    "gallery" will search by mineral id, which may not exist for all
    list specimens. In that case, use `get_urls_by_photoscroll`. However,
    this method will only make one request, while the other may use more.

    `index` is the index of the first image to download (0-indexed).
    This function returns up to IMAGES_PER_DOWNLOAD number of images.
    The new index is returned as the first element of the tuple.
    """

    # calculate the page we need to go to, 20 per page
    page = (index // 20) + 1
    async with session.get(
        f"{BASE_URL}/gallery.php?min={mineral_id}&cf_pager_page={page}"
    ) as resp:
        text = await resp.text()

    soup = BeautifulSoup(text, "lxml")
    raw_image_urls = tuple(
        map(lambda x: BASE_URL + x.find("img")["src"], soup(class_="userbigpicture"))
    )
    match_page = page_number_regex.match(
        soup.find(class_="pnpagecount").find("b").string
    )
    if not match_page:
        raise ValueError("No page number found!")
    current_page = int(match_page.group(1))
    total_pages = int(match_page.group(2))

    image_urls = raw_image_urls[index % 20 : (index % 20) + IMAGES_PER_DOWNLOAD]
    index += IMAGES_PER_DOWNLOAD
    if len(image_urls) < IMAGES_PER_DOWNLOAD:
        image_urls = raw_image_urls[-IMAGES_PER_DOWNLOAD:]
        if current_page >= total_pages:
            index = 0
    if index % 20 == 0 and current_page >= total_pages:
        index = 0

    return (index, image_urls)


async def get_urls_by_photoscroll(
    session: aiohttp.ClientSession, specimen_name: str, index: int
) -> Tuple[int, Optional[Tuple[str, ...]]]:
    """Return URLS of images of the specimen to download.

    This method uses mindat.org's "photoscroll" page to download
    images. "photoscroll" will search mindat by mineral name (if
    found) or keyword (if the mineral name is invalid). However,
    this method uses more requests. Specifically, 1 request if index
    is less than 50, and additional (up to 2) requests per 15 index,
    up to the number of images mindat has.

    `index` is the index of the first image to download (0-indexed).
    This function returns up to IMAGES_PER_DOWNLOAD number of images.
    The new index is returned as the first element of the tuple.
    """
    # calculate the page we need to go to, 50 on first page, 15 per page after
    pages = 1 if index < 50 else ((index - 50) // 15) + 2
    if pages == 1:
        async with session.get(
            f"{BASE_URL}/photoscroll.php?searchbox={specimen_name}"
        ) as resp:
            text = await resp.text()
        soup = BeautifulSoup(text, "lxml")
        raw_image_urls = tuple(
            map(lambda x: BASE_URL + x["src"], soup.find(id="photoscroll")("img"))
        )
    else:
        async with session.head(
            f"{BASE_URL}/photoscroll.php?searchbox={specimen_name}"
        ):
            pass
        for _ in range(pages - 2):
            async with session.head(BASE_URL + "/photoscroll.php?id=1"):
                pass
        async with session.get(BASE_URL + "/photoscroll.php?id=1") as resp:
            text = await resp.text()
            if not text:
                return (0, None)
        soup = BeautifulSoup(text, "lxml")
        raw_image_urls = tuple(map(lambda x: BASE_URL + x["src"], soup("img")))

    offset = index if index < 50 else (index - 50) % 15
    image_urls = raw_image_urls[offset : offset + 5]
    index += IMAGES_PER_DOWNLOAD
    if len(image_urls) < IMAGES_PER_DOWNLOAD:
        image_urls = raw_image_urls[-IMAGES_PER_DOWNLOAD:]

    if index < 50 or (index - 50) % 15 == 0:
        async with session.get(BASE_URL + "/photoscroll.php?id=1") as resp:
            text = await resp.text()
            if not text:
                index = 0

    return (index, image_urls)


async def download_images(
    session: aiohttp.ClientSession, urls: Tuple[str, ...], directory: str
):
    """Manages image downloads."""
    for path, url in zip(map(lambda x: f"{directory}{x}.", range(len(urls))), urls):
        try:
            async with session.get(url) as resp:
                with open(
                    path
                    + CONTENT_TYPE_LOOKUP[resp.headers["content-type"].split(";")[0]],
                    "wb",
                ) as f:
                    while True:
                        block = await resp.content.read(1024 * 8)
                        if not block:
                            break
                        f.write(block)
        except aiohttp.ClientError as e:
            capture_exception(e)
            logger.info(f"Client error occurred while downloading {url}")
