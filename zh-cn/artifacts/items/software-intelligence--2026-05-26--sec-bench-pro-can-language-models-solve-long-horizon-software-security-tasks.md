---
source: arxiv
url: https://arxiv.org/abs/2605.26548v1
published_at: '2026-05-26T04:59:49'
authors:
- Hwiwon Lee
- Jiawei Liu
- Dongjun Kim
- Ziqi Zhang
- Chunqiu Steven Xia
- Lingming Zhang
topics:
- software-security
- code-intelligence
- llm-agents
- vulnerability-discovery
- benchmarking
- proof-of-concept-generation
relevance_score: 0.86
run_id: materialize-outputs
language_code: zh-CN
---

# SEC-bench Pro: Can Language Models Solve Long-Horizon Software Security Tasks?

## Summary
## 摘要
SEC-bench Pro 是一个基准，用来测试 LLM 编码代理能否在大型 JavaScript 引擎中发现并证明真实的长周期软件安全漏洞。论文报告称，当前代理在 V8 和 SpiderMonkey 上解决的任务都不到 40%。

## 问题
- 现有安全基准常依赖 fuzzing harness、sanitizer 跟踪、生成的漏洞描述或按补丁评分，这些信息会给代理提供真实漏洞猎手拿不到的线索。
- 真实的 JS 引擎漏洞很重要，因为 V8 和 SpiderMonkey 在浏览器和运行时中执行不受信任的代码，利用这些漏洞可能导致远程代码执行。
- 长周期漏洞猎取需要查看源码、配置环境、动态测试，以及围绕 JIT、垃圾回收、对象布局、沙箱和内存安全行为构造 PoC。

## 方法
- SEC-bench Pro 以已披露报告为基础构建任务，这些报告包含具体 PoC 和对应的修复。
- 一个三阶段流程收集报告、用编码代理重建历史上的易受攻击环境，并用自动化 oracle 验证每个实例。
- 每个被接受的任务都提供 vulnerable version、fixed version 和 latest version 的 Docker 镜像。
- 评分系统会在这三个镜像上运行每个提交的 PoC，然后用 LLM 评审判断证据是否对应目标漏洞，而不是无关崩溃。
- 简单说，这个基准把真实漏洞报告变成可重复的安全任务，并检查代理能否在接近真实的条件下产出可用 PoC。

## 结果
- 数据集包含 183 个已验证漏洞：V8 中 103 个，SpiderMonkey 中 80 个。
- V8 子集包括 86 个符合赏金条件的报告和 17 个不符合赏金条件的报告，累计获得 Google VRP 奖励 $1,540,750。
- 最强的单代理配置在 V8 上解决 33/103 个任务，即 32.0%，在 SpiderMonkey 上解决 31/80 个任务，即 38.8%。
- 开放权重的 Kimi-K2.6 基线在 V8 上解决 12/103 个任务，即 11.7%。
- ClaudeCode 和 Codex 解决的任务集合不同；两者并集在 V8 上达到 39/103，即 37.9%，在 SpiderMonkey 上达到 39/80，即 48.8%。
- 只按崩溃计分的评审会把 168 个配置-实例成功算进去，而按判定后的成功只有 117 个，少算 51 个，或 43.6%，说明目标归因会改变测得分数。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.26548v1](https://arxiv.org/abs/2605.26548v1)
