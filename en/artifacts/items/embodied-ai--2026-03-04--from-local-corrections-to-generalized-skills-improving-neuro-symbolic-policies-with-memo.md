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
- neuro-symbolic-robotics
- human-feedback
- retrieval-augmented-generation
- skill-learning
- robot-manipulation
relevance_score: 0.87
run_id: materialize-outputs
language_code: en
---

# From Local Corrections to Generalized Skills: Improving Neuro-Symbolic Policies with MEMO

## Summary
MEMO studies how to accumulate local natural-language corrections after robot task failures into retrievable, generalizable skill templates, thereby improving the zero-shot performance of neuro-symbolic manipulation policies on novel tasks. The core idea is to write human feedback and successful code into a continuously evolving skillbook, and use clustering to compress scattered corrections into more general text guidance and parameterized code.

## Problem
- Although neuro-symbolic robot policies can decompose complex tasks into semantic subtasks, actual execution is still limited by the existing skill library; when an appropriate skill is missing, even strong high-level reasoning will fail.
- Existing feedback-based methods usually only remember a single local correction or fine-tune an existing skill, making it difficult to turn "this fix" into "a new skill usable in the future."
- This matters because for general-purpose manipulation robots facing new objects, new mechanisms, and new tasks, the bottleneck is often not planning but the lack of generalizable skills that can ground language into action.

## Approach
- MEMO builds a retrieval-augmented **skillbook** that stores human natural-language corrections, distilled high-level guidance, and code templates generated after task success as entries in a vector database.
- At run time, the robot first decomposes a task into subtasks, then retrieves relevant feedback or function templates according to an "action token + object token," using this content as context to help generate code for the current subtask rather than mechanically reusing old code.
- For user feedback, the system first performs paraphrasing/generalization: removing overly task-specific descriptions and extracting higher-level rules that can be used across tasks whenever possible; for successful subtasks, it abstracts the execution code into parameterized function templates.
- In the offline stage, MEMO clusters skillbook entries by embedding, and conditioned on successful code templates, has a language model compress, rewrite, and resolve conflicts, producing more compact and consistent general feedback and skill templates.
- The paper collects **224** pieces of human feedback from multiple training tasks; evaluation is conducted on several held-out novel tasks, including *Place the apple on the table*, *Pour the can*, *Close the bottle*, *Empty the cabinet*, and *Put the food in the oven*.

## Results
- The paper explicitly claims that on **previously unseen tasks**, MEMO achieves a **higher zero-shot success rate** than the robot foundation model and a neuro-symbolic baseline that only retrieves relevant human feedback but **does not perform generalized clustering**.
- From the described experimental setup, the authors use **224** pieces of human feedback to build the skillbook and evaluate cross-task generalization on **5 held-out tasks**; this supports their central claim of going "from local corrections to generalized skills."
- The caption text for Figure 4 states that as the skillbook grows, methods such as **MEMO-C** and **DROC-V** that **do not perform clustering-based generalization** tend to plateau, whereas MEMO continues to improve by aggregating local corrections into general guidance.
- The abstract also claims that MEMO outperforms existing baselines in both **simulation and the real world**, and can generalize to novel tasks; the excerpt shows a **zero-shot** use case of a real robot on *Empty the Cabinet*.
- However, the provided excerpt does **not include complete quantitative results** (for example, exact success-rate percentages, variance, relative improvement magnitudes, or per-baseline comparison tables), so it is not possible to accurately list numbers such as "X% higher than a certain baseline."

## Link
- [http://arxiv.org/abs/2603.04560v1](http://arxiv.org/abs/2603.04560v1)
