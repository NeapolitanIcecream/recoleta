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

# Executable Validation for Agent-Written Java Code

## Summary
可执行测试正在成为代理编写代码的实际控制点。最清楚的流程变化是：多票据代理工作的累计安全审查、用于依赖分诊的自动生成 JUnit 漏洞证明测试，以及在接受 Java issue 修复前先做 fail-to-pass 复现测试。

## Cumulative-diff exploit checks for agent-authored Jira ticket chains
让编码代理处理普通待办票据的团队，应当对累计 diff 加一道安全检查，而不只是看最新票据。MOSAIC-Bench 说明了原因：三个看起来无害的票据可以组合成一次可利用的应用改动，九个生产级编码代理在分阶段链路上的攻击成功率达到 53.3% 到 85.9%，而整个基准里只有两次拒绝。

一个可落地的版本是给代理编写的多票据工作加一条 CI 作业：把变更后的服务部署到 Docker 中，对受影响面运行确定性的 exploit oracle，再要求第二个审阅提示词读取完整的累计 diff，并采用对抗式安全角色。MOSAIC-Bench 发现，中性审阅代理把 24.8% 经 oracle 确认有漏洞的累计 diff 当作普通 pull request 通过，而按渗透测试者角色审阅后，评测子集上的绕过率下降了。最先适合落地的场景是高风险 Web 应用工作，代理在多个票据里会碰到身份验证、授权、对象映射、反序列化、文件处理或查询构造。

### Evidence
- [MOSAIC-Bench: Measuring Compositional Vulnerability Induction in Coding Agents](../Inbox/2026-05-05--mosaic-bench-measuring-compositional-vulnerability-induction-in-coding-agents.md): MOSAIC-Bench reports staged Jira-style attack chains, deterministic Docker proof-of-concept oracles, high attack success rates across production coding agents, and reviewer-agent miss rates.
- [MOSAIC-Bench: Measuring Compositional Vulnerability Induction in Coding Agents](../Inbox/2026-05-05--mosaic-bench-measuring-compositional-vulnerability-induction-in-coding-agents.md): The paper reports reviewer-agent approval of confirmed vulnerable cumulative diffs and lower evasion under pentester-framed review.

## JUnit proof-of-vulnerability tests for reachable dependency CVEs
处理依赖告警的 Java 团队，可以让编码代理生成一个可运行的 JUnit 漏洞证明测试，绑定到某个应用入口点。PoVSmith 给出了一套具体做法：找到能到达有漏洞库 API 的公开应用方法，生成一个包含漏洞 API、CVE 或 issue ID、受影响版本、调用路径和示例利用测试的 JUnit 测试，然后用构建和执行日志修复测试。

这正对应安全工程师反复遇到的问题：扫描器说某个库版本受影响，但团队需要证据证明漏洞行为能通过自己的代码到达。在 PoVSmith 对 33 对 Java 应用-库组合的评估中，系统找到了 152 条正确调用路径，编译通过了 141 个生成测试，并在 84 个案例中触发了漏洞。一个小规模内部试点可以在最近的依赖告警上跑这套流程，并记录三个简单结果：调用路径正确、测试可编译、执行能触发漏洞。

### Evidence
- [Generating Proof-of-Vulnerability Tests to Help Enhance the Security of Complex Software](../Inbox/2026-05-05--generating-proof-of-vulnerability-tests-to-help-enhance-the-security-of-complex-software.md): PoVSmith describes the application-level call-path search, JUnit PoV generation, build-feedback repair loop, and results across 33 Java application-library pairs.
- [Generating Proof-of-Vulnerability Tests to Help Enhance the Security of Complex Software](../Inbox/2026-05-05--generating-proof-of-vulnerability-tests-to-help-enhance-the-security-of-complex-software.md): The paper reports 152 generated tests and 84 tests that demonstrated feasible attacks through vulnerable libraries.

## Fail-to-pass reproduction tests before Java issue fixes
Java 维护者可以要求在修复 bug 之前先生成一个代理写的复现测试。这个测试必须在当前有问题的代码上失败，在修复后通过，让审阅者用一个可执行检查确认问题被复现并修掉。

TDD-Bench-Java 和 e-Otter++ 把这套流程写得足够具体，企业 Java 仓库可以直接参考：先从 issue 报告里定位可能相关的文件和函数，再在正确的包和测试目录里创建一个新的 Java 测试类，在旧代码上运行它，读取构建或测试日志，并最多迭代 10 次修改。对 13 个开源仓库里的 250 个 Java issue，e-Otter++ 在 Claude-Sonnet-4.5 上达到 43.6% 的 fail-to-pass，在 GPT-5.2 上达到 46.4%。基于执行结果的修正比初始生成器提升了 9.4 和 13.6 个百分点，这说明构建日志修复是有用的支撑层。

### Evidence
- [Reproduction Test Generation for Java SWE Issues](../Inbox/2026-05-05--reproduction-test-generation-for-java-swe-issues.md): TDD-Bench-Java defines fail-to-pass reproduction tests for Java issues and reports e-Otter++ workflow details and benchmark results.
- [Reproduction Test Generation for Java SWE Issues](../Inbox/2026-05-05--reproduction-test-generation-for-java-swe-issues.md): The paper states that reproduction tests fail on the current code base and pass after the issue has been addressed.
