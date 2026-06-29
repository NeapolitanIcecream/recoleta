---
source: arxiv
url: https://arxiv.org/abs/2605.04704v2
published_at: '2026-05-06T09:55:36'
authors:
- Junhao Ye
- Dingrong Pan
- Hanyuan Liu
- Yuchen Hu
- Jie Zhou
- Ke Xu
- Xinwei Fang
- Xi Wang
- Nan Guan
- Zhe Jiang
topics:
- rtl-verification
- uvm-automation
- code-intelligence
- llm-agents
- hardware-engineering
- testbench-generation
relevance_score: 0.78
run_id: materialize-outputs
language_code: zh-CN
---

# UVMarvel: an Automated LLM-aided UVM Machine for Subsystem-level RTL Verification

## Summary
## 摘要
UVMarvel 通过使用 LLM 构建 UVM testbench 并改进激励，自动化子系统级 RTL 验证。论文声称，它在类工业子系统基准上平均代码覆盖率达到 95.65%，达到 90% 覆盖率的运行时间为 4.5 小时。

## 问题
- RTL 验证消耗了约 70% 的 IC 前端工作量，而子系统级 UVM testbench 的构建仍然需要专家手工编码。
- 以往基于 LLM 和模板的 UVM 流程主要停留在 IP 级，难以处理总线时序、IP 间依赖、协议语义和长篇角落场景序列。
- 初始的 LLM 生成激励平均覆盖率可能低于 40%，因为它们会重复简单模式，遗漏多步子系统行为。

## 方法
- UVMarvel 将规格和 RTL 转换为五部分 IR：模块名称、接口描述、寄存器配置、时序特性和功能描述。
- 总线协议库为 APB、AHB、AXI、P-Channel 和 Q-Channel 提供 UVM 骨架，包括接口、driver、monitor 和 agent；LLM 填充 DUT 相关字段。
- Coverage Analyser 从仿真器覆盖率报告中提取未覆盖和部分覆盖项，并把压缩后的目标交给 LLM。
- Signal Tracker 通过 Verilog 文件追踪未覆盖信号，找到相关语句和可控的顶层 I/O 路径。
- Verilog Patcher 围绕这些语句重建最小有效 RTL 切片，然后由 GPT-4.1、Claude 4.5 和 Gemini 2.5 Pro 生成或修复新的 UVM 序列。

## 结果
- UVMarvel 在六个子系统基准上报告的平均代码覆盖率为 95.65%，这六个基准分别是 Watchdog、Pwrctrl、Cordic、IdleControl、LPctrl 和 Busremap。
- 各设计的代码覆盖率分别为：Watchdog 98.84%、Pwrctrl 93.66%、Cordic 100%、IdleControl 94.90%、LPctrl 90.83%、Busremap 95.66%。
- 功能覆盖率分别为：Watchdog 100%、Pwrctrl 90.64%、Cordic 100%、IdleControl 96.12%、LPctrl 89.33%、Busremap 98.27%。
- 基准集覆盖了 APB、AHB、AXI、Q-Channel 和 P-Channel 设计，每个设计包含 3 到 10 个模块，RTL 行数约为 800 到 3000 以上。
- 论文声称，UVMarvel 在 4.5 小时内达到 90% 代码覆盖率，比专家手工流程快 20.17 倍，不包括人工 IR 和测试规划阶段。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.04704v2](https://arxiv.org/abs/2605.04704v2)
