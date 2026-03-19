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
relevance_score: 0.24
run_id: materialize-outputs
language_code: en
---

# World Properties without World Models: Recovering Spatial and Temporal Structure from Co-occurrence Statistics in Static Word Embeddings

## Summary
This paper shows that static word embeddings (GloVe, Word2Vec) trained only on text co-occurrence already allow fairly strong spatial structure and weaker but stable temporal structure to be linearly recovered. Based on this, the authors question the claim that linear probe decodability alone can demonstrate that LLMs have learned a “world model” beyond text.

## Problem
- The paper addresses the question of whether geographically and temporally decodable information in LLM hidden states indicates that the model has formed a “world model,” or whether these structures were already latent in text co-occurrence statistics.
- This matters because many arguments about whether LLMs possess world models rely precisely on whether probes can read out spatial and temporal variables from representations.
- If static word embeddings can achieve similar decoding, then being “linearly readable” is not, by itself, sufficiently strong evidence.

## Approach
- Use the same class of methods as related LLM probing work: train ridge regression linear probes on static word vectors from GloVe 6B 300d and Word2Vec Google News 300d.
- Make predictions on two datasets: latitude, longitude, temperature, and other attributes for 100 world cities, and birth/death/midlife years for 194 historical figures.
- Use negative controls to test selectivity: also predict attributes such as elevation, GDP, and population to see whether the probe is simply able to “read out anything.”
- Conduct semantic interpretability analysis: compute similarities between words and city vectors to identify which word distributions align most with latitude/temperature/era.
- Perform semantic subspace ablations: remove PCA subspaces such as “country names” and “climate words,” then examine how much predictive performance drops, and compare this with random ablations of the same dimensionality.

## Results
- On world cities, static embeddings recover substantial geographic signal: test-set $R^2$ for latitude is 0.709 (GloVe) and 0.663 (Word2Vec), for longitude 0.782 and 0.866, and for temperature 0.471 and 0.617.
- Temporal prediction for historical figures is weaker but stable: birth year $R^2$ is 0.484 (GloVe) and 0.521 (Word2Vec); death year is 0.460 and 0.516; midlife year is 0.472 and 0.519, with MAE around 338–364 years, indicating more of an “era-level” than precise date signal.
- Negative controls show that not all world properties are linearly recoverable: $R^2$ for GDP per capita drops as low as -2.577, population as low as -2.960, and elevation is near 0 or negative, indicating that the signal is selective.
- Compared with LLM results, the authors cite Llama-2-70B reaching $R^2=0.91$ on a related city-coordinate task; although higher, static word vectors already reach 0.71–0.87, enough to show that “linear decodability” alone cannot support conclusions about representations beyond text.
- Semantic analysis shows the signal is interpretable: for example, warmer cities are closer to *dengue*, *cyclone*, and *tropical* (highest correlation about $r=+0.62$), while colder cities are closer to *chemist*, *physicist*, and *skiing* (lowest about $r=-0.67$); a cold–warm composite score correlates with temperature at $r=-0.79$ and with latitude at $r=0.61$, while modern–ancient correlates with birth year at $r=0.63$.
- Subspace ablations provide stronger evidence: removing a 20-dimensional “country names” subspace reduces latitude $R^2$ by 0.409 ($z=25.9$) and temperature by 0.420 ($z=11.0$); removing a 19-dimensional “climate and weather” subspace reduces temperature $R^2$ by 0.639 ($z=14.6$); removing six semantic subspaces together drops latitude from 0.71 to 0.27 (a 62% decrease) and temperature from 0.47 to -0.83, while randomly removing 105 dimensions lowers latitude by only about 0.05.

## Link
- [http://arxiv.org/abs/2603.04317v1](http://arxiv.org/abs/2603.04317v1)
