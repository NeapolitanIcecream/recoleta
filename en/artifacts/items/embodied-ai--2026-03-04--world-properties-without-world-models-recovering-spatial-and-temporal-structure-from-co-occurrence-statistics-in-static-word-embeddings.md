---
source: arxiv
url: http://arxiv.org/abs/2603.04317v1
published_at: '2026-03-04T17:37:05'
authors:
- Elan Barenholtz
topics:
- static-word-embeddings
- probing
- world-models
- distributional-semantics
- spatial-temporal-structure
relevance_score: 0.06
run_id: materialize-outputs
language_code: en
---

# World Properties without World Models: Recovering Spatial and Temporal Structure from Co-occurrence Statistics in Static Word Embeddings

## Summary
This paper challenges the common interpretation that “if spatial/temporal information can be linearly probed from a language model, then it must contain an internal world model.” The authors show that co-occurrence statistics in static word embeddings alone can recover fairly strong geographic signals and weaker but stable temporal signals, so linear decodability by itself is insufficient to prove a text-transcending world representation.

## Problem
- The paper asks: when spatial/temporal structure can be linearly recovered from LLM hidden states, does that mean the model learned a “world model,” or were these structures already latent in textual co-occurrence statistics?
- This matters because if simple distributed representations already contain similar signals, then positive probing results alone cannot demonstrate that the model truly formed an internal world representation beyond language.
- The authors also care about whether these signals are interpretable and selective, rather than probes arbitrarily “digging out” any property from the vectors.

## Approach
- Using the same type of **linear ridge regression probe** as related work, they directly predict attributes of cities and historical figures from static embeddings **GloVe 6B 300d** and **Word2Vec Google News 300d**.
- They construct two main datasets: **100 world cities** (predicting latitude, longitude, temperature, founding year, elevation, GDP, per capita, population) and **194 historical figures** (predicting birth/death/midlife year), using an 80/20 split and 5-fold cross-validation to choose regularization parameters, and report held-out $R^2$.
- To explain where the signal comes from, the authors perform **semantic neighbor/similarity analysis**: examining which ordinary words have similarities to city vectors that most strongly correlate with latitude, temperature, or historical period.
- They further perform **semantic subspace ablations**: subtracting PCA subspaces spanned by words such as “country names,” “climate words,” and “continent/region names” from city vectors, then measuring how much probe performance drops, and comparing this with ablations of random subspaces of the same dimensionality.

## Results
- On **world cities**, static embeddings already recover substantial geographic signal: for GloVe/Word2Vec, **latitude $R^2=0.709/0.663$**, **longitude $R^2=0.782/0.866$**, **mean annual temperature $R^2=0.471/0.617$**; **founding year is about $R^2=0.267/0.260$**. But **elevation, GDP per capita, and population** have near-zero or negative $R^2$, showing the signal is selective rather than arbitrarily probeable.
- On **historical figures**, the temporal signal is weaker but stable: birth year **$R^2=0.484/0.521$，MAE=356/338 years**; death year **$R^2=0.460/0.516$，MAE=364/338 years**; midlife year **$R^2=0.472/0.519$，MAE=360/338 years**. The authors therefore describe this as more like “coarse-grained era structure” rather than precise temporal localization.
- Compared with prior LLM probing results, the static embeddings here achieve **$R^2=0.71$–$0.87$** for city coordinates, lower than the cited **Llama-2-70B city-coordinate $R^2=0.91$**; historical time **$R^2=0.48$–$0.52$** is also below the cited **Llama-2 $R^2=0.84$**, but still sufficient to support the paper’s core claim: **linear recoverability alone cannot prove a world model**.
- Semantic interpretability analysis finds that warm cities are closer to words like **dengue/cyclone/coconut/tropical** (e.g., *dengue* correlates with temperature at **$r=+0.62$**), while cold cities are closer to **chemist/physicist/violinist/skiing** (e.g., *chemist* **$r=-0.67$**). Simple contrast axes also work: the **cold–warm** composite score correlates with **latitude at $r=0.61$** and with **temperature at $r=-0.79$**; **modern–ancient** correlates with birth year at **$r=0.63$**.
- Subspace ablations provide stronger causal evidence: after removing the **country-name** subspace, GloVe shows **latitude $R^2=0.409$（$z=25.9$）** and **temperature $R^2=0.420$（$z=11.0$）**; after removing the **climate/weather** subspace, **temperature $R^2=0.639$（$z=14.6$）**, causing temperature prediction to drop from **0.47 to -0.17**. When six semantic subspaces are ablated together, **latitude falls from 0.71 to 0.27 (a 62% drop)** and **temperature falls from 0.47 to -0.83**; by contrast, randomly removing the same **105/300** dimensions only reduces latitude by **0.05**, indicating that the recoverable signal truly depends on interpretable lexical co-occurrence gradients.

## Link
- [http://arxiv.org/abs/2603.04317v1](http://arxiv.org/abs/2603.04317v1)
