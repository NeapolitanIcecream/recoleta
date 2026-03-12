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
- knowledge-graph
- optimization-modeling
- type-aware-retrieval
- dependency-closure
relevance_score: 0.08
run_id: materialize-outputs
---

# Type-Aware Retrieval-Augmented Generation with Dependency Closure for Solver-Executable Industrial Optimization Modeling

## Summary
本文提出一种面向工业优化建模的类型感知 RAG 方法，通过“依赖闭包”自动补齐变量、参数、索引集和约束所需的最小上下文，从自然语言稳定生成可被求解器执行的代码。核心价值在于减少 LLM 在优化建模中的结构性幻觉，让生成结果从“看起来像代码”变成“真的能编译求解”的模型。

## Problem
- 要解决的问题是：把工业场景中的自然语言需求自动翻译成**可编译、可求解**的优化模型代码，而不是只生成语义上合理但实际不可执行的代码。
- 这很重要，因为工业优化模型中每个约束都必须引用已声明且类型正确的变量、参数和索引；一旦缺声明、类型不一致或依赖不完整，模型就无法被 LINGO/Gurobi/CPLEX 等求解器执行。
- 现有 RAG 多检索非结构化文本片段，缺少“类型一致性”和“依赖闭包”保证，导致 LLM 经常出现结构性幻觉，尤其在约束密集型工业优化任务中更严重。

## Approach
- 构建**类型化知识库/知识图谱**：把论文和求解器代码解析为带类型的知识单元，如 decision-variables、parameters、index-sets、constraints、objective-functions、auxiliary-rules。
- 在图中显式编码数学依赖关系，如 `used_in`、`depends_on`、`aligns_to`，把论文里的概念与代码中的具体符号对齐。
- 对用户自然语言请求做**混合检索**：一方面用向量检索找语义相关背景，另一方面从知识图谱中找到相关种子节点与结构化定义。
- 对目标实体计算**最小依赖闭包**：沿 executability-critical 边做 BFS，只保留让该目标约束/目标函数“定义完整、可执行”所必需的最小符号集合。
- 将类型定义、依赖子图说明和语义片段一起喂给 LLM（文中示例为 WizardCoder-33B），使模型主要负责“翻译成代码”，而不是自行猜测缺失结构。

## Results
- 在电池生产需求响应案例中，方法成功自动生成包含激励收益项与削峰约束的可执行 LINGO 代码；文中称**常规 RAG 基线失败**，无法生成可执行代码。
- 该需求响应模型在**120 秒内收敛到全局最优**；场景设定为 **24 小时 / 144 个 10 分钟时段**，在第 **16–17 小时（时段 91–102）** 要求至少**削减 10 kW**，激励价格为 **0.54 美元/kWh**。
- 在该案例中，最终产量从 **828 降到 786**，减少 **5.1%**；但利润从 **2776.86 美元**提升到 **2780.51 美元**，增加 **0.13%**，说明模型能在生产损失与需求响应收益间取得平衡。
- 论文还声称在柔性作业车间调度（FJSP）案例中，方法**持续生成可编译模型并达到已知最优解**，体现跨领域泛化；同时称**基线方法在所有测试实例中完全失败**。
- 消融实验的核心结论是：**异构知识源整合**与**类型感知依赖闭包**对避免结构性幻觉、保证可执行性是必需的。
- 但在给定摘录中，除电池需求响应案例外，**未提供更完整的 FJSP 数值表格或具体基线指标**。

## Link
- [http://arxiv.org/abs/2603.03180v1](http://arxiv.org/abs/2603.03180v1)
