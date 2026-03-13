---
source: arxiv
url: http://arxiv.org/abs/2603.08806v1
published_at: '2026-03-09T18:04:54'
authors:
- Tzafrir Rehan
topics:
- llm-agents
- prompt-compilation
- behavioral-testing
- mutation-testing
- specification-gaming
relevance_score: 0.08
run_id: materialize-outputs
---

# Test-Driven AI Agent Definition (TDAD): Compiling Tool-Using Agents from Behavioral Specifications

## Summary
TDAD把工具型LLM智能体开发变成“像写软件一样先写测试再编译提示词”的流程，用行为规格自动生成测试，并迭代修改提示词直到通过。它重点解决生产级智能体难以验证、容易回归和被测试投机取巧的问题，并给出带隐藏测试、语义变异测试和规格演化评估的完整方法。

## Problem
- 现有LLM agent开发主要靠手工试错和抽查，**无法系统验证**是否满足工具调用顺序、策略合规、PII保护、确定性输出等行为要求。
- 提示词的小改动会造成**静默回归**，很多问题只在上线后才暴露，这对合规、安全和运维都很重要。
- 如果只针对可见测试优化，系统可能**投机取巧（specification gaming）**：表面通过测试，但真实行为并不正确。

## Approach
- 把agent开发视为“编译”问题：输入是YAML行为规格（工具、策略、决策树、响应契约），输出是编译后的提示词和工具描述。
- 用两个编码agent分工：**TestSmith**先把规格转成可执行测试；**PromptSmith**再根据可见测试失败信息，迭代修改提示词直到通过。
- 为了减少“背题”，TDAD加入三层防投机机制：**可见/隐藏测试拆分**、**语义变异测试**（故意生成有缺陷的提示词变体，看测试能否抓住）、以及**规格从v1到v2演化时的回归安全评估**。
- 它还把**工具描述**当作一等优化对象，并要求agent通过结构化`respond`工具输出，测试直接检查工具调用轨迹和结构化字段，而不是只看自然语言文本。
- 评测基于**SpecSuite-Core**，包含4个深规格化agent任务：SupportOps、DataInsights、IncidentRunbook、ExpenseGuard。

## Results
- 在 **SpecSuite-Core** 的 **24次独立试验**（4个规格 × 2个版本 × 3次）中，TDAD报告 **v1编译成功率 92%**。
- 对成功的 **v1** 运行，平均**隐藏测试通过率（HPR）为 97%**，说明不仅能过可见测试，也有较强泛化到保留测试的能力。
- 对规格演化后的 **v2**，编译成功率降到 **58%**，但论文称多数失败运行也只是**还差 1–2 个可见测试**未过，说明方法在变更需求下仍接近成功。
- **v2** 的平均隐藏测试通过率为 **78%**，低于v1，反映规格演化更难，但仍保留了相当的泛化能力。
- 语义变异测试的**变异分数（MS）为 86%–100%**；另有 **87%** 的变异意图能成功激活，说明测试套件通常能检测常见错误行为。
- 规格演化回归安全分数 **SURS 平均 97%**；论文还给出一些具体案例：如DataInsights在v1有 `HALLUCINATE_NUMBERS` 变异漏检，v2补上了该测试缺口；ExpenseGuard的v2因新增审批阈值规则，编译迭代从 **2次增至5次**。

## Link
- [http://arxiv.org/abs/2603.08806v1](http://arxiv.org/abs/2603.08806v1)
