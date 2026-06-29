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
## 总结
Phoenix-bench 测试软件编码代理能否在可执行的 EDA 检查下修复真实的 Verilog/SystemVerilog 仓库问题。论文发现，当前代理从 SWE-bench 迁移到硬件任务时表现较差，主要原因是它们抓不住跨模块的信号流依赖。

## 问题
- 现有硬件 LLM 基准通常只测孤立的模块生成、语法修复或局部调试，缺少仓库导航、分层感知定位、EDA 执行和维护式补丁编辑。
- 真实硬件 bug 往往会通过端口、参数、时钟、复位和信号流在已实例化的模块之间扩散。按软件方式沿调用图搜索，会停在症状文件，错过 bug 的源头。
- 这很重要，因为硬件补丁必须通过模拟器、解析器、综合或测试平台检查，同时不能破坏已有行为。

## 方法
- Phoenix-bench 包含 114 个 GitHub 仓库中的 511 个已验证 Verilator 实例，来自对 786 个仓库中 18,010 个 issue 的爬取。
- 每个任务都包含 issue、仓库快照、开发者补丁、设计流程标签、fail-to-pass 测试、pass-to-pass 测试，以及一个固定到 Docker 的开源 EDA 环境。
- 评估器只有在失败的目标测试通过、之前通过的测试仍然通过时才接受补丁。
- 研究评估了 4 个商业代理和 8 个开源代理结构，覆盖 4 个 LLM 骨干模型，然后加入两个诊断项：文件级 oracle 定位和一轮 testbench 日志反馈。

## 结果
- Phoenix-bench 上表现最好的商业代理 resolved rate 仍然不高：Claude Code 搭配 Claude Opus 4.7 达到 38.6%，OpenAI Codex 搭配 GPT-5.5 达到 38.0%，Gemini CLI 达到 37.4%，GitHub Copilot coding agent 达到 32.7%。
- OpenHands 是表中最强的开源结构：搭配 GPT-5.2 时为 33.9%，搭配 Gemini-3-Pro 时为 33.5%，搭配 Qwen3-Coder-480B 时为 32.3%，搭配 DeepSeek-V3.2 时为 26.0%。
- 同样的代理从 SWE-bench Verified 到 Phoenix-bench 下降了 37 到 58 个百分点。搭配 Qwen3-Coder-480B 的 OpenHands 从 SWE-bench Verified 上的 69.6% 降到 Phoenix-bench 上的 32.3%。
- 文件级 oracle 定位只把 resolved rate 提高了 1.4 个百分点，因为代理还是会改错模块，或者破坏了原本不需要改动的文件。
- 一轮 testbench 日志反馈把 resolved rate 提高到大约 42% 到 45%，说明具体的失败测试证据比文件名更能给代理提供有效指引。
- Phoenix-bench 实例比 SWE-bench Verified 更大，也更跨文件：平均 gold patch 会修改 737.5 行 HDL 和 5.7 个 HDL 文件，语料包含 71,048 个 TESTCASE 检查，patch-line 覆盖率为 99.91%。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.15226v1](https://arxiv.org/abs/2605.15226v1)
