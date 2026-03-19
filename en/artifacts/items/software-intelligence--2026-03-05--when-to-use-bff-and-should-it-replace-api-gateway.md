---
source: hn
url: https://reactdevelopment.substack.com/p/when-to-use-bff-and-should-it-replace
published_at: '2026-03-05T23:30:00'
authors:
- javatuts
topics:
- backend-for-frontend
- api-gateway
- software-architecture
- microservices
- frontend-backend-integration
relevance_score: 0.28
run_id: materialize-outputs
language_code: en
---

# When to Use BFF and Should It Replace API Gateway?

## Summary
This article explains the difference in responsibilities between BFF (Backend for Frontend) and API Gateway, and provides architectural guidance on when to introduce one, when to avoid one, and when the two should work together. The core argument is: BFF is responsible for client-facing data shaping and aggregation, while API Gateway is responsible for the common infrastructure entry point; the two generally should not replace each other.

## Problem
- The article addresses the question of when teams need a BFF in modern backend architecture, whether it should replace an API Gateway, and how to avoid overengineering or blurred responsibilities in single-frontend and multi-frontend scenarios.
- This matters because if the frontend connects directly to multiple backend services, it must take on complex logic such as request orchestration, response transformation, error handling, pagination, and filtering, which makes clients more complex and slows evolution.
- If API Gateway and BFF are treated as the same thing, the system may look simple early on, but as the business grows, responsibilities like routing, security, rate limiting, aggregation, transformation, and caching get piled into a single component, increasing maintenance cost.

## Approach
- The article uses an architectural pattern comparison approach: it first defines the origin and purpose of BFF, then compares the typical responsibilities of an API Gateway, clarifying that they are not the same type of component.
- Put simply: an API Gateway is like a “main entrance gatekeeper,” responsible for securely forwarding requests to the correct service; a BFF is like a “waiter tailored for a specific frontend,” responsible for organizing data from multiple backends into the form that client needs most.
- It recommends the flow: **Client → API Gateway → BFF → Microservices**, where the Gateway handles infrastructure concerns such as SSL, authentication, rate limiting, and routing, while the BFF handles client logic such as aggregation, field trimming, adapting pagination/sorting, and adding UI-specific fields.
- It uses scenario-based criteria to explain when to use BFF: it is more valuable when there are multiple clients, legacy or raw backend data, pages that need cross-service aggregation, frontend teams that need to iterate independently, or a need to reduce client requests; it may be unnecessary when the system is simple, has a single backend service, and already returns data that matches the UI.
- The article also discusses BFF ownership from an organizational collaboration perspective, noting that it can be maintained by the frontend team, while operationally it is still a backend component.

## Results
- The article **does not provide experiments, benchmarks, or formal quantitative metrics**, so there are no precise data points, datasets, or numerical improvements to report.
- The strongest concrete conclusion is that in mature architectures, API Gateway and BFF should be layered to work together rather than having BFF replace the Gateway; the typical request path is **Client → API Gateway → BFF → Microservices**.
- The article gives clear practical benefits, including that a BFF can return differently shaped data for different clients—for example, smaller payloads for mobile, richer data for web, and operational information for admin dashboards.
- It cites SoundCloud’s practice as a case study, claiming that after splitting a single API into multiple client-specific BFFs, teams were able to iterate faster and reduce the risk of a unified backend API becoming a bottleneck, but it **does not provide specific figures for speed, latency, or cost**.
- Its conclusion on whether to merge BFF and API Gateway is that it can be acceptable in scenarios with a “small internal application + single client + simple backend + low load + minimal data transformation”; however, once the system enters a continuously growing microservices environment, separating responsibilities is usually easier to maintain and more scalable.

## Link
- [https://reactdevelopment.substack.com/p/when-to-use-bff-and-should-it-replace](https://reactdevelopment.substack.com/p/when-to-use-bff-and-should-it-replace)
