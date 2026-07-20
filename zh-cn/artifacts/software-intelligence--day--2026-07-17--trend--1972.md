---
kind: trend
trend_doc_id: 1972
granularity: day
period_start: '2026-07-17T00:00:00'
period_end: '2026-07-18T00:00:00'
topics:
- "\u7F16\u7801\u4EE3\u7406"
- "\u8F6F\u4EF6\u6D4B\u8BD5"
- "\u4EE3\u7406\u6CBB\u7406"
- "\u4EE3\u7801\u5B89\u5168"
run_id: materialize-outputs
aliases:
- recoleta-trend-1972
tags:
- recoleta/trend
- "topic/\u7F16\u7801\u4EE3\u7406"
- "topic/\u8F6F\u4EF6\u6D4B\u8BD5"
- "topic/\u4EE3\u7406\u6CBB\u7406"
- "topic/\u4EE3\u7801\u5B89\u5168"
language_code: zh-CN
---

# 验证正聚焦于真正重要的代码路径

## 概览
近期证据使操作性验证更加精准。DiffTestGen 针对发生变更的行为，而 GapForge 针对未覆盖的编译器区域；两者的表现都优于覆盖范围更广的测试生成基线。治理和安全研究将同一原则延伸到了测试之外，但其中一些结论仍依赖小规模研究或不完整的报告。

## 研究发现

### 面向变更与覆盖缺口的测试
当测试生成以具体的执行目标为锚点时，基于 LLM 的测试正变得更加有效。DiffTestGen 利用调用图、文档和覆盖率反馈来触达修改后的 Python 代码。在 463 个拉取请求中，它发现了其中 78.2% 的行为差异，平均联合覆盖率达到 90.7%。

GapForge 将同样的目标定位逻辑应用于编译器覆盖缺口。它推断触达未覆盖区域所需的程序结构和编译器选项。在 72 小时的运行中，它比 WhiteFox 多覆盖了 24,736 行 GCC 代码和 19,798 行 LLVM 代码，并发现了 12 个编译器故障。这些结果进一步支持了近期关于可执行检查的证据，表明反馈的位置和结构很重要，而不仅仅是是否存在测试循环。

#### 资料来源
- [DiffTestGen: Change-Directed LLM-Based Testing for Exposing Behavioral Differences](../Inbox/2026-07-17--difftestgen-change-directed-llm-based-testing-for-exposing-behavioral-differences.md): 报告了 463 个拉取请求的结果，包括 78.2% 的行为差异发现率和 90.7% 的平均联合覆盖率。
- [GapForge: Directed Compiler Fuzzing via Coverage-Gap Analysis](../Inbox/2026-07-17--gapforge-directed-compiler-fuzzing-via-coverage-gap-analysis.md): 介绍了面向覆盖缺口的目标定位，并报告了相较于 WhiteFox 额外覆盖的 GCC 和 LLVM 代码行数。

### 仓库层面的证据义务
代理控制正被规定为仓库政策，而不是留给临时审查。Agent Governance Manifest 将贡献风险、所需证据、责任归属和维护者审批关卡关联起来。在一项小规模受控评估中，使用这些材料后，风险标签的准确恢复率从 15/37 提升到 37/38；感知到的审查支持度则从七分制的 3.27 提升到 6.14。

一个包含 85 个工程循环的公开库展示了更轻量的实现模式：每个工作流都定义检查项、停止条件和可供审查的产物。这些示例具体明确，但没有提供总体成功率或基线评估。总体而言，这些来源支持流程规范性正在增强这一判断；不过，只有该 manifest 提供了审查收益的受控证据。

#### 资料来源
- [Making Agent-Mediated Contributions Governable: A Project-Level Governance Manifest for Open-Source AI Collaboration](../Inbox/2026-07-17--making-agent-mediated-contributions-governable-a-project-level-governance-manifest-for-open-source-ai-collaboration.md): 报告了风险标签恢复率和感知审查支持度的受控评估结果。
- [Loop Library for Engineers](../Inbox/2026-07-17--loop-library-for-engineers.md): 展示了 85 个包含明确检查、度量和审查步骤的可复用工作流。

### 作为安全边界的提示词与训练代码
安全证据现在将指令和导入的代码都视为可信计算基的一部分。一项由解析器驱动的研究发现，移除提示词中的约束、守卫条件、条件语句或概念绑定，可能会改变开放式大语言模型生成不安全代码的可能性。现有结果没有提供效应量或按模型划分的漏洞率，因此影响程度仍不确定。

《Code-Poisoning Property Inference Attacks》展示了更直接的供应链风险：恶意训练代码可以编码私有数据集属性，之后通过仅标签查询将其提取出来。该论文报告称，在四个数据集、八种架构和 18 个属性上，攻击准确率均为 100%，且没有降低模型准确率。综合来看，这些研究表明，在生成指令和可执行依赖进入自动化工作流之前，应对二者进行审查。

#### 资料来源
- [The Language of Security: How Prompt Syntax Shapes Secure Code Generation in Open LLMs](../Inbox/2026-07-17--the-language-of-security-how-prompt-syntax-shapes-secure-code-generation-in-open-llms.md): 指出句法约束、守卫条件、条件语句和概念绑定会影响不安全代码的生成。
- [Code-Poisoning Property Inference Attacks](../Inbox/2026-07-17--code-poisoning-property-inference-attacks.md): 界定了通过托管仓库和编码代理实施恶意代码供应链攻击的路径。
