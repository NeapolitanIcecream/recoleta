---
source: hn
url: https://reactdevelopment.substack.com/p/when-to-use-bff-and-should-it-replace
published_at: '2026-03-05T23:30:00'
authors:
- javatuts
topics:
- backend-for-frontend
- api-gateway
- microservices
- system-architecture
- client-specific-api
relevance_score: 0.01
run_id: materialize-outputs
language_code: en
---

# When to Use BFF and Should It Replace API Gateway?

## Summary
This article discusses the difference in responsibilities between **BFF (Backend for Frontend)** and **API Gateway**, and under what circumstances a BFF should be introduced, when it can coexist with a gateway, or be temporarily combined with it. The core conclusion is: BFF is well suited for client-specific data aggregation and interface customization, while an API Gateway is better suited for infrastructure responsibilities such as routing, security, and rate limiting.

## Problem
- The problem the article addresses is: in modern multi-client or complex single-frontend systems, **whether it is necessary to introduce a BFF, and whether it should replace the API Gateway**.
- This matters because if the frontend connects directly to multiple backend services, it must take on complex logic such as request orchestration, data transformation, error handling, pagination, and filtering, which makes the client heavier and slows iteration.
- Another key issue is architectural boundaries: if the gateway and BFF are mixed together, it may seem simpler in the short term, but over time a single component may end up carrying too many responsibilities, harming maintainability and scalability.

## Approach
- The article uses an **architectural pattern analysis** approach, comparing the responsibility boundaries of BFF and API Gateway, rather than proposing a new algorithm or system implementation.
- It defines the API Gateway as the **infrastructure entry layer**, responsible for routing, SSL termination, authentication token validation, rate limiting, traffic distribution, and similar concerns, and typically not carrying business logic.
- It defines the BFF as a **backend adaptation layer for a specific client**, responsible for aggregating data from multiple microservices, trimming fields, transforming responses into UI-friendly structures, and adapting differences such as pagination and sorting.
- The article recommends the combination: **Client → API Gateway → BFF → Microservices**, where the gateway handles common infrastructure concerns and the BFF handles client-specific customization logic.
- It also provides decision criteria: BFF is more suitable for multiple clients, legacy/raw backend data, multi-service aggregation, independent frontend/backend iteration, and performance-sensitive scenarios; while a single backend, simple systems, responses already matching the UI, and unified team collaboration may not require it.

## Results
- This is not an experimental paper and **does not provide quantitative experimental results, benchmark datasets, metric improvements, or statistical comparison figures**.
- The strongest concrete claim in the article is that in a mature microservices architecture, the recommended layered composition is **Client → API Gateway → BFF → Microservices**, rather than having BFF replace the API Gateway.
- Using SoundCloud as a case background, the article claims that after splitting a single API into multiple client-oriented BFFs, different teams were able to **iterate faster** and better adapt to differences between Web and mobile, but **it does not provide percentage improvements in speed or performance numbers**.
- It explicitly gives an example of differing needs between mobile and Web: mobile may request **10 items/page**, while Web may request **50 items/page**, illustrating that the value of BFF lies in customizing interfaces according to client needs rather than uniformly exposing raw backend capabilities.
- Its concluding result is that for small, low-load, single-client systems with low transformation needs, BFF and gateway responsibilities can be temporarily combined; but as the system grows, **separating responsibilities usually leads to a clearer, more scalable architecture**.

## Link
- [https://reactdevelopment.substack.com/p/when-to-use-bff-and-should-it-replace](https://reactdevelopment.substack.com/p/when-to-use-bff-and-should-it-replace)
