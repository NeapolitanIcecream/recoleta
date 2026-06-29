---
source: arxiv
url: https://arxiv.org/abs/2606.23685v1
published_at: '2026-06-22T17:59:52'
authors:
- Jiaming Liu
- Yinxi Wang
- Chenyang Gu
- Siyuan Qian
- Xiangju Mi
- Hao Chen
- Jiawei Chen
- Qingpo Wuwu
- Xiaoqi Li
- Nuowei Han
- Yiming Zhang
- Xuheng Zhang
- Yang Yue
- Yeqing Yang
- Lei Wang
- Peng Jia
- Hao Tang
- Shanghang Zhang
topics:
- vision-language-action
- human-to-robot-transfer
- latent-world-models
- robot-manipulation
- dexterous-manipulation
- human-demonstrations
relevance_score: 0.93
run_id: materialize-outputs
language_code: zh-CN
---

# LaST-HD: Learning Latent Physical Reasoning from Scalable Human Data for Robot Manipulation

## Summary
## 概要
LaST-HD 通过把人手和机器人轨迹对齐到共享的潜在动力学空间，训练 VLA 机器人策略从人手演示中学习。它还配套低成本动作捕捉手套和人机混合训练方案，用于跨夹爪和灵巧手的操作任务。

## 问题
- 机器人 VLA 策略需要大量真实机器人演示，但遥操作速度慢、受硬件限制且成本高。
- 人手演示更容易采集，但当人手与机器人夹爪或灵巧手在形状、关节和动力学上不同时，直接迁移会失败。
- 论文关注跨具身操作学习，让人类数据帮助机器人泛化到新物体、新位置和新场景。

## 方法
- LaST-HD 使用基于 Janus-Pro、SigLIP-Large 和 1.5B DeepSeek-LLM 主干的 Mixture-of-Transformers VLA 模型，其中一个专家负责潜在推理，另一个专家负责动作生成。
- 一个以动作为条件的世界模型在未配对的人手和机器人轨迹上训练。它的前向动力学特征成为 VLA 推理专家的潜在目标。
- 策略通过流匹配学习机器人动作，同时用与世界模型目标的余弦相似度监督其潜在 token。
- OOL Glove 记录 21 个人手-手腕关键点，并通过指尖距离规则和逆运动学重定向，把人类动作转成夹爪和灵巧手的监督信号。
- 训练先使用人机混合协同训练，然后在失败状态使用人手在线纠正，并回放旧数据以减少遗忘。

## 结果
- 域内评估覆盖 3 种具身形态上的 6 个真实世界任务。LaST-HD 平均成功率为 0.73，π0.5 为 0.62，Cosmos-Policy 为 0.52，LaST0 为 0.63。
- 在域内任务上，LaST-HD 在 Sort Fruits 上达到 0.95，在 Put Items to Bag and Zip 上达到 0.80。人机混合变体在每个任务使用 50 条机器人演示和 50 条 OOL Glove 演示时，平均成功率为 0.68。
- 在仅加入额外人类数据的泛化设置中，LaST-HD 的全局平均成功率为 0.56；在相同未见人类数据设置下，LaST0 为 0.46。
- 按场景划分，使用未见人类数据的 LaST-HD 在 6 个任务中，对未见位置的平均成功率为 0.41，对未见物体为 0.58，对未见背景为 0.68。
- OOL Glove 的报告指标为：单只手套低于 100 g，频率超过 200 Hz，延迟低于 10 ms，关键点位置平均 RMS 误差低于毫米级，数据采集速度比机器人遥操作快 4-5 倍。
- 报告称，人手在线纠正使用 20 分钟 OOL Glove 数据即可把新环境准确率提高到 90% 以上；在展示的 Sort Fruits 纠正研究中，20 条轨迹在未见背景上达到 100%，60 条轨迹在未见物体上达到 100%。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.23685v1](https://arxiv.org/abs/2606.23685v1)
