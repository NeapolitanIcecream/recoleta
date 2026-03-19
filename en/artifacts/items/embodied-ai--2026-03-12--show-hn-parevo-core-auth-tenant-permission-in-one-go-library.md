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
- access-control
- backend-infrastructure
relevance_score: 0.01
run_id: materialize-outputs
language_code: en
---

# Show HN: Parevo Core – Auth, tenant, permission in one Go library

## Summary
Parevo Core is a framework-agnostic and storage-agnostic Go library that integrates authentication, multi-tenancy, and permission management into a single set of components, aiming to reduce duplicated backend implementation work in applications. It is primarily oriented toward engineering integration and product development efficiency, rather than problems in robotics or foundation model research.

## Problem
- It aims to solve the problem that **authentication, tenant isolation, and access control** in backend systems are often implemented separately, repeatedly developed, and difficult to maintain consistently.
- This matters because these capabilities are foundational infrastructure for nearly all SaaS and enterprise applications; fragmented integration increases security risk, development cost, and migration difficulty.
- The text also emphasizes supporting different web frameworks and different database/cache backends, avoiding lock-in to a single technology stack.

## Approach
- The core approach is to provide **a unified Go library** that places auth, tenant, and permission capabilities into a single composable service layer.
- For authentication, it includes multiple common mechanisms: JWT, OAuth2, SAML, LDAP, API keys, WebAuthn, magic link.
- For multi-tenancy, it provides tenant context, tenant lifecycle, and feature flags, helping applications carry tenant information through request handling and business logic layers.
- For permissions, it supports RBAC, ABAC, and cached checks, using a unified approach for role-/attribute-based access control and accelerated permission validation.
- To make integration easy, it also claims to be framework-agnostic and storage-agnostic, supporting net/http, chi, gin, echo, fiber, GraphQL, as well as MySQL, Postgres, MongoDB, Redis, memory.

## Results
- The provided text **does not give paper-style quantitative results**: there are no precise benchmarks, datasets, latency, throughput, security improvement percentages, or numerical comparisons against baseline methods.
- The most concrete engineering result is feature coverage: **7 authentication methods** (JWT, OAuth2, SAML, LDAP, API keys, WebAuthn, magic link).
- The most concrete compatibility result is support for **6 frameworks/interfaces** (net/http, chi, gin, echo, fiber, GraphQL).
- The most concrete storage coverage is support for **6 backend types** (MySQL, Postgres, MongoDB, Redis, memory, plus the adaptation approach implied by being storage-agnostic).
- The text also provides multiple runnable examples: **5 example entry points** (nethttp-basic, gin-modular, notification, blob, admin-panel), indicating that its usability claims are geared more toward practical engineering adoption than research breakthroughs.

## Link
- [https://github.com/parevo/core](https://github.com/parevo/core)
