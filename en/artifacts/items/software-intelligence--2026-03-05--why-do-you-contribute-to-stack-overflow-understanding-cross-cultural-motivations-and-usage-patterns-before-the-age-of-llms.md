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
- developer-motivation
- q-and-a-communities
- mixed-methods
relevance_score: 0.38
run_id: materialize-outputs
language_code: en
---

# Why Do You Contribute to Stack Overflow? Understanding Cross-Cultural Motivations and Usage Patterns before the Age of LLMs

## Summary
This paper investigates why Stack Overflow contributors participated in the platform before LLMs broadly affected software engineering, and compares motivational differences across the United States, China, and Russia. The authors find that the most common motivations are self/company promotion and altruistic problem-solving, and that different cultural backgrounds correspond to different participation patterns.

## Problem
- The paper addresses the question: **Why do Stack Overflow contributors participate, how do these motivations vary across cultures, and are these motivations consistent with actual platform behavior**.
- This matters because Q&A communities are a core source in the software engineering knowledge ecosystem and also an important source of human data for LLM training; without understanding participation motivations, it is difficult to sustain long-term community vitality.
- Although prior research has discussed motivations for using Stack Overflow, there is still a **lack of large-scale cross-country/cross-cultural comparisons**, especially evidence linking “self-reported motivations” with “actual behavioral indicators.”

## Approach
- The authors use a **mixed-methods** approach: first conducting qualitative content analysis on 600 “About Me” profiles, then performing quantitative linguistic analysis and correlation analysis on the full dataset of **268,215** contributors.
- The data cover **222,162 users from the United States, 27,720 from China, and 18,333 from Russia**, spanning more than **11 years (2008/09–2019/09)**.
- Based on coding schemes from prior work, the authors identify **17 motivation categories** from the profiles; compared with the initial scheme, they add **8 categories**, such as make-friends, advertise, share-ideas, increase-reputation, wander, correct, earn-money-directly, and find-jobs.
- To scale to the full dataset, the authors use **WordNet synonym expansion + text matching** to automatically identify motivational expressions from all profiles, and then use **Spearman correlation** to connect motivations with 11 categories of platform activity indicators (e.g., reputation, upvotes/downvotes, number of answers, number of edits, profile length, tenure on the site, etc.).

## Results
- Overall, the authors report that the **primary motivations for participation are advertising opportunities and altruistic/problem-solving participation**; the qualitative and quantitative results corroborate each other, and the **chi-square test shows the differences are statistically significant (p < 0.05)**.
- In the cross-cultural comparison, **U.S. users show a stronger tendency toward promotion/self-advertising**; **Chinese users are more learning-oriented**, and the authors explicitly state that the proportion of Chinese contributors using Stack Overflow for learning is **more than twice that of the United States and Russia**.
- In terms of scale, the conclusions are based on **268,215 users** and **600 manually coded profiles**; the inter-rater agreement for manual coding first reached **85% agreement**, and after discussion reached **100% agreement**.
- Regarding behavioral associations, the **Spearman correlation coefficient between “About Me” length and the advertise motivation is about 0.350**, which is highlighted in the paper as a relatively strong correlation; that is, the more detailed the profile, the more likely it is written for promotional purposes.
- Other correlation results include positive correlations between profile length and **post-answers-and-comments (0.107)**, **thinking (0.100)**, and **find-friends (0.100)**, and a negative correlation with **learning (-0.100)**, indicating that learning-oriented users tend to engage less in self-presentation.
- The paper does not present “breakthrough algorithmic metrics” such as task performance gains; its strongest concrete contribution is proposing a **cross-cultural baseline profile linking motivations and behaviors** for understanding the Stack Overflow knowledge contribution ecosystem before the LLM era.

## Link
- [http://arxiv.org/abs/2603.05043v1](http://arxiv.org/abs/2603.05043v1)
