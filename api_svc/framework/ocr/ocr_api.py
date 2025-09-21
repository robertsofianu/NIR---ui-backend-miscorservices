import base64
import json
import os
import re

from framework.ocr.models import \
    BillInfo, Provider, Customer, InvoiceDetail, Totals, Invoice
from openai import OpenAI
from framework.db.no_sql_db import NoSQLDB


class OcrApi:
    def __init__(self, token: str = "", image_path: str = ""):
        self.image_path = image_path
        self.token = token

    API_KEY = os.getenv("OPENAI_API_KEY")
    MODEL_PATH = "framework/ocr/models/model.json"
    IMAGES_DB_NAME = "images"
    IMAGES_COLLECTION_NAME = "images"
    NO_SQL_DB = NoSQLDB()
    
    client = OpenAI(api_key=API_KEY)

    def process_image_from_local_path(self):
        self.image_path = r"/Users/sofianurobert/Desktop/Nir Proj/WhatsApp Image 2025-08-12 at 22.19.08.jpeg"
        with open(self.image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")

    def convert_bytes_to_base64(self, image_bytes: bytes) -> str:
        return base64.b64encode(image_bytes).decode("utf-8")
    
    def process_image_from_token(self) -> None:
        if not self.token:
            raise ValueError("Token must be set before calling this method.")

        resp = list(self.NO_SQL_DB.get_collection_after_token(db_name=self.IMAGES_DB_NAME,
                                                              collection_name=self.IMAGES_COLLECTION_NAME,
                                                              token=self.token))
        return [self.convert_bytes_to_base64(row_image['data']) 
                for row_image in resp]

    def load_model(self) -> str:
        with open(self.MODEL_PATH, "r") as model_file:
            return str(json.load(model_file))

    def create_api_prompt(self) -> str:
        image_collection = self.process_image_from_token()
        if len(image_collection) == 1:
            prompt = f"Get all the details from this invoice and return them in a JSON format. \
                I need bill info: invoice number and date, also the provider, \
                and all the invoice details, like product, number of products, etc. \
                Give me just the Json nothing else. Use this model: {self.load_model()}."
        else:
            prompt = f"""You are given {len(image_collection)} images that together form a single invoice, split across multiple parts. 
                        Extract all invoice details and return them as a single, well-structured JSON object. 
                        Required fields:
                        - Bill info: invoice number and date
                        - Provider details
                        - Customer details
                        - Invoice line items: product name, quantity, price, etc.
                        - Totals

                        Only return the JSON object, nothing else. 
                        Use the following model for the expected output format: {self.load_model()}."""
        return prompt
    
    def create_content_for_multiple_images(self) -> list:
        images = self.process_image_from_token()
        content = [{"type": "input_text", "text": self.create_api_prompt()}]
        for image in images:
            content.append({"type": "input_image", "image_url": f"data:image/jpeg;base64,{image}", "detail": "auto"})
        return content

    def get_invoice_details(self) -> dict:
        resp = ""
        open_ai_api_prompt = \
            json.loads(self.client.responses.create(
                model="gpt-4.1",
                input=[
                    {
                        "role": "user",
                        "content": self.create_content_for_multiple_images()
                    }
                ]).json())
        try:
            resp = open_ai_api_prompt["output"][0]["content"][0]["text"]
            print("Response received successfully.")
        except TypeError:
            print("Error: Unexpected response format")
            print(open_ai_api_prompt)

        return json.loads(re.sub(r"^```(?:json)?|```$", "",
                      resp.strip(), flags=re.MULTILINE).strip())

    def parse_invoice(self) -> Invoice:
        fetched_invoice_details = self.get_invoice_details()

        bill_info = BillInfo(**fetched_invoice_details["bill_info"])
        provider = Provider(**fetched_invoice_details["provider"])
        customer = Customer(**fetched_invoice_details["customer"])
        invoice_detail = [InvoiceDetail(**item) for \
            item in fetched_invoice_details["invoice_details"]]
        totals = Totals(**fetched_invoice_details["totals"])

        return Invoice(
            bill_info=bill_info,
            provider=provider,
            customer=customer,
            invoice_details=invoice_detail,
            totals=totals
        )

if __name__ == "__main__":
    ocr_api = OcrApi(token="3dc5d7ccad555b4e8567831c530f3ebbcfc175be3ea9b30c86df31bb71884683")
