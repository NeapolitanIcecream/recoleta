---
kind: trend
trend_doc_id: 617
granularity: day
period_start: '2026-04-23T00:00:00'
period_end: '2026-04-24T00:00:00'
topics:
- coding-agents
- test-generation
- static-analysis
- runtime-verification
- human-oversight
run_id: materialize-outputs
aliases:
- recoleta-trend-617
tags:
- recoleta/trend
- topic/coding-agents
- topic/test-generation
- topic/static-analysis
- topic/runtime-verification
- topic/human-oversight
language_code: zh-CN
---

# 编码代理研究正在收紧对生成与验证的控制

## Overview
当天最强的一批工作通过收窄模型可自由发挥的范围，并加入基于真实行为运行的检查，让 AI 编码更可用。测试生成、静态分析和运行时监控都变得更有结构。共同思路很简单：让模型负责提出方案，把更多安全关键工作交给约束、执行反馈和验证工件。

## Clusters

### 编码代理的控制面
质量控制正作为明确工件嵌入编码代理工作流。`GROUNDING.md`把领域规则当作一等输入，优先级高于项目指令，并要求代理在引用具体规则的情况下拒绝无效请求。在静态分析中，表现最好的方案也限制了自由生成：带类型约束的 JSON 中间表示优于直接编写 CPGQL，也优于带工具调用的代理循环。这两篇论文指出了同一个实际结论：当模型负责解释，而硬约束和确定性代码负责保证有效性时，代理的帮助更大。

#### Evidence
- [Agentic AI-assisted coding offers a unique opportunity to instill epistemic grounding during software development](../Inbox/2026-04-23--agentic-ai-assisted-coding-offers-a-unique-opportunity-to-instill-epistemic-grounding-during-software-development.md): 定义了 GROUNDING.md、它相对其他上下文文件的优先级，以及对无效科学编程请求的定性拒绝行为。
- [Less Is More: Measuring How LLM Involvement affects Chatbot Accuracy in Static Analysis](../Inbox/2026-04-23--less-is-more-measuring-how-llm-involvement-affects-chatbot-accuracy-in-static-analysis.md): 表明在 Joern 查询翻译中，受 schema 约束的 JSON 中间表示优于直接生成查询，也优于代理式工具调用。

### 测试生成更接近真实行为
这一时期的测试工作开始针对普通覆盖率捕捉不到的行为。TestGeneralizer 从一个真实测试出发，推断背后的场景模式，并将其扩展成更多可执行用例；论文报告称，它相对 EvoSuite、gpt-o4-mini 和 ChatTester 有明显提升，并在一项实地研究中有 16 个生成测试被合并。CAT 为 Java 测试生成加入调用链和依赖关系上下文，并报告在 Defects4J 和较新的 GitHub 项目上，其行覆盖率和分支覆盖率都优于 PANTA。PrismaDV 把同样的思路用于数据系统，同时读取下游任务代码和数据集画像，再生成面向任务的数据检查；它在一个基准上提升超过 20 个 F1 点，在另一个基准上提升超过 26 个 F1 点。

#### Evidence
- [Generalizing Test Cases for Comprehensive Test Scenario Coverage](../Inbox/2026-04-23--generalizing-test-cases-for-comprehensive-test-scenario-coverage.md): 面向场景的测试扩展在基准测试中取得提升，并有仓库贡献被接受。
- [Read the Paper, Write the Code: Agentic Reproduction of Social-Science Results](../Inbox/2026-04-23--read-the-paper-write-the-code-agentic-reproduction-of-social-science-results.md): 具备调用链感知的 Java 测试生成在多个基准上比 PANTA 有更好的覆盖率。
- [PrismaDV: Automated Task-Aware Data Unit Test Generation](../Inbox/2026-04-23--prismadv-automated-task-aware-data-unit-test-generation.md): 面向任务的数据单元测试结合代码和数据上下文，并报告了可观的 F1 提升。

### 运行时检查突破测试套件边界
另一个明显方向是从现有测试中推断运行时验证。FlyCatcher 把测试转成项目特定的运行时检查器，结合静态分析和 LLM 合成来跟踪影子状态，并在执行期间捕获无声的语义故障。在来自四个 Java 系统的 400 个测试上，它推断出 334 个检查器，其中 300 个被判定为正确，并且比 T2C 多检测出 5.2 倍的变异体。这让验证在代码生成之后、测试套件运行结束之后仍然保持开启，因此对那些不会导致程序崩溃的故障很有用。

#### Evidence
- [FlyCatcher: Neural Inference of Runtime Checkers from Tests](../Inbox/2026-04-23--flycatcher-neural-inference-of-runtime-checkers-from-tests.md): 运行时检查器推断、影子状态机制，以及相对 T2C 的定量提升。

### 人工监督仍在回路中
还有一条较小的设计线索关注的是：当代理通过软件代替人行动时，人需要什么。HX 这篇文章认为，主要设计要求是可引导性、可审计性和干预点，并给出一个具体例子：代理应向用户显示 78% 的置信度。文章属于概念性讨论，没有基准测试，因此分量不如上面的论文。它仍然是理解这一时期其他工作的一个有用视角：很多更强的论文都在模型输出周围加入了约束、检查点或恢复循环。

#### Evidence
- [HX Is the New UX: Designing for the Harness Experience](../Inbox/2026-04-23--hx-is-the-new-ux-designing-for-the-harness-experience.md): 为面向代理产品设计中的可引导性、透明性、干预和显式置信度展示提供了概念框架。
