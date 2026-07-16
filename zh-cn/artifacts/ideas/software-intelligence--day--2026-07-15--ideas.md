---
kind: ideas
granularity: day
period_start: '2026-07-15T00:00:00'
period_end: '2026-07-16T00:00:00'
run_id: materialize-outputs
status: succeeded
topics:
- agent evaluation
- coding agents
- software security
- agent governance
tags:
- recoleta/ideas
- topic/agent-evaluation
- topic/coding-agents
- topic/software-security
- topic/agent-governance
language_code: zh-CN
---

# 结合交互历史与可执行证据的智能体发布检查

## 摘要
智能体评估应保留那些会改变行为的交互条件；安全和拉取请求工作流则应将有后果的操作绑定到可检查的证据和范围狭窄的授权上。近期最有用的改进包括：测试工具适应能力的发布检查、由证据门控的安全发现，以及围绕当前编码智能体使用中常见的单维护者工作流设计的轻量级授权收据。

## 持久智能体会话中的工具故障转移发布测试
使用冗余 API 的智能体平台团队应将无提示后端切换加入发布测试，并在每个受支持的 harness 上运行这些测试。AgentCompass 表明，改变 harness 可能使同一模型的 SWE-bench-Pro 得分相差数个百分点，并暴露不同的轨迹故障。set-shifting 基准揭示了另一项运行风险：在持久会话中可靠性发生变化后，即使存在等效的可用工具，智能体仍可能锁定在过时的工具例程上。因此，发布报告应包含按模型和 harness 划分的矩阵，记录切换后的工具调用占比、任务完成率、重复调用次数和恢复延迟，而不只是汇总任务成功率。成本最低的检查方式，是重放一小组接近生产环境的会话，在中途无提示地使首选后端失效，并与新会话对照组比较恢复情况；这可以判断损失是由会话历史还是后端故障本身造成的。

### 资料来源
- [AgentCompass: A Unified Evaluation Infrastructure for Agent Capabilities](../Inbox/2026-07-15--agentcompass-a-unified-evaluation-infrastructure-for-agent-capabilities.md): 在 SWE-bench-Pro 上，Claude-Opus-4.8 使用 Mini-SWE-agent 时得分为 66.21，使用 OpenHands 时为 73.87；轨迹分析还识别出重复调用和空输出等可由 harness 暴露的故障模式。
- [Set-shifting Behavioral Test for Harnessed Agents](../Inbox/2026-07-15--set-shifting-behavioral-test-for-harnessed-agents.md): 在隐藏的可靠性切换中，智能体会形成重复的工具例程；报告的累计 set-shifting 准确率范围为 mimo-v2.5 的 0.02 至 0.33，以及 deepseek-v4-pro 的 0.17 至 0.82。

## 带证据门控并选择性升级至沙箱的仓库安全发现
应用安全团队应避免让自动化仓库发现直接阻止合并，除非其声称的漏洞机制得到代码路径、配置、注册表记录或沙箱跟踪的支持。DREA 通过由假设引导的仓库探索提升了漏洞检测能力，但在评估的系统中，26–55% 的真阳性预测存在有缺陷的理由。ProfMalPlus 提供了一种实用的升级模式：先使用静态行为图和保留源代码结构的切片，只有在判断仍无法确定时，才请求注册表补充信息或沙箱证据。应用于拉取请求扫描时，检测器可以先输出临时假设，收集能够证伪该假设的最低成本证据，并将生成的切片或跟踪结果附加到审查中。首先可以对当前真阳性告警样本重新标注机制是否正确，并衡量经过专家审查后，有多少原本会阻止合并的发现失去支持。

### 资料来源
- [DREA: Decoupled Reasoning and Exploration Agents for Repository-Level Vulnerability Detection](../Inbox/2026-07-15--drea-decoupled-reasoning-and-exploration-agents-for-repository-level-vulnerability-detection.md): DREA 将 DeepSeek-V3.2 的成对正确率从 19% 提升至 42%，并将超过 93% 的 token 转移给其他组件；但各系统中有 26–55% 的真阳性预测由有缺陷的理由支持。
- [ProfMalPlus: Agent-Coordinated Detection of Malicious NPM Packages via Static-Dynamic Analysis Synergy](../Inbox/2026-07-15--profmalplus-agent-coordinated-detection-of-malicious-npm-packages-via-static-dynamic-analysis-synergy.md): ProfMalPlus 会将无法确定的判断路由至注册表补充信息或沙箱执行，并报告了 98.1% 的 F1，以及 88.9% 的行级定位 F1。

## 面向编码智能体拉取请求的具体操作授权收据
代码托管服务商应在占主导地位的单人编码智能体工作流中测试范围狭窄、针对具体操作的授权，而不是一开始就启用组织范围的自主权限。在所观察的 GitHub 样本中，88.7% 的智能体拉取请求工作流涉及一名人类，仓库的中位数产出是在三个月内创建一到两个智能体拉取请求。EBAE 为这一场景提供了具体的执行规则：智能体可以提出操作，但只有当一次性证书、策略、新鲜度状态和确切意图在同一 epoch 内保持一致时，受保护的执行器才会放行该操作。GitHub App 可以将维护者的批准转换为短期收据，并将其限制在一个仓库、一个分支、一个提交范围，以及创建拉取请求或重新运行 CI 等具体操作内。由于 EBAE 没有定量评估，首个有用的测试应关注运行效果：在低流量仓库中，将审批时间、被拒绝的过期操作数量和维护者覆盖操作次数，与现有 GitHub App 权限流程进行比较。

### 资料来源
- [Early Adoption of Agentic Coding Tools by GitHub Projects](../Inbox/2026-07-15--early-adoption-of-agentic-coding-tools-by-github-projects.md): 在 2,361 个仓库中，项目中位数在三个月内产生一到两个智能体拉取请求；单人工作流占观察案例的 88.7%。
- [EBAE: A protocol for bounding the real-world authority of autonomous agents](../Inbox/2026-07-15--ebae-a-protocol-for-bounding-the-real-world-authority-of-autonomous-agents.md): EBAE 将提议与受保护执行分离，并要求针对具体操作的一次性授权，以及一致的策略、新鲜度和防回滚状态；所提供的证据未报告定量评估。
