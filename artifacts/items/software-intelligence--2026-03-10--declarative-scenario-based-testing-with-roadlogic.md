---
source: arxiv
url: http://arxiv.org/abs/2603.09455v1
published_at: '2026-03-10T10:11:09'
authors:
- Ezio Bartocci
- Alessio Gambi
- Felix Gigler
- Cristinel Mateis
- "Dejan Ni\u010Dkovi\u0107"
topics:
- autonomous-driving
- scenario-testing
- declarative-specification
- answer-set-programming
- runtime-monitoring
relevance_score: 0.38
run_id: materialize-outputs
---

# Declarative Scenario-based Testing with RoadLogic

## Summary
本文提出 **RoadLogic**，把声明式的 OpenSCENARIO DSL（OS2）自动转成可执行且可验证的自动驾驶仿真。它试图补上“高层场景规范”到“具体仿真实例”之间缺少开源系统化落地工具的空白。

## Problem
- 现有自动驾驶场景测试多依赖命令式场景编写，开发者需要手工枚举大量变体，覆盖率差、成本高。
- OS2 这类声明式语言能更简洁地描述“想要什么场景”，但缺少把规范系统化实例化为具体仿真的开源方法。
- 这很重要，因为自动驾驶需要在大量、稀有且安全关键的交通情境中做可重复、可扩展的仿真验证。

## Approach
- 先把 OS2 场景翻译成**符号自动机**，用状态和带约束的转移来表示顺序、并行、择一以及空间/关系约束。
- 再把这个自动机编码成 **Answer Set Programming (ASP)** 规划问题，让求解器生成满足场景约束的**高层离散计划**。
- 然后把高层计划细化成每个车辆的**waypoints/轨迹目标**，交给 **FrenetiX** 运动规划器在 **CommonRoad** 中生成物理可行仿真。
- 最后用从同一符号自动机生成的**基于规范的监控器**检查执行轨迹，只保留符合原始 OS2 语义的仿真结果。

## Results
- 论文宣称 **RoadLogic 是首个开源框架**，可将 OS2 声明式规范自动实例化为“现实且满足规范”的仿真。
- 在 **CommonRoad** 上对“多种代表性/多样化 OS2 逻辑场景”进行了评估，并结合 **clingo** 与 **FrenetiX** 完成端到端流程。
- 摘要给出的核心结果是：系统能够在**几分钟内（within minutes）**稳定生成**真实感强且满足规范**的仿真。
- 还声称通过**参数采样**能够捕获**多样行为变体**，从而支持更系统的场景化测试。
- 提供的摘录中**没有更细的定量指标**（如成功率、平均耗时、场景数量、与具体基线的数值对比），因此无法报告更完整的数字化比较。

## Link
- [http://arxiv.org/abs/2603.09455v1](http://arxiv.org/abs/2603.09455v1)
