---
kind: trend
trend_doc_id: 1567
granularity: day
period_start: '2026-06-18T00:00:00'
period_end: '2026-06-19T00:00:00'
topics:
- coding agents
- software engineering
- agent safety
- code evaluation
- compiler tuning
- benchmarking
run_id: materialize-outputs
aliases:
- recoleta-trend-1567
tags:
- recoleta/trend
- topic/coding-agents
- topic/software-engineering
- topic/agent-safety
- topic/code-evaluation
- topic/compiler-tuning
- topic/benchmarking
language_code: zh-CN
---

# 编码代理需要经过失败测试的指导和带关卡的执行

## 概览
这一时期的编码代理工作由运行证据来判断：用失败来测试仓库指令，用基线测试为拉取请求设关卡，以及用基准暴露语言和项目规模上的差距。Probe-and-Refine、Phoenix 和 Multi-LCB 定下了基调：有用的自动化需要一个执行环境来记录尝试过什么，以及失败发生在哪里。

## 研究发现

### 仓库 issue 代理
仓库上下文正在变成可测试、可编辑、可复用的对象。Probe-and-Refine 先生成仓库指导，运行合成的缺陷修复探针，再把失败信息折回到一份紧凑的指导文件中。在 500 个 SWE-bench Verified 实例上，它报告的平均解决率为 33.0%，相比之下，静态仓库指导为 28.3%，无上下文为 25.5%。增益主要来自更多可评估补丁，这说明更好的指导能帮助代理找到代码库中的正确区域。

Phoenix 把类似的工程思路用于 GitHub issue 解决。它把工作拆给规划器、复现器、编码器、测试器、失败分析器和拉取请求代理。它的测试器会比较干净基线运行和打补丁后的运行，只有在变更没有新增失败测试时才打开拉取请求。在一个经过筛选的 24 任务 SWE-bench Lite 切片上，Phoenix 报告有 18 个任务经 oracle 判定已解决，并且成功运行中没有 PASS_TO_PASS 回归。

#### 资料来源
- [Probe-and-Refine Tuning of Repository Guidance for Coding Agents](../Inbox/2026-06-18--probe-and-refine-tuning-of-repository-guidance-for-coding-agents.md): Probe-and-Refine 方法和 SWE-bench Verified 结果
- [Phoenix: Safe GitHub Issue Resolution via Multi-Agent LLMs](../Inbox/2026-06-18--phoenix-safe-github-issue-resolution-via-multi-agent-llms.md): Phoenix 架构、基线感知测试和 SWE-bench Lite 结果

### 代理安全控制
工具权限现在是可测量的代理失败模式。ToolPrivBench 为每个任务提供低权限和高权限工具，这些工具都能完成任务，因此不必要的高权限选择可以被直接计数。在 11 个模型中，有 6 个模型的过度权限工具使用率超过 30%。Qwen3-8B 达到 64.9%，LLaMA-3.1-8B 达到 55.9%。报告中的示例显示，通用安全调优迁移效果差，这把权限选择指向了独立的训练和评估目标。

面向生产的代理文章也把同一边界具体化。Vercel 的 Eve 把持久会话、沙箱、审批、通道、追踪和评测打包进一个开源 TypeScript 运行时。另一篇生产简报认为，涉及 auth、payments、secrets 和不可信输入的变更，在合并前需要规格说明、测试、威胁建模、审查、审计轨迹和具名的人类负责人。共同要求很简单：代理可以快速行动，敏感变更需要明确关卡。

#### 资料来源
- [When Lower Privileges Suffice: Investigating Over-Privileged Tool Selection in LLM Agents](../Inbox/2026-06-18--when-lower-privileges-suffice-investigating-over-privileged-tool-selection-in-llm-agents.md): ToolPrivBench 设计和过度权限工具选择结果
- [Eve](../Inbox/2026-06-18--eve.md): Eve 生产运行时控制、审批、沙箱、追踪和评测
- [The Line Vibe Coding Can't Cross](../Inbox/2026-06-18--the-line-vibe-coding-can-t-cross.md): 带关卡的 AI 生成代码生产指导

### 更广的代码基准
只看 Python 代码分数，对于当前关于编码能力的主张来说范围太窄。Multi-LCB 把 LiveCodeBench 扩展到 12 种语言，同时保留发布日期过滤和隐藏测试。它报告称，在摘录中 GPT-OSS-120B Medium 的平均成绩最高，为 67.8 Pass@1；Qwen3-235B-A22B-Thinking-2507 在 Python 和 C++ 上得分更高，但在 Rust、Ruby 和 Go 上下降。这个结果让跨语言差异显现出来，而不是被单一 Python 数字遮住。

JAMER 增加了另一项压力测试：Godot 上的项目级游戏代码。它的流程从超过 240,000 个候选仓库中筛到 8,133 个行为有效的项目，然后评估编译成功率、结构完整性和运行时行为。在代码补全任务上，运行时通过率从小项目的 80.4% 降到大项目的 5.7%。代理运行在部分设置中提高了编译和运行时通过率，但论文报告运行时行为质量没有提升。

#### 资料来源
- [Multi-LCB: Extending LiveCodeBench to Multiple Programming Languages](../Inbox/2026-06-18--multi-lcb-extending-livecodebench-to-multiple-programming-languages.md): Multi-LCB 多语言基准设计和 Pass@1 结果
- [JAMER: Project-Level Code Framework Dataset and Benchmark on Professional Game Engines](../Inbox/2026-06-18--jamer-project-level-code-framework-dataset-and-benchmark-on-professional-game-engines.md): JAMER 数据集构建和项目规模基准结果

### 可测量的可靠性和优化循环
可靠性研究正在测试廉价的代理多样性是否能掩盖缺陷。N-version programming 研究在 5 个代理执行环境、23 个模型配置和 3 种语言上生成了 69 个实现。经过验收筛选后，48 个版本在 100 万个随机输入上运行。独立性假设失败了：随机独立预测为 115.36 个共同失败案例，实际出现 429 个。多数投票仍然有帮助，把三版本单元的平均失败数从单版本的 387.44 降到 130.99。

AutoPass 把证据循环模式用于编译器调优。它使用 LLVM 中间表示、优化备注、运行时测量和硬件计数器来修订 pass 流水线。在 64 个工作负载上，三轮版本在论文预算下的 10 个平台-套件设置中有 9 个报告最佳结果；相对于 LLVM -O3，几何平均加速比在 x86-64 上为 1.043×，在 ARM64 上为 1.117×。

#### 资料来源
- [N-Version Programming with Coding Agents](../Inbox/2026-06-18--n-version-programming-with-coding-agents.md): N-version programming 设置、共模失败和多数投票结果
- [AutoPass: Evidence-Guided LLM Agents for Compiler Performance Tuning](../Inbox/2026-06-18--autopass-evidence-guided-llm-agents-for-compiler-performance-tuning.md): AutoPass 证据引导的编译器调优方法和加速结果
