---
source: hn
url: https://github.com/blue-monads/potatoverse
published_at: '2026-03-04T23:20:39'
authors:
- born-jre
topics:
- web-app-platform
- cms-paas
- go
- sqlite
- sandboxing
relevance_score: 0.01
run_id: materialize-outputs
language_code: en
---

# Show HN: Potatoverse, home for your vibecoded apps

## Summary
PotatoVerse is an application hosting platform that combines a CMS with a lightweight PaaS, aiming to host web applications with server-side code using a single static Go binary and SQLite. It emphasizes application isolation, extensible executor/capability interfaces, and simplified installation, packaging, and hosting workflows.

## Problem
- The project attempts to solve the problem that deployment and hosting for small web applications are too heavy, platforms are fragmented, and extension mechanisms are inconsistent, making it easier for developers to publish applications with backend logic.
- It focuses on isolation and permission boundaries when multiple applications coexist, such as suborigin isolation, per-application independent data access, and a capability registration mechanism.
- This matters because many lightweight application scenarios do not require a full cloud platform or complex CMS/PaaS stack, but still need deployability, extensibility, and some security isolation.

## Approach
- The core mechanism is to make the entire platform a static Go executable with built-in UI assets and SQLite, so deployment is as close as possible to “download and run.”
- Applications are called spaces and run in isolated environments, with isolation provided by suborigin by default; backend code currently runs in a Lua VM, with planned WASM support in the future, while also allowing native Go or custom executors.
- The platform exposes platform services to applications through **capabilities**, and applications access these capabilities through a unified invocation interface; it also supports event-driven asynchronous app-to-app extensions.
- The data layer provides a simple KV store or SQLite, and restricts each application to accessing only its own isolated tables; installation and upgrades are supported via repositories, zip upload, or URL, and repositories can be self-hosted to avoid a single centralized store.

## Results
- The text does not provide formal experiments, benchmarks, or quantitative evaluation results, so there are no precise numerical metrics to report.
- The strongest concrete claim is that the platform can run as a **single static Go binary**, with built-in **SQLite** and bundled UI assets, reducing deployment complexity.
- The system currently supports a **Lua** executor, and explicitly plans follow-on capabilities including a **WASM** executor, **Postgres** support, backups, and HTTP tunnels.
- In terms of application isolation, it claims support for **suborigin**-based space isolation and table-level access restrictions based on SQL statement parsing, but provides no security validation data.
- The author explicitly labels the project as **Alpha Software**, with current bugs, breaking changes, and incomplete functionality; the tunnel system is also known to have limitations for **WebSockets** and isolated-origin mode.

## Link
- [https://github.com/blue-monads/potatoverse](https://github.com/blue-monads/potatoverse)
