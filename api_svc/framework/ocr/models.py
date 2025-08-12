from dataclasses import dataclass
from typing import List

@dataclass
class BillInfo:
    invoice_number: str
    invoice_series: str
    invoice_date: str

@dataclass
class Provider:
    name: str
    address: str
    CIF: str

@dataclass
class Customer:
    name: str
    address: str
    location: str

@dataclass
class InvoiceDetail:
    product: str
    unit: str
    quantity: float
    unit_price: float
    value_without_vat: float
    vat_rate: int
    vat_value: float

@dataclass
class Totals:
    total_without_vat: float
    total_vat: float
    total_with_vat: float

@dataclass
class Invoice:
    bill_info: BillInfo
    provider: Provider
    customer: Customer
    invoice_details: List[InvoiceDetail]
    totals: Totals
