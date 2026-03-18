---
kind: ideas
granularity: week
period_start: '2026-03-09T00:00:00+00:00'
period_end: '2026-03-16T00:00:00+00:00'
run_id: 9962d634-8d84-43a0-b716-c93138ff05db
status: succeeded
stream: software_intelligence
topics:
- code-agents
- software-engineering
- evaluation
- mcp
- agent-infrastructure
- safety
tags:
- recoleta/ideas
- topic/code-agents
- topic/software-engineering
- topic/evaluation
- topic/mcp
- topic/agent-infrastructure
- topic/safety
pass_output_id: 58
pass_kind: trend_ideas
upstream_pass_output_id: 56
upstream_pass_kind: trend_synthesis
---

# 代码代理闭环深化，MCP与可验证治理同步升温

## Summary
本周更值得做的机会集中在控制面补齐，而不是再造一个更聪明的代理。证据比较扎实的方向有三类：一是把真实 PR 评测、噪声约束和 MCP 工具筛选结合起来，做代码审查代理的上线决策与路由控制；二是把 MCP 浏览器、人工接管和可验证证据链结合起来，做可审计的授权网页自动化；三是把工具最小暴露与命令执行拦截结合起来，做面向代码或运维代理的执行策略网关。以上想法都直接对应本周新出现或明显升温的能力拼图，且各自都有明确的第一批用户与可执行验证步骤。

## Opportunities

### 面向 PR 审查代理的噪声约束评测与路由控制台
- Kind: tooling_wedge
- Time horizon: near
- User/job: 研发效能团队、平台工程团队；工作是为组织选择、评估并上线代码审查代理，同时控制误报对开发者体验的伤害。

**Thesis.** 可以做一套面向代码审查与 PR 自动化的上线前评估控制台：不是再做一个审查代理，而是帮助平台工程团队在接入多个审查或修复工具时，按 PR 类型、风险等级与噪声容忍度做可配置评测和路由。核心价值是把 CR-Bench 一类有用性和 SNR 指标带入真实采购与灰度流程，再结合 MCP 服务器侧 tool gating，避免所有工具同时暴露给模型。

**Why now.** 以前代码审查代理缺少贴近真实 PR 的统一评测，团队很难知道更高召回是否只是制造更多噪声。现在评测基准和工具选择控制面同时出现，第一次具备了把是否值得上线做成产品化决策流程的条件。

**What changed.** 本周出现的变化不是单一模型更强，而是评测口径开始从结果导向转向过程和可用性导向。CR-Bench 明确把真实 PR、Usefulness Rate 和 SNR 拉进主评估指标；同时 MCP 侧开始允许服务器参与工具筛选，而不是让模型面对全量工具盲选。

**Validation next step.** 选 2 到 3 个现有代码审查代理或内部提示流，在同一批真实 PR 上复现 Usefulness Rate、SNR 与召回率；再为只读审查、风险升级、自动修复建议三类请求分别加上 tool gating，测一周内的误报率、token 成本与开发者采纳率变化。

#### Evidence
- [CR-Bench: Evaluating the Real-World Utility of AI Code Review Agents](../Inbox/2026-03-10--cr-bench-evaluating-the-real-world-utility-of-ai-code-review-agents.md): CR-Bench 显示代码审查代理在真实 PR 中存在明显的召回率—噪声权衡，单看找出多少 bug 会误导采购与上线决策。
- [Giving MCP servers a voice in tool selection](../Inbox/2026-03-15--giving-mcp-servers-a-voice-in-tool-selection.md): _tool_gating 原型说明服务器侧可在每轮工具选择前排除无关工具，已出现 318 tokens/turn 的直接节省，并支持对确定性命令跳过模型。

### 面向授权网页工作流的可审计 MCP 浏览器执行层
- Kind: workflow_shift
- Time horizon: near
- User/job: 财务运营、法务运营、采购运营和需要在 SaaS 后台执行高频网页流程的内部团队；工作是安全地半自动完成登录后操作，并在事后证明做过什么。

**Thesis.** 可以做一个面向合规敏感内部流程的可审计浏览器执行层，服务于财务、法务、采购和运营团队的授权网页操作自动化。重点不是更强的网页代理，而是把 MCP 浏览器会话、人工接管、登录态管理和可验证证据链打包成一条可接审计的执行通道。

**Why now.** 过去企业不愿让代理进入真实网页登录流程，主要不是因为不会点按钮，而是因为登录态、失败接管和审计留痕都不完整。现在执行能力和证据能力在同一周同时补齐，形成了更接近可部署产品的组合。

**What changed.** 浏览器能力不再只是临时外挂到代理框架里，而开始以 MCP 原生服务形式提供，同时加入 human takeover、auth profile、审批闸门和会话持久化。另一边，浏览器执行记录也从普通截图日志升级为可独立验证的签名证据链。

**Validation next step.** 挑选 1 个高频且目前依赖人工登录的内部网页流程，例如供应商门户下载对账单或后台提交合规表单；用现成 MCP 浏览器接入并补 proof bundle，测 20 次任务中的完成率、人工接管率、审计复核时间，以及是否满足内部审计留痕要求。

#### Evidence
- [Auto-Browser – An MCP-native browser agent with human takeover](../Inbox/2026-03-12--auto-browser-an-mcp-native-browser-agent-with-human-takeover.md): Auto-Browser 把浏览器做成 MCP 原生服务，并补上 human takeover、登录态复用、审批和审计，说明授权网页流程开始可接入生产辅助系统。
- [Show HN:Conduit–Headless browser with SHA-256 hash chain - Ed25519 audit trails](../Inbox/2026-03-11--show-hn-conduit-headless-browser-with-sha-256-hash-chain-ed25519-audit-trails.md): Conduit 把浏览器操作写成 SHA-256 哈希链和 Ed25519 签名的 proof bundle，说明浏览器自动化的事后可验证性开始具备可实现方案。

### 面向代码与运维代理的执行策略网关
- Kind: tooling_wedge
- Time horizon: near
- User/job: 平台安全团队、基础设施团队、内部 AI 平台团队；工作是允许代理使用 shell 和内部工具，但要限制提示注入、误调用和高风险命令执行。

**Thesis.** 可以做一层面向代码代理和 DevOps 代理的执行策略网关，统一覆盖工具暴露、命令拦截、审批和回放。它的产品切入点不是泛化安全平台，而是专门服务那些已经给代理开放 shell、脚本或运维工具的团队，帮助他们在不重写代理框架的前提下加上执行层护栏。

**Why now.** 过去很多团队的做法还是靠系统提示和粗粒度沙箱，但一旦代理真的有 shell 权限，这些做法不够。现在已经出现明确的执行层拦截实现与 MCP 侧最小暴露机制，给产品化安全控制留出了清晰接口。

**What changed.** 治理讨论已从 prompt 层下沉到执行层。除了提示注入案例直接暴露出命令执行风险，MCP 侧也开始出现服务器参与工具筛选的机制，说明控制面正在往前和往下同时延伸。

**Validation next step.** 在一个已有的内部代码代理或运维 Copilot 环境中，先接入最小版本：工具白名单、高风险命令 denylist 和人工审批。连续记录两周代理请求，统计被拦截命令类型、误拦截率、人工审批负担，以及与未加网关时相比的事故近失事件数量。

#### Evidence
- [Execwall – firewall to stop ModelScope CVE-2026-2256 (AI agent command injectn)](../Inbox/2026-03-13--execwall-firewall-to-stop-modelscope-cve-2026-2256-ai-agent-command-injectn.md): Execwall 把代理安全边界下沉到命令执行层，针对提示注入后的 OS 命令执行给出 Seccomp-BPF、策略引擎和 namespace 隔离。
- [Giving MCP servers a voice in tool selection](../Inbox/2026-03-15--giving-mcp-servers-a-voice-in-tool-selection.md): _tool_gating 说明 MCP 生态正在从暴露更多工具转向最少暴露什么，可把风险控制前移到工具选择阶段。
