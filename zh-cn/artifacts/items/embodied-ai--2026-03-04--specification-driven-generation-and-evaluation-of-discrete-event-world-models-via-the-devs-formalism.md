---
source: arxiv
url: http://arxiv.org/abs/2603.03784v1
published_at: '2026-03-04T06:50:32'
authors:
- Zheyu Chen
- Zhuohuan Li
- Chuanhao Li
topics:
- world-models
- discrete-event-systems
- devs
- llm-code-generation
- trace-based-verification
relevance_score: 0.6
run_id: materialize-outputs
language_code: zh-CN
---

# Specification-Driven Generation and Evaluation of Discrete-Event World Models via the DEVS Formalism

## Summary
本文提出一种从自然语言规范自动生成**离散事件世界模型**的方法：用 DEVS 形式化把环境写成可执行模拟器，并用基于事件轨迹的规则检查来评估其是否符合规范。其目标是在“手工显式模拟器”和“隐式神经世界模型”之间找到一个更可验证、可调试、且可在线适配的中间方案。

## Problem
- 现有世界模型常处于两端：**手工模拟器**可靠但难适配，**隐式神经模型**灵活但长时程滚动时不易约束、验证和调试。
- 对许多由**事件顺序、时序与因果关系**主导的环境（如队列系统、工作流、消息驱动多智能体、部分具身任务规划），需要一种既显式又可快速生成的世界模型。
- 从自然语言生成这类模型时，**没有唯一代码级真值**，因此传统的参考实现比对或逐步预测准确率不适合作为评价标准。

## Approach
- 采用 **DEVS (Discrete Event System Specification)** 作为世界模型表示：把环境拆成有局部状态、输入输出事件、内部/外部/冲突转移和时间推进函数的原子组件，再用耦合模型连接成层级系统。
- 提出一个**分阶段 LLM 生成流水线**：先做结构综合，推断组件层次、端口模式和交互图；再做行为综合，为每个原子组件生成事件处理与定时代码。
- 通过固定的**接口契约**约束生成结果：模拟器接收外部干预配置/输入流，并输出统一 JSONL 事件轨迹，降低多组件代码生成时的耦合与上下文负担。
- 评价上不要求和某个“标准实现”一致，而是让模拟器输出**结构化事件轨迹**，再检查这些轨迹是否满足从规范导出的时间与语义约束，如先后关系、响应约束、时间边界、安全/守恒性质。
- 一旦违反约束，框架可给出**局部化诊断**，指出违反了哪条规则以及涉及哪些实体/状态变量，便于迭代修正生成的模型。

## Results
- 论文的核心贡献是**方法与框架**：提出“规范驱动生成 + 轨迹驱动验证”的离散事件世界模型方案，目标是获得**长时程一致性、可复现性、可验证性**与**按需快速综合**。
- 文中明确声称生成模型适用于一类由离散事件主导的环境，包括**queueing/service operations、embodied task planning、message-mediated multi-agent coordination** 等，但给定摘录中**没有报告具体实验指标、数据集规模或基线对比数字**。
- 生成流水线被描述为可利用 DEVS 模块化实现**并行生成原子组件**，从而提升在线按需综合的可行性；这是定性主张，摘录中**无生成速度、成功率或消融实验数值**。
- 评估框架能基于事件轨迹进行**可复现验证与局部诊断**，替代代码等价性评测；但摘录中**未提供约束满足率、诊断精度、或与单阶段生成/隐式世界模型的量化比较**。

## Link
- [http://arxiv.org/abs/2603.03784v1](http://arxiv.org/abs/2603.03784v1)
