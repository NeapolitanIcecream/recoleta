---
source: arxiv
url: https://arxiv.org/abs/2606.10933v1
published_at: '2026-06-09T14:44:43'
authors:
- Aman Sharma
- Sushrut Thorat
- Paras Chopra
topics:
- coding-agents
- metaprogramming
- esoteric-languages
- code-benchmarks
- tool-use
- software-agents
relevance_score: 0.94
run_id: materialize-outputs
language_code: zh-CN
---

# Frontier Coding Agents Use Metaprogramming to Adapt to Unfamiliar Programming Languages

## Summary
## 总结
论文发现，前沿编程代理在不熟悉的编程语言上表现最好时，通常先用熟悉语言写生成器，再借助本地执行调试生成出来的目标语言代码。

## 问题
- 标准编程基准常在 Python、JavaScript、常见库和公开仓库里测试代理，这些场景里已有曝光会掩盖它们在适应新语言时的缺口。
- 真实的软件工作会遇到内部 DSL、专有配置格式、生成式 API 和本地工具，而这些往往几乎没有公开训练数据。
- 论文测试代理能否在一次会话中学到足够信息，去编写、运行、调试并提交在陌生可执行接口中正确的程序。

## 方法
- 作者评估了六个已部署的编程代理：Claude Opus 4.6、Claude Sonnet 4.6、Claude Haiku 4.5、GPT-5.4 xhigh、GPT-5.4 mini 和 Kimi K2.5。
- 他们使用 EsoLang-Bench 的四种语言进行 80 题序列测试：Brainfuck、Befunge-98、Whitespace 和 Shakespeare。
- 每个代理都在持久工作区中运行，可进行文件编辑、shell 访问、本地解释器调用，并且每题最多提交 3 次隐藏测试。
- 研究的主要机制是元编程：代理先写一个 Python、JavaScript 或 Rust 程序来生成目标 esolang 源码，然后在本地测试并修改这个生成器。
- 诊断实验会限制元编程、加入书面策略指导、提供辅助库，并调整解释器调用和输出 token 的预算。

## 结果
- EsoLang-Bench 对不同代理的区分度远高于几个主流基准：六个代理的平均分跨度在 EsoLang-Bench 上是 88.4 个百分点，而在 SWE-Bench Verified 上是 6.6，在 Terminal-Bench 2.0 上是 33.3，在 LiveCodeBench v6 上是 43.5。
- EsoLang-Bench 的主要平均分分别是：GPT-5.4 xhigh 99.7%，Claude Opus 4.6 86.9%，Claude Sonnet 4.6 66.3%，GPT-5.4 mini 32.5%，Claude Haiku 4.5 24.7%，Kimi K2.5 11.3%。
- 在 Brainfuck 上，GPT-5.4 xhigh 解决率为 98.8%，Opus 4.6 为 80.0%，而 Haiku 4.5 和 Kimi K2.5 都是 5.0%。
- 主机语言生成解释了 Brainfuck 提升中的很大一部分：Opus 4.6 用 Python 生成器解出 64/80，JavaScript 生成器解出 63/80，Rust 生成器解出 55/80；直接编写目标语言时为 27/80。GPT-5.4 xhigh 用这三种主机语言分别解出 79/80、77/80 和 79/80，直接编写时为 29/80。
- 书面策略迁移帮助不大，但可执行的辅助代码能帮助中等水平代理：在 Brainfuck 上，Sonnet 4.6 在库支持下从 12/80 提升到 64/80，GPT-5.4 mini 从 5/80 提升到 53/80；在 Befunge-98 上，Sonnet 从 64/80 提升到 78/80，GPT-5.4 mini 从 11/80 提升到 64/80。
- 更多本地解释器调用和输出 token 会帮助那些已经在构建有效策略的代理；Haiku 4.5 仍然接近下限，而 Opus 4.6 会随着解释器访问增加而提升，并且用比 Sonnet 4.6 更少的输出 token 就能在 Brainfuck 和 Befunge-98 的前 20 题上达到 20/20。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.10933v1](https://arxiv.org/abs/2606.10933v1)
