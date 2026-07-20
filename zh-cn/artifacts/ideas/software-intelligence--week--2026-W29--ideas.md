---
kind: ideas
granularity: week
period_start: '2026-07-13T00:00:00'
period_end: '2026-07-20T00:00:00'
run_id: materialize-outputs
status: succeeded
topics:
- coding agents
- agent evaluation
- software testing
- runtime verification
- repository context
- software security
tags:
- recoleta/ideas
- topic/coding-agents
- topic/agent-evaluation
- topic/software-testing
- topic/runtime-verification
- topic/repository-context
- topic/software-security
language_code: zh-CN
---

# 与验证失败和运行框架变更关联的编码代理控制

## 摘要
可以将仓库探索推迟到验证发现具体知识缺口之后，从而减少不必要的上下文，同时保留深入修复的路径。另一方面，运行框架升级需要配套的安全回归测试，因为交互层的变化可能导致同一个模型对不安全操作的拦截或执行结果发生逆转。

## 由验证触发的仓库问答，用于编码代理修复
编码代理团队应在最小修复未通过验证时触发针对性的仓库问答，而不是在每次编辑前都进行同样广泛的探索。E3 表明，从最小可行执行路径开始，并在验证失败后扩展范围，可以减少冗余工作；ACQUIRE 则表明，围绕仓库机制、依赖关系和契约提出明确问题，可以挽救原本会失败的修复。DiffTestGen 提供了具体的升级信号：通过公共入口针对变更函数运行测试，可以发现无法解释的新旧行为差异，或变更行覆盖率停滞的问题。

一种实际的修复循环可以先估计范围，制作最小的合理补丁，再运行面向变更的测试。测试失败后，将失败转化为面向只读代理的仓库问题；这些带有文件和函数引用的答案随后用于指导下一版补丁。成本最低且有用的评估方式，是在同一组问题上进行消融实验，比较始终启用问答、不启用问答和由验证触发问答三种方案，并测量已解决问题数、令牌数和修复轮次。

### 资料来源
- [Do AI Agents Know When a Task Is Simple? Toward Complexity-Aware Reasoning and Execution](../Inbox/2026-07-14--do-ai-agents-know-when-a-task-is-simple-toward-complexity-aware-reasoning-and-execution.md): E3 在包含 121 个编辑的受控基准测试中保持了 100% 的成功率，同时将令牌数降低了 91%；但其在更广泛部署中的表现尚未得到证实。
- [Know Before Fix: QA-Driven Repository Knowledge Acquisition for Software Issue Resolution](../Inbox/2026-07-13--know-before-fix-qa-driven-repository-knowledge-acquisition-for-software-issue-resolution.md): ACQUIRE 将 SWE-bench Verified 的 Pass@1 提高了 3.8–4.4 个百分点，并在由失败转为成功的案例中将修复轮次减少了 17.1%。
- [DiffTestGen: Change-Directed LLM-Based Testing for Exposing Behavioral Differences](../Inbox/2026-07-17--difftestgen-change-directed-llm-based-testing-for-exposing-behavioral-differences.md): DiffTestGen 使用变更函数、公共入口和联合覆盖率反馈，在 463 个拉取请求中的 78.2% 中发现了行为差异。

## 面向编码代理发布的运行框架替换安全测试
即使模型保持不变，编码代理发布工程师也应将运行框架升级视为与安全相关的行为变化。AgentCompass 发现，运行框架的选择会改变基准分数和轨迹失败模式。在软件包安装实验中，仅替换运行框架，就使一次不可信注册表攻击的拦截结果从 10/10 变为 9/30；另一种变体则朝相反方向变化。因此，模型层面的安全声明不能替代对实际交付的模型–运行框架组合进行测试。

在发布运行框架或权限策略变更之前，应使用同一个模型，在固定的依赖安装攻击和良性对照上运行当前版本与候选版本，然后比较不安全命令是否在执行前被拦截，并检查记录的轨迹。发布凭证应将结果绑定到运行框架版本、工具策略、命令集和源代码状态；Proof-or-Stop 展示了拒绝过时、遭篡改或已重新配置证据的底层机制，但明确没有证明语义正确性。

### 资料来源
- [AgentCompass: A Unified Evaluation Infrastructure for Agent Capabilities](../Inbox/2026-07-15--agentcompass-a-unified-evaluation-infrastructure-for-agent-capabilities.md): AgentCompass 将基准、运行框架和环境分离开来，并报告了不同运行框架之间的分数和失败模式差异。
- [Setup Complete, Now You Are Compromised: Weaponizing Setup Instructions Against AI Coding Agents](../Inbox/2026-07-16--setup-complete-now-you-are-compromised-weaponizing-setup-instructions-against-ai-coding-agents.md): 在模型保持不变的情况下，替换运行框架改变了不可信注册表场景中的检测结果；确定性的安装前检查弥补了大部分已观察到的差距。
- [Proof-or-Stop: Don't Trust the Agent, Trust the Evidence -- Loop Engineering for Verifiable Evidence-Gated Lifecycle Control](../Inbox/2026-07-16--proof-or-stop-don-t-trust-the-agent-trust-the-evidence-loop-engineering-for-verifiable-evidence-gated-lifecycle-control.md): Proof-or-Stop 将证据绑定到源代码、策略和命令集哈希，并拒绝了测试中的 18 类篡改；但其评估仅使用了一个模型系列和一个自托管语料库。
