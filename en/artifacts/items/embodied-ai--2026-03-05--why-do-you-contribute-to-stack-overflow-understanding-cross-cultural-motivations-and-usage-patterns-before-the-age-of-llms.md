---
source: arxiv
url: http://arxiv.org/abs/2603.05043v1
published_at: '2026-03-05T10:51:04'
authors:
- Sherlock A. Licorish
- Elijah Zolduoarrati
- Tony Savarimuthu
- Rashina Hoda
- Ronnie De Souza Santos
- Pankajeshwara Sharma
topics:
- stack-overflow
- cross-cultural-analysis
- online-community
- motivation-analysis
- software-engineering
relevance_score: 0.02
run_id: materialize-outputs
language_code: en
---

# Why Do You Contribute to Stack Overflow? Understanding Cross-Cultural Motivations and Usage Patterns before the Age of LLMs

## Summary
This paper examines why Stack Overflow contributors participated in the platform before the widespread adoption of LLMs, focusing on differences in motivation across the United States, China, and Russia, and how those motivations relate to actual behavior. The authors find that advertising/self-presentation and altruistic problem-solving are the primary motivations, and that different cultural groups emphasize different priorities.

## Problem
- The paper addresses the question: **Why do Stack Overflow contributors participate, how do these motivations vary by country/culture, and are these motivations reflected in platform behavior**.
- This matters because the continued activity of Q&A communities is tied to the long-term survival of the software engineering knowledge ecosystem; at the same time, in the age of LLMs, data from such communities is also an important source of human knowledge for model training.
- Prior research has discussed general motivations, but evidence on **cross-cultural differences** and the **motivation-behavior relationship** remains insufficient.

## Approach
- The authors use a **mixed-methods** approach: first conducting directed content analysis on 600 “About Me” profiles, then performing quantitative linguistic analysis on the full dataset of **268,215** contributors.
- The data covers **September 2008 to September 2019** and includes user profiles and activity records from the **United States (222,162) / China (27,720) / Russia (18,333)**.
- Based on existing coding schemes and inductive extensions, they ultimately identify **17 motivation categories**, including learning, asking questions, answering/commenting, advertising, self-promotion, making friends, job seeking, earning money, and others.
- They then use **WordNet synonym expansion** to map these 17 motivation categories onto the full set of profile texts, and apply **Spearman correlation analysis** to test relationships between “stated motivations” and “actual platform activity metrics” (such as profile length, reputation, votes, number of answers, and time on the platform).
- Put simply, the core mechanism is: **first manually summarize motivation categories, then expand those categories to large-scale text, and finally examine why people from different countries say they came to the platform and how they actually use it.**

## Results
- Overall, the authors argue that **the main motivations for participation are advertising/self-presentation and altruistic problem-solving and contribution**; at the same time, many users did not explicitly state a motivation in their profiles. The authors report that the qualitative and quantitative results are broadly consistent, and that the **chi-square test shows significant differences (p < 0.05)**.
- In cross-cultural terms, **users from the United States show a stronger advertising/self-promotion motivation**; **Chinese users show a more pronounced learning orientation**, which the authors say is “**more than twice that of the United States and Russia**.” Russia is included as a comparison group, but the excerpt does not provide more detailed numerical proportions.
- In terms of scale, the study analyzes **268,215** contributors, **600** manually coded profiles, a platform timespan of **more than 11 years**, and ultimately develops a **17-category** motivation framework.
- Regarding correlations, the authors report that the **Spearman correlation coefficient between “About Me” length and advertising motivation is 0.350**, one of the stronger correlations emphasized in the paper, suggesting that the more detailed a profile is, the more likely it is to have a promotional purpose.
- Other correlation results include: **answering/commenting motivation and profile length, r = 0.107**; **friendship motivation and profile length, r = 0.100**; **thinking/problem-solving motivation and profile length, r = 0.100**; while **learning motivation and profile length, r = -0.100**, indicating that learning-oriented users tend to engage in less self-presentation.
- The authors also claim that users oriented toward problem-solving **spend less time on the platform**; users with detailed profiles are more inclined toward advertising, socializing, sharing ideas, and building reputation. The excerpt does not provide the complete tables or final comparative values for all metrics, so more comprehensive quantitative results are not visible in the current text.

## Link
- [http://arxiv.org/abs/2603.05043v1](http://arxiv.org/abs/2603.05043v1)
