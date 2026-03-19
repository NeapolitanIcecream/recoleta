---
source: arxiv
url: http://arxiv.org/abs/2603.10940v1
published_at: '2026-03-11T16:26:20'
authors:
- Joy Saha
- Trey Woodlief
- Sebastian Elbaum
- Matthew B. Dwyer
topics:
- autonomous-driving
- specification-based-testing
- temporal-logic
- scenario-generation
- simulation-testing
relevance_score: 0.34
run_id: materialize-outputs
language_code: zh-CN
---

# STADA: Specification-based Testing for Autonomous Driving Agents

## Summary
STADA 是一个面向自动驾驶代理的基于规格测试生成框架，直接从形式化时序逻辑规格中系统生成满足前置条件的仿真场景。它的目标是比模板、人工或随机方法更全面且更高效地覆盖与安全规则相关的行为空间。

## Problem
- 现有自动驾驶仿真测试通常依赖模板、人工编写或随机生成场景，难以**系统性**覆盖某条安全规格的所有关键前置情形。
- 对形式化安全需求进行验证时，如果测试没有真正触发规格前置条件，就无法有效检查代理是否遵守对应规则。
- 自动驾驶规则同时涉及**空间关系**与**时间演化**，其可能满足方式很多，人工枚举成本高且容易漏掉重要边界行为。

## Approach
- STADA 以 SceneFlow 规格为输入，将安全规则写成 **LTLf 时序逻辑 + RFOL 空间关系**，把“什么场景相关”直接从规格里读出来。
- 它先分析前置条件，把公式中的析取与时序结构拆解为一组彼此不同的**关系图（relational graphs, RGs）**，每个 RG 表示一种满足前置条件的结构化场景配置。
- 然后根据 RG 自动构造初始静态场景，并在仿真地图上为 ego 和 NPC 生成与 RG 一致的可行路径；用 k-shortest paths 加贪心多样化选择，保留更有差异的轨迹。
- 在仿真执行时，ego 由被测自动驾驶系统控制，NPC 由自动驾驶脚本控制，并通过基于纵向距离的动态调速来提高触发规格前置条件的概率。
- 最后用规格监测器评估轨迹，并使用 3 种覆盖指标（细粒度配置覆盖、oneflip 覆盖、二值覆盖）衡量测试是否真正覆盖了规格定义的行为空间。

## Results
- 论文在多种用 SceneFlow 形式化的 **LTLf** 规格上评估 STADA，并使用 **3 个互补覆盖标准**进行比较。
- 在**最细粒度覆盖指标**上，STADA 的覆盖率相比最佳基线达到**超过 2×**。
- 在**最粗粒度覆盖指标**上，STADA 相比最佳基线实现了**75% 的覆盖提升**。
- 在达到与最佳基线**相同覆盖率**时，STADA 只需要**6 倍更少的仿真次数**。
- 实现层面，STADA 基于 **Scenic** 生成初始场景、基于 **Python/CARLA** 生成和执行仿真，并在**两个不同的驾驶代理**上与**三个基线方法**比较。
- 摘要与节选未给出更细的绝对数值（如具体覆盖百分比、每个数据集/规格上的逐项分数），但核心定量主张是更高覆盖和显著更低仿真成本。

## Link
- [http://arxiv.org/abs/2603.10940v1](http://arxiv.org/abs/2603.10940v1)
