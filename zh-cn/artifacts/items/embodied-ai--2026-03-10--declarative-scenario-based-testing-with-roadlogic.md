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
- openscenario-dsl
- answer-set-programming
- runtime-monitoring
relevance_score: 0.08
run_id: materialize-outputs
language_code: zh-CN
---

# Declarative Scenario-based Testing with RoadLogic

## Summary
本文提出 **RoadLogic**，把声明式的 OpenSCENARIO DSL（OS2）自动转成可执行的自动驾驶仿真，用于系统化场景测试。核心价值是把“描述想测试什么场景”和“如何具体执行仿真”连接起来，并提供开源实现。

## Problem
- 现有自动驾驶场景测试多依赖命令式/操作式场景定义，开发者需要手工枚举大量变体，覆盖率差且成本高。
- OS2 这类声明式语言能高层表达场景意图，但缺少系统化、开源的方法把规范自动实例化为具体且可运行的仿真。
- 这很重要，因为真实道路穷尽测试既昂贵又危险，而仿真测试需要大量**符合规范且多样化**的具体场景实例。

## Approach
- 先把 OS2 场景规格翻译成**符号自动机**，把顺序、并行、分支以及空间/关系约束表示成状态与转移条件。
- 再把该自动机编码成 **Answer Set Programming (ASP)** 规划问题，用求解器生成满足约束的高层离散计划。
- 接着把高层计划细化为各车辆的路点/目标，并交给 **FrenetiX** 运动规划器在 **CommonRoad** 中生成物理可行、避免碰撞的轨迹。
- 最后利用由符号自动机派生的**运行时监控**检查生成的执行轨迹是否满足原始 OS2 规格，只保留合规仿真。
- 简单说：先“逻辑上想出一个满足条件的交通剧本”，再“用运动规划把它开出来”，最后“自动验收是否真的符合原剧本”。

## Results
- 论文声称 **RoadLogic 是首个开源框架**，可将声明式 OS2 规格自动实例化为现实且符合规格的仿真；文中未给出可核验的同类开源基线数值对比。
- 在 **CommonRoad** 框架上评估了多种代表性/多样化 OS2 逻辑场景，并结合 **clingo** 与 **FrenetiX** 完成端到端生成与验证。
- 定性结果称系统能在 **minutes（数分钟）** 内稳定地产生**真实且满足规格**的仿真执行。
- 通过**参数采样**，系统能够覆盖同一抽象场景下的**多样行为变体**；摘录中未提供具体变体数量或覆盖率数字。
- 摘录中**没有详细量化指标**（如成功率、平均生成时间、对比基线提升百分比、数据集规模等），最强的具体主张是：端到端自动化、规格合规、开源、并能在数分钟内生成多样化场景实例。

## Link
- [http://arxiv.org/abs/2603.09455v1](http://arxiv.org/abs/2603.09455v1)
