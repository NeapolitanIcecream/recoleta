---
source: hn
url: https://github.com/DimitriBouriez/navagent-mcp
published_at: '2026-03-05T23:36:46'
authors:
- DimitriBouriez
topics:
- web-automation
- browser-agent
- token-efficiency
- anti-bot
- mcp
- chrome-extension
relevance_score: 0.08
run_id: materialize-outputs
language_code: en
---

# Show HN: NavAgent – CDP-free, token-efficient web automation for AI

## Summary
NavAgent is a lightweight web automation tool for AI that replaces screenshots or verbose accessibility trees with compact numbered lists of elements, significantly reducing context token costs. It controls the browser via Chrome extension native messaging rather than CDP, emphasizing stronger anti-detection capabilities and broader website compatibility.

## Problem
- Existing AI web automation often relies on screenshots or ARIA/accessibility trees, which makes context very bloated, increases token costs, and slows agent decision-making.
- Many solutions are based on CDP, which can easily expose automation fingerprints and be identified by anti-scraping/anti-bot systems such as Cloudflare and Akamai.
- Modern websites include SPAs, shadow DOM, iframes, and rich-text editors, which often cause general-purpose web agents to fail or behave unstably; this matters because real-world web operations need to run reliably in these complex frontend environments.

## Approach
- The core mechanism is: instead of giving the model the webpage as an image or a full accessibility tree, it scans the DOM, extracts interactive elements, compresses them into a short numbered list, and lets the model output actions like `browse_click(6)`.
- The system consists of two required components: a locally running `navagent-mcp` server and a Chrome extension; the MCP client connects to the local server via stdio, then communicates with the extension through a localhost WebSocket, and the extension uses `chrome.tabs.sendMessage` to drive a content script that scans and manipulates the page.
- To cover complex webpages, it supports SPA hash routing, forcibly opening and traversing shadow DOM, cross-`same-origin` iframe access, and text input in `contenteditable` editors such as DraftJS/ProseMirror using `execCommand('insertText')`.
- To improve element discovery, it combines strong clickability rules (such as `<a>`, `<button>`, ARIA interactive roles, `tabindex>=0`) with weak clickability heuristics (such as `cursor:pointer`, `data-*`, framework click directives), and adds landmarks/zone detection plus a post-scan `querySelectorAll` safety fallback.
- To reduce detection risk, it avoids CDP, does not trigger the `navigator.webdriver` flag, and emphasizes native extension messaging, a real local browser session, the user's own cookies/logins, and zero telemetry.

## Results
- The clearest quantified benefit given in the text is token efficiency: compared with screenshots, the numbered-list approach can avoid about **2000+ tokens** of input, and compared with ARIA/accessibility trees it can avoid about **15k-20k tokens** of input, but no standardized benchmarks or end-to-end task success rates are provided.
- On engineering validation, the project claims **111 tests** (`vitest + jsdom`), indicating the author has provided basic test coverage for the implementation, though this is not an academic benchmark result.
- Compatibility claims include: usable on **any website**, supporting **SPAs, shadow DOM, same-origin iframes, contenteditable editors**, and compatible with multiple MCP clients (such as Claude Code, Claude Desktop, Cursor, Windsurf, Zed, OpenClaw).
- Anti-detection claims include: because it uses Chrome native extension messaging rather than CDP, the system claims to be **undetectable/anti-bot-proof** against services such as **Cloudflare** and **Akamai**, but the excerpt provides no experimental setup, detection pass rates, or baseline comparison data.
- Specific verifiable information on security and deployment includes: the default WebSocket port is **61822**, it listens only on **127.0.0.1**, the extension's minimum permissions are `activeTab`, `storage`, and `alarms`, and it claims **zero telemetry**.

## Link
- [https://github.com/DimitriBouriez/navagent-mcp](https://github.com/DimitriBouriez/navagent-mcp)
