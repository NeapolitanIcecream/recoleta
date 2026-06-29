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
Clover 是一个自动化 RTL 修复系统，把 LLM 代理、基于 SMT 的符号修复和针对修复假设的搜索过程结合起来。它面向经过验证的硬件 bug 修复场景，在这里，纯模板修复会漏掉很多 bug，而纯 LLM 修复在长 RTL 代码和波形数据上不稳定。

## 问题
- RTL 程序修复速度慢、成本高，因为工程师必须检查代码、运行仿真、读取波形，并在多轮迭代中尝试补丁。
- 现有 RTL 修复方法分成两个都不够强的极端：符号系统精确，但只覆盖少量修复模板；LLM 系统灵活，但会丢失上下文、误读低层级轨迹，并生成不一致的补丁。
- 真实 RTL bug 往往需要在不同抽象层上做多步修复，所以单一修复策略覆盖不了全部修复空间。

## 方法
- Clover 把 RTL 修复看作对代码状态的结构化搜索。主代理提出 bug 假设，每次应用一个补丁，运行验证，并保留成功的修改，从而支持多步修复。
- 系统按任务类型分派工作：LLM 子代理处理代码理解和 lint 修复，基于 SMT 的符号修复处理符合修复模板的低层级编辑。
- 它加入了一个面向 RTL 的工具箱，包括仿真器访问、VCD 轨迹查看器、用于代码导航的语言服务器、Verilator 和自定义 lint 工具，方便代理检查设计并测试候选修复。
- 主要搜索方法是随机思维树：每个假设和对话状态都会变成搜索树中的一个节点，Clover 根据通过的测试平台数量、查询次数、编译错误、token 使用量和补丁数量组成的启发式规则，采样要扩展的节点。
- Clover 在既有符号 RTL 修复上增加了一个用于时序 bug 的 cycle-shift 模板，并让代理决定何时调用每个模板，然后把求解器输出转成源代码级的补丁动作。

## 结果
- 在 RTL-Repair 基准上，Clover 在固定时间限制内修复了 **96.8%** 的 bug。
- 论文称，这比传统基线多修复了 **94%** 的 bug，比基于 LLM 的基线多修复了 **63%** 的 bug。
- Clover 报告的平均 **pass@1 为 87.5%**，作者用这一结果说明搜索过程提高了可靠性，而不只是提高了峰值成功率。
- 这段摘要把基准命名为 **RTL-Repair**，并与传统符号/模板方法和先前基于 LLM 的 RTL 修复系统进行比较，但提供的文本里没有完整的逐基线表格。
- 论文还声称它把修复流程扩展到了 **SystemVerilog**，并加入了 **cycle-shift** 修复模板，不过这段摘要没有给出这些新增内容单独的消融结果。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.17288v1](http://arxiv.org/abs/2604.17288v1)
