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
AutoMat 测试编码代理能否复现计算材料科学论文中的结论级结果。主要结果是否定的：表现最好的测试代理在 85 条主张上的成功率只有 54.1%，而只根据论文恢复工作流是最难的情况。

## 问题
- 在软件工程基准上表现良好的编码代理，到了计算科学里可能会失败，因为论文会省略流程细节，需要领域工具，也需要科学判断。
- 这个问题很重要，因为代理可以运行代码并产出看起来合理的文件，但方法或证据可能用错。
- 计算材料科学是一个很难的测试场景，因为工作流可能涉及 DFT、分子动力学、机器学习模型、自定义代码、HPC 任务和后处理。

## 方法
- 作者构建了 AutoMat，收录了由材料科学领域专家从真实论文中整理出的 85 条主张。
- 每个任务都会给代理一个主张、论文、元数据和可选工件；用于评估的隐藏专家复现步骤会保留。
- 任务覆盖从论文复现、从工件复现和从工件解释。
- 评估了五种代理配置：使用 Claude Sonnet 4.6 的 AutoMat 专用编排代理、使用 Claude Opus 4.6 的 Claude Code、使用 Claude Sonnet 4.6 的 Claude Code、使用 Kimi K2.5 的 Claude Code，以及使用 GPT-5.4 的 Codex CLI。
- 另一个评估代理检查轨迹、日志、文件和报告，然后按 1-5 分打分；得分 4 或 5 视为成功。

## 结果
- 使用 Opus 4.6 的 Claude Code 整体最好，85 条主张的平均可复现性得分为 3.52，成功率为 54.1%。
- 使用 GPT-5.4 的 Codex CLI 整体最弱，平均得分为 2.44，成功率为 23.5%。
- 从论文复现的平均得分为 1.5 到 2.2，各系统的成功率几乎为零。
- 从工件复现更容易，平均得分为 3.1 到 4.1，成功率为 39% 到 77%。
- 从工件解释仍然不稳定，成功率为 33% 到 50%。
- 这个 LLM 评估器基于 40 个由 SME 打分的运行进行了校准，二次加权 kappa 为 0.69，1 分以内准确率为 0.80。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.00803v1](https://arxiv.org/abs/2605.00803v1)
