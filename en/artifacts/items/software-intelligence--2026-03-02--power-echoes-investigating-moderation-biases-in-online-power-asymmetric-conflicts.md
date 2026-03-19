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
- bias-analysis
- power-asymmetry
- online-conflict
relevance_score: 0.35
run_id: materialize-outputs
language_code: en
---

# Power Echoes: Investigating Moderation Biases in Online Power-Asymmetric Conflicts

## Summary
This paper investigates whether human moderators in online **power-asymmetric** conflicts tend to favor the more powerful party, and how AI suggestions change that bias. Using real consumer–merchant conflicts and an experiment with 50 participants, the authors find that human moderation exhibits multiple biases in favor of the powerful party; AI can mitigate most of these biases, but also amplifies a few.

## Problem
- The paper addresses the following question: in online conflicts involving **power asymmetry**, such as those between consumers and merchants, what kinds of biases related to “power cues” do human moderators exhibit, and do AI suggestions reduce or intensify these biases?
- This matters because many platforms still rely on human or crowd moderators to decide “whom to support,” while the more powerful party is often better able to cite rules, display professionalism, offer compensation, or make threats, which may systematically skew moderation outcomes and harm the rights of weaker parties as well as platform credibility.
- Existing research has discussed content moderation bias, but there has been almost no systematic study of the types of bias that arise in **power-asymmetric conflict moderation** or of the effects of human-AI collaboration.

## Approach
- Drawing on the social psychology theory of **Bases of Social Power**, the authors organize power cues in online conflicts into a taxonomy and propose 10 types of “power expression,” such as legitimate claim, authority citation, punishment threat, compensation, expert knowledge, group preference, statement order, expression tone, choice trap, and length difference.
- The data come from real consumer–merchant conflicts on Dianping. The authors collected about **60,000** samples and then sampled and coded conflict cases for the experiment.
- The experiment uses a mixed design with **50** participants, divided into two groups: the **human moderation** group made judgments independently, while the **human-AI moderation** group saw additional “AI suggestions” on the same cases.
- To avoid variation in outputs from different large models, the authors used a **Wizard-of-Oz** design: they actually prepared high-quality suggestions in advance, but told participants that these suggestions came from AI, allowing them to study how judgments change when people treat the suggestions as AI-generated.
- Put simply, the core method is: **slightly alter the power cues within the same type of conflict, then compare judgments made by humans alone with judgments made after seeing AI suggestions, to see which cues push moderators toward the more powerful party and how AI changes that push.**

## Results
- For **RQ1**, the authors report that human moderation shows **5 types** of power-related bias favoring the more powerful party; the abstract does not provide detailed statistical values or effect sizes for each type.
- For **RQ2**, these biases do not disappear entirely under human-AI moderation; AI’s impact is mixed: **4 biases are mitigated, 1 is eliminated**, but at the same time **1 new bias is introduced and 1 is amplified**.
- The experimental scale in the paper is **50 participants**, using real consumer–merchant conflicts as the scenario; this is the clearest quantitative experimental setup stated in the paper.
- On the data side, the authors collected about **60,000** Dianping conflict samples covering **17** topics, and focused primarily on the top **5** topics; the top five topics account for **92.7%** of the total samples.
- The paper also reports one specific finding: when AI suggestions explicitly provide a perspective on why the moderator **should not support the other party**, moderators are more likely to shift toward supporting the weaker party.
- The provided excerpt **does not include** more fine-grained numerical results, such as significance tests, Likert means, specific baseline comparisons, or percentage increases/decreases broken down by bias category.

## Link
- [http://arxiv.org/abs/2603.01457v1](http://arxiv.org/abs/2603.01457v1)
