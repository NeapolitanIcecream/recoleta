---
kind: ideas
granularity: day
period_start: '2026-03-30T00:00:00'
period_end: '2026-03-31T00:00:00'
run_id: materialize-outputs
status: succeeded
topics:
- code-repair
- context-compression
- agent-security
- program-analysis
- code-generation
tags:
- recoleta/ideas
- topic/code-repair
- topic/context-compression
- topic/agent-security
- topic/program-analysis
- topic/code-generation
language_code: zh-CN
---

# LLM 编码控制面

## Summary
围绕 LLM 编码系统，三条控制点上的具体工作正在成形：在修复前压缩仓库上下文、在 LLM 调用边界上恢复污点和切片、以及限制编码代理在开发者机器上能碰什么。证据最强的是那些报告了修复准确率、分析质量或操作工作流可测效果的论文；安全工具还处在早期的地方，证据较弱，但已经具体到可以直接测试。

## 补丁生成前的结构化代码上下文压缩
代码修复系统现在可以在检索和补丁生成之间加入专门的上下文压缩阶段。证据指向一个明确的目标：保留仓库结构，把代码按文件、函数、类头、语句块等单位打分，并把最终提示词控制在固定的 token 预算内。SWEzze 报告了大约 6 倍压缩、51.8% 到 71.3% 的 token 减少，以及在 GPT-5.2、DeepSeek-V3.2 和 Qwen3-Coder-Next 上对 SWE-bench Verified 5.0% 到 9.2% 的提升。训练信号也足够具体，可以在更小的内部实验里复现：从可通过测试的修复中提取最小充分上下文，再用这些蒸馏后的片段训练 reranker。

对已经在跑 issue 修复或仓库级修复流程、而且要为大提示词付费的团队来说，落地路径很直接。一个便宜的验证方法是回放一小批已解决样本，把未压缩提示词和结构化压缩器做对比，并同时跟踪三项指标：补丁通过率、完成率和总提示 token。旁边那项修复研究给出的提醒也很有用。更好的定位有帮助，但不会消除下游瓶颈。即使给了 oracle 文件和行范围，系统在原生流水线里仍低于 50% 成功率，而最佳固定附加上下文探针只比三个系统的 Solved@10 并集多解决了 6 个案例。这说明上下文压缩应该被当作一个运营组件，用来降成本和聚焦，同时把提示词构建和补丁生成质量分开衡量。

### Evidence
- [Compressing Code Context for LLM-based Issue Resolution](../Inbox/2026-03-30--compressing-code-context-for-llm-based-issue-resolution.md): Reports the structured compression method, 6x compression, large token cuts, and repair gains on SWE-bench Verified.
- [Beyond Localization: Recoverable Headroom and Residual Frontier in Repository-Level RAG-APR](../Inbox/2026-03-30--beyond-localization-recoverable-headroom-and-residual-frontier-in-repository-level-rag-apr.md): Shows that even with much stronger localization, repair success remains capped, so context handling and synthesis still need separate work.

## LLM 调用点的 NL/PL 边界污点分析
安全审查团队可以在静态分析里加入一个 NL/PL 边界步骤，用来处理构造提示词并把模型输出当作 SQL、JSON、shell 命令、文件路径或生成代码消费的代码。新论文给出了一个具体的分析方式：在每个 LLM 调用点，按信息在输出中保留了多少来给占位符打标签，用这些标签判断跨调用的污点传播，在占位符被阻断时缩小 backward slice。按论文报告的基准，这个两阶段流水线在污点传播上达到 F1 0.923，并且在含有不传播占位符的文件里把 slice 大小平均缩小了 15%。

这对应一个真实的运维问题。现有污点分析会在模型调用处断开，但高风险模式往往很简单：不可信输入进入提示词，程序随后执行返回的产物。论文把这一点和真实的 prompt injection、sandbox escape 案例联系起来。一个实用的第一版实现，是给 Python 或 TypeScript 服务做一个检查器，标记流向 sink 的模型输出，并在每个发现旁记录占位符到输出的标签。团队可以先在很小的一段代码上试，比如基于 LLM 的 SQL 生成或 agent 工具调用，再把告警数量和审查时间与不考虑边界的污点规则做对比。

### Evidence
- [Crossing the NL/PL Divide: Information Flow Analysis Across the NL/PL Boundary in LLM-Integrated Code](../Inbox/2026-03-30--crossing-the-nl-pl-divide-information-flow-analysis-across-the-nl-pl-boundary-in-llm-integrated-code.md): Defines the NL/PL boundary taxonomy and reports F1 0.923 for taint propagation plus 15% smaller backward slices.

## 编码代理的本地最小权限沙箱
编码代理需要一个位于模型外部、也位于 IDE 外部的最小权限包装层。最直接的实现，是先给文件系统、网络和系统调用设置默认拒绝的本地沙箱，再只放行任务实际需要的路径和操作。greywall 就是这种形态的一个例子：它是一个单二进制沙箱，内置代理配置，支持识别 shell 结构的命令拦截，还有一个学习模式，可以跟踪文件访问并把它变成可复用的配置。

安全代码审查里的工作流证据也指向同一方向。Claude Code 在人类审查者把任务范围收窄、核实结论并在运行上下文里纠正事实错误时，确实有用。这样的审查模式可行，但前提还是工具可以拿到很宽的本地权限。沙箱能把这个缺口补上，让它适合在真实开发机器上日常使用。首批部署对象是那些在敏感仓库里使用 Claude Code、Cursor、Codex 或 Aider、但没有容器隔离的团队。一个便宜的检查方法，是在学习到的 profile 下跑一次正常的编辑和测试流程，记录被拦截的动作，再统计其中有多少是无害的过度拦截，多少是真正需要的访问。

### Evidence
- [The Blackwall Between Your AI Agent and Your Filesystem](../Inbox/2026-03-30--the-blackwall-between-your-ai-agent-and-your-filesystem.md): Describes a deny-by-default sandbox for coding agents with filesystem, network, and syscall controls plus learned least-privilege profiles.
- [Leveling Up Secure Code Reviews with Claude Code](../Inbox/2026-03-30--leveling-up-secure-code-reviews-with-claude-code.md): Shows a human-verified coding workflow where the model was useful but made at least one factual error, supporting containment around agent use.
