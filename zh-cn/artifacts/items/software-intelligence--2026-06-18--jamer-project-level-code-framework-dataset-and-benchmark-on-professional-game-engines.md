---
source: arxiv
url: https://arxiv.org/abs/2606.19830v1
published_at: '2026-06-18T06:17:46'
authors:
- Jianwen Sun
- Chuanhao Li
- Zizhen Li
- Yukang Feng
- Fanrui Zhang
- Yifei Huang
- Yu Dai
- Kaipeng Zhang
topics:
- project-level-code-generation
- code-benchmark
- godot
- game-development
- code-agents
- dataset-curation
relevance_score: 0.84
run_id: materialize-outputs
language_code: zh-CN
---

# JAMER: Project-Level Code Framework Dataset and Benchmark on Professional Game Engines

## Summary
## 摘要
JAMER 提出了 JamSet 和 JamBench：一个基于 Godot、面向项目级游戏代码的数据集和基准，由经过验证的 Game Jam 项目构建。它对代码智能研究有价值，因为它测试模型能否生成多文件、可运行的游戏项目，而不只测试短脚本或局部编辑。

## 问题
- 现有游戏代码基准大多覆盖单文件游戏、网页游戏、局部编辑或小型任务集，因此遗漏了专业引擎上的项目级工程能力。
- 游戏行为很难用单元测试验证，因为交互式运行时行为没有简单的预期输出。
- 开源游戏仓库噪声很高；作者报告称，约 96% 的候选项目因缺失文件、编译错误、版本不匹配或运行时崩溃而未通过筛选。

## 方法
- 作者收集了约 240,000 个候选仓库，筛选出 Godot 4.x 2D 项目，要求至少有 1,200 行游戏代码且 addon 代码少于 1,000 行，然后在 Godot headless 模式下验证。
- 验证流水线检查文件完整性、编译情况、30 秒启动稳定性，以及通过确定性输入注入收集 60 秒运行时行为。
- JamBench 包含 300 个经人工验证的项目，分为 Small、Medium 和 Large 三档；JamSet 包含剩余 7,833 个经验证项目，并被转换为多轮训练数据。
- 该基准包含两类任务：基于主题的完整项目生成，以及函数、脚本和完整脚本粒度的代码补全。
- 评估使用 L1/L2/L3a 通过率、衡量静态项目形态的 Structural Completeness Score，以及衡量运行时相似度的 Behavioral Alignment Score。

## 结果
- 该流水线从超过 240,000 个候选项目中提取出 8,133 个行为有效的项目；其中 300 个组成 JamBench，7,833 个组成 JamSet。
- 该基准规模大于文中列出的既有游戏代码基准：GameDevBench 有 132 个任务，OpenGame 有 150 个提示，AutoUE 有 20 个任务，V-GameGym 有 2,219 个单文件样本。
- 在 Task 1a 纯主题生成中，最佳普通模型的 L3a 运行时通过率为：Gemini 3.1 Pro 78.7%，Claude Opus 4.6 77.3%，GPT-5.4 77.3%；BAS 仍然偏低，GPT-5.4 为 0.17，Gemini 3.1 Pro 为 0.14。
- 在带有玩法描述的 Task 1b 中，Gemini 3.1 Pro 达到 58.7% L3a、0.57 SCS 和 0.31 BAS；GPT-5.4 达到 60.7% L3a、0.63 SCS 和 0.31 BAS。
- 在 Task 2a 中，运行时通过率从小型项目的 80.4% 降至大型项目的 5.7%，显示出明显的规模失效。
- Code-agent 运行提高了 Task 1 的编译和运行时通过率，例如 Claude Opus 4.6 agent 将 Task 1b L3a 从 50.0% 提高到 80.0%，但论文报告称运行时行为质量没有提升；JamSet 微调将 Qwen3.5-27B 在 Task 1a 上的 BAS 从 0.09 提高到 0.21，L3a 从 58.7% 提高到 62.0%。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.19830v1](https://arxiv.org/abs/2606.19830v1)
