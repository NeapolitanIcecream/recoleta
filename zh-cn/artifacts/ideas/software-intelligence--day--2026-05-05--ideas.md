---
kind: ideas
granularity: day
period_start: '2026-05-05T00:00:00'
period_end: '2026-05-06T00:00:00'
run_id: materialize-outputs
status: succeeded
topics:
- coding agents
- software security
- test generation
- multi-agent systems
- code search
- quantum software
tags:
- recoleta/ideas
- topic/coding-agents
- topic/software-security
- topic/test-generation
- topic/multi-agent-systems
- topic/code-search
- topic/quantum-software
language_code: zh-CN
---

# 代理编写 Java 代码的可执行验证

## Summary
可执行测试正在成为代理编写代码的实用控制点。最清晰的流程变化包括：对代理执行的多工单工作做累计安全审查，为依赖分诊生成 JUnit 漏洞证明测试，以及在接受 Java issue 修复前要求先失败后通过的复现测试。

## 面向代理编写的 Jira 工单链的累计 diff 漏洞利用检查
允许编码代理处理普通待办工单的团队，应该对累计 diff 增加安全检查，而不只检查最新工单。MOSAIC-Bench 给出了原因：三个看起来无害的工单可以组合成一个可被利用的应用变更，九个生产级编码代理在分阶段攻击链上的攻击成功率达到 53.3% 到 85.9%，整个基准中只有两次拒绝。

一个可落地的做法是为代理编写的多工单工作增加 CI 任务：在 Docker 中部署变更后的服务，对受影响的攻击面运行确定性的漏洞利用 oracle，并要求第二个审查提示以对抗性安全角色读取完整累计 diff。MOSAIC-Bench 发现，中立审查代理会把 24.8% 经 oracle 确认存在漏洞的累计 diff 当作常规拉取请求批准，而渗透测试人员视角的提示降低了评估子集上的规避率。首批适合采用的场景是高风险 Web 应用工作：代理在多个工单中修改认证、授权、对象映射、反序列化、文件处理或查询构造。

### Evidence
- [MOSAIC-Bench: Measuring Compositional Vulnerability Induction in Coding Agents](../Inbox/2026-05-05--mosaic-bench-measuring-compositional-vulnerability-induction-in-coding-agents.md): MOSAIC-Bench 报告了分阶段的 Jira 风格攻击链、确定性的 Docker 概念验证 oracle、生产级编码代理上的高攻击成功率，以及审查代理的漏报率。
- [MOSAIC-Bench: Measuring Compositional Vulnerability Induction in Coding Agents](../Inbox/2026-05-05--mosaic-bench-measuring-compositional-vulnerability-induction-in-coding-agents.md): 论文报告了审查代理会批准已确认存在漏洞的累计 diff，并且渗透测试人员视角的审查会降低规避率。

## 面向可触达依赖 CVE 的 JUnit 漏洞证明测试
处理依赖告警的 Java 团队，可以要求编码代理生成一个可运行的 JUnit 漏洞证明测试，并把它绑定到应用入口点。PoVSmith 给出了具体做法：找到能触达易受攻击库 API 的应用公共方法，使用易受攻击的 API、CVE 或 issue ID、受影响版本、调用路径和一个示例漏洞利用测试来生成 JUnit 测试，然后用构建和执行日志修复测试。

这对应安全工程师反复遇到的问题：扫描器提示某个库版本受影响，但团队需要证据证明易受攻击的行为可以通过自己的代码触达。在 PoVSmith 对 33 个 Java 应用-库配对的评估中，系统找到了 152 条正确调用路径，141 个生成测试编译成功，并在 84 个案例中触发了漏洞。一个小规模内部试验可以把这个流程用于近期依赖告警，并衡量三个简单结果：调用路径是否正确、测试是否能编译、执行时是否触发漏洞。

### Evidence
- [Generating Proof-of-Vulnerability Tests to Help Enhance the Security of Complex Software](../Inbox/2026-05-05--generating-proof-of-vulnerability-tests-to-help-enhance-the-security-of-complex-software.md): PoVSmith 描述了应用级调用路径搜索、JUnit PoV 生成、基于构建反馈的修复循环，以及 33 个 Java 应用-库配对上的结果。
- [Generating Proof-of-Vulnerability Tests to Help Enhance the Security of Complex Software](../Inbox/2026-05-05--generating-proof-of-vulnerability-tests-to-help-enhance-the-security-of-complex-software.md): 论文报告了 152 个生成测试，其中 84 个测试证明可以通过易受攻击的库发起可行攻击。

## Java issue 修复前的先失败后通过复现测试
Java 维护者可以要求在开始修复 bug 之前，先由代理生成复现测试。这个测试必须在当前有 bug 的代码上失败，并在修复后通过，让审查者获得一个可执行检查，确认问题已被复现并已被移除。

TDD-Bench-Java 和 e-Otter++ 给出了足够具体的流程，企业 Java 仓库可以照此采用：根据 issue 报告定位可能相关的文件和函数，在正确的包和测试目录中创建一个新的 Java 测试类，在旧代码上运行它，读取构建或测试日志，并最多修订 10 轮。在来自 13 个开源仓库的 250 个 Java issue 上，e-Otter++ 使用 Claude-Sonnet-4.5 达到 43.6% 的先失败后通过率，使用 GPT-5.2 达到 46.4%。基于执行结果的精修比初始生成器分别提高 9.4 和 13.6 个百分点，说明构建日志修复是有用的支撑层。

### Evidence
- [Reproduction Test Generation for Java SWE Issues](../Inbox/2026-05-05--reproduction-test-generation-for-java-swe-issues.md): TDD-Bench-Java 定义了 Java issue 的先失败后通过复现测试，并报告了 e-Otter++ 的流程细节和基准结果。
- [Reproduction Test Generation for Java SWE Issues](../Inbox/2026-05-05--reproduction-test-generation-for-java-swe-issues.md): 论文说明复现测试会在当前代码库上失败，并在 issue 被解决后通过。
