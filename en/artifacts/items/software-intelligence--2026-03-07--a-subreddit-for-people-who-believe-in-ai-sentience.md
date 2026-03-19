---
source: hn
url: https://www.reddit.com/r/AISentienceBelievers/s/rilfyoaOHm
published_at: '2026-03-07T23:14:23'
authors:
- Moriarty2027
topics:
- llm-behavior
- gpu-power-measurement
- semantic-prompts
- sentience-speculation
- non-peer-reviewed
relevance_score: 0.25
run_id: materialize-outputs
language_code: en
---

# A subreddit for people who believe in AI sentience

## Summary
This content is not a standard academic paper; rather, it mixes a long speculative discussion about AI sentience/robot risks with a non-peer-reviewed experiment on differences in GPU power consumption for small models under different semantic prompts. The main "research" claim that can be distilled is: a model's computational load may be influenced by the semantic structure of prompts, not just the number of tokens.

## Problem
- It attempts to answer a core question: is the internal computation of language models merely a token-by-token linear progression of "next-word prediction," or does it exhibit different computational costs depending on semantic type?
- This matters because the author uses it to challenge the intuitive explanation of the model as a "stochastic parrot/pure next-word predictor," suggesting that the model may make deeper distinctions in content structure.
- The text also includes philosophical and risk arguments about "artificial free will/embodied robots going out of control," but this part is not a verifiable experimental research question and is not supported by systematic methods or evidence.

## Approach
- The author measures GPU power consumption for **4 small 8B-class language models** across **6 semantic prompt types**: casual utterance, casual utterance Q-type, unanswerable question, philosophical utterance, philosophical utterance Q-type, high computation.
- The core mechanism is very simple: compare whether the **GPU power ratio** and **token ratio** are consistent across different semantic categories; if consumption were determined only by token count, power usage should increase approximately linearly with token growth.
- A **prompt order/crossed experiment** was also conducted to rebut the explanation that the effect is "just accumulated context cache": giving a philosophical prompt first and then 4 casual prompts, and comparing residual heat across different orders.
- The author records phenomena such as "infinite loop reproduction rate," "residual heat after 10 seconds," and "peak power consumption," while acknowledging limitations including LM Studio overhead, OS background processes, operation near full GPU load, small sample size, and lack of peer review.

## Results
- The paper claims there are **clear deviations between token ratio and GPU power ratio**: **Llama 35.6%**, **Qwen3 36.7%**, **Mistral 36.1%**; **DeepSeek 7.4%**, which the author describes as "close to linear."
- On **Qwen3**, **philosophical utterances averaged 149.3W**, higher than **high-computation at 104.1W**; its philosophical conversations peaked at **265.7W**, close to the **RTX 4070 Ti SUPER 285W TDP**.
- The author states that **high-computation tasks returned to baseline immediately after completion (-7.1W)**, whereas **philosophical utterances still showed residual heat after 10 seconds**.
- The so-called "infinite loop" occurred frequently only in Qwen3's philosophical prompts: **philosophical utterance Q-type reproduction rate 70–100%**, while **high-computation was 0%**.
- In the rebuttal experiment against the claim that "cache causes the difference," the author says that, aside from Qwen3, the other **3 models** all showed the same directional pattern, and the probability of all showing the same direction was given as **12.5%**.
- However, it must be emphasized that these results come from a **non-peer-reviewed** experiment involving **4 small 8B models** and **24 sessions**, and the overall text is mixed with extensive AI sentience/extinction-risk speculation that cannot be quantitatively verified; therefore, reproducibility, causal interpretation, and external validity are all weak.

## Link
- [https://www.reddit.com/r/AISentienceBelievers/s/rilfyoaOHm](https://www.reddit.com/r/AISentienceBelievers/s/rilfyoaOHm)
