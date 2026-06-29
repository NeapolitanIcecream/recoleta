---
source: arxiv
url: https://arxiv.org/abs/2606.13102v1
published_at: '2026-06-11T09:30:09'
authors:
- Chengbo Yuan
- Zicheng Zhang
- Mingjie Zhou
- Wendi Chen
- Yi Wang
- Zhuoyang Liu
- Dantong Niu
- Shuo Wang
- Hui Zhang
- Wenkang Zhang
- Yingdong Hu
- Yuanqing Gong
- Wanli Xing
- Chuan Wen
- Cewu Lu
- Kaifeng Zhang
- Yang Gao
topics:
- tactile-manipulation
- generalist-robot-policy
- sensor-transfer
- contact-rich-control
- robot-pretraining
relevance_score: 0.88
run_id: materialize-outputs
language_code: en
---

# FTP-1: A Generalist Foundation Tactile Policy Across Tactile Sensors for Contact-Rich Manipulation

## Summary
FTP-1 is a generalist tactile policy for contact-rich robot manipulation that can train across many tactile sensor types and robot embodiments. It matters because current tactile policies are usually tied to one sensor setup, which limits transfer and reuse.

## Problem
- Tactile data changes a lot across sensors in modality, resolution, and shape, so a policy trained on one setup often fails on another.
- Prior tactile policies and tactile-VLA methods stay tied to fixed embodiments, while vision-language-action models often ignore touch.
- The paper asks whether one pretrained tactile policy can learn reusable tactile skills across heterogeneous hardware and transfer to unseen tactile sensors.

## Approach
- It builds Morphology-Aware Tactile Token Space (MTTS), which maps different tactile inputs into a shared token set based on 24 functional areas.
- It uses sensor-specific encoders for image, array, and state tactile inputs, then projects them into the same latent space.
- It adds a shared tactile Transformer expert that models the tactile tokens before they are fused with a c0_0.5-style vision-language-action policy.
- It pretrains on FTP-1-Dataset, a mix of 26 sources, about 3,000 hours of data, and 21 tactile sensors, including human and robot demonstrations.
- During finetuning, it reuses the pretrained tactile components on both seen and unseen sensors.

## Results
- On the UniVTAC simulation benchmark, FTP-1 gets 66.66% average success rate, or 59.5% when the two easier lift tasks are removed.
- On UniVTAC, the next best method reaches 49.16% overall and 42% without lifts, so FTP-1 is about 17.5 points higher on both metrics.
- On real-robot tasks with seen sensors, FTP-1 gets 62.5% average success rate across Sharpa North and Sharpa&Dexmate.
- On unseen sensor setups, FTP-1 gets 46.6% average success rate, compared with 15.0% for FTP-c0_0.5, a gain of +31.6 points.
- The paper also reports that FTP-1 outperforms a no-tactile-pretraining control on unseen FlexivXense by +37.5%, which it uses to argue that the tactile branch learns transferable knowledge.

## Link
- [https://arxiv.org/abs/2606.13102v1](https://arxiv.org/abs/2606.13102v1)
