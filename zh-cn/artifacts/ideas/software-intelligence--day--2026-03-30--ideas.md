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
围绕 LLM 编码系统的三个控制点，已经开始出现更具体的工作：在修复前压缩仓库上下文、在 LLM 调用边界上恢复污点传播和切片分析，以及限制编码代理在开发者机器上能接触到的内容。证据在论文报告了对修复准确率、分析质量或操作流程的可测效果时最强；在安全工具仍处于早期阶段的地方则较弱，但这些方案已经具体到可以在实践中测试。

## 补丁生成前的结构化代码上下文压缩
代码修复栈现在可以在检索和补丁生成之间加入一个专门的上下文压缩阶段。证据指向一个很实用的目标：保留仓库结构，按文件、函数、类头和语句块等单元为代码打分，并让最终提示适配固定的 token 预算。SWEzze 报告称，在 GPT-5.2、DeepSeek-V3.2 和 Qwen3-Coder-Next 上的 SWE-bench Verified 基准中，它实现了约 6x 压缩、51.8% 到 71.3% 的 token 降幅，以及 5.0% 到 9.2% 的修复成功率提升。训练信号也足够具体，可以在更小规模的内部实验中复现：从成功修复里提取最小充分上下文，然后用这些蒸馏出的片段训练一个重排器。

对于已经在运行 issue-resolution 或仓库级修复流程、并且在为大提示付费的团队，这个采用理由很直接。一个低成本的验证方法是回放一小组已解决样本，对比未压缩提示和结构化压缩器，并同时跟踪三个指标：补丁通过率、完成率和提示总 token 数。旁边那篇修复研究给出的提醒也很有用。更好的定位有帮助，但不会消除下游瓶颈。即使系统拿到了 oracle 文件和行范围，在各自原生流程中的成功率仍低于 50%，而固定附加上下文的最佳探针在三系统 Solved@10 并集之外也只多解决了 6 个案例。这说明应把上下文压缩视为一个提升成本效率和聚焦度的运行组件，同时继续分别衡量提示构造和补丁合成的质量。

### Evidence
- [Compressing Code Context for LLM-based Issue Resolution](../Inbox/2026-03-30--compressing-code-context-for-llm-based-issue-resolution.md): 报告了结构化压缩方法、6x 压缩、大幅 token 降低，以及在 SWE-bench Verified 上的修复增益。
- [Beyond Localization: Recoverable Headroom and Residual Frontier in Repository-Level RAG-APR](../Inbox/2026-03-30--beyond-localization-recoverable-headroom-and-residual-frontier-in-repository-level-rag-apr.md): 表明即使定位能力强很多，修复成功率仍然有上限，因此上下文处理和合成仍需单独改进。

## 用于 LLM 调用点的 NL/PL 边界污点分析
安全审查团队可以给构建提示并将模型输出作为 SQL、JSON、shell 命令、文件路径或生成代码来消费的代码，在静态分析中加入一个 NL/PL 边界分析阶段。新论文为这个分析阶段给出了具体形态：在每个 LLM 调用点，为每个占位符标注其信息有多少保留到了输出中，用这些标签决定污点是否跨调用传播，并在占位符被阻断时裁剪反向切片。按论文报告的基准，这个两阶段流程在污点传播预测上达到了 F1 0.923，并在包含不传播占位符的文件中将切片大小平均减少了 15%。

这对应一个真实的操作问题。现有污点分析在模型调用处会断掉，尽管风险模式通常很简单：不可信输入进入提示，程序随后执行返回的产物。论文把这和真实的 prompt-injection 与 sandbox-escape 案例联系了起来。一个务实的第一版可以是面向 Python 或 TypeScript 服务的检查器，标记流向 sink 的模型输出，并在每条发现旁记录占位符到输出的标签。团队可以先在一小块代码上测试，比如 LLM 支持的 SQL 生成或 agent 工具调用，再将告警数量和审查时间与不识别边界的污点规则做对比。

### Evidence
- [Crossing the NL/PL Divide: Information Flow Analysis Across the NL/PL Boundary in LLM-Integrated Code](../Inbox/2026-03-30--crossing-the-nl-pl-divide-information-flow-analysis-across-the-nl-pl-boundary-in-llm-integrated-code.md): 定义了 NL/PL 边界分类法，并报告了污点传播 F1 0.923，以及反向切片缩小 15%。

## 面向编码代理的本地最小权限沙箱
编码代理需要一个位于模型之外、也位于 IDE 之外的最小权限封装层。眼下可做的方案是一个本地沙箱层，从默认拒绝的文件系统、网络和 syscall 权限开始，只授予任务实际需要的路径和操作。greywall 就是这种形态的一个例子：它是单二进制沙箱，带有内置代理配置、理解 shell 结构的命令拦截，以及一种学习模式，可以跟踪文件访问并把结果转成可复用的配置。

安全代码审查中的工作流证据也指向同一个方向。Claude Code 在人工审查者把任务收窄、核验结论并在运行中的上下文里纠正事实错误时是有用的。这是一种可行的审查模式，但它仍然默认工具可以被信任去访问广泛的本地资源。对于开发者机器上的日常使用，沙箱可以补上这个缺口。第一批部署对象是那些在敏感仓库上使用 Claude Code、Cursor、Codex 或 Aider、但没有容器隔离的团队。一个低成本检查方法是在学习得到的配置下跑一轮正常的编辑和测试流程，记录被拦截的动作，并统计其中有多少是无害的过度拦截，有多少是任务确实需要的访问。

### Evidence
- [The Blackwall Between Your AI Agent and Your Filesystem](../Inbox/2026-03-30--the-blackwall-between-your-ai-agent-and-your-filesystem.md): 描述了一种面向编码代理的默认拒绝沙箱，包含文件系统、网络和 syscall 控制，以及学习得到的最小权限配置。
- [Leveling Up Secure Code Reviews with Claude Code](../Inbox/2026-03-30--leveling-up-secure-code-reviews-with-claude-code.md): 展示了一种需要人工核验的编码工作流，模型虽然有用，但至少出现过一次事实错误，因此需要在代理使用外围加上约束。
