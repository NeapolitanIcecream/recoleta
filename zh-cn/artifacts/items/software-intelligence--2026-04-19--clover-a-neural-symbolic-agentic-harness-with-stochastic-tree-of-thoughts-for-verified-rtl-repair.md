---
source: arxiv
url: http://arxiv.org/abs/2604.17288v1
published_at: '2026-04-19T07:04:49'
authors:
- Zizhang Luo
- Yansong Xu
- Runlin Guo
- Fan Cui
- Kexing Zhou
- Mile Xia
- Hongyuan Hou
- Yuhao Luo
- Yun Liang
topics:
- rtl-repair
- neural-symbolic-agents
- tree-of-thoughts
- hardware-verification
- code-intelligence
relevance_score: 0.88
run_id: materialize-outputs
language_code: zh-CN
---

# Clover: A Neural-Symbolic Agentic Harness with Stochastic Tree-of-Thoughts for Verified RTL Repair

## Summary
## 摘要
Clover 是一个自动化 RTL 修复系统，结合了 LLM 智能体、基于 SMT 的符号修复，以及对修复假设进行搜索的过程。它面向经过验证的硬件缺陷修复；纯模板修复会漏掉很多缺陷，而纯 LLM 修复在处理较长的 RTL 代码和波形数据时不稳定。

## 问题
- RTL 程序修复缓慢且成本高，因为工程师需要检查代码、运行仿真、阅读波形，并在多轮迭代中反复尝试补丁。
- 现有 RTL 修复方法分成两个各有明显短板的方向：符号系统精确，但只支持少量修复模板；LLM 系统灵活，但可能丢失上下文、误读底层轨迹，并生成不一致的补丁。
- 真实的 RTL 缺陷往往需要在不同抽象层上完成多个修复步骤，因此单一修复策略无法覆盖完整的修复空间。

## 方法
- Clover 将 RTL 修复视为对代码状态进行结构化搜索。主智能体提出缺陷假设，每次应用一个补丁，运行验证，并保留成功的修改，从而执行多步修复。
- 系统按任务类型分配工作：LLM 子智能体负责代码理解和 lint 修复，基于 SMT 的符号修复负责符合修复模板的底层修改。
- 它加入了一个 RTL 专用工具箱，包含仿真器访问、VCD 轨迹查看器、用于代码导航的语言服务器、Verilator 和自定义 linter，使智能体可以检查设计并测试候选修复。
- 其主要搜索方法是 stochastic tree-of-thoughts：每个假设和对话状态都成为搜索树中的一个节点，Clover 再根据一个启发式规则采样要扩展的节点。该规则基于已通过的测试平台数量、查询次数、编译错误、token 使用量和补丁数量。
- Clover 在已有符号 RTL 修复方法上加入了用于时序缺陷的 cycle-shift 模板，并让智能体决定何时调用各个模板，然后将求解器输出转换为源代码级别的补丁操作。

## 结果
- 在 RTL-Repair 基准上，Clover 在固定时间限制内修复了 **96.8%** 的缺陷。
- 论文称，与传统基线相比，这一结果多覆盖了 **94%** 的缺陷；与基于 LLM 的基线相比，多覆盖了 **63%** 的缺陷。
- Clover 报告平均 **pass@1 为 87.5%**。作者据此认为，该搜索过程提升的不只是最高成功率，也提高了可靠性。
- 摘录中将基准名称写为 **RTL-Repair**，并与传统符号/模板方法以及此前基于 LLM 的 RTL 修复系统进行了比较，但所给文本没有提供各个基线的完整表格。
- 论文还声称，通过将修复流程扩展到 **SystemVerilog** 并加入 **cycle-shift** 修复模板，符号方法的适用范围更广；但摘录没有给出这些改动单独的消融结果。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.17288v1](http://arxiv.org/abs/2604.17288v1)
