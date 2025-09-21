from datetime import datetime
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

import argparse
from framework.utils.utils import Utils

class OcrService(Utils):
    def __init__(self):
        parser = argparse.ArgumentParser(description="OCR Invoice Parser")
        parser.add_argument('--token', type=str, 
                            help='API token for authentication')
        args = parser.parse_args()
        super().__init__(token=args.token)

    def load_invoice_records(self):
        invoice_details = self.ocr_api.get_invoice_details()
        invoice_details["config"] = {
            "token": self.ocr_api.token,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.no_sql_db.add_json_to_collection("invoices", "invoices", 
                                              invoice_details)

if __name__ == "__main__":
    ocr_service = OcrService()
    ocr_service.load_invoice_records()
