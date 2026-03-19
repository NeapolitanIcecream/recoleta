---
source: hn
url: https://github.com/rivaas-dev/rivaas
published_at: '2026-03-07T23:40:49'
authors:
- atkrad
topics:
- go-web-framework
- cloud-native
- opentelemetry
- openapi
- http-router
relevance_score: 0.01
run_id: materialize-outputs
language_code: en
---

# High-performance Go web framework; Ships with OpenTelemetry, OpenAPI docs

## Summary
This is not a robotics or foundation model paper, but a high-performance cloud-native web framework for Go called Rivaas. It emphasizes high-performance routing, built-in observability, automatic OpenAPI documentation, and modular production-grade capabilities.

## Problem
- It addresses the problem that in Go service development, “high-performance routing, production-grade middleware, observability, documentation generation, and configuration management” are often scattered across multiple libraries, making integration costly.
- This matters because cloud-native API services need to be both fast and reliable, while also being easy to monitor, deploy, and maintain.
- The project also attempts to avoid forcing developers to choose between an “all-in-one framework” and “independently reusable components.”

## Approach
- The core mechanism is to provide a **batteries-included** `app` layer that integrates routing, logging, metrics, tracing, health checks, validation, OpenAPI, and related capabilities by default.
- The routing layer uses a **radix tree router with Bloom filter optimization**, aiming for higher throughput and lower overhead in request matching.
- Observability is integrated natively with **OpenTelemetry** and supports backends such as Prometheus, OTLP, and Jaeger, simplifying production monitoring integration.
- It adopts a multi-module repository design, where each subpackage can be used independently and versioned separately, balancing “framework-style ease of use” with “library-style flexibility.”
- It includes 12 production-grade middleware components, as well as operational features such as graceful shutdown, health checks, panic recovery, and mTLS.

## Results
- The text claims the framework is **high-performance** and that it “runs benchmarks on every router release,” and also compares it with **Gin, Echo, Chi, Fiber**, but this excerpt **does not provide specific throughput, latency, or memory figures**.
- It provides **12** built-in production-grade middleware components: accesslog, recovery, cors, requestid, timeout, ratelimit, basicauth, bodylimit, compression, security, methodoverride, trailingslash.
- It supports **Go 1.25+**.
- Health checks support configurable readiness probes; metrics can be exposed by default at **`:9090/metrics`**; tracing supports **OTLP (`localhost:4317`)** and stdout examples.
- The project structure includes **10+** modules that can be used independently (such as app, router, binding, validation, logging, metrics, tracing, openapi), emphasizing modular reuse and independent version management.
- Relative to the user’s stated areas of interest, this work has **almost no direct relation** to embodied AI or robot foundation model topics.

## Link
- [https://github.com/rivaas-dev/rivaas](https://github.com/rivaas-dev/rivaas)
