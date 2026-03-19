---
source: hn
url: https://detexify.kirelabs.org/classify.html
published_at: '2026-03-14T22:32:41'
authors:
- jruohonen
topics:
- latex-tools
- symbol-recognition
- hand-drawn-input
- interactive-search
relevance_score: 0.28
run_id: materialize-outputs
language_code: en
---

# Detexify

## Summary
Detexify is a tool that helps LaTeX users find the corresponding LaTeX command by sketching a symbol by hand. Its core value is reducing the time spent manually searching through symbol manuals. It is better understood as a practical symbol-recognition system rather than a research work describing a novel algorithm in detail.

## Problem
- LaTeX users often cannot remember the commands for rare mathematical or technical symbols, so they have to manually search through long lists such as `symbols-a4.pdf`, which is time-consuming and inefficient.
- This retrieval friction interrupts writing and typesetting workflows, reducing productivity when using LaTeX.
- The existing need is: users know “what it looks like” but do not know “what the command is called.”

## Approach
- Users directly sketch the target symbol in the interface, and the system returns possible matching LaTeX commands based on stroke shape.
- The underlying mechanism is essentially a symbol classification or similarity-retrieval backend based on sketch/handwritten input, mapping visual form to LaTeX symbol commands.
- The system supports continued training or expansion of the symbol library; the text explicitly says that if a symbol is “not trained enough,” it can be further trained, and if it is unsupported, users can request that it be added.
- The tool provides a frontend, backend, and Mac app, emphasizing practical usability and interaction convenience rather than theoretical derivation.

## Results
- The provided content **does not give any quantitative experimental results**; it reports no accuracy, recall, latency, dataset size, or comparison with baseline methods.
- The strongest concrete outcome claim is that Detexify lets users “draw a symbol and view matching results,” thereby simplifying the process of finding LaTeX symbol commands.
- The text also claims that the Mac app is “finally stable enough,” but **provides no stability metrics or test data**.
- The system allows users to participate in training and to expand the supported symbol set, indicating that its recognition ability depends on training coverage, but **no coverage figures are provided**.

## Link
- [https://detexify.kirelabs.org/classify.html](https://detexify.kirelabs.org/classify.html)
