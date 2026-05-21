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
这篇立场论文认为，过度依赖 LLM 编码代理会削弱工程师的心智模型，并使软件故障更难诊断。论文提出，应对 AI 生成代码采取更严格的培训、评审和数据控制。

## 问题
- LLM 编码可能让代码生产与人的理解脱节，形成“认识论债务”：系统实际行为与维护者可解释内容之间的差距。
- 论文称，工程师如果接受 AI 补丁却不追踪其逻辑，在宕机、安全事件或依赖故障中可能无法有效应对。
- 对合成代码的递归训练和复用可能缩小代码模式的范围，并传播不安全或平庸的解决方案。

## 方法
- 论文将认识论债务定义为一种人机系统接口成本，区别于代码库中的技术债务。
- 论文使用 Polanyi 的默会知识、“氛围编码”、“机械化趋同”以及由递归生成数据导致的模型崩塌来构建论证。
- 论文以 Amazon Q Developer 和报道中的 2026 年 Amazon 事件作为案例，分析 AI 辅助代码评审风险。
- 论文建议在核心教育中实行“无氛围编码”，对 AI 辅助的生产变更进行高级工程师评审，建立从规格到代码的可追溯性，采用基于属性的测试、依赖影响审计、性能剖析，以及经过筛选的人类编写代码语料库。

## 结果
- 论文报告称，Amazon Q Developer 将 30,000 个生产应用迁移到 Java 17，估计节省 4,500 个开发者年和每年 2.6 亿美元成本。
- 论文引用了自动生成代码评审在未经人工修改情况下 79% 的接受率，并将其作为橡皮图章式评审模式的证据。
- 论文声称 2026 年发生了两起 Amazon 事件：一次持续六小时的主要电商店面宕机，以及一次持续 13 小时、与 GenAI 辅助变更相关的 AWS 成本管理服务中断。
- 论文引用 Shukla 等人的研究称，在没有严格人工干预的情况下，AI 代码生成经过五轮迭代后，严重安全漏洞增加了 37.6%。
- 论文没有提出新的受控实验或基准测试；其主要贡献是一个概念性风险模型和一组治理建议。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2604.26855v2](https://arxiv.org/abs/2604.26855v2)
