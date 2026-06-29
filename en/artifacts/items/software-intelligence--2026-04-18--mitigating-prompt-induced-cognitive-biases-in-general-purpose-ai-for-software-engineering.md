---
source: arxiv
url: http://arxiv.org/abs/2604.16756v2
published_at: '2026-04-18T00:11:35'
authors:
- Francesco Sovrano
- Gabriele Dominici
- Alberto Bacchelli
topics:
- prompt-bias
- software-engineering
- llm-evaluation
- prompt-engineering
- reasoning-cues
relevance_score: 0.92
run_id: materialize-outputs
language_code: en
---

# Mitigating Prompt-Induced Cognitive Biases in General-Purpose AI for Software Engineering

## Summary
This paper studies whether wording alone can push general-purpose AI systems toward worse software engineering decisions, and whether simple prompting can fix that. The main result is that common prompt tricks do little, while injecting explicit software engineering best-practice rules cuts bias sensitivity by about 51% on average.

## Problem
- The paper targets **prompt-induced cognitive bias** in software engineering decision support: models change their answer because of biased wording such as framing, popularity hints, or hindsight cues, even when the task logic stays the same.
- This matters because many software engineering tasks arrive as natural-language requirements, tradeoff questions, design choices, and prioritization prompts, so small phrasing changes can push a model toward a worse decision.
- Prior PROBE-SWE results cited here show bias sensitivity from **5.9% to 35.3%** across eight bias types, reaching **49%** on more complex tasks.

## Approach
- The authors use **PROBE-SWE**, a benchmark of paired biased and unbiased software engineering dilemmas with matched logic, to isolate answer changes caused only by wording.
- They test several off-the-shelf prompting methods on cost-effective models from the **GPT, LLaMA, and DeepSeek** families: chain-of-thought, imperative self-debiasing, impersonated self-debiasing, and implication prompting.
- Their core idea is that software engineering decisions need explicit background rules such as best practices, but biased wording can make the model skip those implicit rules and follow a shortcut.
- To counter that, they introduce **axiomatic background self-elicitation** and **axiomatic reasoning cues**: short declarative software engineering rules are added to the prompt before the model answers.
- They also report a thematic analysis of output language to identify linguistic patterns linked to higher bias sensitivity, and mention a robustness check with open-ended answers plus an analysis of the DevGPT corpus.

## Results
- On RQ1, common prompt methods do not reliably solve the problem. **Chain-of-thought performs worst at 16.1% average sensitivity**, compared with the **no-strategy baseline at 12.9%**.
- **Implication prompting** reaches **13.3%** average sensitivity, also worse than baseline.
- **Imperative self-debiasing (10.3%)** and **impersonated self-debiasing (10.2%)** improve on baseline, and their combination **BW+IsD** reaches **8.3%**, a **4.6 percentage-point** drop from **12.9%** baseline.
- Even with that drop, the paper says there are **no statistically significant per-bias reductions** after FDR correction for BW+IsD, BW, or IsD alone (**all p >= 0.07**), and no significant per-model improvements either.
- The paper’s main claimed breakthrough is the axiomatic prompting method, which **reduces overall bias sensitivity by about 51% on average (p < .001)**.
- For some bias types, the reduction reaches **up to 73%**. The excerpt does not provide the full per-bias table for the axiomatic method, but these are the strongest quantitative claims stated in the text.

## Link
- [http://arxiv.org/abs/2604.16756v2](http://arxiv.org/abs/2604.16756v2)
