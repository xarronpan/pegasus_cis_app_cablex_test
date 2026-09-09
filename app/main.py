import libs.app.main.main as main
from .. import config

class Application(main.Application):

    def __init__(self):
        cfg = {}
        main.Application.__init__(self, config.appid, config.locale, cfg)

    def get_doc_types(self):
        return [
            {"type": "vat", "name": "增值税发票"},
            {"type": "export_declaration", "name": "报关单"},
        ]

    def get_smtp_send_email_config(self) -> dict|None:
        return {
            "email_addr": config.email_addr,
            "smtp_host": config.smtp_host,
            "smtp_password": config.email_pwd,
            "write_to_sent_mailbox": False,
            "sent_mailbox": "Sent Messages",
            "imap_host": config.imap_host,
            "imap_password": config.email_pwd,
        }

    def get_msgraph_send_email_config(self) -> dict|None:
        return None
