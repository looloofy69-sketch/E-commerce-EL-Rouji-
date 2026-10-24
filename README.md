# EL-Rouji E-commerce

**Status:** product and technical specification baseline; no runnable storefront implementation is present in this repository at this baseline.  
**Baseline:** 24 October 2026  
**Related platform:** [EL-Rouji](https://github.com/looloofy69-sketch/EL-Rouji)

> **Repository naming:** the existing GitHub repository used for this work is `looloofy69-sketch/E-commerce-EL-Rouji-`. It is used here because it is the existing e-commerce-related repository. No repository named exactly `EL-Rouji-e-commerce` was found in the current GitHub results.

## Purpose

This repository defines a proposed e-commerce product aligned with the EL-Rouji ecosystem. It separates product requirements, architecture, data contracts, and security requirements from the AI-assistant source code.

The initial market and operational assumptions are not confirmed requirements. A local-first Algeria scenario may be a useful starting point, but supported currencies, online payment providers, cash-on-delivery rules, shipping areas, invoicing, consumer rights, and tax handling must be confirmed with the product owner and qualified local advisors before implementation.

## Documentation map

- [Machine-readable product/checkout/error schemas](schemas/)

- [Product requirements and MVP](docs/PRODUCT_REQUIREMENTS.md)
- [Proposed architecture](docs/ARCHITECTURE.md)
- [Proposed data model](docs/DATA_MODEL.md)
- [API contract draft](docs/API_CONTRACTS.md)
- [Security and operations](docs/SECURITY_OPERATIONS.md)
- [Roadmap and release gates](docs/ROADMAP.md)
- [Change log](CHANGELOG.md)

## Initial product concept

A merchant/customer commerce application could include:
- Product catalog, categories, product detail pages, availability, and search.
- Cart and checkout with server-side price/stock validation.
- Orders, order status, cancellation/refund workflows, and customer order history.
- Merchant/admin catalog and inventory management.
- Delivery address and shipping/fulfillment workflows.
- Payment-provider adapter with server-verified payment status.
- Administrative audit trails and basic sales/fulfillment reporting.

All of these are **proposed capabilities**, not implemented features.

## Design principles

- Server-side price, inventory, authorization, and order-state enforcement.
- Never store raw payment-card data or payment secrets in the app database or Git.
- Do not mark an order paid because a browser redirect says so; verify the payment server-to-server.
- Make checkout and order creation idempotent against duplicate submissions.
- Keep customer data minimal and apply explicit retention/deletion rules.
- Avoid promising a payment provider, shipping service, regulatory compliance, or launch date before verification.
- Keep the storefront usable on mobile and in the confirmed customer languages.
- Treat AI-generated descriptions/recommendations as drafts that require merchant control and factual checks.

## Existing ecosystem

- [EL-Rouji core app](https://github.com/looloofy69-sketch/EL-Rouji)
- [EL-Rouji-jobs](https://github.com/looloofy69-sketch/EL-Rouji-jobs)
- [EL-Rouji datasets](https://github.com/looloofy69-sketch/EL-Rouji-datasetes)

The repository contains specifications, not a deployed commerce service. Do not expose it as an operational store until implementation, payment/shipping integration, security review, and end-to-end QA are complete.
