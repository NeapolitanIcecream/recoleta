---
source: arxiv
url: http://arxiv.org/abs/2603.10864v1
published_at: '2026-03-11T15:16:58'
authors:
- Martin Obaidi
- Marc Herrmann
- Jendrik Martensen
- "Jil Kl\xFCnder"
- Kurt Schneider
topics:
- sentiment-analysis
- software-engineering
- developer-communication
- longitudinal-study
- team-dynamics
relevance_score: 0.01
run_id: materialize-outputs
language_code: en
---

# Exploring Indicators of Developers' Sentiment Perceptions in Student Software Projects

## Summary
This paper studies how developers' sentiment perceptions of the same piece of text change over time and with individual/team factors in student software projects. The conclusion is that sentiment perception is not stable and depends more on the ambiguity of the statement itself than on strong and stable individual differences or project-phase effects.

## Problem
- The problem it addresses is: why developers perceive the same written message as positive, negative, or neutral, and whether that judgment changes over time.
- This matters because misreading sentiment in communication can affect collaboration, team climate, and trust in the outputs of sentiment analysis tools in software engineering.
- Prior research has mostly used static, cross-sectional labeling; it lacks systematic analysis of longitudinal change within the same person, as well as factors such as emotion, life circumstances, conflict, and project phase.

## Approach
- The authors conducted a **four-wave longitudinal survey study** with 81 computer science students participating in team software projects; in the broader course context, there were 204 students and 28 team projects in total.
- In each wave, participants labeled **30 decontextualized developer statements** as positive / neutral / negative; the statements came from GitHub and Stack Overflow datasets, with roughly balanced positive, neutral, and negative classes.
- They also collected multiple types of self-reported variables: long-term mood traits, emotional reactivity, short-term mood states (PANAS), life satisfaction, team relationship conflict and task conflict, and project phase.
- Analytically, they examined within-person stability and correlations, and also used **GEE repeated-measures models** at the statement level to analyze which factors drive more positive / more neutral / more negative labels.
- They also recorded labeling rationales, confidence, and sources of uncertainty to explain which statements were more likely to trigger changes in perception.

## Results
- The study used a longitudinal design based on **81 students, 4 survey waves, and 30 statements per wave**; the authors explicitly state that sentiment perception shows only **moderate stability** within individuals, and that label changes are concentrated on **high-ambiguity statements**.
- Signals at the correlation level were generally **very small**, and **none remained significant after global multiple-testing correction**; the excerpt does not provide specific correlation coefficient values.
- In the statement-level **GEE repeated-measures models**, **higher mood trait levels and higher emotional reactivity** were associated with **a greater tendency to label statements as positive and a lower tendency to label them as neutral**.
- Predictors of **negative** labeling were weaker, with at most **trend-level** findings; the paper gives **task conflict** as an example that may be associated with more negative labeling, but the evidence is not strong.
- The authors state that there is **no clear evidence** that project phase systematically affects sentiment perception.
- The excerpt contains limited quantitative detail: the clearly extractable numbers are mainly **4 waves, 81 participants, and 30 statements**; it does not provide more detailed metrics such as accuracy, effect sizes, p-values, or relative improvement over baseline.

## Link
- [http://arxiv.org/abs/2603.10864v1](http://arxiv.org/abs/2603.10864v1)
