---
source: hn
url: https://blog.cloudflare.com/enterprise-mcp/
published_at: '2026-05-12T23:46:13'
authors:
- Daviey
topics:
- mcp
- agentic-workflows
- enterprise-ai-security
- ai-governance
- tool-use
- token-efficiency
relevance_score: 0.78
run_id: materialize-outputs
language_code: en
---

# Scaling MCP adoption: Our ref architecture – simpler,safer&cheaper deployments

## Summary
Cloudflare describes a governed enterprise MCP deployment that moves MCP servers off employee machines and behind shared access, logging, DLP, and cost controls. The strongest claimed gain is Code Mode, which cuts tool-definition context from about 9,400 tokens to 600 tokens for one internal portal setup.

## Problem
- Enterprise MCP adoption creates risks: authorization sprawl, prompt injection, unvetted local servers, tool injection, supply chain exposure, and data leakage.
- Local MCP servers leave version choice, updates, and source trust to individual employees, which makes audit and policy enforcement hard.
- Large MCP deployments also waste context because a client may receive every tool schema before it knows which tools it needs.

## Approach
- Cloudflare runs MCP servers as remote services on its developer platform, with a central team managing templates, CI/CD, secrets, audit logging, and default-deny write controls.
- Cloudflare Access supplies OAuth-based authentication and checks SSO, MFA, IP, location, and device attributes before private MCP servers can be used.
- MCP server portals give each employee one client endpoint that exposes only authorized internal and third-party MCP servers, with logging, policy enforcement, and DLP rules.
- Code Mode collapses many upstream MCP tools into two portal tools: search finds tool definitions on demand, and execute runs sandboxed JavaScript that calls the selected tools.
- AI Gateway sits between MCP clients and LLM providers for provider switching and token limits, while Cloudflare Gateway scans traffic for shadow MCP servers using URL and JSON-RPC body patterns.

## Results
- A Cloudflare MCP server design exposes thousands of Cloudflare API endpoints through 2 tools and claims a 99.9% reduction in token use compared with exposing all endpoints as separate tools.
- In one internal portal connected to 4 MCP servers, 52 tools used about 9,400 context tokens for definitions; Code Mode reduced this to about 600 tokens across 2 portal tools, a 94% reduction.
- The Jira plus Google Drive example takes 2 tool calls with Code Mode: 1 search call and 1 execute call. The non-Code Mode version would require full schemas upfront and 3 separate tool invocations.
- The proposed shadow MCP detection uses URL paths such as /mcp and /mcp/sse plus JSON-RPC body matches for methods including initialize, tools/call, tools/list, resources/read, resources/list, prompts/list, and sampling/createMessage.
- The excerpt gives product and deployment claims and does not include an external benchmark or controlled evaluation against other MCP security products.

## Link
- [https://blog.cloudflare.com/enterprise-mcp/](https://blog.cloudflare.com/enterprise-mcp/)
