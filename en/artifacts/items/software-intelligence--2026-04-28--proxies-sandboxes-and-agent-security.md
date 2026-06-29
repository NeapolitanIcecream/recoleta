---
source: hn
url: https://www.gouthamve.dev/proxies-sandboxes-and-agent-security/
published_at: '2026-04-28T23:41:32'
authors:
- gouthamve
topics:
- agent-security
- credential-proxy
- sandboxing
- ai-sre
- prompt-injection
- gvisor
relevance_score: 0.66
run_id: materialize-outputs
language_code: en
---

# Proxies, Sandboxes and Agent Security

## Summary
The post describes a practical security design for letting an AI SRE manage a home lab without exposing real service credentials to the agent. It uses credential-injection HTTP proxies and considers gVisor sandboxes for stricter network control.

## Problem
- An SRE agent needs access to GitHub, Kubernetes, Grafana, Todoist, Matrix, and other tools, which creates a credential exposure risk.
- Prompt injection through web pages or documents could make the agent read secrets and send them out through normal network calls.
- Destructive commands are less severe in this setup because the agent runs in a rootless container and the author keeps important state in git.

## Approach
- Put fake credentials inside the agent container, such as `fake-todoist-token`, and route HTTP and HTTPS traffic through a credential proxy.
- Configure the proxy to replace fake tokens with real tokens for specific hosts and headers, such as `api.todoist.com` `Authorization` and `api.parallel.ai` `x-api-key`.
- Add the proxy CA certificate to the container trust store so the proxy can inspect and rewrite HTTPS requests.
- Use domain allow or deny rules in a gVisor-based sandbox to intercept outbound requests below the application proxy layer.

## Results
- The post reports no quantitative benchmark results, datasets, or accuracy metrics.
- No breakthrough result is claimed; the strongest claim is that proxy-based token injection can keep real credentials out of the agent container.
- The proxy design handled credential injection for at least 3 example services: Todoist, Parallel, and Matrix.
- The author found 2 concrete proxy integration failures: Chrome with Playwright did not pick up the proxy CA, and the Matrix client path did not honor `HTTP_PROXY` because of library behavior.
- The gVisor sandbox claim is concrete but unmeasured: its Go networking stack can intercept outbound requests even when an application ignores `HTTP_PROXY`.

## Link
- [https://www.gouthamve.dev/proxies-sandboxes-and-agent-security/](https://www.gouthamve.dev/proxies-sandboxes-and-agent-security/)
