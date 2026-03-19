---
source: hn
url: https://github.com/rivaas-dev/rivaas
published_at: '2026-03-07T23:40:49'
authors:
- atkrad
topics:
- go-web-framework
- cloud-native
- observability
- openapi
- high-performance-routing
relevance_score: 0.49
run_id: materialize-outputs
language_code: en
---

# High-performance Go web framework; Ships with OpenTelemetry, OpenAPI docs

## Summary
Rivaas is a Go web framework for cloud-native scenarios, focused on high-performance routing, out-of-the-box observability, automatic OpenAPI documentation, and a modular component design that can be used independently. It aims to integrate common production capabilities into a lightweight yet complete development stack.

## Problem
- It addresses the problem of “fragmented capabilities and high integration cost” in Go web service development: developers often need to manually assemble routing, logging, metrics, tracing, validation, and documentation generation.
- It addresses the gap between development and production deployment for production-grade API services: many lightweight frameworks lack key capabilities such as graceful shutdown, health checks, panic recovery, mTLS, and observability.
- This matters because cloud-native services need to be both fast and reliable, while also being easy to monitor, govern, and maintain; otherwise, engineering complexity and operational costs increase.

## Approach
- The core approach is to provide a **batteries-included** `app` layer that unifies routing, logging, metrics, tracing, configuration, validation, error handling, OpenAPI, and related capabilities, so developers can start a service with only a small amount of code.
- Underneath, it uses an independent high-performance `router` module based on a **radix tree router with Bloom filter optimization**, aiming to improve routing performance while keeping the API easy to use.
- It adopts a modular architecture: each package such as `router`, `binding`, `validation`, `openapi`, `logging`, `metrics`, and `tracing` can be used independently, and each has its own `go.mod`, supporting independent version evolution.
- It includes OpenTelemetry-native observability, supports Prometheus, OTLP, and Jaeger, and automatically propagates service metadata and lifecycle management.
- It provides 12 production-grade middleware components, along with common backend capabilities such as health checks, graceful shutdown, request binding and validation, and automatic OpenAPI generation, reducing engineering assembly effort.

## Results
- The text explicitly claims **high-performance routing** and says that “benchmarks are run on every router release,” with comparison targets including frameworks such as **Gin, Echo, Chi, Fiber**.
- However, this excerpt **does not provide specific benchmark numbers**, so throughput, latency, memory usage, or relative percentage improvements cannot be confirmed.
- Quantifiable feature claims include: **12** built-in production-ready middleware components; support for exposing Prometheus metrics at **`:9090/metrics`**; and a requirement of **Go 1.25+**.
- Architecturally, it includes **11** major modules/packages (such as `app`, `router`, `binding`, `validation`, `logging`, `metrics`, `tracing`, `openapi`, etc.) and uses a multi-module repository to support independent reuse.
- The strongest practical claim is that, compared with frameworks that only provide basic routing, Rivaas packages performance, observability, documentation, validation, and production operations capabilities together, emphasizing the combined engineering value of being “production-ready + cloud-native + modular,” rather than a single algorithmic breakthrough.

## Link
- [https://github.com/rivaas-dev/rivaas](https://github.com/rivaas-dev/rivaas)
