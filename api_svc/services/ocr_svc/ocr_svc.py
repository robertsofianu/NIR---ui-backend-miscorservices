from framework.ocr.ocr_api import OcrApi

open_api = OcrApi(image_path="/Users/sofianurobert/Downloads/WhatsApp Image 2025-08-12 at 22.19.08.jpeg")
print(open_api.parse_invoice())
