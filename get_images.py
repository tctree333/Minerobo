import os
import re
from typing import List, Tuple

import aiohttp
from bs4 import BeautifulSoup

BASE_URL = "https://www.mindat.org"
CONTENT_TYPE_LOOKUP = {"image/png": "png", "image/jpeg": "jpg"}
mineral_id_regex = re.compile(r"\/min-(\d+)\.html")
page_number_regex = re.compile(r"Page (\d+) of (\d+)")

async def get_images(data, category, item):
    data.logger.info(f"downloading images for {item}")
    if category is None or item is None:
        return
    directory = f"bot_files/images/{category}/{item}/"
    os.makedirs(directory)
    if len(os.listdir(directory)) != 0:
        data.logger.info("images already exist!")
    index = int(data.database.zscore("image.index:global", item) or 0)
    async with aiohttp.ClientSession() as session:
        mineral_id = await get_mineral_id(session, item)
        new_index, urls = await get_urls(session, mineral_id, index)
        await download_images(data.logger, session, urls, directory)
    data.database.zadd("image.index:global", {item: index})

async def get_mineral_id(session: aiohttp.ClientSession, item: str) -> int:
    """Return Mindat's ID for the specimen."""
    async with session.head(f"{BASE_URL}/search.php?name={item}") as resp:
        match = mineral_id_regex.match(resp.headers["location"])
        if match:
            return int(match.group(1))
        raise ValueError(f"Mineral ID not found for {item}!")


async def get_urls(
    session: aiohttp.ClientSession, mineral_id: int, index: int
) -> Tuple[int, Tuple[str, ...]]:
    """Return URLS of images for the specimen to download."""
    page = (index // 20) + 1
    async with session.get(
        f"{BASE_URL}/gallery.php?min={mineral_id}&cf_pager_page={page}"
    ) as resp:
        text = await resp.text()

    soup = BeautifulSoup(text, "lxml")
    raw_image_urls = tuple(map(lambda x: BASE_URL + x.find("img")["src"], soup(class_="userbigpicture")))
    match_page = page_number_regex.match(soup.find(class_="pnpagecount").find("b").string)
    if not match_page:
        raise ValueError("No page number found!")
    current_page = int(match_page.group(1))
    total_pages = int(match_page.group(2))

    image_urls = raw_image_urls[index % 20:(index%20)+5]
    index += 5
    if len(image_urls) < 5:
        image_urls = raw_image_urls[-5:]
        if current_page >= total_pages:
            index = 0
    if index % 20 == 0 and current_page >= total_pages:
        index = 0

    return (index, image_urls)


async def download_images(logger, session: aiohttp.ClientSession, urls: Tuple[str, ...], directory: str):
    """Manages image downloads."""
    for path, url in zip(map(lambda x: f"{directory}{x}.", range(len(urls))), urls):
        try:
            async with session.get(url) as resp:
                with open(path + CONTENT_TYPE_LOOKUP[resp.headers["content-type"].split(";")[0]], "wb") as f:
                    while True:
                        block = await resp.content.read(
                            1024 * 8
                        )
                        if not block:
                            break
                        f.write(block)
        except aiohttp.ClientError:
            logger.info(f"Client error occurred while downloading {url}")
