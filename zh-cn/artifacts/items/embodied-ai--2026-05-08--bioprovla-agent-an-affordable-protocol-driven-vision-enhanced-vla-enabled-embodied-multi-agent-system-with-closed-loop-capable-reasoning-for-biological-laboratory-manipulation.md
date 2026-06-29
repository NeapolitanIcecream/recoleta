---
source: arxiv
url: https://arxiv.org/abs/2605.07306v1
published_at: '2026-05-08T06:15:40'
authors:
- Zhaohui Du
- Zhe Wang
- Hongmei Fei
- Xiwen Cao
- Ting Xiao
- Qi Wang
- Huanbo Jin
- Jiaming Gu
- Quan Lu
- Zhe Liu
topics:
- vision-language-action
- robot-lab-automation
- wet-lab-manipulation
- closed-loop-verification
- robot-data-augmentation
- low-cost-robotics
relevance_score: 0.82
run_id: materialize-outputs
language_code: zh-CN
---

# BioProVLA-Agent: An Affordable, Protocol-Driven, Vision-Enhanced VLA-Enabled Embodied Multi-Agent System with Closed-Loop-Capable Reasoning for Biological Laboratory Manipulation

## Summary
## 摘要
BioProVLA-Agent 是一个低成本湿实验室机器人系统，可将生物学自然语言流程转成经过验证的机器人子任务。它在每个动作前后加入视觉检查，并用面向实验室的在线视觉增强训练一个轻量 VLA 策略。

## 问题
- 生物学流程通常是非结构化文本，实验室用户必须把操作步骤转换成机器人脚本或固定自动化流程。
- 试管、瓶子和液体容器等湿实验室物体常常是透明或反光的，这会让基于视觉的操作在强反光、边缘不清和过曝条件下更不稳定。
- 多步骤实验在执行过程中需要状态检查，因为一次放置、抓取或倾倒失败就可能破坏后续步骤并浪费样本。

## 方法
- Tailored LLM Protocol Agent 将流程解析为子任务单元，每个单元包含指令、前置条件、完成条件和知识库索引。
- Guiding Decision Agent 负责调度子任务、处理重试、在需要时调整步骤顺序，并在验证持续失败时请求人工介入。
- VLM-RAG Verification Agent 结合相机观测、机器人状态、检索到的实验室操作知识，以及成功/失败示例，检查任务是否就绪和是否完成。
- VLA Embodied Agent 使用基于轻量 SmolVLA 的策略执行已验证的子任务。
- AugSmolVLA 在微调期间加入在线视觉扰动，覆盖透明实验器具、镜面反射、光照变化、物体边界模糊和过曝。

## 结果
- 该系统运行在一个低成本机器人平台上，硬件成本约为 800-850 美元。
- 基准测试覆盖 15 个原子任务、6 个复合工作流和 3 个代表性的双臂任务。
- 测试任务包括离心管装载、试管分拣、废弃物处理、旋盖和液体倾倒。
- 论文比较了 AugSmolVLA、ACT、X-VLA 和原始 SmolVLA 在正常和高曝光条件下的表现。
- 摘要片段没有给出准确的成功率、错误率或 p 值。它声称 AugSmolVLA 提高了执行稳定性，在精确放置、透明物体操作、复合工作流和视觉退化场景中的提升更大。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.07306v1](https://arxiv.org/abs/2605.07306v1)
