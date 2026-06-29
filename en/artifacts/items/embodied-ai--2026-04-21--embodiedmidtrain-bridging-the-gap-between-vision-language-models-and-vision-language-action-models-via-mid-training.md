---
source: arxiv
url: http://arxiv.org/abs/2604.20012v1
published_at: '2026-04-21T21:40:58'
authors:
- Yiyang Du
- Zhanqiu Guo
- Xin Ye
- Liu Ren
- Chenyan Xiong
topics:
- vision-language-action
- robot-foundation-model
- mid-training
- data-selection
- embodied-learning
relevance_score: 0.96
run_id: materialize-outputs
language_code: en
---

# EmbodiedMidtrain: Bridging the Gap between Vision-Language Models and Vision-Language-Action Models via Mid-training

## Summary
EmbodiedMidtrain adapts a vision-language model to robot control before VLA fine-tuning by selecting VLM training samples that look most similar to robot data. The paper shows that this mid-training step improves downstream manipulation performance across benchmarks and backbones with much smaller models and training budgets.

## Problem
- VLAs usually start from off-the-shelf VLMs trained on broad tasks such as captioning, VQA, and document understanding, while robot policy training uses manipulation trajectories tied to physical interaction.
- The paper measures this mismatch and finds that VLA data form compact clusters that are separated from the broader VLM distribution, so the starting representation is poorly aligned for action learning.
- This matters because plain VLA fine-tuning must bridge that gap on its own, which limits downstream robot performance.

## Approach
- The method trains a lightweight binary classifier on frozen VLM features to tell VLA samples apart from VLM samples.
- The classifier score is used as a proximity score: higher-scoring VLM samples are treated as more similar to the robot-data distribution.
- It ranks a large VLM data pool sample by sample, keeps the top-K most VLA-aligned examples, and mid-trains the VLM on this curated mixture before VLA fine-tuning.
- The pipeline does not change the VLM or VLA architecture; it changes the data used in the intermediate training stage.
- The candidate pool includes both general VLM data and embodied-oriented VLM data, so the selected subset keeps some diversity while shifting toward spatial and embodied content.

## Results
- On **Calvin ABC-D**, **InternVL3.5-1B** improves from **3.173** to **3.714** average sequence length after EmbodiedMidtrain. Its 5-step completion score rises from **0.406** to **0.551**.
- On **SimplerEnv-Bridge**, the same **InternVL3.5-1B** model improves from **36.5** to **56.3** success rate. On **Libero-10**, it improves from **39.0** to **54.2**.
- On **Qwen3VL-2B**, EmbodiedMidtrain improves **Calvin** from **3.205** to **3.584**, **SimplerEnv-Bridge** from **38.5** to **45.8**, and **Libero-10** from **33.8** to **40.2**.
- The mid-trained **InternVL3.5-1B** beats expert VLA baselines on **Calvin**: **3.714** average length vs **3.509** for **π0** and **2.548** for **OpenVLA**.
- The gains come with much smaller reported training budgets: the mid-trained models use **1.0M / 4.1M / 4.1M** samples seen on **Calvin / Simpler / Libero**, compared with **7.7M / 25.6M / 25.6M** for the reproduced expert-VLA and off-the-shelf-VLM baselines.
- In ablations on **InternVL3.5-1B**, the learned estimator beats random selection and other scoring rules: **Calvin 3.714** vs **3.398** for random selection, **Simpler 56.3** vs **43.8**, and **Libero 54.2** vs **48.4**. It also beats feature-distance (**3.126 / 53.1 / 51.2**), VLA-conditioned perplexity (**3.159 / 55.2 / 48.0**), and delta perplexity (**1.527 / 39.6 / 54.2**).

## Link
- [http://arxiv.org/abs/2604.20012v1](http://arxiv.org/abs/2604.20012v1)
