import sciolyid.web
import sciolyid.web.tasks as tasks

from config import config

sciolyid.web.setup(config)
tasks.run_beat(["--loglevel=info"])
