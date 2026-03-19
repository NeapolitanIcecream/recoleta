---
source: arxiv
url: http://arxiv.org/abs/2603.08640v2
published_at: '2026-03-09T17:18:00'
authors:
- Ben Rank
- Hardik Bhatnagar
- Ameya Prabhu
- Shira Eisenberg
- Karina Nguyen
- Matthias Bethge
- Maksym Andriushchenko
topics:
- llm-agents
- post-training
- benchmarking
- ai-rd-automation
- instruction-tuning
relevance_score: 0.08
run_id: materialize-outputs
language_code: zh-CN
---

# PostTrainBench: Can LLM Agents Automate LLM Post-Training?

## Summary
本文提出 **PostTrainBench**，用于衡量前沿LLM代理能否在受限算力下自主完成LLM后训练。结果表明，代理已能显著提升基础模型并在少数定向任务上超过官方指令微调模型，但整体仍远落后于通用指令模型。

## Problem
- 论文要解决的问题是：**如何系统评测LLM代理是否能自主完成LLM后训练**，而不只是做零散的科研子任务。
- 这很重要，因为后训练直接决定模型的指令跟随、推理、工具使用与安全性；如果代理能自动做这一步，就意味着AI研发自动化可能真正加速。
- 现有基准大多不覆盖“给定基础模型→自主找数据/写代码/跑实验→提交训练后模型”的端到端流程，因此难以衡量真实能力与风险。

## Approach
- 作者构建了 **PostTrainBench**：给代理一个基础LLM、一个目标评测任务、**10小时+1张H100**、互联网和开发工具，但**不提供预设策略、训练代码或训练数据**。
- 代理可自主执行完整后训练流程：上网找资料、下载/筛选数据、写脚本、调参、训练并提交checkpoint；最终只看提交模型在保留测试集上的分数。
- 基准覆盖 **4个基础模型 × 7个任务**，包括数学、代码、函数调用、科学问答、创意写作和医疗对话；并比较多种CLI代理脚手架与底层模型。
- 为保证评测有效性，作者用 **LLM judge** 检查作弊/违规，如训练集污染测试集、替换模型、直接下载现成指令模型等；违规则回退为基础模型分数。
- 除了总体榜单，论文还分析了脚手架影响、推理强度、时间预算和失败模式，以评估代理后训练的能力边界与安全问题。

## Results
- **总体最佳代理**为 Claude Opus 4.6 (Claude Code)，加权平均分 **23.2% ± 1.8**；明显高于 **base zero-shot 7.5%**，但仍大幅落后于 **官方instruction-tuned基线 51.1%**。
- 分任务看，代理在 **BFCL函数调用** 上最强：最佳代理达到 **75.9% ± 17.8**，而基础模型仅 **1.5%**；说明在目标明确、反馈清晰的任务上，代理可有效“爬坡优化”。
- 论文声称代理在少数定向场景**超过官方指令模型**：例如 **GPT-5.1 Codex Max** 将 **Gemma-3-4B** 在 **BFCL** 上做到了 **89%**，而官方模型是 **67%**；**SmolLM3-3B** 在 **BFCL** 上代理做到 **91% vs. 84%** 官方；**Gemma-3-4B** 在 **GPQA** 上 **33% vs. 31%** 官方。
- 但在更难、更广泛的任务上表现仍弱：如 **AIME 2025** 最佳平均仅 **5.0% ± 3.5**，**ArenaHard Writing** 约 **10.1%** 顶尖水平，很多配置在 **GPQA** 上仍低于随机猜测的 **25%**。
- 示例执行中，Claude Opus 4.5 可将 **Gemma-3-4B** 在 **HumanEval** 上从 **0% 提升到 37.3%**，用了 **104轮交互、9小时20分、API成本4.62美元**，显示代理已具备较长链路实验与调试能力。
- 消融结果显示：时间有帮助但收益递减，**1小时** 时代理平均约 **10–12%**（高于7.5%基线）；GPT-5.1 Codex Max 的 **medium reasoning** 最优，分数 **19.7 ± 0.3**，优于 **low 15.5 ± 0.4** 和 **high 17.2 ± 0.04**，且 high 模式token消耗约 **1.89M vs. 0.96M**。

## Link
- [http://arxiv.org/abs/2603.08640v2](http://arxiv.org/abs/2603.08640v2)
