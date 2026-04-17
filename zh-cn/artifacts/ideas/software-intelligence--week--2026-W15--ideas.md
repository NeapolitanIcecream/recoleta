---
kind: ideas
granularity: week
period_start: '2026-04-06T00:00:00'
period_end: '2026-04-13T00:00:00'
run_id: materialize-outputs
status: succeeded
topics:
- coding-agents
- verification
- benchmarks
- security
- repo-scale-evaluation
tags:
- recoleta/ideas
- topic/coding-agents
- topic/verification
- topic/benchmarks
- topic/security
- topic/repo-scale-evaluation
language_code: zh-CN
---

# 面向代理编写代码的验证关卡

## Summary
近期最清晰的产品方向，是把验证放进执行闭环里。一条路径是外部策略层：只有满足可追溯性和测试义务的代理修改才能通过。另一条路径是代码仓库迁移工作流：把翻译后的测试和修复报告当作一等工件。第三条路径是面向 AI 编写代码的安全关卡：在选定的 diff 上证明可利用性，而不是依赖提示词或传统静态扫描器。

## 编码代理写入路径中的外部策略与证明检查
代理在保存代码前必须满足的治理文件，正在成为一类可落地的产品形态，适合那些要求每次变更都具备可追溯性、架构规则和测试证据的团队。Nidus把这条路推进得最远：需求、架构、工作流、追踪关系和证明义务都放在一个工件里，每次变更在持久化前都要经过结构检查和 Z3 校验。明确的用户是受监管或高保障环境中的工程团队，他们已经有 CI、代码评审和政策文档，但当代理工作跨越工单、文档和代码时，仍然会丢失上下文。可构建的产品是一个位于编码代理写入路径中的外部策略与验证层，它用机器可读的违规信息拒绝变更，并保留一份持久记录，说明某次变更为何通过。

一个低成本的验证步骤，是先把它用在一个狭窄工作流上，比如新增一个功能，而这个功能必须包含更新后的测试、关联需求和获批的架构说明。如果工具能拒绝不完整的代理修改，并返回能帮助下一次尝试成功的可执行失败信号，团队就会使用它。如果它只是再产出一份静态检查清单，进展就会停住。这个方向现在有可信度，因为论文报告了一个在 100,000 行系统上的自举部署，每次提交都检查证明义务，其中还有一个具体案例：一次交付因缺少测试文件被拒绝，代理补上缺失的测试文件后才通过。

### Evidence
- [Nidus: Externalized Reasoning for AI-Assisted Engineering](../Inbox/2026-04-06--nidus-externalized-reasoning-for-ai-assisted-engineering.md): 描述了一个治理运行时：变更要经过求解器检查、每次提交都要满足证明义务，并给出了一个因补上缺失测试后才通过的具体被拒变更案例。
- [Nidus: Externalized Reasoning for AI-Assisted Engineering](../Inbox/2026-04-06--nidus-externalized-reasoning-for-ai-assisted-engineering.md): 摘要直接说明了自举部署和外部化约束执行模型。

## 带有测试翻译和修复报告的代码仓库迁移工作流
代码仓库迁移代理需要一个专门的验证闭环，在代码被接受前完成测试翻译、覆盖缺口测量，并把修复报告送回上游。ReCodeAgent给出了这个工作流的具体模板。它先用 Analyzer 和 Planning 阶段梳理仓库结构与依赖关系，再由 Validator 运行翻译后的测试，为未覆盖函数生成额外测试，并把失败信息反馈给 Translator。对于负责大规模内部代码库语言迁移、SDK 重写或框架升级的平台团队，这是一类可以直接构建的产品。

有用的范围比“跨所有语言对的全自动翻译”要窄。可以先从一类迁移开始，在这类迁移中，团队已经清楚目标技术栈，而且更在意行为保持而不是风格绝对一致。早期产品可以把迁移计划、名称映射、翻译后的测试、未覆盖函数和修复闭环作为可审查工件展示出来。证据支持把它看作工作流变化，而不只是基准测试技巧：移除 Validator 会让测试通过率下降 30.3 个百分点，而完整系统在 118 个真实项目上达到 99.4% 的编译成功率和 86.5% 的测试通过率。

### Evidence
- [ReCodeAgent: A Multi-Agent Workflow for Language-agnostic Translation and Validation of Large-scale Repositories](../Inbox/2026-04-08--recodeagent-a-multi-agent-workflow-for-language-agnostic-translation-and-validation-of-large-scale-repositories.md): 给出了多代理工作流，包括翻译后的测试、覆盖缺口检查和修复报告，也提供了显示 Validator 作用的消融结果。
- [ReCodeAgent: A Multi-Agent Workflow for Language-agnostic Translation and Validation of Large-scale Repositories](../Inbox/2026-04-08--recodeagent-a-multi-agent-workflow-for-language-agnostic-translation-and-validation-of-large-scale-repositories.md): 摘要确认了面向大规模项目的仓库级自主翻译与验证。

## 面向安全敏感 AI 代码变更的可利用性关卡
面向 AI 编写代码的安全审查需要一层可利用性检查，而不能只靠提示词加固和静态扫描。Broken by Default 把这个缺口说得很具体：在 3,500 个生成程序中，55.8% 至少包含一个由 COBALT 发现的漏洞，其中 1,055 个发现被 Z3 证明可利用；而在子集测试中，6 个工业工具合起来漏掉了 97.8% 的形式化证明案例。安全提示词只把平均漏洞率降低了 4 个百分点。对于在解析器、认证流程、内存管理或输入处理上使用编码代理的团队，实际可构建的产品是一个关卡：筛出安全敏感 diff，为可能的弱点类别生成证明义务或见证输入，并在可利用性被证明时阻止合并。

这类方案应先用于那些弱点类别已知、漏报代价很高的狭窄表面：C 和 C++ 内存代码、认证处理器、面向 SQL 的请求代码、归档解压路径等。第一版产品不需要做全程序证明。它需要针对一小组常见失效模式证明或证伪可利用性，并把见证附在评审中。论文里的自审结果也给了一个工作流线索：模型在评审模式下有 78.7% 的概率识别出自己生成的易受攻击输出，所以“生成 + 证明审查”的配对路径，比单独信任生成阶段更容易成立。

### Evidence
- [Broken by Default: A Formal Verification Study of Security Vulnerabilities in AI-Generated Code](../Inbox/2026-04-07--broken-by-default-a-formal-verification-study-of-security-vulnerabilities-in-ai-generated-code.md): 报告了核心漏洞率、Z3 证明结果、安全提示词消融、工业工具漏检率，以及自审能力与生成能力之间的不对称。
- [Broken by Default: A Formal Verification Study of Security Vulnerabilities in AI-Generated Code](../Inbox/2026-04-07--broken-by-default-a-formal-verification-study-of-security-vulnerabilities-in-ai-generated-code.md): 论文摘要说明了形式化验证框架和可利用性的关键数字。
