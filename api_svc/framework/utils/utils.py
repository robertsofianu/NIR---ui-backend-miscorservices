from framework.db.no_sql_db import NoSQLDB
from framework.ocr.ocr_api import OcrApi

class Utils:
    def __init__(self, image_path: str = ""):
        self.image_path = image_path
        self.no_sql_db = NoSQLDB()
        if image_path:
            self.ocr_api = OcrApi(image_path=image_path)
        self.user = 'default_user'