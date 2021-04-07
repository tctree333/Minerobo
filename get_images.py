import logging
import os
import shutil
import time
from typing import Tuple

import aiohttp
from sentry_sdk import capture_exception

import mindat

CONTENT_TYPE_LOOKUP = {"image/png": "png", "image/jpeg": "jpg"}

MAX_IMAGES_SAVED = 20
CYCLE_DOWNLOAD_COUNT = 2
FIRST_DOWNLOAD_COUNT = 5

logger = logging.getLogger("minerobo")


async def get_images(data, category, item):
    logger.info(f"downloading images for {item}")
    if category is None or item is None:
        return
    directory = f"bot_files/images/{category}/{item}/"
    os.makedirs(directory, exist_ok=True)

    count = CYCLE_DOWNLOAD_COUNT

    existing_files_count = len(os.listdir(directory))
    if existing_files_count < MAX_IMAGES_SAVED:
        count = FIRST_DOWNLOAD_COUNT

    index = int(data.database.zscore("image.index:global", item) or 0)
    async with aiohttp.ClientSession() as session:
        new_index, urls = await mindat.get_urls(session, item, index, count, existing_files_count == 0)

        if existing_files_count >= MAX_IMAGES_SAVED:
            index = new_index
            await download_images(session, urls, directory)
        elif len(urls) != 0:
            index += len(urls)
            await download_images(session, urls, directory)
    data.database.zadd("image.index:global", {item: index})

    # remove extra images
    directory_files = os.listdir(directory)
    extra = len(directory_files) - MAX_IMAGES_SAVED
    if extra > 0:
        for image in tuple(sorted(directory_files))[:extra]:
            os.remove(directory + image)


async def download_images(
    session: aiohttp.ClientSession, urls: Tuple[str, ...], directory: str
):
    """Manages image downloads."""
    logger.info("downloading images")
    for i, url in enumerate(urls):
        try:
            async with session.get(url) as resp:
                # have a time and index based filename for sorting purposes
                # uses midnight April 1st, 2021 UTC+00 as epoch
                path = f"{directory}{round((time.time()-1617235200) * 100000000)+i}."
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
