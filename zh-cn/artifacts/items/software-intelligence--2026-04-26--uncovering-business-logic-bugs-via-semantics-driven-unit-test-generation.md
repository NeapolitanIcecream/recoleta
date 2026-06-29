---
source: arxiv
url: http://arxiv.org/abs/2604.23509v1
published_at: '2026-04-26T03:06:16'
authors:
- Chen Yang
- Junjie Chen
topics:
- unit-test-generation
- business-logic-bugs
- code-intelligence
- llm-for-software-engineering
- requirements-engineering
relevance_score: 0.9
run_id: materialize-outputs
language_code: zh-CN
---

# Uncovering Business Logic Bugs via Semantics-Driven Unit Test Generation

## Summary
## 摘要
SeGa 从业务需求而不是只从代码生成单元测试，用来捕捉代码中心型测试生成器会漏掉的业务逻辑缺陷。它先从需求文档中构建结构化语义条目，再检索与目标方法相关的部分，并用这些内容引导基于 LLM 的测试生成。

## 问题
- 这篇论文针对的是 **业务逻辑缺陷**：代码违反了预期的产品规则、流程或策略，即使代码看起来有效且能正常执行。
- 现有单元测试生成方法大多 **以代码为中心**。它们关注控制流、类型和执行行为，所以常常会漏掉和 PRD 中需求相关的缺陷。
- 在企业软件里，这个问题很重要，因为很多正确性规则写在需求文档、团队约定和流程约束里，而不是方法签名或局部代码结构中。

## 方法
- SeGa 先从产品需求文档构建一个 **语义知识库**。它把表格和图转成文本，去掉无关内容，并提取出按共同业务意图分组的 **功能项**。
- 它把每个功能项存进结构化 **DSL**，这样需求比原始 PRD 文本更少噪声，也更容易检索。
- 对于一个焦点方法，**语义推理代理** 会检查该方法及其附近代码，用自然语言概括方法的预期行为，再用这个概括去检索最相关的功能项。
- 然后，SeGa 从检索到的功能项中导出 **业务场景**。每个场景会把一条相关需求转成明确的前置条件、触发动作、预期结果和语义约束。
- **测试生成代理** 同时使用代码上下文和这些场景生成单元测试，编译修复步骤会修正构建问题，让测试能在真实仓库中运行。

## 结果
- 评估覆盖 **4 个工业 Go 项目**，包含 **60 个真实业务逻辑缺陷**。
- SeGa 检出 **29 个缺陷**，而 CHATTESTER 检出 **7 个**，SymPrompt 检出 **7 个**，HITS 检出 **6 个**，RATester 检出 **4 个**。这比对比的 LLM 基线多出 **22 到 25 个缺陷**。
- SeGa 的精确率是 **0.73**，而 CHATTESTER 为 **0.54**，SymPrompt 为 **0.54**，HITS 为 **0.55**，RATester 为 **0.57**。论文说明这相当于 **26.9% 到 34.3% 的精确率提升**。
- 在 **6 个生产仓库** 的部署中，SeGa 找到了 **16 个此前未知的业务逻辑缺陷**。开发者确认并修复了这 16 个缺陷。
- 论文还给出了具体的误报来源：推断出的失败场景不合理、需求文档含糊或不完整，以及模型看不到的团队特有工程约定。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.23509v1](http://arxiv.org/abs/2604.23509v1)
