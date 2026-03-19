---
source: arxiv
url: http://arxiv.org/abs/2603.01457v1
published_at: '2026-03-02T05:16:11'
authors:
- Yaqiong Li
- Peng Zhang
- Peixu Hou
- Kainan Tu
- Guangping Zhang
- Shan Qu
- Wenshi Chen
- Yan Chen
- Ning Gu
- Tun Lu
topics:
- content-moderation
- human-ai-collaboration
- algorithmic-bias
- power-asymmetry
- online-conflict
- hci
relevance_score: 0.02
run_id: materialize-outputs
language_code: en
---

# Power Echoes: Investigating Moderation Biases in Online Power-Asymmetric Conflicts

## Summary
This paper investigates whether human moderators tend to favor the more powerful party in online **power-asymmetric** conflicts, and how AI suggestions change this bias. Through an experiment with 50 participants, the authors find that manual moderation exhibits multiple biases in favor of the powerful party, while AI assistance mostly mitigates these biases, though in a few cases it can amplify them or introduce new ones.

## Problem
- The paper addresses whether, in online conflicts with **power asymmetry** such as consumer-merchant disputes, human moderation systematically favors the stronger party with more resources, rule knowledge, and expressive advantages.
- This matters because such conflicts are common on real platforms, and moderation decisions often determine who is seen as more "credible" and who receives support, directly affecting the weaker party’s ability to defend their rights, their sense of fairness, and trust in the platform.
- Existing research has focused more on bias in general content moderation, but there is a lack of systematic evidence on **moderation bias in power-asymmetric conflicts** and on **the impact of AI suggestions on such bias**.

## Approach
- Grounded in social power theory (six sources of power), the authors derived a taxonomy of **10 forms of power expression** from real consumer-merchant conflict data on Dianping, including legitimacy claims, authority citation, punishment threats, compensation, expert knowledge, group preference, statement order, tone of expression, choice traps, and length differences.
- They developed a web-based experimental system, "I Support," in which participants rated conflict samples on a 5-point scale to indicate which side they supported more, i.e., which side they considered more reasonable/more credible.
- The experiment recruited **50 participants**, randomly assigned to two groups: one performed fully human moderation, and the other performed **human-AI collaborative moderation**.
- In the AI group, the authors used a **Wizard-of-Oz** design: they first crowdsourced high-quality suggestions from real moderators, then told participants these were "AI-generated," in order to control variation across LLM outputs and study the "algorithmic compliance effect."
- By comparing judgment differences across conditions with different forms of power expression, the authors identified power-related biases in human moderation and analyzed whether AI suggestions mitigated or amplified these biases.

## Results
- The experimental sample consisted of **50 participants**; the paper explicitly claims this is the **first** systematic study of bias in human moderation and human-AI collaborative moderation under power-asymmetric conflicts.
- In fully human moderation, the authors found **5 power-related biases favoring the stronger party**.
- In human-AI collaborative moderation, these biases generally still existed, but AI affected them inconsistently: the authors report that **4 biases were mitigated and 1 was eliminated**.
- At the same time, AI may also introduce negative effects: the authors report that **1 new bias was introduced, and 1 existing bias was amplified**.
- The paper also presents one specific finding: when AI suggestions are framed from the perspective of "why the other side should not be supported," moderators are more easily prompted to support the weaker party.
- The provided excerpt **does not include more detailed statistics** (such as p-values, effect sizes, specific proportional changes for each bias, or group means), so more precise quantitative improvement figures cannot be reported.

## Link
- [http://arxiv.org/abs/2603.01457v1](http://arxiv.org/abs/2603.01457v1)
