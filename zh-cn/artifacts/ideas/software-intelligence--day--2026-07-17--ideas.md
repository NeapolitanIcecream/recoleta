---
kind: ideas
granularity: day
period_start: '2026-07-17T00:00:00'
period_end: '2026-07-18T00:00:00'
run_id: materialize-outputs
status: succeeded
topics:
- coding agents
- software testing
- agent governance
- code security
tags:
- recoleta/ideas
- topic/coding-agents
- topic/software-testing
- topic/agent-governance
- topic/code-security
language_code: zh-CN
---

# 面向代理介导软件变更的有针对性证据

## 摘要
仓库政策可以将贡献风险转化为具体、可执行的证据：用于验证行为变更的差分测试、用于安全敏感型提示词的变异测试，以及用于导入机器学习训练代码的隐私探测。实际的共同变化是，依据贡献可能失败的路径选择验证方式，而不是接受通用测试或准确率结果。

## 针对代理编写的拉取请求进行风险触发的差分测试
开源维护者可以在仓库清单中，将每类贡献风险映射为可执行的测试义务。对于普通库变更，代理应识别修改的函数和公共入口，生成变更前后对照测试，并附上观察到的行为差异和联合覆盖率。编译器或工具链变更则可以触发区域级模糊测试，记录到达相关覆盖缺口所需的程序结构和选项。DiffTestGen 在 463 个拉取请求中的 78.2% 发现了行为差异，而 GapForge 通过覆盖缺口定位发现了 12 个编译器故障；Agent Governance Manifest 则单独表明，明确的风险和证据规则提高了审阅者准确恢复风险标签的能力。

具体做法是在清单中加入受影响的执行目标、允许的行为变更、所需的测试模式、覆盖率证据和未解决缺口等字段，同时由维护者保留最终接受决定。一项低成本检查是，按照这套政策重新评估近期由代理编写的拉取请求，并将新发现的行为和审阅耗时与项目当前的通用 CI 证据进行比较。

### 资料来源
- [DiffTestGen: Change-Directed LLM-Based Testing for Exposing Behavioral Differences](../Inbox/2026-07-17--difftestgen-change-directed-llm-based-testing-for-exposing-behavioral-differences.md): DiffTestGen 在 463 个拉取请求中的 78.2% 发现了行为差异，平均联合覆盖率为 90.7%。
- [GapForge: Directed Compiler Fuzzing via Coverage-Gap Analysis](../Inbox/2026-07-17--gapforge-directed-compiler-fuzzing-via-coverage-gap-analysis.md): GapForge 推断未覆盖区域所需的程序结构和编译器选项；与 WhiteFox 相比，它在 GCC 中额外覆盖了 24,736 行，在 LLVM 中额外覆盖了 19,798 行。
- [Making Agent-Mediated Contributions Governable: A Project-Level Governance Manifest for Open-Source AI Collaboration](../Inbox/2026-07-17--making-agent-mediated-contributions-governable-a-project-level-governance-manifest-for-open-source-ai-collaboration.md): 使用 AGM 支持材料后，准确风险标签恢复率从 15/37 提高到 37/38，感知到的审阅支持度从 3.27 提高到 6.14。

## 面向安全敏感型编码代理工作流的提示词变异测试
维护可复用编码代理工作流的安全团队，可以将提示词作为有版本控制的安全控制进行测试。工作流测试应解析每条提示词，每次删除或移动一个防护条件、条件语句、限定词或概念绑定，针对一组固定的安全相关任务生成代码，并在受支持的模型上将 CodeQL 发现结果与未修改提示词的结果进行比较。这相当于对指令本身应用软件变异测试。

这一做法基于两个尚不完整但相互补充的观察：解析器驱动的实验发现，细粒度提示词成分会影响生成不安全代码的可能性；Loop Library 则表明，工程团队已经在将检查和停止条件封装为可复用的自然语言工作流，但该库没有报告总体评估结果。由于所提供的提示词研究没有给出效应量和按模型划分的漏洞率，团队应先在自己的提示词和模型组合上运行这项测试；如果某些子句的变异反复改变 CWE 的出现率，就应将其变为受保护的回归用例，而不是仅作为风格指导。

### 资料来源
- [The Language of Security: How Prompt Syntax Shapes Secure Code Generation in Open LLMs](../Inbox/2026-07-17--the-language-of-security-how-prompt-syntax-shapes-secure-code-generation-in-open-llms.md): 该研究使用安全相关提示词的解析器驱动变体，并报告约束、防护条件、条件语句、概念绑定及其位置会影响生成不安全代码的可能性。
- [Loop Library for Engineers](../Inbox/2026-07-17--loop-library-for-engineers.md): 该公开库包含 85 个带有明确检查和停止条件的可复用循环。

## 针对导入的机器学习训练代码进行成对合成数据隐私探测
审查第三方或代理生成训练代码的机器学习隐私与合规团队，需要设置一道关卡，用于检测隐蔽的数据集属性通道，即使任务准确率保持不变也能发现。应在仓库政策中将导入的训练流水线标记为高风险贡献，然后要求在成对的合成数据集上执行带仪器的清洁室运行；这两个数据集只在一个敏感聚合属性上存在差异。审阅者应检查候选代码是否插入合成样本、是否基于数据集统计量进行分支，然后测试固定的仅标签探针能否可靠区分训练时使用了哪一种数据集属性。

CPPIA 报告称，在四个数据集、八种架构和 18 种属性上，属性推断准确率达到 100%，且没有降低模型准确率，因此普通的准确率和回归检查无法发现该攻击。Agent Governance Manifest 提供了分配风险类别、证据义务和维护者关卡的机制。这项成对运行只能作为筛查测试——论文摘录没有提供按数据集划分的指标和查询次数——但如果能观察到可复现的标签信号，审阅者就有具体依据在使用私有数据前拒绝或隔离该流水线。

### 资料来源
- [Code-Poisoning Property Inference Attacks](../Inbox/2026-07-17--code-poisoning-property-inference-attacks.md): CPPIA 通过托管代码或代理提供的代码植入被污染的训练行为，随后通过仅标签查询提取私有数据集属性。
- [Making Agent-Mediated Contributions Governable: A Project-Level Governance Manifest for Open-Source AI Collaboration](../Inbox/2026-07-17--making-agent-mediated-contributions-governable-a-project-level-governance-manifest-for-open-source-ai-collaboration.md): Agent Governance Manifest 将贡献风险和贡献者证据准备，与维护者的验证关卡及决策权联系起来。
