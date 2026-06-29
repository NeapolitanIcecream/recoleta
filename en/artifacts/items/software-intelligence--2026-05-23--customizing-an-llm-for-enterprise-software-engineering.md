---
source: hn
url: https://arxiv.org/abs/2605.16517
published_at: '2026-05-23T22:23:12'
authors:
- daureg
topics:
- enterprise-llm
- code-intelligence
- software-engineering
- llm-finetuning
- developer-tools
- internal-code-data
relevance_score: 0.96
run_id: materialize-outputs
language_code: en
---

# Customizing an LLM for Enterprise Software Engineering

## Summary
Gemini for Google (GfG) adapts Gemini to Google's internal software engineering work using proprietary development data, continued training, and post-training. The paper claims lower interaction cost and better code retention in a blind study with 29,000 developers.

## Problem
- Enterprise software teams create large private traces of code changes, reviews, deployments, and maintenance work, but general LLMs do not learn directly from that company-specific data.
- Better internal models matter because software engineering assistance must match local code, tools, architecture, and review expectations.
- The main risk is that extra training on internal data can damage general model ability through catastrophic forgetting.

## Approach
- The authors build Gemini for Google, a Gemini adaptation tuned for Google's internal software engineering environment.
- They curate a proprietary software engineering dataset at trillion-token scale.
- Training includes continued pre-training plus post-training so the model learns internal code and workflows while staying usable as an assistant.
- A mid-training strategy is used to reduce catastrophic forgetting during customization.
- The paper also describes deployment of downstream developer applications built on the customized model.

## Results
- In a blind A/B study with 29,000 Google developers, GfG beat unnamed baselines in developer interaction metrics.
- Mean iterations per turn fell by 23% versus the baselines, meaning developers needed fewer back-and-forth turns to complete a request.
- Code survival rates increased by about 17% versus the baselines, meaning more generated or assisted code remained in use.
- The adaptation process is described across 4 areas: signal extraction, data preparation, full-stack tuning, and downstream application deployment.

## Link
- [https://arxiv.org/abs/2605.16517](https://arxiv.org/abs/2605.16517)
