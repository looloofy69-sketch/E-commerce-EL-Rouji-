"""Validate the draft e-commerce JSON Schema contract shapes."""
from __future__ import annotations

import json
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_DIR = ROOT / "schemas"


def load_schema(name: str) -> dict:
    with (SCHEMA_DIR / name).open("r", encoding="utf-8") as stream:
        schema = json.load(stream)
    Draft202012Validator.check_schema(schema)
    return schema


class SchemaMetaTests(unittest.TestCase):
    def test_all_contract_schemas_are_valid_draft_2020_12(self) -> None:
        for path in sorted(SCHEMA_DIR.glob("*.schema.json")):
            with self.subTest(schema=path.name):
                schema = load_schema(path.name)
                Draft202012Validator.check_schema(schema)

    def test_product_valid_shape_passes(self) -> None:
        validator = Draft202012Validator(load_schema("product.schema.json"))
        product = {
            "id": "prod_001",
            "slug": "blue-shirt",
            "title": "Blue Shirt",
            "description": "Synthetic product fixture",
            "status": "draft",
            "currency": "DZD",
            "priceMinor": 2500,
            "availability": "in_stock",
            "variants": [{
                "id": "var_001",
                "sku": "BLUE-M",
                "label": "Blue / M",
                "priceMinor": 2500,
                "availability": "in_stock",
                "options": {"color": "blue", "size": "M"},
            }],
        }
        self.assertEqual(list(validator.iter_errors(product)), [])

    def test_product_rejects_client_or_internal_fields_outside_contract(self) -> None:
        validator = Draft202012Validator(load_schema("product.schema.json"))
        product = {
            "id": "prod_001", "slug": "blue-shirt", "title": "Blue Shirt",
            "description": "", "status": "published", "currency": "DZD",
            "priceMinor": 2500, "availability": "in_stock", "ownerEmail": "customer@example.com",
        }
        self.assertTrue(any("Additional properties" in error.message for error in validator.iter_errors(product)))

    def test_checkout_delivery_requires_address(self) -> None:
        validator = Draft202012Validator(load_schema("checkout-request.schema.json"))
        payload = {"cartId": "cart_1", "idempotencyKey": "req-0123456789ab", "fulfillmentMethod": "delivery"}
        self.assertTrue(any(list(error.absolute_path) == [] for error in validator.iter_errors(payload)))

    def test_checkout_allows_delivery_with_address_and_pickup_without_one(self) -> None:
        validator = Draft202012Validator(load_schema("checkout-request.schema.json"))
        delivery = {
            "cartId": "cart_1", "idempotencyKey": "req-0123456789ab",
            "fulfillmentMethod": "delivery", "shippingAddressId": "addr_1",
        }
        pickup = {
            "cartId": "cart_1", "idempotencyKey": "req-0123456789ab",
            "fulfillmentMethod": "pickup",
        }
        self.assertEqual(list(validator.iter_errors(delivery)), [])
        self.assertEqual(list(validator.iter_errors(pickup)), [])

    def test_checkout_rejects_client_computed_money_and_payment_state(self) -> None:
        validator = Draft202012Validator(load_schema("checkout-request.schema.json"))
        payload = {
            "cartId": "cart_1", "idempotencyKey": "req-0123456789ab",
            "fulfillmentMethod": "pickup", "grandTotal": 1, "currency": "DZD",
            "paymentStatus": "PAID", "role": "admin",
        }
        self.assertTrue(list(validator.iter_errors(payload)))

    def test_checkout_rejects_invalid_idempotency_key(self) -> None:
        validator = Draft202012Validator(load_schema("checkout-request.schema.json"))
        payload = {"cartId": "cart_1", "idempotencyKey": "x", "fulfillmentMethod": "pickup"}
        self.assertTrue(list(validator.iter_errors(payload)))


if __name__ == "__main__":
    unittest.main()
