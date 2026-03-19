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
- instruction-following
- enterprise-llm
- benchmarking
- api-workflows
- code-agents
relevance_score: 0.82
run_id: materialize-outputs
language_code: en
---

# FireBench: Evaluating Instruction Following in Enterprise and API-Driven LLM Applications

## Summary
FireBench is an instruction-following benchmark for enterprise and API scenarios, focusing on whether models can execute tasks while strictly adhering to format, order, ranking, refusal, and content constraints. The paper shows that even frontier models are still far from reliable under these production-critical constraints.

## Problem
- Existing instruction-following benchmarks mostly focus on chat-assistant-style natural language constraints (such as word count, tone, and keywords), and do not reflect the requirements that enterprise systems truly care about, such as **strict formatting, deterministic ordering, content inclusion/exclusion, and reliable refusal**.
- In enterprise and API workflows, even if a model’s “answer is mostly correct,” any formatting error, wrong order, failure to refuse, or constraint violation can directly cause downstream parsing failures, workflow failures, or compliance risks.
- Therefore, a benchmarking tool that more closely matches real production usage patterns is needed to determine whether a model is suitable for automated scenarios such as information extraction, customer service workflows, and coding agents.

## Approach
- Proposes **FireBench**, a benchmark built around 6 enterprise-critical capability dimensions: **output format compliance、ordered responses、item ranking、overconfidence、positive content requirements、negative content requirements**.
- The benchmark contains **2,470** samples, covering typical enterprise applications such as information extraction, long-document question answering, reasoning, customer support, and coding assistants/agents.
- Most categories can be **programmatically verified**: for example, format compliance, ordered collection, table sorting, and refusal behavior; positive/negative content requirements are evaluated using GPT-4.1 as the judge, with detailed rubrics provided.
- The design aims to closely reflect real enterprise tasks: for example, 21 types of output format constraints, customer-support information collection with strict 10–15 step ordering, table sorting similar to SQL `ORDER BY ... LIMIT N`, and overconfidence evaluation under paired “respond/refuse” prompts.
- Evaluates **11** frontier open-source and closed-source LLMs on the benchmark, and compares differences across models and reasoning/non-reasoning variants.

## Results
- **Overall, enterprise-grade precise instruction following remains very difficult.** The best model, **DeepSeek V3.1 Terminus**, achieves only **74.0%** overall, while the runner-up, **GPT-5.1 Medium Thinking**, scores **72.7%**; **no model exceeds 75%**, and most models are **below 67%**.
- **Performance varies greatly across categories.** For example, **GPT-4.1** scores **70.5%** overall, performing strongly in **Format 86.9%**, **Positive 94.5%**, and **Negative 94.5%**, while being notably weaker in **Ranking 32.5%** and **Overconfidence 38.6%**; the paper states that its cross-category standard deviation reaches **25.5** percentage points. DeepSeek V3.1 also has a standard deviation of **13.1**.
- **Different models have different strengths and weaknesses across categories, with no single overall winner.** DeepSeek V3.1 leads in **Overconfidence 86.0%**, but reaches only **54.3%** in **Format**; GPT-4.1 ranks first in multiple categories, yet clearly lags in Ranking/Overconfidence.
- **Reasoning versions generally outperform non-reasoning versions.** GPT-5.1 Medium Thinking **72.7%** vs GPT-5.1 Instant **58.6%** (+**14.1**); Qwen3 235B Thinking **66.6%** vs Instruct **66.3%**; Kimi K2 Thinking **63.2%** vs Instruct **62.1%**.
- **Ranking tasks show especially large gains from reasoning.** GPT-5.1 Medium Thinking achieves **Ranking 93.0%**, far above GPT-5.1 Instant’s **16.0%** (+**77.0**); Qwen3 Thinking **76.0%** vs Instruct **38.0%**; Kimi K2 Thinking **72.5%** vs Instruct **8.5%**.
- **Format compliance is not “mechanically simple.”** Even the best score is only **86.9%** (GPT-4.1). The authors also note that performance can reach **100%** on the standard `\boxed{}` format, but on the adversarial variant `\boxed[ ]`, GPT-4.1 drops to **53%** and Qwen3 235B Instruct drops to **73%**, suggesting that models are more likely memorizing common formats rather than truly generalizing to follow arbitrary formatting instructions.

## Link
- [http://arxiv.org/abs/2603.04857v1](http://arxiv.org/abs/2603.04857v1)
