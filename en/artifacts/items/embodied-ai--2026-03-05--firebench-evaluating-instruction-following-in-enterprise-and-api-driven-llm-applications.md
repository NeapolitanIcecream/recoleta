---
source: arxiv
url: http://arxiv.org/abs/2603.04857v1
published_at: '2026-03-05T06:25:50'
authors:
- Yunfan Zhang
- Yijie Bei
- Jetashree Ravi
- Pawel Garbacki
topics:
- llm-evaluation
- instruction-following
- enterprise-llm
- api-reliability
- benchmark
relevance_score: 0.03
run_id: materialize-outputs
language_code: en
---

# FireBench: Evaluating Instruction Following in Enterprise and API-Driven LLM Applications

## Summary
FireBench is an instruction-following benchmark for enterprise and API scenarios, specifically testing whether models can execute tasks while strictly adhering to format, order, content constraints, and uncertainty requirements. The paper shows that current frontier LLMs are still clearly unreliable under these production-critical constraints.

## Problem
- Existing instruction-following benchmarks mostly focus on chat-assistant-style constraints (such as word count, tone, and keywords) and do not reflect the truly critical needs in enterprise/API workflows: **strict formats, fixed ordering, content inclusion/exclusion, and refusal**.
- In enterprise settings, even if a model’s “answer is mostly correct,” as long as the output format is wrong, the step order is wrong, forbidden content is included, or it answers recklessly when uncertain, it can directly break downstream automated workflows. This makes the problem highly important.
- The paper aims to solve: **how to systematically evaluate precise instruction-following ability of LLMs in real enterprise and API-driven applications**, in order to support model selection, diagnosis, and improvement.

## Approach
- Introduces **FireBench**, a benchmark built around 6 enterprise-critical capability dimensions: output format compliance, ordered responses, item ranking, overconfidence, positive content requirements, negative content requirements.
- The benchmark covers a variety of real applications: long-document information extraction, knowledge/reasoning QA, multi-turn customer support workflows, table ranking, coding agents, and more, with **2,470** samples in total.
- Subtasks are designed to be verifiable whenever possible: most are scored automatically by program; for positive/negative content requirements, GPT-5 is used to generate constraints and rubrics, and GPT-4.1 serves as the judge.
- Sample counts include: format **1,300**, ordered responses **200**, ranking **200**, overconfidence **370**, positive content **200**, negative content **200**.
- The benchmark evaluates **11** frontier open-source and closed-source models, comparing overall performance, category differences, and differences between reasoning and non-reasoning versions.

## Results
- **Even the strongest overall model did not exceed 75%**: DeepSeek V3.1 Terminus ranked first with **74.0%**, GPT-5.1 Medium Thinking second with **72.7%**, and GPT-4.1 at **70.5%**; most models scored **below 67%**, showing that enterprise/API instruction following is far from solved.
- **Performance varies greatly across categories**: DeepSeek V3.1 has a cross-category standard deviation of **13.1** percentage points; GPT-4.1 shows the highest variation at **25.5** percentage points. GPT-4.1 is very strong on Format **86.9%**, Positive **94.5%**, and Negative **94.5%**, but weak on Ranking **32.5%** and Overconfidence **38.6%**.
- **Different categories have different leaders**: Format is best on GPT-4.1 at **86.9%**; Ordered Responses is best on GPT-4.1 at **76.3%**; Ranking is best on GPT-5.1 Medium Thinking at **93.0%**; Overconfidence is best on DeepSeek V3.1 at **86.0%**; Positive is best on GPT-4.1 at **94.5%**; Negative is a tie between GPT-4.1 / Kimi K2 Instruct at **94.5%**.
- **Reasoning versions are usually stronger**: GPT-5.1 Medium Thinking scores **72.7%** versus GPT-5.1 Instant at **58.6%**, an improvement of **14.1** points; Kimi K2 Thinking **63.2%** versus Kimi K2 Instruct **62.1%**; Qwen3 235B Thinking **66.6%** versus Instruct **66.3%**.
- **Ranking tasks show the largest reasoning advantage**: GPT-5.1 Medium Thinking scores **93.0%** on Ranking, while GPT-5.1 Instant reaches only **16.0%** (+**77.0** points); Qwen3 Thinking **76.0%** vs Instruct **38.0%**; Kimi K2 Thinking **72.5%** vs Instruct **8.5%**.
- **Format following remains fragile**: although GPT-4.1 performs best in the format category, it still reaches only **86.9%**. The authors further note that models appear to memorize familiar formats rather than generalize: on the standard `\boxed{}`, both GPT-4.1 and Qwen3 235B Instruct achieve **100%**, but on the adversarial variant `\boxed[ ]`, they drop to **53%** and **73%**, respectively.

## Link
- [http://arxiv.org/abs/2603.04857v1](http://arxiv.org/abs/2603.04857v1)
