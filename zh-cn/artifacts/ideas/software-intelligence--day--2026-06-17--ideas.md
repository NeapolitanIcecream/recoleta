---
kind: ideas
granularity: day
period_start: '2026-06-17T00:00:00'
period_end: '2026-06-18T00:00:00'
run_id: materialize-outputs
status: succeeded
topics:
- coding agents
- software engineering benchmarks
- security agents
- agent harnesses
- LLM infrastructure
- software architecture
tags:
- recoleta/ideas
- topic/coding-agents
- topic/software-engineering-benchmarks
- topic/security-agents
- topic/agent-harnesses
- topic/llm-infrastructure
- topic/software-architecture
language_code: zh-CN
---

# 关注来源的编码代理评估

## Summary
编码代理工作正在转向几类检查：保留任务来源、区分可见正确性与隐藏安全行为，并把代理推理转化为可执行证据。这些实际改动足够小，可以放进现有评估和安全工作流中测试：让同一个模型通过多个运行框架执行，要求安全专用隐藏测试，要求审计代理写出可证伪断言，并基于截止日期前可用的仓库证据构建面向未来的任务。

## 面向漏洞修复代理的模型加运行框架安全回归测试
安全团队评估编码代理时，应把模型和代理运行框架作为一组来评分。Endor Labs 让 Claude Fable 5 通过 Cursor 重新执行同一组 200 个漏洞修复任务，并与早先的 Claude Code 运行结果比较。经过反作弊和严格测试调整后，Cursor + Fable 5 达到 72.6% FuncPass 和 29.0% SecPass；Claude Code + Fable 5 达到 59.8% FuncPass 和 19.0% SecPass。

工作流变化很具体：保留一组固定的真实漏洞修复任务，让同一个模型通过每个候选 IDE 或 CLI 运行框架执行，并分别报告 FuncPass、SecPass、超时、空补丁和确认作弊。SecPass 的拆分很重要，因为补丁可能通过可见功能测试，但漏洞仍然存在。在 Endor Labs 的比较中，Cursor 独有的 25 个安全胜出案例里有 13 个属于 Claude Code 运行通过了功能测试但未通过隐藏安全测试的情况。

一个低成本采用检查是从组织过去的漏洞修复中抽取 20 个任务。如果同一个模型在 Cursor、Claude Code 和任何内部运行框架上的 SecPass 结果不同，采购和 AppSec 团队得到的购买信号会比只看模型排行榜分数更有用。

### Evidence
- [Claude Fable 5: The harness matters more than the model](../Inbox/2026-06-17--claude-fable-5-the-harness-matters-more-than-the-model.md): 报告同一个 Claude Fable 5 模型在 Cursor 与 Claude Code 下的比较，包括 FuncPass、SecPass、作弊，以及功能测试通过补丁中的安全差距。
- [Claude Fable 5: The harness matters more than the model](../Inbox/2026-06-17--claude-fable-5-the-harness-matters-more-than-the-model.md): 描述基准设置，包括真实项目、每个任务一个补丁、Docker 隔离、FuncPass 和 SecPass。

## 用断言支撑的 LLM 安全审计发现模糊测试
LLM 安全审计代理应在被判断的代码位置，把自己的安全假设写成可执行断言。Code-Augur 采用这种做法：代理构建威胁模型，在认为代码安全时把局部不变量记录为源代码内断言，并把插桩后的程序交给引导式灰盒模糊测试器。断言失败后，要么生成漏洞报告，要么生成代理必须改进的错误规格。

这让安全工程师在代理说某个文件安全后，可以检查一个直接产物。存活下来的断言也可以和审计记录一起保存，之后附近代码变更时，评审人员可以重新测试同一组假设。论文报告称，Code-Augur 在开源项目中发现了 22 个新漏洞；截至论文写作时，其中 16 个已由开发者修复或确认。

首次实现可以针对解析器、图像编解码器、协议处理器和其他输入密集型代码。要求代理只为攻击者可控输入边界和状态转换输出断言，运行现有模糊测试目标或使用一小段模糊测试预算，并在提交漏洞前分诊断言失败。

### Evidence
- [Code-Augur: Agentic Vulnerability Detection via Specification Inference](../Inbox/2026-06-17--code-augur-agentic-vulnerability-detection-via-specification-inference.md): 总结 Code-Augur 的方法：威胁模型、源代码内断言、引导式灰盒模糊测试、分诊，以及报告的开源漏洞结果。
- [Code-Augur: Agentic Vulnerability Detection via Specification Inference](../Inbox/2026-06-17--code-augur-agentic-vulnerability-detection-via-specification-inference.md): 说明 Code-Augur 将局部不变量写入断言，并使用模糊测试器证伪这些假设，同时报告 22 个新漏洞，其中 16 个已修复或确认。

## 面向编码代理基准的预测条件仓库任务
基准维护者可以基于截止日期前可用的仓库信号生成任务，从而减少对公开拉取请求的直接重放。SWE-Future 从快照前的问题、拉取请求、标签、标题和短文本构建证据包，预测任务族，冻结这些预测，然后用后续拉取请求元数据验证。后续补丁用于验证，不用作任务提示或黄金解法。

报告的数据集提供了足够细节，可用于小规模内部试验。在一项覆盖 80 个仓库的回顾性研究中，SWE-Future 在 76 个仓库中生成了 260 个任务族。最终发布集包含 61 个仓库中的 200 个可执行任务，并带有隐藏测试、黄金补丁、验证标签、来源信息和执行日志。错误修复预测的信号最清楚，139 个错误修复任务族中有 89 个与后续工作形成强匹配或相关匹配。

评估负责人可以先在 10 个活跃仓库上试点：冻结一个快照，从更早的问题和 PR 文本生成错误修复和增强任务族，等待一个验证窗口，然后只从匹配后续项目工作的任务族合成可执行任务。由此得到的基准带有来源链和时间边界，比复制公开 issue 和 PR 配对更容易审计。

### Evidence
- [SWE-Future: Forecast-Conditioned Data Synthesis for Future-Oriented Software Engineering Agents](../Inbox/2026-06-17--swe-future-forecast-conditioned-data-synthesis-for-future-oriented-software-engineering-agents.md): 描述 SWE-Future 的快照前证据包、预测验证、隐藏测试、黄金补丁、来源信息、执行日志，以及主要回顾性结果。
- [SWE-Future: Forecast-Conditioned Data Synthesis for Future-Oriented Software Engineering Agents](../Inbox/2026-06-17--swe-future-forecast-conditioned-data-synthesis-for-future-oriented-software-engineering-agents.md): 解释重放公开 GitHub 问题和拉取请求带来的污染问题，并介绍基于预测条件的任务合成。
