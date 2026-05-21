---
kind: ideas
granularity: day
period_start: '2026-05-14T00:00:00'
period_end: '2026-05-15T00:00:00'
run_id: materialize-outputs
status: succeeded
topics:
- coding agents
- software engineering
- agent safety
- open-ended coding
- sandbox infrastructure
- RAG
- program synthesis
tags:
- recoleta/ideas
- topic/coding-agents
- topic/software-engineering
- topic/agent-safety
- topic/open-ended-coding
- topic/sandbox-infrastructure
- topic/rag
- topic/program-synthesis
language_code: zh-CN
---

# 代码智能体验证控制

## Summary
代码智能体工作正在收敛到团队现在就能构建和测试的运营控制：用于发布和质量判定的沙盒服务、用于 shell 访问和技能的逐任务权限关卡，以及具备可度量检索和文档质量的仓库上下文系统。共同的采用障碍，是在真实工作流约束下完成验证。

## 用于代码智能体发布和 CI 质量判定的 Kubernetes 沙盒服务
训练或评估软件工程智能体的团队，应把执行环境和智能体运行框架分开。一个小型 Kubernetes 服务可以负责沙盒创建、命令执行、文件 I/O、网络策略、销毁和日志，然后通过稳定 API 把这些操作提供给训练运行、评测和内部试点。

Orchard 展示了这一层的形态：它在运行时向任务容器注入轻量执行智能体，避免在重复命令中走较慢的 Kubernetes exec 路径，并报告了 0.280 秒的平均命令延迟。同一个环境服务支持软件工程、浏览器使用和生产力智能体任务。对已经为每个领域维护独立运行框架的团队来说，这一点有实际价值。

当沙盒能提供可执行的质量判定信号时，采用理由最强：单元测试、编译器输出、CI 状态、日志和指标。一项涵盖 92 篇研究的综述发现，工业界的智能体使用集中在带有可执行反馈的阶段；一项对 12 家公司的访谈研究发现，更强的实验性智能体难以上生产，因为人工审查仍是主要质量判定路径。一个可行的第一步测试，是把现有代码智能体试点接入沙盒 API，并记录通过率、命令延迟、失败动作轨迹，以及重复运行中的 CI 可复现性。

### Evidence
- [Orchard: An Open-Source Agentic Modeling Framework](../Inbox/2026-05-14--orchard-an-open-source-agentic-modeling-framework.md): Orchard 描述了 Kubernetes 原生环境服务、沙盒生命周期操作、延迟结果和 SWE-bench Verified 结果。
- [Orchard: An Open-Source Agentic Modeling Framework](../Inbox/2026-05-14--orchard-an-open-source-agentic-modeling-framework.md): 该论文报告了 Orchard-SWE 在 SFT 和 RL 后的结果，并描述了通过重复沙盒交互进行智能体训练。
- [Assistance to Autonomy: A Systematic Literature Review of Agentic AI across the Software Development Life Cycle](../Inbox/2026-05-14--assistance-to-autonomy-a-systematic-literature-review-of-agentic-ai-across-the-software-development-life-cycle.md): 这项系统综述把工业采用与可验证的软件阶段和可执行反馈循环联系起来。
- [Agentic AI in Industry: Adoption Level and Deployment Barriers](../Inbox/2026-05-14--agentic-ai-in-industry-adoption-level-and-deployment-barriers.md): 这项访谈研究指出，验证是阻止更强实验性智能体进入实际工作流的主要障碍。

## 代码智能体获得 shell 访问前的逐任务读取、写入和执行策略
代码智能体部署需要在智能体接触代码仓库或终端之前加入权限预检步骤。该步骤应为请求的任务生成路径级读取、写入和执行 allowlist，审查每个授权条目是否有任务依据以及是否暴露敏感内容，然后在沙盒中按该策略运行智能体。

AuthBench 给团队提供了具体评估模式。在敏感任务上，完全访问权限达到 94.0% 的任务成功率，同时攻击成功率为 65.8%。人工审查的黄金权限达到 81.7% 的任务成功率，攻击成功率为 0.0%。生成的策略仍有暴露：Gemini 3.1 Pro 在敏感任务上达到 85.8% 的任务成功率，攻击成功率为 28.3%。

同一个关卡也应覆盖第三方技能。Semantic Compliance Hijacking 把恶意意图藏在自然语言技能说明中，使智能体在正常工作中写入并运行有害代码。在报告的测试中，纯文本操纵技能在论文引用的扫描器下检测率为 0.00%，而完整泄露和远程代码执行的成功率在各项测试配置中都较高。一个有用的内部检查，是建立一套小型红队仓库任务，包含密钥、良性技能、投毒技能和预期 allowlist，并按任务成功率和攻击成功率评分。

### Evidence
- [Do Coding Agents Understand Least-Privilege Authorization?](../Inbox/2026-05-14--do-coding-agents-understand-least-privilege-authorization.md): AuthBench 定义了权限边界推断，并报告了完全访问、黄金权限和生成策略下的任务成功率与攻击成功率。
- [Do Coding Agents Understand Least-Privilege Authorization?](../Inbox/2026-05-14--do-coding-agents-understand-least-privilege-authorization.md): 该论文把最小权限授权表述为具备 shell、代码仓库和文件访问能力的智能体的部署要求。
- [Exploiting LLM Agent Supply Chains via Payload-less Skills](../Inbox/2026-05-14--exploiting-llm-agent-supply-chains-via-payload-less-skills.md): 这篇技能供应链论文描述了 SCH、其攻击设置、泄露和 RCE 成功率范围，以及扫描器检测结果。
- [Exploiting LLM Agent Supply Chains via Payload-less Skills](../Inbox/2026-05-14--exploiting-llm-agent-supply-chains-via-payload-less-skills.md): 该内容片段报告了机密性和 RCE 的峰值成功率，以及被操纵技能文件的 0.00% 检测率。

## 用检索器对比测试和依赖顺序文档评估代码智能体的仓库上下文
开发者工具团队可以把代码仓库上下文作为可度量的子系统来提升代码智能体可靠性。先针对智能体实际执行的任务做检索器对比测试：缺陷修复、代码摘要和代码生成。把 BM25 作为基线，比较 dense retrieval 和 hybrid retrieval，并跟踪检索到的文件是否支持最终补丁或回答。

这项 RAG 研究把查询处理、检索、上下文精炼和生成分开，然后在 Python 软件任务上测试这些部分。其主要实证结论是，检索器选择对最终质量的影响往往大于生成器选择，并且 BM25 在测试任务中仍有竞争力。对把主要精力放在更换模型、却没有度量检索的团队来说，这个发现有用。

文档也可以纳入同一上下文层。MemDocAgent 按依赖顺序生成仓库文档，把先前论断保存在记忆中，验证一致性，并存储已接受文档供后续步骤使用。在 20 个 Python 仓库上，GPT-5-mini 运行生成了 3,323 份文档，完整性得分 0.958，真实性得分 0.952，帮助性得分 0.800。一个可行的上线方式，是先为一个服务构建文档，基于近期 issue 或 pull request 运行检索评估，并检查智能体补丁是否引用了人工审查者认为相关的文件和文档。

### Evidence
- [Not All RAGs Are Created Equal: A Component-Wise Empirical Study for Software Engineering Tasks](../Inbox/2026-05-14--not-all-rags-are-created-equal-a-component-wise-empirical-study-for-software-engineering-tasks.md): 这项 RAG 研究比较了流水线组件，并报告称在软件任务中，检索器侧选择往往比生成器选择更重要。
- [Not All RAGs Are Created Equal: A Component-Wise Empirical Study for Software Engineering Tasks](../Inbox/2026-05-14--not-all-rags-are-created-equal-a-component-wise-empirical-study-for-software-engineering-tasks.md): 该论文描述了覆盖查询处理、检索、上下文精炼和生成器的组件级 RAG 评估。
- [Remember Your Trace: Memory-Guided Long-Horizon Agentic Framework for Consistent and Hierarchical Repository-Level Code Documentation](../Inbox/2026-05-14--remember-your-trace-memory-guided-long-horizon-agentic-framework-for-consistent-and-hierarchical-repository-level-code-documentation.md): MemDocAgent 报告了按依赖顺序生成仓库文档、记忆、验证和总体文档质量得分。
- [Remember Your Trace: Memory-Guided Long-Horizon Agentic Framework for Consistent and Hierarchical Repository-Level Code Documentation](../Inbox/2026-05-14--remember-your-trace-memory-guided-long-horizon-agentic-framework-for-consistent-and-hierarchical-repository-level-code-documentation.md): 该内容片段说明了仓库文档如何作为上下文，帮助人类开发者和代码智能体浏览大型代码库。
