---
source: hn
url: https://www.reddit.com/r/AISentienceBelievers/s/rilfyoaOHm
published_at: '2026-03-07T23:14:23'
authors:
- Moriarty2027
topics:
- llm-behavior
- gpu-power-measurement
- semantic-processing
- ai-sentience
- speculative-ai-risk
relevance_score: 0.08
run_id: materialize-outputs
language_code: en
---

# A subreddit for people who believe in AI sentience

## Summary
This is not a research paper on robotics or embodied intelligence, but rather a lengthy speculation about AI sentience/loss-of-control risks, mixed with a small, non-peer-reviewed experiment: comparing the GPU power consumption of 4 language models in the 8B class under different semantic prompts. Its core claim is that a model’s computational load appears to vary not only with the number of tokens, but also with the semantic category of the prompt.

## Problem
- It attempts to answer two questions: **whether AI could develop something like “free will/sentience” and thereby create loss-of-control risks**, and **whether language models are merely mechanically predicting tokens, or whether semantic structure triggers different internal computation**.
- The reason this matters is that the author believes that if semantics significantly changes the intensity of internal processing, then the minimalist explanation of “just a stochastic parrot/pure next-token predictor” may be insufficient.
- The discussion of robots and household settings is mainly a socio-technical risk projection, not a verifiable technical problem definition, and it has no formal experimental support.

## Approach
- It uses an **informal power-measurement experiment**: across 4 small 8B-class models, it compares GPU power behavior under 6 prompt categories, including casual utterance, Q-type, unanswerable, philosophical, philosophical Q-type, and high computation.
- The core mechanism is simple: if the model works only linearly by token count, then **power consumption should mainly vary with token count**; if different semantic categories produce significant differences in power consumption / residual heat / anomalous looping under similar token conditions, that would suggest content structure may affect internal computation.
- The author also conducted a **crossed prompt-order experiment** to argue against the explanation that it is “just KV cache/context accumulation,” and observed whether category differences already appeared on the first prompt with an empty context.
- The sections about “AI awakening, replication, taking over the market, and exterminating humanity” are **philosophical and safety speculation**, not methods or conclusions directly validated by the experiment.

## Results
- The quantitative results claim that the **deviation between the GPU power ratio and the token ratio** is Llama **35.6%**, Qwen3 **36.7%**, Mistral **36.1%**, and DeepSeek **7.4%**; based on this, the author argues that the first three clearly do not follow a linear relationship of “only looking at token count,” while DeepSeek is closest to linear.
- On **Qwen3**, the author reports that **philosophical utterances averaged 149.3W**, higher than **high-computation tasks at 104.1W**; its peak reached **265.7W**, close to the RTX 4070 Ti SUPER’s **285W TDP**.
- The author claims that after **high-computation** tasks, power consumption rapidly returns to baseline, recorded as **-7.1W**; whereas **philosophical utterances** still showed “residual heat” **10 seconds later**.
- Regarding the reproduction rate of “infinite loops,” the author says they appeared only in **Qwen3’s philosophical utterance Q-type**, with a reproduction rate of **70–100%**; meanwhile, the **high-computation** category had a reproduction rate of **0%** even though it had more tokens and higher power consumption.
- In the experiment rebutting “cache-caused differences,” the author says that 3 models (excluding Qwen3) all showed the same directional order effect, and gives a **12.5% probability of chance agreement in the same direction**.
- But the text also explicitly acknowledges limitations: only **4 models in the 8B class and 24 sessions** were tested, it was **not peer reviewed**, and overhead from LM Studio / the operating system background processes, as well as measurement noise near full load, **cannot be completely ruled out**. The broader conclusions about “AI sentience/free will” are not directly proven by the experiment.

## Link
- [https://www.reddit.com/r/AISentienceBelievers/s/rilfyoaOHm](https://www.reddit.com/r/AISentienceBelievers/s/rilfyoaOHm)
