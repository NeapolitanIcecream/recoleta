---
source: arxiv
url: https://arxiv.org/abs/2606.04769v1
published_at: '2026-06-03T11:51:32'
authors:
- Yutao Shi
- Xiaohan Zhang
- Xiangjing Zhang
- Xihua Shen
- Hui Ouyang
- Huming Qiu
- Mi Zhang
- Min Yang
topics:
- mcp-security
- tool-calling
- code-intelligence
- agent-safety
- static-analysis
- llm-evaluation
relevance_score: 0.86
run_id: materialize-outputs
language_code: zh-CN
---

# Description-Code Inconsistency in Real-world MCP Servers: Measurement, Detection, and Security Implications

## Summary
## 摘要
本文研究 MCP 服务器中的描述与代码不一致：工具描述向 LLM 传达一种行为，而代码实际执行的是另一种行为。论文定义了这一问题类别，构建了 DCIChecker 来检测它，并在真实 MCP 服务器上进行测量。

## 问题
- MCP 智能体会根据名称、schema 和自然语言描述选择工具。在规划阶段，LLM 通常无法检查将要运行的代码。
- 当描述遗漏行为、夸大能力或隐藏副作用时，智能体可能选错工具、触发不想要的状态变化、浪费资源，或泄露数据。
- MCP 不要求检查工具描述是否与实现一致，因此过时文档、含糊规格、功能漂移和恶意描述都可能误导智能体。

## 方法
- 论文将 DCI 定义为 2 个主类和 7 个子类：功能不匹配包括未声明、夸大、误报和含糊行为；未声明副作用包括资源过度消耗、状态修改和数据泄露。
- DCIChecker 从 4 种常见的 MCP 注册模式中提取每个工具的名称、schema、描述和入口函数。
- 它使用基于 AST 的跨过程分析，为每个工具构建代码包：入口代码、按深度 k=3 追踪到的项目本地辅助函数，以及在可能时解析参数后的敏感 API 调用。
- 它用 Direct-Reverse-Arbitration 提示法比较描述和代码包：一个提示检查一致性，一个提示搜索不一致，第三个提示解决标签或子类分歧。
- 实现使用 claude-sonnet-4-5-20250929-thinking，temperature 为 0，top-p 为 1.0，生成长度上限为 4,096 token。

## 结果
- 测量覆盖了来自 2,214 个真实 MCP 服务器的 19,200 对描述-代码样本。
- DCIChecker 报告 9.93% 的样本存在 DCI，约为 19,200 个工具中的 1,907 个不一致工具。
- 论文称 DCI 呈长尾分布：少数服务器占了大多数有问题的工具，但摘录没有给出精确比例。
- 功能性误表述被报告为主要的 DCI 类别，其中夸大功能被指出最常见；摘录没有给出子类计数。
- 论文声称 Direct-Reverse-Arbitration 比单向提示法有更高的 precision 和 recall，但摘录没有给出精确的 precision、recall 或基线数值。
- 报告的安全影响包括工具调用失败、工具优先级判断错误、非预期系统行为，以及更强的工具投毒攻击；摘录没有给出攻击成功率数据。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.04769v1](https://arxiv.org/abs/2606.04769v1)
