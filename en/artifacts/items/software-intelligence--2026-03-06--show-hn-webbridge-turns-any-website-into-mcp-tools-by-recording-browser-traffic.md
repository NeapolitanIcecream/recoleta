---
source: hn
url: https://github.com/jalabulajunx/WebBridge
published_at: '2026-03-06T23:29:40'
authors:
- nonstopnonsense
topics:
- mcp-tools
- browser-traffic-recording
- code-generation
- web-automation
- privacy-audit
relevance_score: 0.89
run_id: materialize-outputs
language_code: en
---

# Show HN: WebBridge turns any website into MCP tools by recording browser traffic

## Summary
WebBridge records a website’s real browser traffic and then has Claude automatically generate callable MCP tools, quickly turning “any website” into an integration usable by AI clients. It also extends to privacy/compliance auditing, generating evidence-based traffic analysis reports through full network capture.

## Problem
- Many websites do not have public APIs, do not offer official integrations, or require extensive manual reverse engineering and coding to integrate their capabilities into MCP/AI workflows, making the barrier to entry very high.
- Traditional automation often depends on site cooperation, a desktop middleware layer, or brittle scripts; when site interfaces change, maintenance costs are high.
- Legal and privacy teams are often limited to reviewing documentation claims and lack network evidence of “what data the application actually sent” for compliance checks.

## Approach
- Use a Chrome extension to record API traffic during normal user actions via Chrome DevTools Protocol; optionally use Full Dump mode to capture all requests for privacy/compliance analysis rather than tool generation.
- Claude reads the recordings, identifies API operations, asks about tool names and key fields, and then automatically writes **strongly typed** MCP server code and configuration.
- The generated server reuses the browser’s authenticated session, cookies, and contextual request capabilities through a local bridge/socket, so there is no need to store passwords or tokens, and no need for the website to provide an official API.
- Provide a `test / install / update / import_har` workflow: automatically test handshakes and tool calls, write to Claude configuration, regenerate only affected tools based on diffs between old and new recordings, and support importing existing traffic from HAR.
- Built-in self-checking and error diagnostics automatically detect common generation errors (such as ESM configuration issues, incorrect bridge mode, and misuse of low-level MCP APIs) and prompt regeneration.

## Results
- Claims “from recording to a working tool” takes about **10 minutes**, with **no hand-written code required**.
- Example given: the York Region public libraries integration can search **9** library catalogs simultaneously (Aurora, East Gwillimbury, Georgina, King Township, Markham, Newmarket, Richmond Hill, Vaughan, and Whitchurch-Stouffville).
- In that example, by recording BiblioCommons search traffic only **once**, it generated at least **3** tools: `search_york_region_libraries`, `search_specific_library`, `list_york_region_libraries`.
- The generation system includes about **10** WebBridge plugin tools for automation workflows such as reading recordings, writing servers, updating, testing, and installing.
- Full Dump mode can output structured privacy reports covering third-party domains, cookies/headers, PII leakage, redirect chains, and SSE frames; however, the text **does not provide quantitative comparison results on standard benchmark datasets**, nor does it report success rate, accuracy, or formal benchmark comparisons with existing solutions.
- In terms of compatibility, the generated MCP servers are claimed to run on various MCP clients, including Claude Desktop, Claude Code, Cursor, VS Code, Windsurf, Cline, and Continue, but this is likewise a functional claim rather than a metric validated through paper-style experiments.

## Link
- [https://github.com/jalabulajunx/WebBridge](https://github.com/jalabulajunx/WebBridge)
