---
source: arxiv
url: https://arxiv.org/abs/2605.00742v2
published_at: '2026-05-01T15:43:43'
authors:
- Theodore Papamarkou
- Pierre Alquier
- Matthias Bauer
- Wray Buntine
- Andrew Davison
- Gintare Karolina Dziugaite
- Maurizio Filippone
- Andrew Y. K. Foong
- Vincent Fortuin
- Dimitris Fouskakis
- Jes Frellsen
- "Eyke H\xFCllermeier"
- Theofanis Karaletsos
- Mohammad Emtiyaz Khan
- Nikita Kotelevskii
- Salem Lahlou
- Yingzhen Li
- Fang Liu
- Clare Lyle
- "Thomas M\xF6llenhoff"
- Konstantina Palla
- Maxim Panov
- Yusuf Sale
- Kajetan Schweighofer
- Artem Shelmanov
- Siddharth Swaroop
- Martin Trapp
- Willem Waegeman
- Andrew Gordon Wilson
- Alexey Zaytsev
topics:
- agent-orchestration
- bayesian-decision-theory
- multi-agent-systems
- code-intelligence
- human-ai-interaction
- tool-routing
relevance_score: 0.87
run_id: materialize-outputs
language_code: zh-CN
---

# Position: agentic AI orchestration should be Bayes-consistent

## Summary
## 摘要
论文主张，智能体 AI 系统应在编排层使用贝叶斯决策规则，同时把 LLM 和工具保留为黑盒预测器。它关注路由、停止、升级和预算选择，因为这些选择中的最佳动作受不确定性、成本和风险影响。

## 问题
- LLM 智能体经常需要选择调用哪个工具或专家、是否询问用户、何时停止，以及投入多少计算资源；token 概率不能清晰映射到任务级不确定性。
- 在多步骤或高风险系统中，这一点会影响结果，因为错误路由、薄弱的停止规则和重复工具调用会浪费预算、增加延迟，或提高安全风险。
- 让 LLM 本身成为完整的贝叶斯更新器成本很高，而且仍可能漏掉动作选择所需的不确定性。

## 方法
- 在 LLM 和工具之上加入一个贝叶斯控制器。它跟踪任务潜变量的后验分布，例如代码是否会通过测试、哪个假设获得最强支持，或哪个智能体可靠。
- 将每条智能体消息或工具输出视为有噪声的证据。在代码示例中，控制器更新 `r_t(y) ∝ r_{t-1}(y) p_i(z_t|y)^{α_i}`，其中 `α_i` 调节来自智能体 `i` 的证据强度。
- 通过后验期望效用或信息价值选择下一步动作。只有当预期收益超过成本 `c_i` 时，控制器才调用另一个智能体；否则它可以停止、询问、弃答或升级。
- 当观测模型设定错误，或重复调用产生相关证据时，使用再校准、似然调节、考虑依赖关系的证据合并和升级。
- 论文用多智能体代码生成/测试、多智能体假设讨论，以及基于已学习能力参数的跨任务路由来说明这一思路。

## 结果
- 论文报告了 0 个实验、0 个数据集和 0 项实证基准比较。它是一篇立场论文，因此没有声称测得准确率、通过率、成本或延迟增益。
- 它声称的主要结果是一个设计论点：贝叶斯控制可以用于 1 个编排层，不需要将 LLM 参数贝叶斯化。
- 它列出实用贝叶斯控制的 7 项期望属性：成本和效用建模、低开销决策、紧凑的交互历史、人类-AI 和多智能体集成、类型化软件接口、多模态输入，以及简单的用户控制。
- 它给出 3 个具体设计示例：代码生成测试、假设审议和跨任务能力路由。
- 在代码示例中，控制器管理 `n` 个智能体、一个二元任务结果 `Y ∈ {0,1}`、每个智能体的成本 `c_i`、可靠性权重 `α_i`，以及 Equation (1) 中的信念更新。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.00742v2](https://arxiv.org/abs/2605.00742v2)
