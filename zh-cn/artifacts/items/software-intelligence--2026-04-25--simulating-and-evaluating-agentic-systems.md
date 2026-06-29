---
source: hn
url: https://www.gojiberries.io/simulating-and-evaluating-agentic-systems/
published_at: '2026-04-25T23:00:50'
authors:
- neehao
topics:
- agent-evaluation
- agent-simulation
- multi-agent-systems
- llm-judge
- software-testing
relevance_score: 0.95
run_id: materialize-outputs
language_code: zh-CN
---

# Simulating and Evaluating Agentic Systems

## Summary
## 摘要
这篇文章认为，代理式系统的测试需要仿真加评估，因为固定提示词数据集和只看对话记录的检查，会漏掉在多步动作、工具调用和状态变化中才出现的失败。文章给出了一套实用的仿真/评估栈，包括场景设计、合成用户、结构化回合日志、确定性断言和经过校准的模型评审。

## 问题
- 代理式系统会跨多个步骤行动，会根据含糊输入分支，会使用工具，还要维护状态，所以当代理走出一条有效但不同的路径时，固定的黄金数据集就会失效。
- 只看对话记录的断言可能会通过，即使代理根本没有使用正确的工具，或者把后端状态改错了；语言记录不是系统真相。
- 单次 LLM 评审噪声很大，也有偏差。文中点名的位置偏差、冗长度偏差、自我增强偏差、评审者内部一致性低，以及对评分提示词表述的敏感性。

## 方法
- 把仿真/评估拆成三个独立阶段：场景数据、仿真运行、回合评估。保持分离，这样团队能分辨故障是来自坏场景、坏模拟器，还是坏评审器。
- 每个场景都定义起始提示词、用户目标、分支对话计划、用户画像、后端夹具，以及明确的期望，比如允许的终态和禁止的动作。
- 在受控环境中端到端运行真实代理，外部服务用模拟替身，合成用户通常是一个 LLM。合成用户按场景计划行动，同时根据代理的实际行为做调整。
- 把每个回合记录为结构化工件：运行后的世界状态、工具调用轨迹、对话记录，以及任何下游表面，例如截图、遥测或音频。
- 用四类断言给回合评分：结果断言看终态，过程断言看工具使用，一致性断言看轨迹和对话记录是否一致，表面断言看用户可见通道实际显示或执行了什么。尽量使用确定性检查，只在范围很窄的问题上用模型评分，并做聚合和校准。

## 结果
- 摘要没有报告基准分数、胜率或消融结果。
- 文中称，仿真/评估能覆盖单元测试、契约测试和组件集成测试碰不到的行为：决策分支、含糊输入处理、上下文中的工具使用、误解后的恢复，以及端到端任务完成。
- 文中给了一个具体的流量加权例子：如果生产流量中 40% 是订单状态查询，场景混合就应该反映这一点，而不是过度抽样退货请求。
- 文中建议每个场景重复多次试验，并报告 pass^k，也就是连续 k 次都通过的概率，同时给出轮数、步骤数、token 数、延迟和工具调用次数的分布，而不是单次运行的点估计。
- 文中列出了一些具体实现选项和工具：Google 的 ADK 用户仿真作为参考模式，CheckList（Ribeiro 等，2020）用于成对方向性测试，以及三个栈工具：understudy、mimiq 和 layoutlens。

## Problem

## Approach

## Results

## Link
- [https://www.gojiberries.io/simulating-and-evaluating-agentic-systems/](https://www.gojiberries.io/simulating-and-evaluating-agentic-systems/)
