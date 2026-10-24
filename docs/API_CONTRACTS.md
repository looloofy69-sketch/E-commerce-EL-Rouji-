# Draft Commerce API Contracts

## 0. Machine-readable contract baseline

JSON Schema Draft 2020-12 contracts are maintained under [schemas/](../schemas/):

- [Public product](../schemas/product.schema.json)
- [Checkout request](../schemas/checkout-request.schema.json)
- [Checkout response](../schemas/checkout-response.schema.json)
- [Error envelope](../schemas/error.schema.json)

Run the contract checks locally with Python 3.11 or later:

```sh
python -m pip install -r requirements-dev.txt
python -m unittest discover -s tests -v
```

GitHub Actions runs the same schema/meta and example-payload tests on pushes and pull requests. These are draft request/response contracts, not live endpoints or proof of server-side enforcement. Before wiring a frontend or provider, the implementation must validate requests again on the server and the product owner must settle market, supported currencies, identity model, fulfillment, and payment policy.

The checkout request intentionally excludes client-supplied currency, prices, totals, tax, role, payment status, and order status. The server must load the cart and catalog, determine allowed fulfillment/payment options, and calculate the authoritative amount. The currency regex checks code shape only; it does not decide which currency the store supports.


**Status:** proposal only. No endpoint in this document is asserted to be implemented or deployed.

Use a versioned base path such as `/api/v1` once the stack is selected. The examples show JSON; final content types, authentication, pagination, error envelopes, and idempotency headers must be agreed with the implementation.

## 1. Common principles

- Validate and authorize every request server-side.
- Return stable error codes with safe user-facing messages.
- Do not disclose whether another customer's private order exists.
- Use pagination and bounded page sizes for lists.
- Never accept client-provided prices, order totals, roles, tenant IDs, or payment status as authoritative.
- Use idempotency keys for checkout/order creation and any payment side effect.
- Define concurrency/conflict behavior for stock and product updates.
- Document rate limits and upload constraints.

## 2. Proposed public/catalog endpoints

| Method | Path | Purpose |
|---|---|---|
| GET | `/api/v1/products` | List published products with bounded search/filter/page |
| GET | `/api/v1/products/:slug` | Read a published product |
| GET | `/api/v1/categories` | List public categories |
| GET | `/api/v1/cart` | Retrieve the current authorized cart |
| POST | `/api/v1/cart/items` | Add a variant/quantity |
| PATCH | `/api/v1/cart/items/:id` | Update quantity |
| DELETE | `/api/v1/cart/items/:id` | Remove a cart line |
| POST | `/api/v1/checkout` | Validate cart and create an order/payment workflow |
| GET | `/api/v1/orders` | List only the current customer's orders |
| GET | `/api/v1/orders/:id` | Retrieve an authorized order summary |

These paths are a naming proposal, not a final or existing API.

## 3. Checkout contract draft

Request example:

```json
{
  "cartId": "cart_example",
  "shippingAddressId": "address_example",
  "fulfillmentMethod": "delivery",
  "paymentMethod": "provider_method_id"
}
```

The server must load current product/variant records, recheck publication and inventory, calculate amounts, determine applicable shipping/tax/discount rules, and persist an immutable order snapshot. Client totals may be used only for display and must be ignored as authoritative values.

Successful response example:

```json
{
  "orderId": "order_example",
  "status": "PENDING_CONFIRMATION",
  "currency": "TBD",
  "amount": "server-calculated",
  "nextAction": {
    "type": "provider_redirect_or_confirmation",
    "url": null
  }
}
```

This is an illustrative contract only. Production amounts should use the actual agreed numeric/string money schema rather than the placeholder.

## 4. Merchant/admin endpoints (proposal)

| Method | Path | Purpose |
|---|---|---|
| POST/PATCH | `/api/v1/admin/products` and `/api/v1/admin/products/:id` | Create/update product drafts |
| POST | `/api/v1/admin/products/:id/publish` | Publish after required validation |
| PATCH | `/api/v1/admin/inventory/:variantId` | Audited inventory adjustment |
| GET | `/api/v1/admin/orders` | Authorized order operations |
| POST | `/api/v1/admin/orders/:id/cancel` | Apply permitted cancellation flow |

All admin routes must enforce role and scope server-side and create audit records for sensitive mutations. Endpoint-level authorization is not optional even when the admin UI hides controls.

## 5. Provider webhook contract

A proposed payment webhook endpoint must:
1. Verify the provider signature using the raw request data as required by that provider.
2. Check timestamp/replay controls where provided.
3. Persist a provider event ID with a unique constraint.
4. Match the event to a known payment attempt.
5. Verify amount, currency, merchant/account, and expected state.
6. Make duplicate events safe to process.
7. Return the provider-required acknowledgment without revealing internal details.

The actual path and procedure depend on the provider selected. Never trust a browser return URL as proof of payment.

## 6. Error model proposal

Example:

```json
{
  "error": {
    "code": "OUT_OF_STOCK",
    "message": "One or more items are no longer available.",
    "requestId": "request_example"
  }
}
```

Potential stable codes include `VALIDATION_ERROR`, `UNAUTHENTICATED`, `FORBIDDEN`, `NOT_FOUND`, `OUT_OF_STOCK`, `PRICE_CHANGED`, `IDEMPOTENCY_CONFLICT`, `PAYMENT_PENDING`, `PAYMENT_FAILED`, `RATE_LIMITED`, and `INTERNAL_ERROR`. Final codes must correspond to real behaviors and be documented with HTTP status semantics.

## 7. Contract test requirements

- Unauthorized access to another customer's cart/order fails.
- A changed price or unavailable product invalidates checkout or requires renewed customer confirmation.
- Duplicate idempotent checkout calls do not create duplicate orders.
- Invalid quantities and unknown variants are rejected.
- Payment webhooks reject invalid signatures and handle repeated valid events idempotently.
- Client failures do not expose stack traces, credentials, or private provider payloads.
- Admin mutations require the correct role/scope and emit audit records.
