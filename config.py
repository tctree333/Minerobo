config = {
    "bot_description": "Minerobo - A SciOly Discord Bot for Rock and Mineral ID",  # short bot description
    "bot_signature": "Minerobo ID - A Rock and Mineral ID Bot",  # signature for embeds
    "prefixes": ["r.", "R."],  # bot prefixes, primary prefix is first in list
    "id_type": "rocks",  # stars, fossils, muscles, etc. - plural noun
    "github_image_repo_url": None,  # link to github image repo
    "support_server": "https://discord.gg/j4HSrrmHpK",  # link to discord support server
    "source_link": "placeholder",  # link to source code (may be hosted on github)
    "name": "minerobo",  # all lowercase, no spaces, doesn't really matter what this is
    # "members_intent": False,  # whether the privileged members intent is enabled in the developer portal
    # "download_func": None,  # asyncronous function that downloads images locally to download_dir
    # "download_dir": "github_download/",  # local directory containing media (images)
    # "data_dir": "data/",  # local directory containing the id data
    "group_dir": "categories/",  # directory within data_dir containing group lists
    # "state_dir": "state/",  # directory within data_dir containing alternate lists
    # "default_state_list": "NATS",  # name of the "state" that should be considered default
    # "wikipedia_file": "wikipedia.txt",  # filename within data_dir containing wiki urls for every item
    # "meme_file": None,
    # "logs": True,  # enable logging
    # "log_dir": "logs/",  # directory for text logs/backups
    "bot_files_dir": "bot_files",  # folder for bot generated files (downloaded images, logs)
    "short_id_type": "min",  # short (usually 1 letter) form of id_type, used as alias for the pic command
    "invite": "https://discord.com/api/oauth2/authorize?client_id=821143596232474684&permissions=51200&scope=bot",  # bot server invite link
    "authors": "person_v1.32",  # creator names
    "category_name": "specimen category",  # space thing, bird order, muscle group - what you are splitting groups by
    "category_aliases": {  # aliases for categories
        "native elements": ["native"],
        "(hydr)oxides": ["hydroxides", "oxides", "hydroxides/oxides"],
        "gypsum varieties": ["gypsum"],
        "amphibole group": ["amphibole"],
        "feldspar - plagioclase": ["plagioclase"],
        "feldspar - pottasium": ["pottasium"],
        "garnet group": ["garnet"],
        "mica group": ["mica"],
        "pyroxine group": ["pyroxine"],
        "quartz varieties": ["quartz"],
        "coal varieties": ["coal"],
        "limestone varieties": ["limestone"],
    },
    # "disable_extensions": [],  # bot extensions to disable (media, check, skip, hint, score, sessions, race, other)
    # "custom_extensions": [],  # custom bot extensions to enable
    "sentry": False,  # enable sentry.io error tracking
    "local_redis": True,  # use a local redis server instead of a remote url
    # "bot_token_env": "token",  # name of environment variable containing the discord bot token
    # "sentry_dsn_env": "SENTRY_DISCORD_DSN",  # name of environment variable containing the sentry dsn
    # "redis_env": "REDIS_URL",  # name of environment variable containing the redis database url
    "backups_channel": 820738627599728658,  # discord channel id to upload database backups (None/False to disable)
    # "backups_dir": "backups/",  # directory to put database backup files before uploading
    "holidays": True,  # enable special features on select holidays
    "sendas": True,  # enable the "sendas" command

    ### WEB STUFF
    # "client_id": 821143596232474684,  # discord client id
    # "base_image_url": None,  # root of where images are hosted
    # "validation_repo_url": None,  # github repo where images are temporarily held
    # "tmp_upload_dir": "uploaded/",  # directory for temporary file storage
    # "validation_local_dir": "validation_repo/",  # directory for cloning the validation repo
    # "git_token_env": "GIT_TOKEN",  # environment variable with github auth token
    # "git_user_env": "GIT_USERNAME",  # environment variable with github auth token
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
    # "verification_server": None,  # invite to special discord server for people adding images, default to support server
}