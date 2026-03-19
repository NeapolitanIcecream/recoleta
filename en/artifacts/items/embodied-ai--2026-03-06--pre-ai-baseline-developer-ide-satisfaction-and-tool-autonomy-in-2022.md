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
relevance_score: 0.02
run_id: materialize-outputs
language_code: en
---

# Pre-AI Baseline: Developer IDE Satisfaction and Tool Autonomy in 2022

## Summary
This paper provides a baseline for software development tool satisfaction **before the widespread adoption of generative AI**: based on a survey of 1,155 developers in July 2022, it finds that overall IDE satisfaction was already high, and that **autonomy in tool choice** was the strongest predictor. Its importance is that it offers a quantifiable "pre-AI reference point" for later assessing whether AI coding tools actually improved or disrupted the developer experience.

## Problem
- The paper addresses the question: before AI coding assistants entered development workflows at scale, what were developers' satisfaction levels with IDEs/development environments, their freedom to choose tools, and the state of cloud IDE usage?
- This matters because without a 2022-style "pre-AI baseline," it is difficult to determine whether later tools such as Copilot, ChatGPT, and AI IDEs brought real improvements or merely changed subjective perceptions.
- The authors also focus on a practical issue: cloud-based development environments were barely adopted routinely in 2022, and the barriers to their adoption (such as network dependence) remain relevant today for cloud-reliant AI agents.

## Approach
- In **July 2022**, the authors conducted a cross-sectional online survey, collecting **1,173** complete responses, of which **1,155** were used for the satisfaction analysis, covering developers from **52 countries**.
- Key measures included: IDE recommendation/satisfaction (0–10), whether developers could freely choose their development tools, whether they were an "experimenter" who likes trying and frequently switching environments, and the current/future adoption status of cloud IDEs.
- Analytical methods included descriptive statistics, t-tests, ANOVA, multivariable linear regression, and **ordered logistic regression** as a robustness check to confirm that the relationship between variables such as autonomy and satisfaction was not a statistical artifact.
- The paper's core mechanism is simple: **it treats "whether one can choose tools independently" as a measurable factor and tests whether its effect on IDE satisfaction exceeds that of common background variables such as experience, role, and organizational size.**
- At the same time, the authors also use retention/continued-use intention, cloud IDE usage tiers, and experimenter segmentation to explain whether hidden attrition and dissatisfaction may still exist behind the "high average satisfaction."

## Results
- Overall IDE satisfaction was high: mean **8.14/10** (95% CI **8.01–8.25**); NPS was **34.7** (95% CI **31.0–38.2**); **50.8%** were promoters, **33.1%** passives, and **16.1%** detractors.
- The tool ecosystem was dominated by **Visual Studio Code**: usage in the sample was **79.0%**; followed by **IntelliJ IDEA 30.1%** and **Visual Studio 26.3%**.
- **Autonomy was the strongest predictor**: developers who could freely choose their IDE had satisfaction of **8.44**, versus **7.73** for those who could not, a difference of **0.71 points** (t(1153)=**6.18**, p<**0.001**, Cohen's d=**0.49**). In multivariable regression, the autonomy coefficient was **β=0.51** (95% CI **0.24–0.78**, p<**0.001**), exceeding demographic and role factors; the ordered logistic regression robustness result was **OR=1.61** (95% CI **1.30–1.99**, p<**0.001**).
- Experience was positively correlated with satisfaction: those with less than 1 year of experience averaged **6.53**, while developers with 20+ years averaged **8.41**; ANOVA **F(4,1151)=12.51**, p<**0.001**, η²=**0.040**. The difference between junior and senior developers was **1.88 points**, Cohen's d=**0.43**.
- Regular adoption of cloud IDEs was extremely low: only **4.3%** were regular users, **16.0%** occasional users, **34.2%** planned to adopt, and **44.6%** had no plans. The abstract further notes that **40.1%** of respondents viewed **network dependence** as the main barrier.
- The "experimenter" group accounted for **29.9%**; they had higher numbers of technologies adopted (**5.9 vs 5.2**, t=**5.38**, p<**0.001**), but no significant difference in satisfaction (the abstract reports **t=0.43, p=0.67**). The authors also claim substantial differences in tool retention rates: **VS Code 68.5%**, traditional IDEs **3.9%–25%**, suggesting that potential attrition risk may still exist despite high average satisfaction.

## Link
- [http://arxiv.org/abs/2603.06050v1](http://arxiv.org/abs/2603.06050v1)
