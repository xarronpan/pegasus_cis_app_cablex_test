import libs.app.export_declaration.base as base
from .. import config

class Application(base.Application):
    def __init__(self):
        cfg = {}
        base.Application.__init__(self, config.appid, config.locale, cfg)

