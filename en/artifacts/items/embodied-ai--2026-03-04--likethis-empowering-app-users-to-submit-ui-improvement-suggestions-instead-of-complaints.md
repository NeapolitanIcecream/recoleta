---
source: arxiv
url: http://arxiv.org/abs/2603.04245v1
published_at: '2026-03-04T16:33:35'
authors:
- Jialiang Wei
- Ali Ebrahimi Pourasad
- Walid Maalej
topics:
- ui-feedback
- genai-for-software-engineering
- image-editing
- mobile-ui
- human-ai-collaboration
relevance_score: 0.02
run_id: materialize-outputs
language_code: en
---

# LikeThis! Empowering App Users to Submit UI Improvement Suggestions Instead of Complaints

## Summary
This paper proposes **LikeThis!**, which transforms users’ vague complaints about mobile app UIs into actionable feedback with visual improvement proposals. The core idea is to let AI generate multiple UI improvement alternatives based on a “user comment + screenshot,” allowing users to directly choose one and submit it to developers.

## Problem
- Existing app store feedback is often **vague, emotional, or lacking actionability**, making it difficult for developers to understand and use it to improve the UI.
- Pure text struggles to accurately express UI problems, while professional design tools are **not suitable for ordinary users** to quickly create interface improvement mockups.
- This matters because low-quality feedback reduces communication efficiency between users and developers, slowing product iteration and UI improvement.

## Approach
- The paper proposes a two-stage GenAI pipeline: first **Suggestion Generation**, then **UI Editing**.
- In the first step, a multimodal large model reads **user textual feedback + app screenshot** and generates multiple textual “solution specifications” (such as increasing font size or improving contrast).
- In the second step, these specifications together with the original screenshot are fed into an image editing model to generate multiple **modified UI candidate images**; the user selects the one that best matches their intent and submits it.
- The system also supports optional **masking to mark problem regions**, so that modifications can be constrained to local areas.
- The paper also implements an **iOS prototype** that supports screenshots, issue descriptions, region marking, viewing candidate solutions, iterative editing, and final submission.

## Results
- In a model benchmarking study based on the **UICrit** dataset, the authors built an evaluation set from **300** critique/screen pairs, of which **120** were used for model comparison, **60** for masking, and **120** for ablation; two annotators achieved an agreement rate of **80.42%** on **120** tasks.
- Across **120** tasks and **240** total annotations, **GPT-Image-1** clearly outperformed Flux, Gemini, and Bagel: it ranked first in user preference **214** times, while the other models achieved only **14 / 8 / 4**.
- On issue resolution, **GPT-Image-1 averaged 2.74/3**, higher than **Flux 1.60**, **Gemini 1.83**, and **Bagel 1.38**; its count of “fully fixed” cases was **200**, compared with **58 / 73 / 32** for the other models. The paper states that these differences were statistically significant (**Wilcoxon-Mann-Whitney, p ≤ 0.05**).
- On fidelity, all models scored relatively high, but **GPT-Image-1 2.83** remained competitive; on robustness (not introducing new issues), **GPT-Image-1 scored 2.88**, higher than **Flux 2.62**, **Gemini 2.23**, and **Bagel 2.02**.
- The paper concludes that, aside from GPT-Image-1, the other models could only at least partially resolve issues on about **25%–53%** of interfaces.
- The user study covered **10** production apps and **15** users; participants considered **85.5%** of the generated suggestions to be “mostly accurate or very accurate.” Developer evaluations showed that feedback with generated improvement images was **easier to understand and more actionable** than feedback alone.

## Link
- [http://arxiv.org/abs/2603.04245v1](http://arxiv.org/abs/2603.04245v1)
