import argparse
from framework.ocr.ocr_api import OcrApi

parser = argparse.ArgumentParser(description="OCR Invoice Parser")
parser.add_argument('--image_path', type=str, 
                    default="/Users/sofianurobert/Downloads/WhatsApp Image 2025-08-12 at 22.19.08.jpeg",
                    help='Path to the invoice image')
args = parser.parse_args()

open_api = OcrApi(image_path=args.image_path)
print(open_api.parse_invoice())
