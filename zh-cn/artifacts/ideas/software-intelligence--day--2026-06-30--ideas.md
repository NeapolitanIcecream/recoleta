---
kind: ideas
granularity: day
period_start: '2026-06-30T00:00:00'
period_end: '2026-07-01T00:00:00'
run_id: materialize-outputs
status: succeeded
topics:
- coding agents
- software maintenance
- performance engineering
- C-to-Rust migration
- agent governance
- benchmarking
tags:
- recoleta/ideas
- topic/coding-agents
- topic/software-maintenance
- topic/performance-engineering
- topic/c-to-rust-migration
- topic/agent-governance
- topic/benchmarking
language_code: zh-CN
---

# 可审计的代码变更自动化

## Summary
当编码智能体围绕审查者已经信任的工件工作时，采用路径最具体：特性到代码映射、profiler 跟踪、编译器诊断、可复现的计时运行和分阶段审批记录。最适合先尝试的是维护和性能工作流，因为团队可以在不改变整个开发流程的情况下衡量定位质量、补丁接受率、构建成功率或计时改进。

## 用于 C/C++ 内存补丁队列的 profiler 派生静态检查
性能团队可以把一次性的内存排查变成可重复的智能体工作流：加载 profiler 跟踪，让智能体编写带源码示例的反模式报告，生成 Clang Static Analyzer 检查器，并打开带语法检查和回滚点的补丁批次。MOA 在 OpenHarmony 5.0 上报告了这种模式：三个被 profiling 的服务产出了 13 个验证过的反模式，随后合成的检查器在七个服务中发现了 10,067 个低效实例。该系统生成了 769 个优化补丁，专家接受率为 92.5%，并报告了平均堆内存和二进制体积下降。

实际落地形态应是绑定 profiler 证据的补丁队列，避免做成自由发挥的优化机器人。每个拟议变更都应带上跟踪中的症状、发现该实例的静态检查规则、受影响的符号和验证结果。小规模试点可以从一个高内存服务和一个反复出现的分配或复制模式开始，然后衡量资深性能工程师无需重写就接受多少生成补丁。

### Evidence
- [MOA: A Profiling-Guided LLM Framework for Memory-Optimization Automation at Codebase Scale](../Inbox/2026-06-30--moa-a-profiling-guided-llm-framework-for-memory-optimization-automation-at-codebase-scale.md): MOA 摘要给出了从 profiler 到反模式、检查器再到补丁的工作流，OpenHarmony 规模，检测到的低效项，生成的补丁，接受率，以及内存和体积结果。
- [MOA: A Profiling-Guided LLM Framework for Memory-Optimization Automation at Codebase Scale](../Inbox/2026-06-30--moa-a-profiling-guided-llm-framework-for-memory-optimization-automation-at-codebase-scale.md): 论文摘要说明了三智能体设计，并报告了 13 个反模式、超过 10,000 个低效项、769 个补丁、92.5% 的专家接受率和堆内存下降。

## 仓库级智能体编辑前的特性到代码映射
维护不熟悉 Java 仓库的团队可以把特性图作为智能体编辑流程中的第一个工件。FeatX 提取 epic-feature 层级，把特性链接到类、方法或文件，并要求用户先编辑特性列表，再由智能体规划并生成行级 diff。它的 UI 还把特性编辑、映射代码检查、智能体规划和补丁审查分开。

这种流程最适合面向产品的维护工作，因为难点通常是找到受特性变更影响的代码。在 FeatX 的研究中，相比 ChatGPT，NASA-TLX 工作负荷从 12.5 降到 7.4；在 38 个特性编辑提交中，函数级修改定位达到 0.385 F1。团队可以通过重放近期特性提交来测试该工作流，检查特性图是否把审查者指向他们实际修改过的函数，然后要求每个智能体 diff 引用它触及的特性节点和代码实体。

### Evidence
- [FeatX: Editing Software by Editing Features for Repository-Level Code Evolution](../Inbox/2026-06-30--featx-editing-software-by-editing-features-for-repository-level-code-evolution.md): FeatX 摘要描述了特性层级提取、特性到代码的映射、多面板工作流、工作负荷结果和定位指标。
- [FeatX: Editing Software by Editing Features for Repository-Level Code Evolution](../Inbox/2026-06-30--featx-editing-software-by-editing-features-for-repository-level-code-evolution.md): 论文正文解释了缺少特性列表和特性到代码映射造成的缺口，并描述了 FeatX 的层级结构和三阶段 Evolution Agent。

## 用于 C-to-Rust 迁移试点的编译器错误修复模板
C-to-Rust 迁移智能体应保留一张按 Rust 编译器诊断索引的修复表。AdaTrans 把错误码映射到修复模板和 Rust 文档片段，然后运行 `cargo build`，测试翻译后的 Rust，并把输出行为与原始 C 程序比较。修复循环还分别处理语法、所有权、行为和模糊失败，并按错误类型使用不同的采样设置。

近期适用场景是迁移具有清晰输入输出行为的自包含 C 模块，粒度为文件级。AdaTrans 在 104 个算法题上报告了 95.51% 的平均编译通过率、基于 fuzz 测试的 81.09% 平均解题率，以及 1.19% 的 unsafe 文件率。迁移团队可以先对一小组模块记录每个编译器错误、选用的修复模板、构建结果、测试结果和 `unsafe` 使用情况。这份日志能给审查者提供具体依据，用来接受、拒绝或改进每个自动修复。

### Evidence
- [AdaTrans: Automated C to Rust Transformation via Error-Adaptive Repair](../Inbox/2026-06-30--adatrans-automated-c-to-rust-transformation-via-error-adaptive-repair.md): AdaTrans 摘要描述了生成-验证-修复循环、从编译器错误到模板的 RAG、验证管线、错误类别，以及报告的通过率、解题率和 unsafe 率。
- [AdaTrans: Automated C to Rust Transformation via Error-Adaptive Repair](../Inbox/2026-06-30--adatrans-automated-c-to-rust-transformation-via-error-adaptive-repair.md): 摘要报告了受控的文件级设置、多阶段验证管线、104 个问题的评估、编译通过率、解题率和 unsafe 文件率。
