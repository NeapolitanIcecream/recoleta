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
本文主张，应把贝叶斯决策规则放到代理式 AI 的编排层，而把 LLM 和工具保持为黑箱预测器。它关注路由、停止、升级和预算选择这些场景，在这些场景中，不确定性、成本和风险决定了最佳动作。

## 问题
- LLM 代理常常要决定调用哪个工具或专家、是否向用户提问、何时停止，以及要花多少算力；token 概率并不能直接对应任务层面的不确定性。
- 这在多步或高风险系统里很重要，因为错误路由、糟糕的停止规则和重复工具调用会浪费预算、增加延迟，或抬高安全风险。
- 把 LLM 本身做成完整的贝叶斯更新器，成本很高，而且即使这样也可能错过对动作选择真正重要的不确定性。

## 方法
- 在 LLM 和工具上方加一个贝叶斯控制器。它跟踪关于潜在任务变量的后验，比如代码是否会通过测试、哪个假设得到更强支持，或者哪个代理更可靠。
- 把每条代理消息或工具输出都视为带噪声的证据。在代码示例中，控制器按 `r_t(y) ∝ r_{t-1}(y) p_i(z_t|y)^{α_i}` 更新，其中 `α_i` 用来削弱来自代理 `i` 的证据。
- 根据后验期望效用或信息价值来选下一步动作。只有当预期收益高于成本 `c_i` 时，控制器才调用另一个代理；否则它可以停止、提问、放弃或升级。
- 当观测模型设定不准，或重复调用产生相关证据时，使用再校准、似然温度调节、考虑依赖关系的证据聚合，以及升级机制。
- 文中用多代理代码生成与测试、多代理假设讨论、以及基于已学能力参数的跨任务路由来说明这个思路。

## 结果
- 文中报告了 0 个实验、0 个数据集和 0 个实证基准比较。它是一篇立场论文，因此没有声称测得的准确率、通过率、成本或延迟提升。
- 它的主要结论是一个设计论点：可以在 1 个编排层应用贝叶斯控制，而不必让 LLM 参数本身变成贝叶斯的。
- 它列出 7 项实用贝叶斯控制应具备的性质：成本和效用建模、低开销决策、紧凑的交互历史、人机与多代理集成、类型化软件接口、多模态输入，以及简单的用户控制。
- 它给出 3 个具体设计例子：代码生成测试、假设讨论、以及跨任务能力路由。
- 在代码示例中，控制器管理 `n` 个代理、一个二元任务结果 `Y ∈ {0,1}`、每个代理的成本 `c_i`、可靠性权重 `α_i`，以及式 (1) 中的信念更新。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.00742v2](https://arxiv.org/abs/2605.00742v2)
