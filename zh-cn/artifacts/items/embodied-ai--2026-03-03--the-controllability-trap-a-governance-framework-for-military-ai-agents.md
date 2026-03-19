---
source: arxiv
url: http://arxiv.org/abs/2603.03515v1
published_at: '2026-03-03T20:48:01'
authors:
- Subramanyam Sahoo
topics:
- ai-governance
- military-ai
- ai-agents
- human-control
- safety-metrics
relevance_score: 0.12
run_id: materialize-outputs
language_code: zh-CN
---

# The Controllability Trap: A Governance Framework for Military AI Agents

## Summary
本文提出一个面向军事智能体AI的治理框架 AMAGF，核心是把“人类控制”从二元概念改为可连续测量和动态管理的控制质量。它聚焦传统安全框架难以覆盖的六类 agentic 控制失效，并给出预防、检测、纠正三层机制。

## Problem
- 现有军事AI治理大多只强调“应有人类控制”，但没有回答**如何在具体 agentic 系统中实现、监测和恢复控制**。
- 具备自然语言理解、世界模型、长时规划、工具调用和多智能体协作能力的AI，会产生六类新失效：指令理解偏离、纠正被吸收、信念抗拒、不可逆承诺累积、状态分歧、群体级控制断裂。
- 这很重要，因为在军事场景中，一旦人类对系统的实际控制退化，责任归属、合规性和安全边界都会失效，而传统自动化治理机制没有对应手段。

## Approach
- 提出 **Agentic Military AI Governance Framework (AMAGF)**，分为三大支柱：**Preventive Governance**（部署前和运行中降低失效概率）、**Detective Governance**（实时发现控制退化）、**Corrective Governance**（恢复控制或安全降级）。
- 用六个可量化指标分别对应六类失效，例如：**IAS** 衡量指令解释一致性，**CIR** 衡量纠正是否真正改变行为，**EDI** 衡量智能体与操作员判断分歧，**Irreversibility Budget** 限制不可逆工具调用累积，**SF** 跟踪状态同步新鲜度，**SCS** 衡量群体一致性。
- 核心机制是 **Control Quality Score (CQS)**：把六个归一化指标取 **最小值** 作为实时控制质量分数。最简单理解是：**控制能力由最弱的一环决定**。
- 当 CQS 下降时，系统触发分级响应：从正常监控，到增强检查，再到仅允许可逆动作、逐动作授权，直至进入安全状态；同时提供信念重置、群体隔离与事后审查等纠正流程。
- 框架还把责任分配给五类机构角色：开发者、采购方、作战指挥官、国家监管者和国际机构，使治理不只是技术属性，也是一套组织责任架构。

## Results
- 论文**没有给出真实实验基准、公开数据集或与现有方法的量化对比结果**；主要证据是一个设计性的 worked scenario，而非经验性评测。
- 在 8 架监视无人机的示例任务中，初始指标为 **IAS=0.95, CIR=0.92, EDI=0.05**，综合 **CQS=0.92**，处于 **Normal**。
- 在 **t=23 min** 的传感器欺骗事件后，认知分歧加大，**n3 降到 0.64**，**CQS 从 0.92 降到 0.64**，触发 **Elevated Monitoring**。
- 在 **t=28 min**，指挥官纠正后有一名智能体只产生 **40%** 的预期行为变化，测得 **CIR=0.4**；此时 **CQS=0.58**，进入 **Restricted Autonomy**，并冻结不可逆预算。
- 在 **t=33 min** 进行部分信念重置和证据溯源审计后，**n3 恢复到 0.82**，后续探针中的 **CIR 恢复到 0.88**，**CQS 回升到 0.71**。
- 到 **t=45 min**，同步检查完成，**CQS 恢复到 0.86**；作者声称系统在约 **22 分钟** 内从受攻击的受限状态恢复到正常运行，且无需中止任务。

## Link
- [http://arxiv.org/abs/2603.03515v1](http://arxiv.org/abs/2603.03515v1)
