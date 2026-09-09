import libs.app.types as types
import libs.app.vat.base as base
from .. import config

_MAX_PRICE_ERROR = 0.003

class Application(base.Application):
    def __init__(self):
        cfg = {}
        base.Application.__init__(self, config.appid, config.locale, cfg)

    def check_header(self, ctx: dict, header: types.Header, order_lines: list[types.OrderLine], options: str) \
        -> tuple[dict[str, str],
                 dict[str, str]]:
        diagnose = {}

        return diagnose, {}

    def check_order_line(self, ctx: dict, header: types.Header, order_line: types.OrderLine, options: str) \
        -> tuple[ str,  # result
                  str   # diagnose
                ]:

        return "succ", ""
