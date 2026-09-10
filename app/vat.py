import libs.app.types as types
import libs.app.vat.base as base
import unicodedata
from .. import config

_MAX_PRICE_ERROR = 0.003

class Application(base.Application):
    def __init__(self):
        cfg = {}
        base.Application.__init__(self, config.appid, config.locale, cfg)

    def normalize_text(self, orgin_text):
        normalized = unicodedata.normalize("NFKC", orgin_text)
        for c in [" "]:
            normalized = normalized.replace(c, "")

        return normalized

    def check_header(self, ctx: dict, header: types.Header, order_lines: list[types.OrderLine], options: str) \
        -> tuple[dict[str, str],
                 dict[str, str]]:
        diagnose = {}

        export_declaration_docs = self.find_all_documents("export_declaration", {}, 0, 1, "create_time")
        if len(export_declaration_docs) == 0:
            diagnose["buyer_name"] = diagnose.get("buyer_name","") + "找不到对应的报关单\n"
            diagnose["buyer_tax_id"] = diagnose.get("buyer_tax_id","") + "找不到对应的报关单\n"
        else:
            doc = export_declaration_docs[0]
            if doc["status"] != "submitted":
                pre_entry_number = header["extentions"]["pre_entry_number"]
                diagnose["buyer_name"] = diagnose.get("buyer_name","") +\
                    f"报关单未提交, 报关单预录入编码: {pre_entry_number}\n"
                diagnose["buyer_tax_id"] = diagnose.get("buyer_tax_id","") +\
                    f"报关单未提交, 报关单预录入编码: {pre_entry_number}\n"
            else:
                doc_content = self.get_document_invoice_content(doc["email_id"], doc["filename"], doc["sheet"])

                buyer_name = header["extentions"]["buyer_name"]
                buyer_tax_id = header["extentions"]["buyer_tax_id"]
                domestic_consignor = doc_content["header"]["extentions"]["domestic_consignor"]
                domestic_consignor_code = doc_content["header"]["extentions"]["domestic_consignor_code"]
                if (self.normalize_text(buyer_name) != self.normalize_text(domestic_consignor)):
                    diagnose["buyer_name"] = diagnose.get("buyer_name","") +\
                        f"销售方名称 {buyer_name} 与报关单境内发货人 {domestic_consignor} 不一致, 报关单预录入编码: {pre_entry_number}\n"

                if buyer_tax_id.strip() != domestic_consignor_code.strip():
                    diagnose["buyer_tax_id"] = diagnose.get("buyer_tax_id","") +\
                        f"销售方识别号 {buyer_tax_id} 与报关单境内发货人代码 {domestic_consignor_code} 不一致, 报关单预录入编码: {pre_entry_number}\n"

        return diagnose, {}

    def check_order_line(self, ctx: dict, header: types.Header, order_line: types.OrderLine, options: str) \
        -> tuple[ str,  # result
                  str   # diagnose
                ]:

        return "succ", ""
