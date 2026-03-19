---
source: arxiv
url: http://arxiv.org/abs/2603.06050v1
published_at: '2026-03-06T09:01:53'
authors:
- "Nikola Bali\u0107"
topics:
- developer-experience
- ide-satisfaction
- tool-autonomy
- cloud-ide
- pre-ai-baseline
relevance_score: 0.68
run_id: materialize-outputs
language_code: en
---

# Pre-AI Baseline: Developer IDE Satisfaction and Tool Autonomy in 2022

## Summary
This paper provides a quantitative baseline of developer IDE satisfaction **before the widespread adoption of generative AI**, based on a survey of 1,155 developers conducted in July 2022. The core finding is that overall IDE satisfaction was already high at the time, and that **freedom to choose tools** was the strongest predictor of satisfaction.

## Problem
- The paper addresses the question: before AI coding tools entered development workflows at scale, what were developers’ actual attitudes toward IDEs, freedom of tool choice, and cloud IDEs? This matters because without a pre-AI baseline, it is impossible to determine what AI tools later changed.
- Looking only at productivity or satisfaction studies from the AI era would confound causality: we would not know whether changes came from AI or from preexisting differences in the tool ecosystem, workflows, or developer experience.
- Another key question is whether superficially high satisfaction masks latent dissatisfaction caused by tool switching, low cloud IDE adoption, and organizational constraints.

## Approach
- The authors conducted a cross-sectional online survey in **July 2022**, collecting **1,173** complete responses, of which **1,155** were used for the satisfaction analysis, covering developers from **52 countries**.
- They measured IDE satisfaction using a **0–10 recommendation score**, while also analyzing variables such as **autonomy in tool choice**, **experience level**, **experimenter** tendencies, and **cloud IDE adoption/barriers**.
- Statistically, they combined means/confidence intervals, t-tests, ANOVA, linear regression, and ordered logistic regression robustness checks; the main goal was to identify the strongest explanatory factors for satisfaction.
- The simplest way to understand the method is: first measure how satisfied people are with their current IDE, then compare differences between those who can freely choose tools and those who are constrained, across different experience levels, and among cloud IDE users.

## Results
- Overall IDE satisfaction was high: mean score **8.14/10**, 95% CI **[8.01, 8.25]**; NPS was **34.7**, with **50.8%** promoters, **33.1%** passives, and **16.1%** detractors.
- The tool ecosystem was highly concentrated: **Visual Studio Code usage 79.0%**, **IntelliJ IDEA 30.1%**, **Visual Studio 26.3%**.
- Autonomy was the strongest predictor: developers who could freely choose their IDE had satisfaction of **8.44**, versus **7.73** for constrained users, a difference of **0.71 points**; t(1153) = **6.18**, **p < 0.001**, Cohen's **d = 0.49**. In multivariable regression, the autonomy coefficient was **β = 0.51 [0.24, 0.78]**, **p < 0.001**; ordered logistic robustness analysis gave **OR = 1.61 [1.30, 1.99]**.
- Experience was positively correlated with satisfaction: ANOVA **F(4,1151)=12.51, p<0.001, η²=0.040**; beginners (<1 year) had a mean of **6.53**, while developers with 20+ years had **8.41**, a difference of **1.88 points**, Cohen's **d = 0.43**.
- The **experimenter** group accounted for **29.9%**. Although they switched tools more often and used more technologies (**5.9 vs 5.2**, t = **5.38**, **p < 0.001**), there was no significant difference in satisfaction (t = **0.43**, **p = 0.67**).
- Regular cloud IDE adoption was extremely low: only **4.3%** were regular users, **16.0%** occasional users, **34.2%** planned to adopt, and **44.6%** had no plans; the abstract also notes that **40.1%** of respondents viewed **network dependence** as the main barrier. The authors also claim significant differences in IDE retention: **VS Code 68.5%**, while traditional IDEs were only **3.9%–25%**. Together, these results form a pre-AI baseline for studying the post-AI era’s “productivity–satisfaction misalignment.”

## Link
- [http://arxiv.org/abs/2603.06050v1](http://arxiv.org/abs/2603.06050v1)
