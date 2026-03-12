---
source: arxiv
url: http://arxiv.org/abs/2603.03180v1
published_at: '2026-03-03T17:41:34'
authors:
- Y. Zhong
- R. Huang
- M. Wang
- Z. Guo
- YC. Li
- M. Yu
- Z. Jin
topics:
- retrieval-augmented-generation
- code-generation
- knowledge-graph
- optimization-modeling
- type-aware-retrieval
relevance_score: 0.82
run_id: materialize-outputs
---

# Type-Aware Retrieval-Augmented Generation with Dependency Closure for Solver-Executable Industrial Optimization Modeling

## Summary
本文提出一种面向工业优化建模的类型感知 RAG 方法，通过“最小依赖闭包”保证从自然语言到求解器代码的生成结果可编译、可求解。核心价值是在复杂约束场景下减少 LLM 的结构性幻觉，使生成模型真正可执行。

## Problem
- 要把自然语言需求自动转换成 **solver-executable** 的优化模型代码，但普通 LLM 常产生缺失声明、类型不一致、符号依赖不完整的问题。
- 这类错误在工业优化中很关键，因为变量、参数、索引集、约束和目标函数必须严格匹配，否则模型无法编译或求解。
- 现有 RAG 多检索无类型文本片段，缺少对数学依赖关系的闭包保证，因此难以支持可靠的优化建模自动化。

## Approach
- 构建一个领域专用的**typed knowledge base / knowledge graph**：从学术论文和求解器代码中解析出变量、参数、约束、目标、索引集等 typed entities，并记录 `used_in`、`depends_on`、`aligns_to` 等关系。
- 对用户自然语言请求先做意图识别和实体抽取，再进行**混合检索**：一方面做向量语义检索获取概念背景，另一方面在知识图谱中做结构化检索定位相关符号。
- 对目标实体计算**minimal dependency closure**：沿 `used_in` 和 `depends_on` 边做受限遍历，找到让该目标“定义完整”的最小符号集合。
- 将闭包中的 typed definitions、依赖子图描述和 top-k 语义片段一起送入 LLM；LLM 主要负责“翻译成 LINGO 代码”，而不是自己猜需要哪些符号。
- 还加入轻量验证与纠错检索，以进一步提高可编译性和可求解性。

## Results
- 在锂电池生产需求响应案例中，系统处理 **24 小时、144 个 10 分钟时段** 的调度问题，并为 **第 16–17 小时（时段 91–102）** 自动加入需求响应激励与负荷削减约束；要求最小削减 **10 kW**，激励价格 **0.54 $/kWh**。
- 生成的修改后模型在 **120 秒内收敛到全局最优**，并成功实现事件窗口内削峰，说明生成代码可编译、可求解且具备业务有效性。
- 在该案例中，最终产量从 **828** 降至 **786**，下降 **5.1%**；但利润从 **$2776.86** 提升到 **$2780.51**，提高 **0.13%**，表明系统能够平衡生产损失与需求响应收益。
- 论文声称常规 RAG baseline 在该案例中**无法生成可执行代码**；而本文方法可生成包含激励项与负荷约束的可执行 LINGO 模型。
- 在第二个柔性作业车间调度（FJSP）案例中，作者声称方法**持续生成可编译模型并达到已知最优解**，展示跨领域泛化；但给定摘录中未提供更具体的数值结果或基线对比表。
- 消融实验的核心结论是：**异构知识源整合**与**类型感知依赖闭包**对避免结构性幻觉、保证 executability 是必要的；摘录中未给出具体消融数值。

## Link
- [http://arxiv.org/abs/2603.03180v1](http://arxiv.org/abs/2603.03180v1)
