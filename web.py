import sciolyid.web

from config import config

sciolyid.web.setup(config)

app = sciolyid.web.get_app()
