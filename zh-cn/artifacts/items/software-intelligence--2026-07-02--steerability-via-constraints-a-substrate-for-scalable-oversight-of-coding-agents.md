---
source: arxiv
url: https://arxiv.org/abs/2607.02389v1
published_at: '2026-07-02T16:24:47'
authors:
- Thomas Winninger
topics:
- coding-agents
- code-review
- software-security
- static-analysis
- agent-oversight
- developer-tools
relevance_score: 0.89
run_id: materialize-outputs
language_code: zh-CN
---

# Steerability via constraints: a substrate for scalable oversight of coding agents

## Summary
## 摘要
论文称，当代码库通过工具强制执行契约，而不是依赖提示词或很长的指导文件时，代码智能体更容易被审查。在一个小型 Python 后门测试中，约束加上一个 200 行的文档 CLI，把 Gemma 4 e4b 审查器的召回率从 54.5% 提高到 90.9%。

## 问题
- 代码智能体可以编写大量代码，但当代码库超过审查者可用上下文时，人类或可信模型审查无法随之扩展。
- 不受约束的智能体会带来安全风险和代码库漂移，因为提示词和散文式规则可能在长任务中被忽略或遗忘。
- 这篇论文对自动化软件生产有意义，因为它针对审查瓶颈，而不只是改进代码生成。

## 方法
- 主要机制是把规则移入可强制执行的代码库约束：ruff、pyrefly、beartype、pydantic strict mode、jaxtyping shapes、frozen dataclasses、Literal discriminators，以及纯 `core/` 与非纯 `runners/` 的拆分。
- 不变量放在代码附近的模块 docstring 中，因此审查者可以连同局部契约一起检查函数，而不需要阅读完整仓库指南。
- 一个基于 griffe 构建的 200 行 `docs` CLI 暴露模块 API、符号签名、dataclass 字段、docstring 和不变量块，用于窄范围的逐函数审查。
- 系统草图还加入了 VM、网络出口 allowlist，以及可检查模型流量的推理代理，不过论文只评估了约束底座和 `docs` 部分。

## 结果
- 在一个合成的 500-LoC Python LM-eval 代码库中，研究者手工插入了 11 个后门；无工具的非约束代码抓到了 6/11 个后门：召回率 54.5%，精确率 100.0%。
- 只给非约束代码加入 `docs` CLI 抓到了 9/11 个后门：召回率 81.8%，精确率 100.0%。
- 只加入约束底座抓到了 9/11 个后门：召回率 81.8%，精确率 88.9%。
- 约束底座与 `docs` 结合后抓到了 10/11 个后门：召回率 90.9%，精确率 95.7%。
- 在最佳设置中，Gemma 4 e4b 抓到了 L1 2/2、L2 1/2、L3 3/3、L4 1/1 和 L5 3/3 个后门。
- 作者称该实验是初步的：它使用 11 个合成后门、一个小型代码库、一个小型审查模型，以及一套手工构建的评分设置。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2607.02389v1](https://arxiv.org/abs/2607.02389v1)
