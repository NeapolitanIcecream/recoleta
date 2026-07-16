---
kind: ideas
granularity: day
period_start: '2026-05-23T00:00:00'
period_end: '2026-05-24T00:00:00'
run_id: materialize-outputs
status: succeeded
topics:
- AI coding agents
- enterprise software engineering
- agent guardrails
- device sandboxes
- AI product due diligence
- software supply chain security
tags:
- recoleta/ideas
- topic/ai-coding-agents
- topic/enterprise-software-engineering
- topic/agent-guardrails
- topic/device-sandboxes
- topic/ai-product-due-diligence
- topic/software-supply-chain-security
language_code: zh-CN
---

# AI 工程的生产控制

## 摘要
AI 工程采用正在转向可度量的生产行为和明确的控制面。最值得照搬的是：给编码代理试点做代码保留测量、审查本地代理包的更新路径，以及为小型设备界面做沙箱化应用加载。

## 内部编码代理推广的代码保留遥测
测试编码代理的工程团队可以在试点仪表板里加两个产品指标：完成一次请求需要多少次来回迭代，以及辅助生成的代码在评审和后续修改后是否还保留。Gemini for Google 在大规模数据上报告了这两个指标；一项覆盖 29,000 名开发者的盲测 A/B 研究显示，平均每轮迭代次数减少了 23%，代码保留率提高了约 17%。

实际落地不需要一开始就做定制基础模型。内部试点可以给代理辅助的 pull request 打标签，把聊天或 IDE 会话和评审结果关联起来，并在固定窗口后抽样检查代码保留情况，比如 30 天或 60 天。多语言仓库还需要变更前清单：检查仓库，验证 API 和工具链，核对依赖和安全规则，并标注代理无法运行的检查。The Polyglot Protocol 在这里很适合作为流程模板，尤其因为它明确列出了仓库发现和验证失败，而这些问题团队在代码评审里已经会碰到。

### 资料来源
- [Customizing an LLM for Enterprise Software Engineering](../Inbox/2026-05-23--customizing-an-llm-for-enterprise-software-engineering.md): GfG reports a 29,000-developer blind A/B study with fewer iterations and higher code survival rates.
- [The Polyglot Protocol – senior-engineer guardrails for AI coding agents](../Inbox/2026-05-23--the-polyglot-protocol-senior-engineer-guardrails-for-ai-coding-agents.md): The Polyglot Protocol defines repository discovery, API verification, dependency checks, testing, security review, and final validation for coding agents.

## 带 shell 访问权限的本地 AI 代理包更新路径清单
使用本地编码代理的团队需要一份清单，列出包名、维护者、安装位置，以及能运行 shell 命令的工具权限。GSD 事件暴露了具体失效模式：即使维护者的信任已经崩塌，npm 包仍可能保留发布路径，而代理包可能在开发者机器上以 bash 或 shell 权限运行。

这个工作流程本身很小，安全团队或开发者体验团队这周就能开始做。列出全局安装和项目内的 AI 代理包，检查 `~/.npm/_npx/` 和 `.claude` 里是否有残留，固定批准的包名，并在给代理开放 shell 权限前要求做一次维护者控制审查。对于通过 npm 安装的工具，审查应包含谁能发布、fork 是否改变了更新路径，以及开发者如何删除旧包。这是把供应链审查用到代理工具上，因为一次更新就可能变成本地代码执行路径。

### 资料来源
- [The Crypto Coin was the tell – thoughts on GSD, and it's crypto rugpull](../Inbox/2026-05-23--the-crypto-coin-was-the-tell-thoughts-on-gsd-and-it-s-crypto-rugpull.md): The post identifies retained npm publish access for original GSD packages and the risk created by shell-capable local agents.
- [The Crypto Coin was the tell – thoughts on GSD, and it's crypto rugpull](../Inbox/2026-05-23--the-crypto-coin-was-the-tell-thoughts-on-gsd-and-it-s-crypto-rugpull.md): The post gives concrete cleanup locations and commands, including npm installs, `~/.npm/_npx/`, and `.claude` directories.

## 用于 ESP32 设备原型的沙箱化热加载 Lua 应用
设备团队可以通过公开窄范围驱动 API，并在设备内沙箱里运行生成的 Lua 应用，来测试 AI 生成的微控制器行为。Resident 在 ESP32 上给出了一个具体模式：应用代码通过 websocket 经 Wi-Fi 推送，运行时不需要编译或刷写固件，并且可以使用按钮事件和显示写入等受限能力，同时被阻止访问网络栈等未开放能力。

这适合交互循环必须保持本地响应的原型。作者提到 150 毫秒是界面感觉即时的响应上限，而每次按键都要等云模型时，这个目标很难达到。一个合适的首轮测试，是带屏幕和按钮的小型设备，比如 M5StickS3 风格套件，再加上 Resident 目前还没有公布的两个指标：应用加载延迟，以及多次热加载下的内存占用。安全测试应包括尝试访问被阻止的 API，尤其是网络功能和驱动接口之外的硬件控制。

### 资料来源
- [Resident: Vibe coding firmware (our new sandbox library for ESP32 devices)](../Inbox/2026-05-23--resident-vibe-coding-firmware-our-new-sandbox-library-for-esp32-devices.md): Resident is described as an ESP32 Lua sandbox for hot-loading AI-authored apps without compiling or flashing firmware.
- [Resident: Vibe coding firmware (our new sandbox library for ESP32 devices)](../Inbox/2026-05-23--resident-vibe-coding-firmware-our-new-sandbox-library-for-esp32-devices.md): The source cites 150 ms as the threshold for instant interaction and explains why cloud calls are too slow for live device loops.
- [Resident: Vibe coding firmware (our new sandbox library for ESP32 devices)](../Inbox/2026-05-23--resident-vibe-coding-firmware-our-new-sandbox-library-for-esp32-devices.md): The source describes the safety concern around unrestricted firmware control and motivates sandboxed device code.
