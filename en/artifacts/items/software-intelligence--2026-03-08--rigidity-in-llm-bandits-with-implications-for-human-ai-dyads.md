---
source: arxiv
url: http://arxiv.org/abs/2603.07717v1
published_at: '2026-03-08T16:42:25'
authors:
- Haomiaomiao Wang
- "Tom\xE1s E Ward"
- Lili Zhang
topics:
- llm-behavior
- decision-making
- bandit-learning
- human-ai-dyads
- cognitive-modeling
relevance_score: 0.43
run_id: materialize-outputs
language_code: en
---

# Rigidity in LLM Bandits with Implications for Human-AI Dyads

## Summary
This paper studies whether large language models, when treated as “decision-makers” in two-armed bandits, exhibit stable and repeatable decision biases. The conclusion is: LLMs often amplify small initial or positional cues into rigid strategies, and this phenomenon remains robust under changes to common decoding parameters.

## Problem
- The paper aims to address: **whether LLMs exhibit robust behavioral biases in interactive decision-making, rather than merely errors at the level of accuracy**.
- This matters because in human-AI collaboration, a model’s early leanings, order effects, and overconfidence may continuously influence human judgment and amplify bias.
- Existing benchmarks usually measure “whether the answer is correct,” but less often test **how models learn, when they explore, and whether they rigidly stick to one choice**.

## Approach
- The authors treated DeepSeek, GPT-4.1, and Gemini-2.5 as experimental participants and tested them in two-armed bandit tasks under symmetric reward conditions (0.25/0.25) and asymmetric reward conditions (0.75/0.25).
- Each condition involved **200 independent simulations × 100 trials**, and compared 4 decoding settings: Strict, Moderate, Default-like, and Exploratory, varying temperature and top-p.
- To enforce a binary choice, outputs were restricted to **1 token**, accepting only `X` or `Y`; invalid outputs were recorded as failures and included in the analysis.
- At the behavioral level, they measured metrics such as total reward, target-arm choice rate, loss-shift / win-shift, choice bias, stubbornness, amplification, and rigidity.
- At the mechanistic level, they fit a **hierarchical Rescorla-Wagner learning model + softmax policy**. The core explanation is very simple: the models **update very slowly (low learning rate), but once they lean one way they choose very rigidly (high inverse temperature)**, so early accidental signals are quickly crystallized.

## Results
- Under symmetric conditions (0.25/0.25), theory suggests performance should be close to 50/50 with about **25/100** reward; the LLMs’ total rewards were indeed close to chance level, for example DeepSeek **24.60±0.62**, Gemini-2.5 **24.71±0.56**, and GPT-4.1 **25.38±0.61**, but the choice distributions were clearly skewed, indicating that they were **not better at learning, but better at solidifying preferences**.
- Under symmetric conditions, Gemini-2.5 under strict decoding showed the strongest bias toward the earlier-presented X: **(X,Y)=(0.61±0.44, 0.39±0.44)**; GPT-4.1 also favored X, such as **(0.55±0.40, 0.45±0.40)**; meanwhile under the strict condition, Loss-Shift was nearly 0: DeepSeek **0.03±0.00**, Gemini **0.03±0.00**, GPT-4.1 **0.09±0.01**.
- The “rigidity” metrics under symmetric conditions were very high: under the Strict setting, the Stubbornness Rate reached DeepSeek **0.97±0.02**, Gemini **0.95±0.03**, and GPT-4.1 **0.90±0.04**; the Rigidity Index was near ceiling at **0.96–0.99±0.01**. Based on this, the authors argue: **in ambiguous environments, LLMs amplify weak positional cues into stubborn one-arm policies**.
- Under asymmetric conditions (0.75/0.25), the models usually selected the better arm, but still behaved too rigidly. Total reward remained below the ideal oracle’s **75/100**, for example DeepSeek **72.68±1.44**, GPT-4.1 **73.15±0.92**, and Gemini’s peak under the strict setting **74.22±1.00**.
- Under asymmetric conditions, the target-arm choice rate under the strict setting was almost at ceiling: DeepSeek **0.95±0.03**, Gemini **0.98±0.02**, GPT-4.1 **0.96±0.01**; but the Adjusted Choice Bias Index was **-0.04 to -0.09**, indicating that relative to the oracle there was still **insufficient re-checking and insufficient exploration**.
- The key mechanistic result from the computational model is: in the symmetric-condition group, learning rates were **μ_A=0.09–0.22**, while inverse temperature was nearly at ceiling **μ_τ=4.9984–4.9991**; in the asymmetric condition, learning rates rose slightly to **0.17–0.33**, but inverse temperature remained extremely high at **4.991–4.998**. The authors regard this as the paper’s core contribution: **using a simple cognitive model to unify “amplifying noise into bias” and “rigid exploitation” as low learning rate + extremely deterministic choice**.

## Link
- [http://arxiv.org/abs/2603.07717v1](http://arxiv.org/abs/2603.07717v1)
