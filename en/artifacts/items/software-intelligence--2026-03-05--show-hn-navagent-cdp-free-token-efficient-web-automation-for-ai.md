---
source: hn
url: https://github.com/DimitriBouriez/navagent-mcp
published_at: '2026-03-05T23:36:46'
authors:
- DimitriBouriez
topics:
- web-automation
- mcp
- browser-agent
- token-efficiency
- anti-bot
relevance_score: 0.91
run_id: materialize-outputs
language_code: en
---

# Show HN: NavAgent – CDP-free, token-efficient web automation for AI

## Summary
NavAgent is an ultra-light web automation solution for AI. It replaces screenshots, CDP, or verbose accessibility trees with a compact numbered list of elements, reducing token costs and improving cross-site usability. It emphasizes local browser execution, low detection risk, and broad compatibility with modern web structures, making it suitable as web interaction infrastructure in the MCP ecosystem.

## Problem
- Existing AI web automation often relies on screenshots or ARIA/accessibility trees, resulting in verbose inputs. A single page may consume about **2000+ tokens** (screenshots) or **15k–20k tokens** (ARIA trees), leading to high cost and significant context waste.
- Many automation solutions depend on **CDP**, which can easily expose automation fingerprints and be detected by anti-scraping/anti-bot systems such as Cloudflare and Akamai, reducing usability on real websites.
- Modern websites contain complex structures such as **SPAs, shadow DOM, iframes, and contenteditable rich-text editors**. Traditional web agents are often unstable or incomplete in their coverage, which matters for coding agents and automated software production because they need to execute tasks reliably in real browsers.

## Approach
- The core mechanism is: **scan the webpage into a numbered list of actionable elements for the AI to view**, instead of providing a full screenshot or the entire accessibility tree; the AI then selects target elements through simple actions such as `browse_click(6)`.
- The system architecture has two parts: **an MCP server + a Chrome extension**. The MCP server connects to clients such as Claude Code, Cursor, and Zed through `stdio`, then communicates with the extension over a local WebSocket.
- On the extension side, a content script scans the DOM via **Chrome native extension messaging** using `chrome.tabs.sendMessage`, and **does not use CDP**; therefore it does not trigger typical automation markers such as `navigator.webdriver`.
- The DOM scanner identifies strongly/weakly clickable elements and additionally handles **SPA hash routing, shadow DOM (forced open), same-origin iframe traversal, contenteditable editors, and page region/landmark detection**, improving navigation and input success rates on complex pages.
- The solution runs entirely in a **local real browser session**, reusing the user's cookies and login state, and claims **zero telemetry**, listening only on local `127.0.0.1`.

## Results
- The clearest quantified benefit provided in the paper/project excerpt is **token efficiency**: compared with about **2000+ tokens** for screenshots and about **15,000–20,000 tokens** for ARIA trees, its numbered-list representation is more compact, but it **does not provide average token counts, compression ratios, or task success statistics on a unified benchmark**.
- Claimed engineering coverage includes support for **SPAs, shadow DOM, same-origin iframes, and contenteditable editors**, and it is shown in navigation examples on real sites such as Amazon; however, it **does not provide datasets, success rates, or comparison baselines**.
- The anti-detection claim is that because it uses **native extension messaging rather than CDP**, it is “undetectable/anti-bot-proof” against systems such as Cloudflare and Akamai; however, there are **no experiment designs, false positive rates, or pass-rate figures**.
- The compatibility claim is that it can connect to **Claude Code, Claude Desktop, Cursor, Windsurf, Zed, OpenClaw**, and “any MCP client,” emphasizing its portability as a general-purpose MCP browser navigation layer.
- For software quality, one concrete number is given: the project has **111 tests** (`vitest + jsdom`), indicating at least some degree of engineering validation, though this **is not equivalent to academic performance metrics**.

## Link
- [https://github.com/DimitriBouriez/navagent-mcp](https://github.com/DimitriBouriez/navagent-mcp)
