---
source: arxiv
url: http://arxiv.org/abs/2603.04560v1
published_at: '2026-03-04T19:44:55'
authors:
- Benjamin A. Christie
- Yinlong Dai
- Mohammad Bararjanianbahnamiri
- Simon Stepputtis
- Dylan P. Losey
topics:
- robot-learning
- neuro-symbolic-policy
- retrieval-augmented-generation
- human-feedback
- skill-learning
relevance_score: 0.39
run_id: materialize-outputs
language_code: en
---

# From Local Corrections to Generalized Skills: Improving Neuro-Symbolic Policies with MEMO

## Summary
MEMO is a method that enables robots to accumulate fragmented human language corrections into reusable skills. Through "retrieval + clustering + code templating," it turns local fixes into general operational capabilities that can transfer to new tasks.

## Problem
- Although neuro-symbolic robots can decompose complex tasks into semantic subtasks, actual execution is still limited by the existing skill library; when an appropriate skill is missing, the task fails.
- Simply remembering a particular human correction text usually only fixes the current scenario and is hard to extend into new skills that generalize across tasks and users.
- As feedback grows, the memory library can become redundant, contradictory, and overly long in context, which hurts retrieval and reasoning performance.

## Approach
- Build a retrieval-augmented **skillbook** that stores two types of content: rewritten text from human corrections after failures, and abstracted code/function templates derived from robot-successful subtask executions.
- At runtime, the task is first decomposed into subtasks, then related feedback or code templates are retrieved from the skillbook by "action + object" similarity, and these are used to help generate new skill code for the current subtask rather than rigidly reusing old code directly.
- Human feedback is first paraphrased and stripped of task-specific details, while higher-level, task-agnostic guidance statements are extracted to improve transferability across scenarios.
- Offline, similar entries in the skillbook are clustered, then compressed and summarized conditioned on successful code templates; duplicate corrections or those that conflict with successful behavior are removed, yielding more generalized text guidance and parameterized function templates.
- The core mechanism can be understood simply as: organizing many natural-language suggestions of "this is wrong here; you should do it this way" into "when encountering this type of object/action in the future, follow this general procedure."

## Results
- The paper explicitly claims that on **unseen new tasks**, MEMO's **zero-shot success rate** is higher than the robot foundation model and neuro-symbolic baselines that only retrieve local human feedback (such as the DROC-V / MEMO-C comparison context mentioned in the paper).
- Data collection covers **20 test tasks used for feedback collection** and **5 held-out evaluation tasks**, for a total of **224 pieces of human feedback**.
- The held-out tasks include **Place the apple on the table, Pour the can, Close the bottle, Empty the cabinet, Put the food in the oven**, which are used to test generalization rather than memorization of the training tasks themselves.
- The paper presents Figure 4 and notes that as the skillbook grows by **user-hours**, the performance of **unclustered MEMO-C and DROC-V tends to plateau**, whereas MEMO maintains a better generalization trend by aggregating local corrections into general guidance.
- The strongest conclusion from the abstract and introduction is that MEMO can synthesize local textual feedback from multiple users and tasks into general code skill templates, thereby achieving stronger generalization on **new tasks** where existing baselines fail.
- This excerpt **does not provide clear final numeric success rates, specific percentage-point gains, or significance statistics**, so more detailed quantitative comparisons cannot be listed reliably.

## Link
- [http://arxiv.org/abs/2603.04560v1](http://arxiv.org/abs/2603.04560v1)
