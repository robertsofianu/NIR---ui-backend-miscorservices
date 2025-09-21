from framework.db.no_sql_db import NoSQLDB
from framework.ocr.ocr_api import OcrApi

class Utils:
    def __init__(self, image_path: str = "", token: str = ""):
        self.image_path = image_path
        self.no_sql_db = NoSQLDB()
        if token:
            self.ocr_api = OcrApi(image_path=image_path, token=token)
        self.user = 'default_user'