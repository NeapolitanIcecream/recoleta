---
source: arxiv
url: https://arxiv.org/abs/2605.00803v1
published_at: '2026-05-01T17:42:12'
authors:
- Ziyang Huang
- Yi Cao
- Ali K. Shargh
- Jing Luo
- Ruidong Mei
- Mohd Zaki
- Zhan Liu
- Wyatt Bunstine
- William Jurayj
- Somdatta Goswami
- Tyrel McQueen
- Michael Shields
- Jaafar El-Awady
- Paulette Clancy
- Benjamin Van Durme
- Nicholas Andrews
- William Walden
- Daniel Khashabi
topics:
- coding-agents
- scientific-reproducibility
- materials-science
- agent-benchmark
- code-intelligence
relevance_score: 0.84
run_id: materialize-outputs
language_code: zh-CN
---

# Can Coding Agents Reproduce Findings in Computational Materials Science?

## Summary
## 摘要
AutoMat 测试编码智能体能否复现计算材料科学论文中的声明级结果。主要结果为负面：表现最好的被测智能体在 85 条声明上的成功率为 54.1%，只依靠论文恢复工作流是最难的情况。

## 问题
- 通过软件工程基准测试的编码智能体在计算科学中可能失败，因为论文会省略流程细节，任务需要领域工具，还需要科学判断。
- 这个问题很重要，因为智能体可能运行代码并生成看似合理的文件，但使用了错误的方法或证据。
- 计算材料科学是一个困难测试场景，因为工作流可能涉及 DFT、分子动力学、ML 模型、自定义代码、HPC 作业和后处理。

## 方法
- 作者构建了 AutoMat，其中包含由材料科学领域专家从真实论文中整理的 85 条声明。
- 每个任务向智能体提供一条声明、论文、元数据和可选工件；隐藏的专家复现步骤用于评估。
- 任务涵盖基于论文的复现、基于工件的复现和基于工件的解释。
- 评估了五种智能体设置：使用 Claude Sonnet 4.6 的 AutoMat 专用编排智能体、使用 Claude Opus 4.6 的 Claude Code、使用 Claude Sonnet 4.6 的 Claude Code、使用 Kimi K2.5 的 Claude Code，以及使用 GPT-5.4 的 Codex CLI。
- 一个独立的评估智能体检查轨迹、日志、文件和报告，然后按 1-5 分为运行打分；4 分或 5 分表示成功。

## 结果
- 使用 Opus 4.6 的 Claude Code 整体表现最好，85 条声明的平均可复现性得分为 3.52，成功率为 54.1%。
- 使用 GPT-5.4 的 Codex CLI 整体最弱，平均得分为 2.44，成功率为 23.5%。
- 基于论文的复现平均得分为 1.5 到 2.2，各系统的成功率接近于零。
- 基于工件的复现更容易，平均得分为 3.1 到 4.1，成功率为 39% 到 77%。
- 基于工件的解释表现不稳定，成功率为 33% 到 50%。
- LLM 评估器使用 40 次由 SME 打分的运行进行校准，二次加权 kappa 达到 0.69，1 分以内准确率为 0.80。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.00803v1](https://arxiv.org/abs/2605.00803v1)
