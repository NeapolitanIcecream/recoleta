---
source: hn
url: https://msgtrail.com/posts/unmasking-the-dagapeyeff-cipher-a-multi-faceted-architecture
published_at: '2026-03-14T23:34:30'
authors:
- evaneykelen
topics:
- classical-cryptanalysis
- unsolved-cipher
- transposition-cipher
- esperanto
- structural-analysis
relevance_score: 0.0
run_id: materialize-outputs
language_code: en
---

# Show HN: Structural analysis of the D'Agapeyeff cipher (1939)

## Summary
This article analyzes the unsolved 1939 D’Agapeyeff cipher and proposes that it should be understood through both page geometry and computational linguistics. The author argues that the clustering of anomalies in a 14x14 arrangement and the 2x98 transposition model together with the Esperanto plaintext hypothesis mutually reinforce one another; although the cipher is not fully solved, the search space is significantly narrowed.

## Problem
- The cipher is 196 digits long, and for more than 80 years neither manual nor computational methods have recovered readable plaintext, making it a classic unsolved cryptographic problem.
- Using only a single perspective (looking only at layout geometry, or only doing unconstrained computational search) may miss key structural clues, which helps explain why progress has been so difficult.
- Solving it matters because it is both a historical cryptographic challenge and a test case for how to combine physical layout traces with modern algorithms in analysis.

## Approach
- First, the 196 symbols are placed into different rectangular grids for comparison, with emphasis on the 14x14 layout, where rare “anomalous” symbols (04, 71, 94, 92, 93) are found to all fall in the 14th column.
- The author interprets this clustering as an underlying “2x7 pulse”: these anomalies all occur at positions that simultaneously satisfy rhythms of 2 and 7, so in a 14x14 arrangement they naturally gather in the final column; in addition, 04 is at the 98th pair, exactly the midpoint of the full text.
- At the computational level, the author no longer assumes English plaintext, but instead assumes Esperanto, and uses simulated annealing search with a “2x98 columnar transposition + Polybius square substitution” model.
- The author uses consistency across multiple independent runs as evidence: if different random seeds repeatedly converge on similar Esperanto vocabulary and high-scoring results, then the outcome is unlikely to be mere overfitting to noise.

## Results
- In the 14x14 grid, the 5 types of anomalous symbols appear 8 times in total, and are reported to fall **entirely** in the 14th column; among them, 92 appears **3 times**, 93 appears **2 times**, while 04, 71, and 94 each appear **once**.
- A key structural point is that 04 is located at the **98th** digit pair, exactly dividing the 196 symbols into two **7x14** halves; the author treats this as a significant central-axis / hinge clue.
- In the computational experiments, the author says that after using Esperanto tetragram statistics, **30** independent simulated annealing runs all recovered similar vocabulary, such as **ESTIS, KAJ, KIEL, TRADUK, KODO, KONTRAU, LANDO**.
- The paper claims that these Esperanto results have fitness “significantly higher than any English baseline” and “close to a natural-language baseline,” but the excerpt **does not provide specific scores, error ranges, or formal baseline values**.
- The strongest conclusion is not “the cipher is solved,” but rather that the visual clustering in 14x14 and the 2x98 Esperanto transposition model are mutually consistent, suggesting that the cipher may have a clear dual geometric-linguistic structure.
- The author also explicitly acknowledges that the cipher **has still not been fully solved**; the current contribution is mainly a more constraining structural interpretation and a candidate direction for reading it.

## Link
- [https://msgtrail.com/posts/unmasking-the-dagapeyeff-cipher-a-multi-faceted-architecture](https://msgtrail.com/posts/unmasking-the-dagapeyeff-cipher-a-multi-faceted-architecture)
