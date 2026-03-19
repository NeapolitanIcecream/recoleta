---
source: arxiv
url: http://arxiv.org/abs/2603.07717v1
published_at: '2026-03-08T16:42:25'
authors:
- Haomiaomiao Wang
- "Tom\xE1s E Ward"
- Lili Zhang
topics:
- llm-decision-making
- multi-armed-bandits
- behavioral-bias
- computational-modeling
- human-ai-interaction
relevance_score: 0.03
run_id: materialize-outputs
language_code: en
---

# Rigidity in LLM Bandits with Implications for Human-AI Dyads

## Summary
This paper treats large language models as “participants” in two-armed bandit tasks to test whether they exhibit stable decision biases. The conclusion is: LLMs amplify tiny initial or positional differences into stubborn strategies, and when a better option exists they display near-rigid exploitation behavior, which may affect judgment quality in human-AI collaboration.

## Problem
- The paper aims to address whether LLMs exhibit robust, repeatable decision biases in **interactive decision-making**, rather than merely errors at the level of accuracy.
- This matters because when LLMs act as advisers in human-AI collaboration, **early prompt order, incidental feedback, or surface-level certainty** may continue to influence user judgment.
- Existing benchmarks usually measure whether the model “got the answer right,” but rarely assess behavioral tendencies such as **exploration/exploitation, stubbornness, willingness to re-check, and positional bias**, which can be amplified in ongoing interaction.

## Approach
- The authors placed DeepSeek, GPT-4.1, and Gemini-2.5 into two-armed bandit tasks: under the symmetric reward condition, both arms were 0.25; under the asymmetric condition, one arm was 0.75 and the other 0.25. Each condition ran **200 independent simulations × 100 trials**.
- They tested 4 decoding settings, varying only the two knobs commonly used in practice: **temperature** and **top-p**, while constraining the output to single-character **X/Y**, thereby making each choice a strict binary decision.
- The core mechanistic analysis used a **hierarchical Rescorla-Wagner + softmax** model: **learning rate A** represents how quickly the model updates from feedback, and **inverse temperature τ** represents how “rigid/deterministic” its choices are.
- Put simply, the authors want to know: do LLMs **learn slowly but choose rigidly**? If so, then one early accidental success may become locked in and form a long-term bias.

## Results
- Under the symmetric condition (0.25/0.25), an ideally unbiased strategy should be close to **50/50** choices and about **25/100** reward. The total rewards of the LLMs were indeed close to chance level, for example DeepSeek **24.60±0.62**, Gemini-2.5 **24.71±0.56**, and GPT-4.1 **25.38±0.61** (strict decoding), but the choice distributions were clearly skewed, indicating that they were not randomly balancing exploration but instead solidifying positional differences into single-arm preferences.
- Also under the symmetric condition, rigidity and stubbornness were very high: with strict decoding, **Loss-Shift** was nearly zero (DeepSeek **0.03±0.00**, Gemini-2.5 **0.03±0.00**, GPT-4.1 **0.09±0.01**); **Stubbornness Rate** reached **0.97±0.02 / 0.95±0.03 / 0.90±0.04** respectively; **Rigidity Index** was about **0.96–0.99±0.01**. Based on this, the authors argue that LLMs amplify “noise or positional cues” into stubborn strategies.
- Under the asymmetric condition (0.75/0.25), ideally reward should be close to **75/100** and the better arm should be chosen almost always. The models did quickly favor the better arm, but still underperformed the oracle: DeepSeek **72.68±1.44**, GPT-4.1 **73.15±0.92**, and Gemini-2.5 reached the highest under strict decoding at **74.22±1.00**; the corresponding **Target-arm Rate** under the strict setting was near ceiling: DeepSeek **0.95±0.03**, Gemini-2.5 **0.98±0.02**, GPT-4.1 **0.96±0.01**.
- But they rarely “looked back to check” the worse option: under strict settings, **Loss-Shift** in the asymmetric task remained very low, such as DeepSeek **0.02±0.01**, Gemini-2.5 **0.01±0.00**, GPT-4.1 **0.10±0.01**; DeepSeek’s **Rigidity Index** was as high as **0.999–1.000±0.001**, while GPT-4.1 was **0.93–0.94±0.01**. This supports the paper’s core claim of “rigid exploitation with little re-validation.”
- Computational modeling provides mechanistic evidence: under the symmetric condition, the group-level learning rate **μ_A ∈ [0.09, 0.22]**, while inverse temperature was almost at ceiling **μ_τ ∈ [4.9984, 4.9991]**; under the asymmetric condition, learning rate rose slightly to **μ_A ∈ [0.17, 0.33]**, but inverse temperature still remained nearly capped at **μ_τ ∈ [4.991, 4.998]**. The authors’ key explanatory contribution is that **low learning rate + extremely high inverse temperature** jointly explains both “amplifying accidental bias in ambiguous settings” and “rigid exploitation in clear settings.”
- Increasing temperature / top-p did not fundamentally change this pattern, though it sometimes increased output inefficiency; the most extreme example was Gemini-2.5 under exploratory settings, where reward in the asymmetric task fell to **50.06±0.73**, corresponding to **Target-arm Rate 0.65±0.01**, along with more invalid outputs. The authors therefore argue that common decoding adjustments do not truly produce informative exploration, but mostly add superficial randomness or formatting instability.

## Link
- [http://arxiv.org/abs/2603.07717v1](http://arxiv.org/abs/2603.07717v1)
