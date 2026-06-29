---
source: hn
url: https://www.obsidiansecurity.com/blog/litellm-privilege-escalation-rce
published_at: '2026-06-11T23:54:00'
authors:
- 13ph03nix
topics:
- llm-security
- ai-gateway
- privilege-escalation
- remote-code-execution
- route-authorization
- agent-security
relevance_score: 0.94
run_id: materialize-outputs
language_code: en
---

# Breaking LiteLLM: From Low-Privilege User to Admin and RCE

## Summary
Obsidian Security reports a CVSS 9.9 exploit chain in LiteLLM that lets a default low-privilege user reach admin routes and then get server-side code execution. The issue matters because LiteLLM sits between agents and model providers, so compromise can alter agent behavior, leak secrets, and push actions into downstream tools.

## Problem
- LiteLLM used caller-supplied route permissions and role checks in ways that let a key gain access beyond the caller’s own role.
- Some admin handlers trusted route checks alone and then accepted dangerous fields or executable code without a second authorization check.
- A compromise of the gateway can expose admin credentials, decrypt keys, and control traffic between an agent and its model.

## Approach
- The researchers traced LiteLLM’s authorization flow through key generation, route checks, user updates, and guardrail endpoints.
- They found that `allowed_routes` values were stored as provided and could widen access instead of only narrowing it.
- They showed that `/key/generate` and related key-write endpoints let an internal user mint a key with `allowed_routes: ["/*"]`, which then reached admin-only routes.
- After reaching admin routes, they chained into `/guardrails` or `/guardrails/test_custom_code` for code execution, and into `/user/update` or `/user/bulk_update` for privilege escalation.
- They also noted that LiteLLM’s MCP stdio support gives proxy admins a direct execution path through subprocess launch.

## Results
- The full chain is rated CVSS 9.9 and reaches admin access plus arbitrary code execution on the LiteLLM server.
- CVE-2026-47101 covers the route authorization bypass through `allowed_routes`.
- CVE-2026-47102 covers role escalation by writing `user_role: "proxy_admin"` through self-update paths.
- CVE-2026-40217 covers guardrail code execution through `exec()` with `__builtins__` available.
- BerriAI shipped fixes across later releases, with the full chain closed in LiteLLM v1.83.14-stable on 2026-04-25.
- The excerpt does not give benchmark-style performance numbers; its quantitative claims are the CVSS score, CVE IDs, endpoint names, and release version.

## Link
- [https://www.obsidiansecurity.com/blog/litellm-privilege-escalation-rce](https://www.obsidiansecurity.com/blog/litellm-privilege-escalation-rce)
