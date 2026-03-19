---
source: hn
url: https://github.com/jalabulajunx/WebBridge
published_at: '2026-03-06T23:29:40'
authors:
- nonstopnonsense
topics:
- mcp-tools
- browser-automation
- traffic-recording
- api-reverse-engineering
- privacy-audit
relevance_score: 0.06
run_id: materialize-outputs
language_code: en
---

# Show HN: WebBridge turns any website into MCP tools by recording browser traffic

## Summary
WebBridge automatically converts website network traffic recorded by users in Chrome into tool servers callable by MCP clients, with the goal of connecting any website to AI workflows **without writing code and without the website's cooperation**. It also extends to privacy/compliance auditing: through "full packet capture," it provides real network requests to the model as evidence for analysis.

## Problem
- Many websites lack official APIs, SDKs, or ready-made MCP integrations, which means connecting website capabilities to MCP clients such as Claude or Cursor usually requires handwritten reverse-engineering code, creating a high barrier and taking significant time.
- Website automation must not only understand request structures, but also handle authentication, sessions, field mapping, testing, installation, and ongoing maintenance for API changes; these steps are fragmented and error-prone.
- For privacy/compliance teams, what documentation claims and what network traffic an application actually sends may not match; reviewing privacy policies alone cannot verify actual data-sharing behavior.

## Approach
- Use a Chrome extension to record API traffic during normal user operations via **Chrome DevTools Protocol**; leverage the browser's existing logged-in state and use cookies/script bridging for authentication, rather than storing passwords or tokens.
- Have Claude read the recordings, identify API actions within them, ask for tool names and key fields, and then automatically generate a **typed MCP server**, exposing it to any compatible client through standard MCP/JSON-RPC over stdio.
- Provide an end-to-end pipeline: `record -> read_recordings -> write_server -> test -> install -> update`, with built-in self-checks for common errors such as ESM configuration, incorrect bridge mode, and misuse of low-level MCP APIs.
- Forward requests between Chrome and the generated server through a native host and Unix socket; support HAR import, incremental updates (regenerating only affected tools), and background-tab keepalive for some sites to maintain JS sessions.
- The "Full Dump" mode is not used to generate tools, but instead captures all network requests (including analytics, trackers, failed requests, SSE, etc.), allowing Claude to generate structured privacy/compliance reports and, together with legal plugins, check whether DPAs, privacy policies, and actual transfers are consistent.

## Results
- It claims **about 10 minutes from recording to a usable tool**, with **no handwritten code required**; this is the core efficiency result in the text, but it is not based on a standard academic benchmark evaluation.
- Example given: an integration generated for **9 public libraries in York Region**, capable of searching **all 9 catalogs** at once, and producing at least **3 tools**: `search_york_region_libraries`, `search_specific_library`, `list_york_region_libraries`.
- This library case reportedly required only **one recording** of BiblioCommons search traffic, after which Claude analyzed it and generated the MCP server, with the **entire process taking less than 10 minutes**.
- The system supports **incremental updates**: when a website API changes, re-record the relevant action and run `webbridge_update` to regenerate only the affected tools rather than rewriting the entire server; the text does not provide success-rate or timing statistics.
- The self-verifying generation process immediately checks for **3 common error types** after writing the server (ESM syntax, incorrect bridge mode, low-level MCP API patterns) and triggers automatic regeneration; however, no concrete error-rate reduction numbers are reported.
- It does not provide academic-style quantitative metrics such as success rate, number of websites covered, comparison baselines versus Playwright or handwritten packet-capture approaches, or privacy-audit accuracy. The strongest concrete claim is: **any website, no code, no site cooperation, MCP tools generated in about 10 minutes**, plus compliance analysis based on real network evidence from full traffic capture.

## Link
- [https://github.com/jalabulajunx/WebBridge](https://github.com/jalabulajunx/WebBridge)
