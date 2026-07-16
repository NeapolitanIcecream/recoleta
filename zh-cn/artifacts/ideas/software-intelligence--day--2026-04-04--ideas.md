---
kind: ideas
granularity: day
period_start: '2026-04-04T00:00:00'
period_end: '2026-04-05T00:00:00'
run_id: materialize-outputs
status: succeeded
topics:
- coding-agents
- repository-level-generation
- program-repair
- runtime-debugging
- agent-safety
- context-pruning
tags:
- recoleta/ideas
- topic/coding-agents
- topic/repository-level-generation
- topic/program-repair
- topic/runtime-debugging
- topic/agent-safety
- topic/context-pruning
language_code: zh-CN
---

# 执行感知的代理控制

## 摘要
执行证据正在进入编码代理工作流的中心。最清楚的产品变化有三类：保留仓库级尝试中有用状态的重试控制器、用于可复现 C 和 C++ 安全漏洞的调试器集成修复循环，以及以和 shell 命令同样严格程度检查文件编辑路径的权限控制。

## 仓库级生成的持久尝试记忆
仓库级编码代理需要一个重试控制器，在完整尝试之间保留明确记忆，并且始终返回目前最好的产物。现有证据指向一种具体设计：每次运行后存储结构化的成功笔记、失败笔记和当前最高分的仓库，再把这些记录连同执行反馈一起送回下一次尝试。LiveCoder 报告在 RAL-Bench 上功能分数最高提升 22.94 分，仓库复用率最高 81.58%，成本降低最高 53.63%。EnvGraph 从另一个角度支持同样的操作变化：很多仓库失败仍然来自安装、依赖和跨文件引用问题，所以重试需要运行时诊断，而不只是更多采样。

实际做法是一个仓库运行器，把每次尝试都记录成持久产物，包含测试结果、安装日志、运行时错误和一条简短诊断记录。评估内部脚手架或新建服务生成上的编码代理时，可以用同一组任务对比三种情况：一次性生成、不带记忆的重复尝试、带持久尝试记忆并在失败时回退到最佳产物的重复尝试。如果效果真实，后续尝试就不会再抹掉前面的部分成功，系统也能在不重复付出同样失败成本的情况下恢复更多可执行产物。

### 资料来源
- [Persistent Cross-Attempt State Optimization for Repository-Level Code Generation](../Inbox/2026-04-04--persistent-cross-attempt-state-optimization-for-repository-level-code-generation.md): LiveCoder reports cross-attempt state, best-repository retention, functional gains, repository reuse, and cost reduction.
- [Toward Executable Repository-Level Code Generation via Environment Alignment](../Inbox/2026-04-04--toward-executable-repository-level-code-generation-via-environment-alignment.md): EnvGraph shows that execution failures often come from dependency and internal reference alignment, which supports runtime-informed retry control.

## 面向 C 和 C++ 漏洞修复的调试器集成补丁循环
C 和 C++ 修复代理可以把调试器优先的流程用于内存安全漏洞。DebugHarness 给出了一条具体路径：从可复现的崩溃和 sanitizer 信号开始，通过 GDB 和 pwndbg 查看运行时状态，使用 rr 沿执行过程回退，用 watchpoint 和 breakpoint 验证根因假设，然后在同一个循环里生成并验证补丁。在 SEC-bench 上，论文报告对 29 个项目中的 200 个真实漏洞实现了约 90% 的修复率，高于 PatchAgent 的 57.5% 和 VulnResolver 的 67.5%。

近期可落地的产品变化，是给已经有 fuzz 输出和 PoC 崩溃的安全团队做一个修复支架，但把根因分析从高级工程师手里拿回来。一个便宜而直接的检查方法是：拿一批可复现的 AddressSanitizer 或崩溃触发漏洞，限制代理只做运行时检查和补丁验证，再和静态代码基线比较首次提出可行根因假设的时间和已验证补丁率。这里最强的证据来自底层内存错误，尤其是崩溃位置和真实缺陷相距很远的情况。

### 资料来源
- [DebugHarness: Emulating Human Dynamic Debugging for Autonomous Program Repair](../Inbox/2026-04-04--debugharness-emulating-human-dynamic-debugging-for-autonomous-program-repair.md): DebugHarness describes the debugger-driven loop and reports the resolution-rate gains on SEC-bench.

## 基于效果的代理文件编辑权限检查
编码代理的权限门需要覆盖文件编辑动作，而不只是 shell 命令。AmPermBench 说明了原因：在 Claude Code auto mode 中，36.8% 的状态变更动作通过了分类器从未检查的 Tier 2 文件编辑，单这一层就产生了 51 个假阴性。端到端假阴性率在 253 个状态变更动作上达到 81.0%，而 artifact 清理尤其容易出问题，因为代理可以编辑 `objects.json`，达到与被拦截命令相同的效果。这支持 DevOps 和内部平台团队做一项具体控制改动：在批准前先把提议的编辑归一成它真实会造成的运行效果，再按这个效果执行策略判断。

可用的实现方式是一个拦截层，把写入、补丁和生成的配置变更按触达的资源和暗含的状态变化进行分类，然后把它们送进和命令执行相同的策略引擎。第一次测试不需要完整基准。取你自己仓库里几项含糊的清理或重启任务，先只用 shell 级权限检查运行代理，再加入编辑路径分类，按单个动作层面比较未被拦截的安全违规逃逸。主要的落地阻力很直接：只信任命令门控的团队，实际上给等价的破坏性动作留下了一条未检查路径。

### 资料来源
- [Measuring the Permission Gate: A Stress-Test Evaluation of Claude Code's Auto Mode](../Inbox/2026-04-04--measuring-the-permission-gate-a-stress-test-evaluation-of-claude-code-s-auto-mode.md): AmPermBench reports the end-to-end false negative rate, the Tier 2 coverage gap, and the artifact-cleanup failure mode through file edits.
- [Measuring the Permission Gate: A Stress-Test Evaluation of Claude Code's Auto Mode](../Inbox/2026-04-04--measuring-the-permission-gate-a-stress-test-evaluation-of-claude-code-s-auto-mode.md): The paper explains that agents achieve equivalent state changes through file edits that the classifier does not evaluate.
