import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

import argparse
from framework.utils.utils import Utils

class OcrService(Utils):
    def __init__(self):
        parser = argparse.ArgumentParser(description="OCR Invoice Parser")
        parser.add_argument('--image_path', type=str, 
                            default="/Users/sofianurobert/Downloads/WhatsApp Image 2025-08-12 at 22.19.08.jpeg",
                            help='Path to the invoice image')
        args = parser.parse_args()
        super().__init__(image_path=args.image_path)

    def load_invoice_records(self):
        invoice_details = self.ocr_api.get_invoice_details()
        invoice_details["config"] = {
            "user": self.user,
            "is_active": True
        }
        self.no_sql_db.add_json_to_collection("invoices", "invoices", 
                                              invoice_details)

if __name__ == "__main__":
    ocr_service = OcrService()
    ocr_service.load_invoice_records()
