# import json
# from openai import OpenAI
# import base64
# import re
# from framework.ocr.models import BillInfo, Provider, Customer, InvoiceDetail, Totals, Invoice

# client = OpenAI(api_key=api_key)

# with open(local_image_path, "rb") as image_file:
#     image_base64 = base64.b64encode(image_file.read()).decode("utf-8")

# with open(MODEL_PATH, "r") as model_file:
#     model_json = str(json.load(model_file))

# response = client.responses.create(
#     model="gpt-4.1",
#     input=[
#         {
#             "role": "user",
#             "content": [
#                 {"type": "input_text", "text": f"Get all the details from this invoice and return them in a JSON format. \
#                     I need bill info: invoice number and date, also the provider, and all the invoice details, like product, number of products, etc. \
#                         Give me just the Json nothing else. Use this model: {model_json} and if discounted price is present use that one instead of the actual price."},
#                 {
#                     "type": "input_image",
#                     "image_url": f"data:image/jpeg;base64,{image_base64}",
#                     "detail": "auto"
#                 }
#             ]
#         }
#     ]
# )

# response_json = json.loads(response.json())
# response_text = response_json["output"][0]["content"][0]["text"]

# cleaned = re.sub(r"^```(?:json)?|```$", "", response_text.strip(), flags=re.MULTILINE).strip()

# # Now parse
# invoice_from_dict = json.loads(cleaned)
# print(invoice_from_dict)
# bill_info = BillInfo(**invoice_from_dict["bill_info"])
# provider = Provider(**invoice_from_dict["provider"])
# customer = Customer(**invoice_from_dict["customer"])
# invoice_details = [InvoiceDetail(**item) for item in invoice_from_dict["invoice_details"]]
# totals = Totals(**invoice_from_dict["totals"])
# invoice = Invoice(
#     bill_info=bill_info,
#     provider=provider,
#     customer=customer,
#     invoice_details=invoice_details,
#     totals=totals
# )

# print(invoice.bill_info.invoice_date)

