---
source: arxiv
url: http://arxiv.org/abs/2603.11287v1
published_at: '2026-03-11T20:26:58'
authors:
- Weimin Fu
- Zeng Wang
- Minghao Shao
- Ramesh Karri
- Muhammad Shafique
- Johann Knechtel
- Ozgur Sinanoglu
- Xiaolong Guo
topics:
- rtl-generation
- verilog
- llm-evaluation
- hardware-synthesis
- code-generation
relevance_score: 0.85
run_id: materialize-outputs
---

# Synthesis-in-the-Loop Evaluation of LLMs for RTL Generation: Quality, Reliability, and Failure Modes

## Summary
本文提出一种“综合在环”的RTL生成评测框架，用综合后面积、时延和警告构成的HQI指标，系统评估32个LLM在202个Verilog任务上的真实硬件可用性。结论是，仅看仿真通过率会明显高估模型能力，而前沿模型已接近专家级质量，但单次部署稳定性和综合失败模式仍是主要瓶颈。

## Problem
- 现有RTL生成评测大多只看语法或仿真是否通过，无法衡量代码是否**可综合**以及综合后的**硬件质量**。
- 对芯片设计而言，功能正确还不够；若面积/时延劣化严重，或根本无法映射到门级电路，生成结果就无法用于真实生产流程。
- 因此需要一个覆盖“语法→综合→功能→QoR”的统一评测方法，避免软件代码评测范式误判硬件生成能力。

## Approach
- 构建了一个分阶段评测流水线：先检查Verilog语法（Icarus Verilog），再做综合（Yosys + Nangate45 45nm），最后运行测试平台验证功能正确性。
- 提出 **HQI (Hardware Quality Index)**，范围0–100；只有同时通过语法、综合和功能三关的设计才计分，并按相对专家参考设计的**面积、时延、警告数**计算质量。
- 在 **202 个任务**（来自 VerilogEval 和 RTLLM）上评测 **32 个模型**，每个模型-任务做 **5 次独立采样**，同时统计复杂度加权的 Coverage、Global HQI（best-of-5）和 ExpHQI（单次期望质量）。
- 设计了工具裁决的综合失败分类法，对通过解析但在Yosys阶段失败的样本做九类诊断，以分析不同模型的系统性失效机制。
- 额外在 **3 个工艺库** 上复综合，验证模型排名对工艺变化是否稳健。

## Results
- 在 **32 个模型、202 个任务、每题5次尝试** 的评测中，模型形成三层结构：**Tier 1** 有 **13** 个模型（Global HQI **>71**），**Tier 2** 有 **11** 个（**53–68**），**Tier 3** 有 **8** 个（**<53**）。
- 最强模型是 **Gemini-3-Pro**，达到 **87.5% Coverage** 和 **85.1 Global HQI**；其后如 **GPT-5.4-Pro 81.3**、**Gemini-3-Flash 81.2**、**GPT-5.3-Codex 80.8**、**GPT-5-Pro 80.5**。最弱模型 **Mistral-Nemo** 仅 **18.1 Global HQI**，文中称最强最弱间硬件实现质量差距约 **4.7×**。
- 单看仿真会高估硬件准备度：所有模型上，**best-of-5 pass rate 平均比 Global HQI 高 7.5 分**；例如 **GPT-4.1** 为 **76.7% pass vs. 62.8 HQI**（差 **13.9**），**Gemini-2.0-Flash** 为 **54.5% pass vs. 39.6 HQI**（差 **14.9**）。
- 部署稳定性存在明显缺口：**best-of-5 与单次期望质量差距为 3.8–22.1 HQI 点**；Tier 1 中位差距也有 **8.2**，说明即使前沿模型单次调用也常达不到其能力上限。
- 在 **32,320** 次总生成中，有 **195** 次是真实综合失败；前三大失效模式占 **76.6%**：**late syntax errors 59 次（30.0%）**、**undefined module references 50 次（25.4%）**、**non-synthesizable constructs 41 次（20.8%）**。
- 失效模式按模型类型显著分化：专有模型更常“晚失败”，其 **46%** 失败为 elaboration 阶段的 late syntax error，且 **synthesis timeout 12%** 仅见于专有模型；开放权重模型更常“早失败”，**undefined module 40%**、**non-synthesizable 29%**、**simulation-only system tasks 13%**，指向其训练数据更偏仿真级RTL而非综合级RTL。另一个稳健性结果是，跨 **3 个工艺库** 的模型排名几乎不变，**Spearman ρ > 0.99**。

## Link
- [http://arxiv.org/abs/2603.11287v1](http://arxiv.org/abs/2603.11287v1)
