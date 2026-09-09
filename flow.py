import libs.flow.match_invoice as match_invoice
import sys
import threading
from . import config

if __name__ == "__main__":
    if len(sys.argv) <= 1:
        print("param is invalid")
        exit(1)

    match_invoice_wfs = match_invoice.WorkFlows(config.appid)

    if sys.argv[1] == "match_invoice":
        match_invoice_wfs.match_invoices()
    elif sys.argv[1] == "serve":

        match_invoice_thread = threading.Thread(target=match_invoice_wfs.serve, args=(2,))
        match_invoice_thread.start()

        match_invoice_thread.join()
    else:
        print("param is invalid")
        exit(1)
