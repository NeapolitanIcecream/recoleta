---
source: hn
url: https://github.com/parevo/core
published_at: '2026-03-12T23:53:15'
authors:
- parevo
topics:
- go-library
- authentication
- multi-tenancy
- authorization
- developer-tooling
relevance_score: 0.54
run_id: materialize-outputs
language_code: en
---

# Show HN: Parevo Core – Auth, tenant, permission in one Go library

## Summary
Parevo Core is a framework-agnostic library for Go that integrates authentication, multi-tenancy, and permission management into a single component, aiming to reduce the cost of repeatedly building foundational security and tenant capabilities in business systems. It is more like an engineering infrastructure library than a research paper, emphasizing pluggability and reuse across storage backends and Web frameworks.

## Problem
- Modern software systems often need to handle authentication, tenant isolation, and access control at the same time, but these capabilities are usually implemented separately, increasing integration complexity and maintenance costs.
- Multi-tenant SaaS or platform systems that lack a unified tenant context, permission model, and authentication entry point are prone to security vulnerabilities, duplicated logic, and framework-coupling issues.
- This matters because authentication/authorization and tenant isolation are core infrastructure for production systems, directly affecting security, development speed, and scalability.

## Approach
- The core method is to package three common foundational capabilities — **auth + tenant + permission** — into a unified Go library, allowing developers to integrate them with minimal configuration.
- The authentication layer supports multiple mechanisms: JWT, OAuth2, SAML, LDAP, API keys, WebAuthn, and magic link, all exposed through the same service interface.
- The multi-tenant layer provides tenant context, tenant lifecycle, and feature flags, helping applications carry and manage tenant state during request processing.
- The permission layer combines RBAC, ABAC, and cached checks to provide unified authorization checks across role-based and attribute-based rules.
- Through storage-agnostic and framework-agnostic design, the library adapts to MySQL, Postgres, MongoDB, Redis, and memory, as well as net/http, chi, gin, echo, fiber, and GraphQL; the core mechanism is a “unified abstraction + adapters” approach.

## Results
- The text **does not provide quantitative experimental results**; there are no paper-style benchmarks, datasets, accuracy figures, latency measurements, or numerical comparisons with baseline methods.
- The strongest concrete claim is that a single library covers **3 core capability categories** at once (auth, multi-tenant, permission), reducing the work of selecting separate tools and manually stitching them together.
- The authentication capability claims support for **7 mechanisms**: JWT, OAuth2, SAML, LDAP, API keys, WebAuthn, and magic link.
- The storage adaptation claims coverage of **5 backend types**: MySQL, Postgres, MongoDB, Redis, and memory.
- The framework adaptation claims coverage of **6 interface/framework types**: net/http, chi, gin, echo, fiber, and GraphQL.
- The repository provides multiple runnable examples, including **nethttp-basic, gin-modular, notification, blob, admin-panel**, indicating that its focus is engineering practicality rather than research novelty.

## Link
- [https://github.com/parevo/core](https://github.com/parevo/core)
