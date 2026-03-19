---
source: hn
url: https://xeolint.com/
published_at: '2026-03-14T23:19:44'
authors:
- antoinelevy27
topics:
- seo
- llm-discoverability
- nextjs
- cli-linter
- developer-tools
relevance_score: 0.02
run_id: materialize-outputs
language_code: en
---

# CLI linter for GEO and SEO discoverability

## Summary
XEOLint is an open-source CLI checking tool for Next.js websites, aimed at improving their ability to be discovered and understood by large language models and search engines. It emphasizes that rapidly developed projects often overlook “discoverability” issues, and provides automated checks to fill that gap.

## Problem
- Many rapidly iterated projects go live quickly, but have shortcomings in **LLM discoverability** and **SEO discoverability**.
- If a website cannot be correctly crawled, parsed, and understood by search engines or AI systems, it directly affects traffic acquisition, content exposure, and the chance that users discover the product.
- This problem matters because as AI-driven search and agent usage increase, websites need to be friendly not only to traditional search engines, but also to LLMs.

## Approach
- The core method is a **CLI linter**: like static code analysis, it checks Next.js websites for discoverability issues.
- It helps developers find problems in the simplest way before release: after installing the tool, run checks to identify defects that affect GEO/SEO.
- Mechanistically, it targets two discovery channels—**LLMs and search engines**—and tries to unify checks for website visibility issues across both entry points.
- Based on the provided information, it is currently **open source v0.1.0** and can be installed via `pip install xeolint`, indicating it is positioned as a lightweight tool that can be integrated into the development workflow.

## Results
- The provided content **does not give any quantitative results**; it does not report datasets, evaluation metrics, baseline methods, or performance improvement figures.
- The strongest concrete claim is that XEOLint “ensures” Next.js websites are **discoverable by LLMs and search engines**.
- The explicitly stated factual information includes: **open source**, version **v0.1.0**, and support for installation via **pip install xeolint**.
- Because experiments, comparisons, and benchmarks are lacking, it is not possible to verify the magnitude of its practical improvement relative to existing SEO tools or website auditing tools.

## Link
- [https://xeolint.com/](https://xeolint.com/)
