---
source: hn
url: https://msgtrail.com/posts/unmasking-the-dagapeyeff-cipher-a-multi-faceted-architecture
published_at: '2026-03-14T23:34:30'
authors:
- evaneykelen
topics:
- cryptanalysis
- unsolved-cipher
- structural-analysis
- esperanto
- simulated-annealing
relevance_score: 0.08
run_id: materialize-outputs
language_code: en
---

# Show HN: Structural analysis of the D'Agapeyeff cipher (1939)

## Summary
This article proposes a combined “structural + computational” analysis of the unsolved 1939 D’Agapeyeff cipher: using page geometry to explain the clustering of anomalous numbers, then using modern cryptanalysis to test possible plaintext languages. The core claim is that the anomalous column in the 14x14 square arises from an underlying 2×7 positional pulse, while the most promising computational explanation is a 2x98 columnar transposition combined with a Polybius square, with the plaintext resembling Esperanto more than English.

## Problem
- The problem to solve is that the D’Agapeyeff cipher has remained unreliably deciphered for **more than 80 years**, and traditional manual and computational methods have failed to extract readable plaintext.
- This matters because it is one of the classic unsolved ciphers; explaining its structure could narrow the search space, correct mistaken language assumptions, and provide methodology for historical cipher research.
- The article also tries to answer a more specific question: when anomalous symbols cluster in the 14th column of the 14x14 arrangement, is that a typographical coincidence, or a trace left by the encryption structure?

## Approach
- First, perform **structural analysis**: arrange the **196** digit pairs into multiple rectangles, focusing on **14x14**. The author finds that **5 types of anomalous symbols** (04, 71, 94, 92, 93), appearing **8 times** in total, all fall in the **14th column**.
- This phenomenon is interpreted as an underlying **2×7 pulse**: these anomalies occur at positions that simultaneously satisfy the “beat of 2” and the “end of a 7-block,” so in a 14x14 layout they systematically land in the last column; among them, **04** appears at the **98th** pair, exactly the midpoint of the full length **196**.
- Then perform **computational analysis**: instead of assuming the plaintext is English, hypothesize that it is **Esperanto**, and use **Simulated Annealing** to search a combined model of **2x98 columnar transposition + Polybius square substitution**.
- Through multiple independent runs, check whether similar vocabulary and near-natural-language scores are recovered consistently; the author treats this cross-seed consistency as evidence against merely “overfitting gibberish.”

## Results
- Structurally, the author claims that when the **196** symbols are arranged as **14x14**, all **8 occurrences** of anomalous symbols are concentrated in the **14th column**; the fact that all **3** occurrences of **92** and both **2** occurrences of **93** also fall in that column is treated as a “statistically significant” non-random clustering.
- The key localization result is that the famous anomaly **04** appears at the **98th** digit pair, the exact midpoint of the full **196**, dividing the text into two **7x14** halves.
- Computationally, the author reports that using Esperanto tetragram statistics, **30 independent solving runs** all converged on similar Esperanto words, such as **ESTIS, KAJ, KIEL, TRADUK, KODO, KONTRAU, LANDO**.
- The article claims that the fitness score of this **2x98 + Polybius + Esperanto** model “**far exceed any English baseline**,” but the excerpt **does not provide specific scores, tables, significance tests, or reproducible experimental settings**.
- The strongest substantive conclusion is not that it has been “solved,” but that the **cipher remains undeciphered**; however, the author argues that the visual structural evidence (14x14 / 2×7) and the computational-linguistic evidence (2x98 / Esperanto) have now been aligned, significantly narrowing the space of plausible hypotheses.

## Link
- [https://msgtrail.com/posts/unmasking-the-dagapeyeff-cipher-a-multi-faceted-architecture](https://msgtrail.com/posts/unmasking-the-dagapeyeff-cipher-a-multi-faceted-architecture)
