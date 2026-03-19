---
source: arxiv
url: http://arxiv.org/abs/2603.04245v1
published_at: '2026-03-04T16:33:35'
authors:
- Jialiang Wei
- Ali Ebrahimi Pourasad
- Walid Maalej
topics:
- human-ai-interaction
- ui-feedback
- multimodal-generation
- image-editing
- mobile-apps
relevance_score: 0.7
run_id: materialize-outputs
language_code: en
---

# LikeThis! Empowering App Users to Submit UI Improvement Suggestions Instead of Complaints

## Summary
This paper proposes **LikeThis!**, which uses generative AI to help ordinary app users turn vague complaints into visualized, actionable UI improvement suggestions. Its core value lies in improving the quality of feedback between users and developers, making it easier for development teams to understand and adopt real user needs.

## Problem
- Feedback submitted by mobile app users is often **vague, destructive, or lacking detail**, making it difficult for developers to understand and act on.
- Text comments alone make it hard to accurately express specific UI improvement ideas, and ordinary users **do not know how to use professional design tools** to create mockups.
- Existing GenAI/AI4SE work mostly focuses on **generating code or entirely new UIs**, rather than helping users **edit existing interfaces and submit in-place improvement suggestions**.

## Approach
- The paper proposes a two-stage pipeline: given a **user comment + current interface screenshot**, it first generates multiple textual **solution specifications**, and then edits the original UI image accordingly to produce multiple improved candidate images.
- In the first step, a multimodal large model generates several alternative design suggestions, each including a short title and specific modification instructions, while also generating a description of the current interface.
- In the second step, the **user issue + interface description + solution specification + original screenshot (optional mask)** are fed into an image editing model to generate the corresponding improved UI.
- The user chooses the one that best matches their intent from 3 candidate solutions, and submits it together with the original issue to the developer, thereby transforming a “complaint” into a “suggestion.”
- The authors also implemented an **iOS prototype**; in the empirical study they used GPT-4o for suggestion generation and GPT-Image-1 for UI editing, and examined the effects of masks and removing the intermediate step.

## Results
- In a model benchmark based on **UICrit**, the authors constructed an evaluation set from **300** critique/screen pairs, of which **120** screens were used for model comparison; two annotators produced **240 annotations** across **120 tasks**, with an agreement rate of **80.42%**.
- **GPT-Image-1** significantly outperformed Flux, Gemini, and Bagel: it received **214** rank-1 preferences from users, while the other models received only **14 / 8 / 4**; its average issue-resolution score was about **2.74–2.75**, while the others scored **1.38–1.83**; average fidelity was **2.83**, and robustness was **2.88–2.89**. The paper states that these advantages reached statistical significance in the relevant comparisons (**Wilcoxon-Mann-Whitney, p ≤ 0.05**).
- By raw counts, GPT-Image-1 was rated as “fully solving the issue” in **200** of **240** annotations, while Flux/Gemini/Bagel were rated so in **58/73/32**, respectively; this also supports the authors’ statement that the other models could at least partially solve issues on only about **25%–53%** of interfaces.
- The user study covered **10** production apps and **15** users; participants considered **85.5%** of the generated suggestions to be “mostly accurate” or “very accurate.”
- Developer evaluation showed that feedback with generated improvement images, compared with feedback without such images, was **easier to understand and more actionable**; the abstract and introduction provide directional conclusions, but the excerpt does not include more detailed developer-side quantitative values.
- The ablation results show that the intermediate **Suggestion Generation** step is key to high-quality UI improvements; masks are only more helpful when the **problem area is small**, and for larger areas they reduce fidelity and are more likely to introduce new issues.

## Link
- [http://arxiv.org/abs/2603.04245v1](http://arxiv.org/abs/2603.04245v1)
