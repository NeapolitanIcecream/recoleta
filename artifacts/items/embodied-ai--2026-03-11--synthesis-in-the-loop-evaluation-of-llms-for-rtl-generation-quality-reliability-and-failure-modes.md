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
- llm-evaluation
- rtl-generation
- verilog
- synthesis-in-the-loop
- hardware-quality
relevance_score: 0.05
run_id: materialize-outputs
---

# Synthesis-in-the-Loop Evaluation of LLMs for RTL Generation: Quality, Reliability, and Failure Modes

## Summary
这篇论文提出了一个“综合在环”的RTL生成评测框架，用于衡量LLM生成Verilog时不仅是否能跑通测试，还是否真正可综合、且综合后的硬件质量是否接近专家设计。作者在202个任务、32个模型、每题5次采样上发现，硬件级能力呈现清晰三层分化，并暴露出单次部署可靠性和失败模式上的系统差异。

## Problem
- 现有RTL生成评测大多只看语法或仿真通过率，无法判断代码是否**可综合**，以及综合后面积、时序、告警是否达标。
- 这很重要，因为芯片RTL开发的真实瓶颈不只是“功能对”，还要求设计能进入后端实现并满足面积/时序约束；仅靠仿真通过会高估LLM对生产级硬件设计的实用性。
- 生成的Verilog即使测试通过，也可能包含不可综合结构，或在面积/延迟上比专家实现差2–5倍，这些都不是传统软件式评测能发现的。

## Approach
- 作者评测了**32个语言模型**，覆盖**202个Verilog任务**（来自 VerilogEval 和 RTLLM），每个模型-任务组合进行**5次独立生成**。
- 采用三级流水线打分：先做**语法有效性**（Icarus Verilog），再做**可综合性**（Yosys + Nangate45 45nm），最后做**功能正确性**（testbench仿真）；任一关失败则HQI记为0。
- 提出**Hardware Quality Index (HQI)**，把通过三关的设计与专家参考在**面积、延迟、告警数**上做归一化比较，得到0–100分；100表示与专家实现持平。
- 使用**复杂度加权 Coverage、Global HQI、Expected HQI**分别衡量：能否解题、best-of-5能力上限、以及单次调用的部署质量，从而显式量化“能力-部署”差距。
- 另外构建了基于Yosys诊断的**九类综合失败 taxonomy**，并在另外两套工艺库上复综合，验证排名跨工艺的稳健性。

## Results
- 在**32个模型、202个任务、每题5次**的评测中，作者发现三层能力结构：**13个模型**位于Tier 1（Global HQI ≥ 71），**11个**位于Tier 2（53–68），**8个**位于Tier 3（<53）。最佳模型是 **Gemini-3-Pro**，达到**87.5% Coverage** 和 **85.1 Global HQI**。
- 头部模型还包括 **GPT-5.4-Pro (81.3 HQI)**、**Gemini-3-Flash (81.2)**、**GPT-5.3-Codex (80.8)**、**GPT-5-Pro (80.5)**；而最强开源权重模型如 **DeepSeek-V3.2 (58.8)**、**Qwen3.5-397B-OSS (58.2)**，比专有Tier 1前沿模型落后约**15–20 HQI点**。
- 论文声称传统仿真通过率会**系统性高估**硬件可用性：所有32个模型上，**best-of-five pass rate 平均比 Global HQI 高 7.5 点**。例如 **GPT-4.1** 的通过率为 **76.7%**，但 Global HQI 只有 **62.8**（差 **13.9**）；**Gemini-2.0-Flash** 为 **54.5% vs 39.6**（差 **14.9**）。
- 单次部署与多次采样的差距明显：**best-of-five 与 single-attempt 的差距为 3.8–22.1 HQI 点**；Tier 1中的中位差距也有**8.2点**。最佳模型 **Gemini-3-Pro** 从 **85.1 Global HQI** 降到 **78.5 Expected HQI**，说明即使前沿模型也需要multi-sample策略。
- 失败分析覆盖**32,320次生成**，其中有**195次真实综合失败**。三大主因占**76.6%**：**late syntax errors 59次 (30.0%)**、**undefined module references 50次 (25.4%)**、**non-synthesizable constructs 41次 (20.8%)**。这表明很多失败发生在“能过解析但过不了综合”的真实硬件约束层面。
- 排名对工艺库变化很稳健：在 Nangate45、IHP SG13G2、OSU 0.35μm 三个库之间，模型排名相关性达到 **Spearman ρ > 0.99**；HQI权重敏感性分析也显示 **ρ ≥ 0.997**、最大名次位移**不超过3位**。这说明其评测结论不是某一套打分细节或工艺库的偶然产物。

## Link
- [http://arxiv.org/abs/2603.11287v1](http://arxiv.org/abs/2603.11287v1)
