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
SeGa 根据业务需求而不只是代码生成单元测试，用来捕获代码中心型测试生成器容易漏掉的业务逻辑缺陷。它从需求文档中构建结构化的语义条目，检索与目标方法相关的部分，并用这些内容引导基于 LLM 的测试生成。

## 问题
- 论文关注的是**业务逻辑缺陷**：代码违反了预期的产品规则、流程或策略，即使代码本身看起来有效、执行也正常。
- 现有单元测试生成方法大多是**以代码为中心**的。它们关注控制流、类型和执行行为，因此经常漏掉那些与 PRD 中书写的需求相关的缺陷。
- 这在企业软件里很重要，因为很多正确性规则存在于需求文档、团队约定和工作流约束中，而不体现在方法签名或局部代码结构里。

## 方法
- SeGa 首先从产品需求文档中构建**语义知识库**。它把表格和图转换为文本，移除无关的文档内容，并提取**功能项**，把同一业务意图下的相关需求归为一组。
- 它把每个功能项存储为结构化 **DSL**，这样比原始 PRD 文本噪声更少，也更容易检索。
- 对于目标方法，**语义推理代理**会检查该方法及其附近代码，用自然语言总结该方法的预期行为，并用这个总结检索最相关的功能项。
- 然后 SeGa 从检索到的功能项中推导出**业务场景**。每个场景把一条相关需求转成明确的前置条件、触发动作、预期结果和语义约束。
- **测试生成代理**同时使用代码上下文和这些场景来生成单元测试，之后通过编译修复步骤解决构建问题，使测试能在真实代码仓库中运行。

## 结果
- 评估覆盖**4 个工业级 Go 项目**，包含**60 个真实业务逻辑缺陷**。
- SeGa 检测出**29 个缺陷**，而 CHATTESTER 检测出 **7** 个，SymPrompt **7** 个，HITS **6** 个，RATester **4** 个。与这些基于 LLM 的基线相比，SeGa 多发现了 **22 到 25 个缺陷**。
- SeGa 的**精确率为 0.73**，而 CHATTESTER 为 **0.54**，SymPrompt 为 **0.54**，HITS 为 **0.55**，RATester 为 **0.57**。论文称这相当于**26.9% 到 34.3% 的精确率提升**。
- 在**6 个生产仓库**中的部署中，SeGa 发现了**16 个此前未知的业务逻辑缺陷**。开发者确认并修复了这 16 个缺陷。
- 论文还给出了具体的误报来源：推断出的失败场景不合理、需求文档含糊或不完整，以及模型无法看到的团队特定工程约定。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.23509v1](http://arxiv.org/abs/2604.23509v1)
