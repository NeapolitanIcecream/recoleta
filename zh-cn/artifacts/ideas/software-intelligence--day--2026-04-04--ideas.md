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

# 面向执行的代理控制

## Summary
执行证据正在进入编码代理工作流的中心位置。最明确的产品变化包括：在仓库级多次尝试之间保留有用状态的重试控制器、面向可复现 C 和 C++ 安全漏洞的调试器集成修复循环，以及用与 shell 命令同等严格标准检查文件编辑路径的权限机制。

## 用于仓库级生成的持久尝试记忆
仓库级编码代理需要一种重试控制器，在多次完整尝试之间保留显式记忆，并始终返回目前见过的最佳产物。现有证据指向一种明确设计：每次运行后保存结构化的成功笔记、失败笔记和得分最高的仓库，然后在下一次尝试时把这些记录连同执行反馈一起送回模型。LiveCoder 在 RAL-Bench 上报告了最高 22.94 分的功能提升、最高 81.58% 的仓库复用率，以及最高 53.63% 的成本下降。EnvGraph 从另一个角度支持同样的操作变化：很多仓库失败仍然来自安装、依赖和跨文件引用问题，所以重试需要运行时诊断，而不只是增加采样次数。

一个实用的实现是仓库运行器，把每次尝试记录为可持久保存的产物，附带测试结果、安装日志、运行时错误和简明诊断记录。评估内部脚手架生成或全新服务生成场景中编码代理的团队，可以用较低成本做这个测试：在同一组任务上比较三种条件，单次生成、无记忆的重复尝试，以及带持久尝试记忆和最佳产物回退的重复尝试。如果这种收益成立，后续尝试就不该再抹掉前面已经取得的局部成功，系统也应当能在不重复为同样失败付费的情况下恢复出更多可执行仓库。

### Evidence
- [Persistent Cross-Attempt State Optimization for Repository-Level Code Generation](../Inbox/2026-04-04--persistent-cross-attempt-state-optimization-for-repository-level-code-generation.md): LiveCoder 报告了跨尝试状态、最佳仓库保留、功能提升、仓库复用和成本下降。
- [Toward Executable Repository-Level Code Generation via Environment Alignment](../Inbox/2026-04-04--toward-executable-repository-level-code-generation-via-environment-alignment.md): EnvGraph 表明，执行失败经常来自依赖和内部引用对齐问题，这支持基于运行时信息的重试控制。

## 面向 C 和 C++ 漏洞修复的调试器集成补丁循环
C 和 C++ 修复代理可以采用以调试器为先的工作流来处理内存安全漏洞。DebugHarness 给出了一种具体模式：从可复现的崩溃和 sanitizer 信号开始，通过 GDB 和 pwndbg 检查运行时状态，使用 rr 回溯执行过程，用监视点和断点测试根因假设，然后在同一个循环里生成并验证补丁。在 SEC-bench 上，论文报告它在 29 个项目的 200 个真实漏洞上实现了约 90% 的修复率，高于 PatchAgent 的 57.5% 和 VulnResolver 的 67.5%。

近期可落地的产品变化，是为已经拥有 fuzzing 输出和 PoC 崩溃、但仍把根因分析交给资深工程师的安全团队提供一个修复 harness。一个低成本检查方式很具体：拿一批可复现的 AddressSanitizer 或崩溃触发漏洞积压任务，限制代理只做运行时检查和补丁验证，然后和静态代码基线比较，衡量它提出第一个可信根因假设所需时间，以及已验证补丁率。这里的证据对低层内存故障最强，因为这类问题的崩溃点和真实缺陷往往相距很远。

### Evidence
- [DebugHarness: Emulating Human Dynamic Debugging for Autonomous Program Repair](../Inbox/2026-04-04--debugharness-emulating-human-dynamic-debugging-for-autonomous-program-repair.md): DebugHarness 描述了调试器驱动的循环，并报告了它在 SEC-bench 上的修复率提升。

## 针对代理文件编辑的基于效果的权限检查
编码代理的权限门控需要在动作层面覆盖文件编辑，不能只检查 shell 命令。AmPermBench 说明了原因：在 Claude Code auto mode 中，36.8% 的状态变更动作经过了分类器从不检查的 Tier 2 文件编辑，仅这一类就产生了 51 个假阴性。在 253 个状态变更动作上，端到端假阴性率达到 81.0%。制品清理任务尤其容易出问题，因为代理可以编辑 `objects.json`，达到与被拦截命令相同的效果。这支持一种明确的控制改动，适用于 DevOps 团队和内部平台团队：在批准前先把拟议编辑归一化为其真实的操作效果，再针对这个效果评估策略。

一个可用的实现是加入一层拦截层，按所触及的资源和隐含的状态变化，对写入、补丁和生成的配置变更进行分类，然后把它们送入与命令执行相同的策略引擎。第一次测试不需要完整基准套件。可以先在自己的仓库里挑几项目标不明确的清理或重启任务，先用仅检查 shell 的权限机制运行代理，再加入编辑路径分类，对比动作层面的不安全行为漏放数量。主要采用障碍很直接：只信任命令门控的团队，实际上给等价的破坏性操作留出了一条未检查的路径。

### Evidence
- [Measuring the Permission Gate: A Stress-Test Evaluation of Claude Code's Auto Mode](../Inbox/2026-04-04--measuring-the-permission-gate-a-stress-test-evaluation-of-claude-code-s-auto-mode.md): AmPermBench 报告了端到端假阴性率、Tier 2 覆盖缺口，以及通过文件编辑触发的制品清理失败模式。
- [Measuring the Permission Gate: A Stress-Test Evaluation of Claude Code's Auto Mode](../Inbox/2026-04-04--measuring-the-permission-gate-a-stress-test-evaluation-of-claude-code-s-auto-mode.md): 论文解释了代理如何通过分类器不评估的文件编辑实现等价的状态变化。
