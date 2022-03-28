import os
from typing import Dict, Any

# from get_images import get_images

config: Dict[str, Any] = {
    "bot_description": "Minerobo - A SciOly Discord Bot for Rock and Mineral ID",  # short bot description
    "bot_signature": "Minerobo - A Rock and Mineral ID Bot",  # signature for embeds
    "prefixes": ["r.", "R."],  # bot prefixes, primary prefix is first in list
    "id_type": "rocks",  # stars, fossils, muscles, etc. - plural noun
    "github_image_repo_url": None,  # link to github image repo
    "support_server": "https://discord.gg/2HbshwGjnm",  # link to discord support server
    "source_link": "placeholder",  # link to source code (may be hosted on github)
    "name": "minerobo",  # all lowercase, no spaces, doesn't really matter what this is
    # "members_intent": False,  # whether the privileged members intent is enabled in the developer portal
    # "download_func": get_images,  # asyncronous function that downloads images locally to download_dir
    # "refresh_images": False,  # whether to run download_func once every 24 hours with None as an argument
    # "evict_images": True,  # whether to delete items from download_dir
    # "evict_frequency": 10.0,  # how often to run eviction function
    # "evict_threshold": 20,  # the number of times a specimen is seen before eviction
    # "max_evict": 1,  # how many specimens to evict at a time
    # "evict_func": get_images,  # function to run during eviction
    "download_dir": "images/",  # local directory containing media (images)
    # "data_dir": "data/",  # local directory containing the id data
    "group_dir": "categories/",  # directory within data_dir containing group lists
    # "state_dir": "state/",  # directory within data_dir containing alternate lists
    # "default_state_list": "NATS",  # name of the "state" that should be considered default
    # "wikipedia_file": "wikipedia.txt",  # filename within data_dir containing wiki urls for every item
    "prompt_file": "prompt.txt",
    # "meme_file": None,
    # "logs": True,  # enable logging
    # "log_dir": "logs/",  # directory for text logs/backups
    "bot_files_dir": "bot_files",  # folder for bot generated files (downloaded images, logs)
    "short_id_type": "r",  # short (usually 1 letter) form of id_type, used as alias for the pic command
    "invite": "https://discord.com/api/oauth2/authorize?client_id=821143596232474684&permissions=51200&scope=bot",  # bot server invite link
    "authors": "person_v1.32",  # creator names
    "extra_about_fields": [
        {
            "name": "Privacy Policy",
            "value": "By using this bot, you agree to our [Privacy Policy](https://sciolyid.org/privacy/).",
        },
        {
            "name": "Attribution",
            "value": "See https://sciolyid.org/minerobo/attribution/ for image sources.",
        },
    ],  # list of dicts containing keys "name" and "value" to be added to the botinfo command
    "category_name": "specimen category",  # space thing, bird order, muscle group - what you are splitting groups by
    "category_aliases": {  # aliases for categories
        "native elements": ["native", "elements"],
        "(hydr)oxides": [
            "hydroxides",
            "oxides",
            "hydroxides/oxides",
            "hydroxide",
            "oxide",
        ],
        "sandstone varieties": ["sandstone"],
        "gypsum varieties": ["gypsum"],
        "amphibole group": ["amphibole"],
        "feldspar - plagioclase": ["plagioclase"],
        "feldspar - potassium": ["potassium"],
        "garnet group": ["garnet"],
        "mica group": ["mica"],
        "pyroxene group": ["pyroxene"],
        "quartz varieties": ["quartz"],
        "coal varieties": ["coal"],
        "schist varieties": ["schist"],
        "limestone varieties": ["limestone"],
        "silicates": ["silicate"],
        "sulfides": ["sulfide"],
        "sulfates": ["sulfate"],
    },
    # "disable_extensions": [],  # bot extensions to disable (media, check, skip, hint, score, sessions, race, other)
    # "custom_extensions": [],  # custom bot extensions to enable
    "sentry": True,  # enable sentry.io error tracking
    "local_redis": False,  # use a local redis server instead of a remote url
    "bot_token_env": "BOT_TOKEN",  # name of environment variable containing the discord bot token
    # "sentry_dsn_env": "SENTRY_DISCORD_DSN",  # name of environment variable containing the sentry dsn
    "redis_env": "REDIS_URL",  # name of environment variable containing the redis database url
    "backups_channel": None,  # discord channel id to upload database backups (None/False to disable)
    # "backups_dir": "backups/",  # directory to put database backup files before uploading
    "holidays": True,  # enable special features on select holidays
    "sendas": True,  # enable the "sendas" command
    ### WEB STUFF
    "client_id": 821143596232474684,  # discord client id
    # "base_image_url": None,  # root of where images are hosted
    # "validation_repo_url": None,  # github repo where images are temporarily held
    # "tmp_upload_dir": "uploaded/",  # directory for temporary file storage
    # "validation_local_dir": "validation_repo/",  # directory for cloning the validation repo
    "git_token_env": "GIT_TOKEN",  # environment variable with github auth token
    "git_user_env": "GIT_USERNAME",  # environment variable with github auth token
    # "git_email_env": "GIT_EMAIL",  # environment variable with github auth token
    # "validation_repo_dir": "",  # directory in validation repo to store files
    # "hashes_url": [],  # urls to raw hashes.csv file in both image repos
    # "ids_url": [],  # urls to raw ids.csv file in both image repos
    # "commit_url_format": [],  # a format string for commit urls to both repos - image repo is first, validation repo is second
    # "sentry_web_dsn_env": "SENTRY_API_DSN",  # name of environment variable containing the sentry dsn
    # "celery_broker_env": "CELERY_BROKER_URL",  # name of environment variable with the database url for celery (broker)
    # "secret_key_env": "FLASK_SECRET_KEY",  # name of environment variable for signed cookies secret key
    # "frontend_url_env": "FRONTEND_URL",  # name of environment variable for frontend url
    # "client_secret_env": "DISCORD_CLIENT_SECRET",  # name of environment variable for discord client secret
    # "discord_webhook_env": "DISCORD_WEBHOOK_URL",  # webhook url for discord notification log
    "discord_webhook_disable": [
        "verify"
    ],  # types of webhooks to disable ("add", "verify", "valid", "error")
    # "verification_server": None,  # invite to special discord server for people adding images, default to support server
    "disable_upload": True,  # disable user uploads
    # "disable_validation": False,  # disable validation
    # "validation_thresholds": {  # number of flags of each type to move the image on during validation
    #     "invalid": 3,
    #     "duplicate": 3,
    #     "valid": 3,
    # },
}

user: str = config["git_user_env"]
token: str = config["git_token_env"]

config["github_image_repo_url"] = "https://{}:{}@github.com/{}/{}".format(
    os.getenv(user),
    os.getenv(token),
    os.getenv(user),
    "Minerobo-Images",
)
config["validation_repo_url"] = "https://{}:{}@github.com/{}/{}".format(
    os.getenv(user),
    os.getenv(token),
    os.getenv(user),
    "Unverified-Minerobo-Images",
)
config["base_image_url"] = "https://{}:{}@raw.githubusercontent.com/{}/{}/main/".format(
    os.getenv(user),
    os.getenv(token),
    os.getenv(user),
    "Minerobo-Images",
)
config["hashes_url"] = [
    "https://{}:{}@raw.githubusercontent.com/{}/{}/main/hashes.csv".format(
        os.getenv(user),
        os.getenv(token),
        os.getenv(user),
        "Minerobo-Images",
    ),
    "https://{}:{}@raw.githubusercontent.com/{}/{}/main/hashes.csv".format(
        os.getenv(user),
        os.getenv(token),
        os.getenv(user),
        "Unverified-Minerobo-Images",
    ),
]
config["ids_url"] = [
    "https://{}:{}@raw.githubusercontent.com/{}/{}/main/ids.csv".format(
        os.getenv(user),
        os.getenv(token),
        os.getenv(user),
        "Minerobo-Images",
    ),
    "https://{}:{}@raw.githubusercontent.com/{}/{}/main/ids.csv".format(
        os.getenv(user),
        os.getenv(token),
        os.getenv(user),
        "Unverified-Minerobo-Images",
    ),
]
