# Product Requirements — EL-Rouji E-commerce

**Status:** proposed baseline. Product-owner decisions are required before implementation.

## 1. Product goal

Provide a reliable commerce workflow in which customers discover products, check availability, place orders, and track fulfillment while merchants manage catalog, inventory, and order operations.

The intended business model (single merchant, multi-vendor marketplace, or hosted storefront platform) is currently **undecided**. This is an architectural decision with major consequences for roles, payments, commissions, disputes, tax, onboarding, and data isolation.

## 2. Primary actors

- **Guest customer:** browse published products and use guest checkout if enabled.
- **Registered customer:** manage profile, addresses, and order history.
- **Merchant/admin:** create products, update prices/stock, manage orders and fulfillment.
- **Support/operator:** investigate order issues with limited, audited access.
- **System integration:** payment provider, shipping/fulfillment provider, notifications, and optional analytics.

Role names and permissions must be formalized before development. If multi-vendor support is chosen, a merchant must not access another merchant's private records.

## 3. Candidate MVP scope

### Storefront
- Browse published products and categories.
- Product details with images, price, availability, variants, and fulfillment restrictions.
- Search/filter/sort with accessible empty and error states.
- Mobile-responsive layout and confirmed languages/currency.

### Cart and checkout
- Add/update/remove cart lines.
- Recalculate prices, discounts, delivery, and totals on the server.
- Recheck inventory during order creation.
- Collect only necessary customer and delivery details.
- Show clear order summary and terms before final submission.
- Protect order creation with idempotency and duplicate-submit handling.

### Orders
- Create an order with immutable line-item price/name snapshots.
- Model payment and fulfillment states separately.
- Display order confirmation, status, and customer-visible history.
- Support defined cancellation, refund/return, and failed-delivery flows; policy details are product-owner decisions.

### Administration
- Restrict catalog and inventory changes to authorized staff/merchant roles.
- Manage product publication, stock, and order fulfillment.
- Record sensitive administrative changes in an audit trail.
- Use pagination, filtering, and bounded exports for operational lists.

## 4. Explicitly out of initial scope unless approved

- Multi-vendor marketplace payouts/commissions.
- Loans, stored-value wallet, or holding customer funds.
- Subscription billing.
- Unrestricted AI-generated publication of product listings.
- Warehouse automation or complex ERP integration.
- Native mobile applications.
- Arbitrary code or plugin execution by merchants.

## 5. Product decisions required

| Decision | Why it matters |
|---|---|
| Single merchant vs marketplace | Tenant model, authorization, payments, payouts, disputes |
| Customer geography and languages | UX, address model, delivery rules, support |
| Currency and pricing conventions | Product and order money model, rounding, reporting |
| Payment methods/providers | Integration contract, settlement, webhook security, local eligibility |
| Shipping and fulfillment | Zones, fees, tracking, failed delivery/returns |
| Product types | Physical, digital, service, variant and inventory rules |
| Guest vs account checkout | Identity, privacy, recovery, order lookup |
| Returns/refunds/cancellation policy | State machine, financial reconciliation, customer support |
| Regulatory/tax/invoice requirements | Legal review and accounting requirements |
| Merchant/admin model | Access controls and audit requirements |

Do not hard-code Algeria-specific provider, tax, payment, or consumer-law assumptions until current official requirements and provider eligibility have been verified.

## 6. Functional acceptance criteria

- Product details and displayed price match the latest server-approved catalog state.
- The server rejects checkout if an item is unpublished, unavailable, incorrectly priced, or out of stock.
- Duplicate checkout requests cannot create duplicate orders or duplicate payment attempts contrary to the documented idempotency behavior.
- Order line items preserve the actual price/name/variant accepted at purchase time.
- Payment status changes only after a verified provider response/webhook or an explicitly documented manual payment flow.
- Customers can access only their own orders.
- Merchant users can access only authorized catalog/inventory/order scope.
- All admin changes that affect catalog, pricing, inventory, orders, or refunds are attributable.
- Clear loading, empty, validation, failure, and retry states exist.
- Core journeys pass desktop/mobile and keyboard/accessibility checks before release.

## 7. Non-functional requirements

- Secure server-side authorization and input validation.
- Bounded request, upload, export, and image-processing sizes.
- Auditable order/payment transitions.
- Idempotency for checkout and provider notifications.
- Documented data retention/deletion and provider data handling.
- Error logging without payment secrets or unnecessary customer data.
- Tested backups/recovery where persistence services support them.
- Accessible, responsive design.
- Stated performance/error targets established with measured baselines rather than invented numbers.

## 8. Release criteria

A working prototype is not a production-ready store. Before launch, payment/shipping flows, pricing and inventory integrity, access control, refund/return policy, provider contracts, customer support, operational monitoring, rollback, and security review must be tested and approved.
