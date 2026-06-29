---
source: arxiv
url: https://arxiv.org/abs/2604.26855v2
published_at: '2026-04-29T16:20:25'
authors:
- Frank Ginac
topics:
- ai-assisted-coding
- software-engineering
- code-review
- human-ai-interaction
- software-reliability
- model-collapse
relevance_score: 0.82
run_id: materialize-outputs
language_code: zh-CN
---

# Cognitive Atrophy and Systemic Collapse in AI-Dependent Software Engineering

## Summary
## 摘要
这篇立场论文认为，过度依赖 LLM 编码代理会削弱工程师的心智模型，让软件故障更难诊断。它主张对 AI 生成代码实施更严格的培训、审查和数据控制。

## 问题
- LLM 编码会把代码生产和人的理解分开，形成“认识论债务”：即系统实际行为与维护者能解释的内容之间的差距。
- 论文认为这很重要，因为如果工程师接受 AI 补丁却不追踪其逻辑，在故障、 امنیت 事件或依赖项失效时就可能失手。
- 递归训练和合成代码复用可能缩小代码模式的范围，并传播不安全或平庸的方案。

## 方法
- 论文把认识论债务定义为人机接口成本，与代码库中的技术债务不同。
- 论文借助波兰尼的默会知识、“vibe coding”、“mechanized convergence”，以及递归生成数据导致的模型坍塌来展开论证。
- 论文以 Amazon Q Developer 和据称的 2026 年 Amazon 事件为案例，说明 AI 辅助代码审查的风险。
- 论文建议在核心教育中采用“no-vibe coding”，对 AI 辅助的生产变更进行资深审查，建立从规格到代码的可追溯性，使用基于属性的测试、依赖影响审计、性能剖析，以及经过筛选的人类编写代码语料库。

## 结果
- 论文称，Amazon Q Developer 将 30,000 个生产应用迁移到 Java 17，估计节省了 4,500 个开发者年和每年 2.6 亿美元成本。
- 论文引用 79% 的自动生成代码审查接受率，且没有人工修改，把这当作例行盖章式审查的证据。
- 论文声称 2026 年 Amazon 发生了两起事件：一次持续 6 小时的核心电商站点中断，以及一次持续 13 小时的 AWS 成本管理服务故障，都与 GenAI 辅助的变更有关。
- 论文引用 Shukla 等人的结果，称在没有严格人工介入的情况下，经过 5 轮 AI 代码生成后，关键安全漏洞增加了 37.6%。
- 论文没有给出新的对照实验或基准测试；其主要贡献是一个概念性风险模型和一组治理建议。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2604.26855v2](https://arxiv.org/abs/2604.26855v2)
