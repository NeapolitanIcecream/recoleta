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
论文认为，测试智能体系统需要把模拟和评估结合起来，因为固定提示词数据集和只看对话记录的检查方式，会漏掉那些在多步动作、工具调用和状态变化过程中出现的失败。文中给出了一套可落地的 sim/eval 方法栈，包括场景设计、合成用户、结构化 episode 日志、确定性断言，以及经过校准的基于模型的评审。

## 问题
- 智能体系统会在多步过程中行动，会根据模糊输入分支决策，会使用工具，并维护状态，因此当智能体走了一条有效但不同的路径时，固定的 golden dataset 就会失效。
- 只针对对话记录做断言，即使智能体从未调用正确工具，或错误修改了后端状态，也可能通过；语言不是系统的记录依据。
- 单次 LLM 评审噪声大且有偏差。论文列出的失效模式包括位置偏差、冗长偏差、自我增强偏差、评分者内部一致性低，以及对评分提示词措辞敏感。

## 方法
- 将 sim/eval 拆成三个独立阶段：场景数据、模拟运行和 episode 评估。保持三者分离，这样团队才能判断失败是来自场景设计差、模拟器差，还是评审器差。
- 为每个场景定义起始提示词、用户目标、分支对话计划、角色设定、后端 fixtures，以及明确预期，例如允许的终止状态和禁止的动作。
- 让真实智能体在受控环境中端到端运行，环境中包含被 mock 的外部服务和一个合成用户，通常是 LLM。这个合成用户会遵循场景计划，同时根据智能体的实际行为调整。
- 将每个 episode 记录为结构化产物：运行后的世界状态、工具调用轨迹、对话记录，以及任何下游呈现内容，例如截图、遥测数据或音频。
- 用四类断言给 episode 打分：针对最终状态的结果断言、针对工具使用过程的过程断言、针对轨迹与对话记录一致性的断言，以及针对用户可见通道实际显示或执行内容的表层断言。能用确定性检查的地方就用确定性检查；只有在问题足够窄时才使用基于模型的评分，并配合聚合和校准。

## 结果
- 摘录中没有报告基准分数、胜率或消融实验数字。
- 文中称，sim/eval 能覆盖单元测试、契约测试和组件集成测试无法触达的行为：决策分支、歧义处理、上下文中的工具使用、对误解的恢复，以及端到端任务完成。
- 它给出一个具体的流量加权例子：如果生产流量中 40% 是订单状态查询，那么场景分布应反映这一点，而不是过度抽样退货请求。
- 文中建议每个场景重复试验，并报告 pass^k，即 k 次运行全部通过的概率；同时报告轮次数、步骤数、token 数、延迟和工具调用次数的分布，而不是单次运行的点估计。
- 文中提到了一些具体实现选项和工具：Google 的 ADK user simulation 可作为参考模式，CheckList（Ribeiro et al., 2020）可用于成对方向性测试，以及三个工具栈工具：understudy、mimiq 和 layoutlens。

## Problem

## Approach

## Results

## Link
- [https://www.gojiberries.io/simulating-and-evaluating-agentic-systems/](https://www.gojiberries.io/simulating-and-evaluating-agentic-systems/)
