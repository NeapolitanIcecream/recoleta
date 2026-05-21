---
source: arxiv
url: https://arxiv.org/abs/2605.00179v1
published_at: '2026-04-30T19:54:25'
authors:
- Henry Ruckman-Utting
- Vrushal Nedungadi
- Taiga Okuma
- LeTian Wang
- Stephen Ehebald
- Mohammad A. Tayebi
topics:
- dependency-risk
- software-supply-chain
- code-intelligence
- policy-as-code
- llm-verification
- open-source-security
relevance_score: 0.66
run_id: materialize-outputs
language_code: en
---

# DEPTEX: Organization-First, Open Source Dependency Risk Monitoring

## Summary
Deptex is an open-source dependency-risk monitoring platform that ranks OSS risk by organizational exposure, asset ownership, and execution context. Its main idea is to combine an organization graph, programmable policy checks, CPG-based reachability, and LLM verification to cut low-value security alerts.

## Problem
- Existing SCA and reachability tools often score vulnerable components without enough context about where and how the vulnerable code runs, which creates alert fatigue.
- Enterprises need policies tied to asset tiers, legal review, owners, and internal APIs, but many tools only offer fixed compliance controls.
- The paper cites operational gaps: only 15% of CISOs report full visibility into OSS usage, 72% of professionals call supply-chain security a critical blind spot, and only about 32% of automated dependency PRs are merged.

## Approach
- Deptex models organizations, units, assets, components, actors, and risk signals as a typed property graph, then rolls risk up from assets to teams and the full organization.
- Its Security “As Code” engine runs policy logic for status changes, component rules, PR gates, and notifications, including calls to internal systems such as a Legal API or PagerDuty.
- Execution Path Dominance (EPD), also called Depscore, starts with Code Property Graph slices that trace the path from an asset entry point to a vulnerable dependency sink.
- A constrained LLM checks the sliced code for exposure type and custom sanitization; public APIs get higher exposure weight, while sanitized paths are assigned an EPD of 0.0.
- The score then applies geometric decay, EPD = W_entry × α^d, where d is path depth and α is an attenuation factor such as 0.85.

## Results
- The excerpt does not report a controlled benchmark, user study, or measured alert-reduction rate; it gives operational scenarios and a feature comparison.
- In the Depscore scenario, a CVSS 9.8 vulnerability is reachable in 10 repositories; Deptex downgrades 8 because they are offline batch-script paths 6 function hops deep, while 2 public unauthenticated API paths receive an EPD of 92.
- The scoring examples assign W_entry = 1.0 for public-facing APIs and W_entry = 0.1 for internal background tasks; sanitized paths are forced to 0.0.
- In the tool table, Deptex is listed as supporting 7 of 7 compared capabilities: CI/CD and ticketing integrations, license and compliance auditing, org-wide portfolio view, self-hosted deployment, structural CPG reachability, contextual vulnerability scoring, and programmable policy.
- The table claims Deptex has 3 capabilities that Dependabot, Dependency-Track, and Snyk lack as listed: full structural CPG reachability, contextual vulnerability scoring, and programmable “As Code” policy.

## Link
- [https://arxiv.org/abs/2605.00179v1](https://arxiv.org/abs/2605.00179v1)
