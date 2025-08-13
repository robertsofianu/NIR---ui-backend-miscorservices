import base64
import json
import os
import re

from framework.ocr.models import \
    BillInfo, Provider, Customer, InvoiceDetail, Totals, Invoice
from openai import OpenAI


class OcrApi:
    def __init__(self, image_path):
        self.image_path = image_path

    API_KEY = os.getenv("OPENAI_API_KEY")
    MODEL_PATH = "/Users/sofianurobert/Projects/go_rect_inv_app/NIR---ui-backend-miscorservices/api_svc/framework/ocr/models/model.json"

    client = OpenAI(api_key=API_KEY)

    def process_image(self):
        with open(self.image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")

    def load_model(self):
        with open(self.MODEL_PATH, "r") as model_file:
            return str(json.load(model_file))

    def create_api_prompt(self):
        return \
            f"Get all the details from this invoice and return them in a JSON format. \
                I need bill info: invoice number and date, also the provider, \
                and all the invoice details, like product, number of products, etc. \
                Give me just the Json nothing else. Use this model: {self.load_model()}."

    def get_invoice_details(self):
        resp = ""
        open_ai_api_prompt = \
            json.loads(self.client.responses.create(
                model="gpt-4.1",
                input=[{"role": "user",
                        "content": [
                            {"type": "input_text", "text": self.create_api_prompt()},
                            {"type": "input_image",
                             "image_url": f"data:image/jpeg;base64,{self.process_image()}",
                             "detail": "auto"
                             }]}]).json())
        try:
            resp = open_ai_api_prompt["output"][0]["content"][0]["text"]
            print("Response received successfully.")
        except TypeError:
            print("Error: Unexpected response format")
            print(open_ai_api_prompt)

        return re.sub(r"^```(?:json)?|```$", "",
                      resp.strip(),
                      flags=re.MULTILINE).strip()

    def parse_invoice(self):
        fetched_invoice_details = json.loads(self.get_invoice_details())

        bill_info = BillInfo(**fetched_invoice_details["bill_info"])
        provider = Provider(**fetched_invoice_details["provider"])
        customer = Customer(**fetched_invoice_details["customer"])
        invoice_detail = [InvoiceDetail(**item) for item in fetched_invoice_details["invoice_details"]]
        totals = Totals(**fetched_invoice_details["totals"])

        return Invoice(
            bill_info=bill_info,
            provider=provider,
            customer=customer,
            invoice_details=invoice_detail,
            totals=totals
        )
