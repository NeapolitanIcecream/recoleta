---
source: arxiv
url: https://arxiv.org/abs/2605.15226v1
published_at: '2026-05-13T14:14:54'
authors:
- Qingyun Zou
- Feng Yu
- Hongshi Tan
- Bingsheng He
- WengFai Wong
topics:
- hardware-engineering
- code-agents
- benchmark
- eda-verification
- verilog-systemverilog
- software-engineering-agents
relevance_score: 0.86
run_id: materialize-outputs
language_code: zh-CN
---

# Is Agentic AI Ready for Real-World Hardware Engineering? A Deep Dive with Phoenix-bench

## Summary
## 摘要
Phoenix-bench 测试软件编码智能体能否在可执行 EDA 检查下修复真实的 Verilog/SystemVerilog 仓库问题。论文发现，当前智能体从 SWE-bench 迁移到硬件任务时表现较差，主要原因是它们漏掉了跨模块信号流依赖。

## 问题
- 现有硬件 LLM 基准通常测试孤立的模块生成、语法修复或局部调试，因此没有覆盖仓库导航、层次感知定位、EDA 执行和维护式补丁。
- 真实硬件 bug 常通过端口、参数、时钟、复位和信号流在实例化模块之间传播。按软件调用图搜索可能停在症状文件，漏掉 bug 源头。
- 这一点很重要，因为硬件补丁必须通过仿真器、解析器、综合或 testbench 检查，同时不能破坏已有行为。

## 方法
- Phoenix-bench 包含来自 114 个 GitHub 仓库的 511 个已验证 Verilator 实例，构建自对 786 个仓库中 18,010 个 issue 的抓取。
- 每个任务包含 issue、仓库快照、开发者补丁、设计流程标签、fail-to-pass 测试、pass-to-pass 测试，以及 Docker 固定的开源 EDA 环境。
- 评测器只在目标失败测试通过且此前通过的测试仍然通过时接受补丁。
- 研究评估了 4 个商业智能体和 8 种开源智能体结构，覆盖 4 个 LLM 骨干模型，并加入两项诊断：文件级 oracle 定位和一轮 testbench 日志反馈。

## 结果
- Phoenix-bench 上最高的商业解决率仍然偏低：搭配 Claude Opus 4.7 的 Claude Code 达到 38.6%，搭配 GPT-5.5 的 OpenAI Codex 达到 38.0%，Gemini CLI 达到 37.4%，GitHub Copilot coding agent 达到 32.7%。
- 表中最强的开源结构是 OpenHands：搭配 GPT-5.2 为 33.9%，搭配 Gemini-3-Pro 为 33.5%，搭配 Qwen3-Coder-480B 为 32.3%，搭配 DeepSeek-V3.2 为 26.0%。
- 同一批智能体从 SWE-bench Verified 到 Phoenix-bench 损失 37 到 58 个百分点。搭配 Qwen3-Coder-480B 的 OpenHands 从 SWE-bench Verified 上的 69.6% 降至 Phoenix-bench 上的 32.3%。
- 文件级 oracle 定位只让解决率提高 1.4 个百分点，因为智能体仍会编辑错误模块，或破坏不需要修改的文件。
- 一轮 testbench 日志反馈把解决率提高到约 42% 至 45%，说明具体的失败测试证据比单独的文件名更能指导智能体。
- Phoenix-bench 实例比 SWE-bench Verified 更大，也涉及更多跨文件修改：gold patch 平均编辑 737.5 行 HDL 和 5.7 个 HDL 文件，语料库包含 71,048 个 TESTCASE 检查，补丁行覆盖率为 99.91%。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.15226v1](https://arxiv.org/abs/2605.15226v1)
