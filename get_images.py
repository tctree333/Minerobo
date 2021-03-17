import os
import shutil

async def get_images(category, item):
    os.makedirs(f"bot_files/images/{category}/{item}/")
    shutil.copyfile("bot_files/images/test.png", f"bot_files/images/{category}/{item}/test.png")