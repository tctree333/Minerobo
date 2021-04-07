import logging
import os
import random
import re
import time
from typing import List, Tuple, Optional

import aiohttp
from bs4 import BeautifulSoup
from sciolyid.util import cache


IMAGES_PER_DOWNLOAD = 5  # probably don't change this over 15, only tested with 5
BASE_URL = "https://www.mindat.org"


# extract mineral id from /min-##.html
mineral_id_regex = re.compile(r"\/min-(\d+)\.html")
# extract page numbers
page_number_regex = re.compile(r"Page (\d+) of (\d+)")

logger = logging.getLogger("minerobo")


# async def get_images(
#     index: int, category: str, item: str, count: int = IMAGES_PER_DOWNLOAD
# ):
#     logger.info(f"downloading mindat images for {item}")
#     if category is None or item is None:
#         return
#     directory = f"bot_files/images/{category}/{item}/"
#     os.makedirs(directory, exist_ok=True)
#     if len(os.listdir(directory)) != 0:
#         logger.info("images already exist!")
#     async with aiohttp.ClientSession() as session:
#         index, urls = await get_urls(session, item, index, count)
#         await download_images(session, urls, directory)
#     return index


async def get_urls(
    session: aiohttp.ClientSession,
    item: str,
    index: int,
    count: int = IMAGES_PER_DOWNLOAD,
    force: bool = True,
) -> Tuple[int, Tuple[str, ...]]:
    mineral_id = await get_mineral_id(item, session)
    if mineral_id:
        return await get_urls_by_mineral_id(session, mineral_id, index, count, force)
    else:
        return await get_urls_by_photoscroll(session, item, index, count, force)


@cache()
async def get_mineral_id(item: str, session: aiohttp.ClientSession) -> Optional[int]:
    """Return Mindat's ID for the specimen."""

    async with session.head(f"{BASE_URL}/search.php?name={item}") as resp:
        match = mineral_id_regex.match(resp.headers.get("location", ""))
        if match:
            return int(match.group(1))
        return None


async def get_urls_by_mineral_id(
    session: aiohttp.ClientSession,
    mineral_id: int,
    index: int,
    images_to_download: int,
    force: bool = True,
) -> Tuple[int, Tuple[str, ...]]:
    """Return URLS of images of the specimen to download.

    This method uses mindat.org's "gallery" page to download images.
    "gallery" will search by mineral id, which may not exist for all
    list specimens. In that case, use `get_urls_by_photoscroll`. However,
    this method will only make one request, while the other may use more.

    `index` is the index of the first image to download (0-indexed).
    This function returns up to `images_to_download` number of images.
    The new index is returned as the first element of the tuple.
    """

    # calculate the page we need to go to, 20 per page
    page = (index // 20) + 1
    async with session.get(
        f"{BASE_URL}/gallery.php?min={mineral_id}&cf_pager_page={page}"
    ) as resp:
        text = await resp.text()

    soup = BeautifulSoup(text, "lxml")
    if soup.find(string="No photos found"):
        return (0, tuple())
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

    if current_page > total_pages:
        return (0, tuple())

    image_urls = raw_image_urls[index % 20 : (index % 20) + images_to_download]
    index += images_to_download
    if len(image_urls) < images_to_download:
        if force:
            image_urls = raw_image_urls[-images_to_download:]
        if current_page >= total_pages:
            index = 0
    if index % 20 == 0 and current_page >= total_pages:
        index = 0

    return (index, image_urls)


async def get_urls_by_photoscroll(
    session: aiohttp.ClientSession,
    specimen_name: str,
    index: int,
    images_to_download: int,
    force: bool = True,
) -> Tuple[int, Tuple[str, ...]]:
    """Return URLS of images of the specimen to download.

    This method uses mindat.org's "photoscroll" page to download
    images. "photoscroll" will search mindat by mineral name (if
    found) or keyword (if the mineral name is invalid). However,
    this method uses more requests. Specifically, 1 request if index
    is less than 50, and additional (up to 2) requests per 15 index,
    up to the number of images mindat has.

    `index` is the index of the first image to download (0-indexed).
    This function returns up to `images_to_download` number of images.
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
                return (0, tuple())
        soup = BeautifulSoup(text, "lxml")
        raw_image_urls = tuple(map(lambda x: BASE_URL + x["src"], soup("img")))

    offset = index if index < 50 else (index - 50) % 15
    image_urls = raw_image_urls[offset : offset + images_to_download]
    index += images_to_download
    if force and len(image_urls) < images_to_download:
        image_urls = raw_image_urls[-images_to_download:]

    if image_urls[-1] == raw_image_urls[-1]:
        async with session.get(BASE_URL + "/photoscroll.php?id=1") as resp:
            text = await resp.text()
            if not text:
                index = 0

    return (index, image_urls)
