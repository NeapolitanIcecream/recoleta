---
source: hn
url: https://github.com/manuelschipper/nah/
published_at: '2026-03-11T23:26:25'
authors:
- schipperai
topics:
- ai-safety
- permission-guard
- developer-tools
- context-aware-security
- llm-agent
- policy-enforcement
relevance_score: 0.03
run_id: materialize-outputs
---

# Show HN: A context-aware permission guard for Claude Code

## Summary
nah 是一个面向 Claude Code 的上下文感知权限守卫，用“按实际行为分类”替代简单的按工具 allow/deny。它试图在不完全关闭权限保护的前提下，自动放行安全操作、阻断危险操作，并把模糊情况交给用户或可选 LLM。

## Problem
- 现有 Claude Code 权限机制主要是按工具做二元 allow/deny，但真实风险取决于**上下文**，同一命令在不同参数、路径、内容下风险差异很大。
- 仅维护 deny list 不可扩展，也容易被模型通过变体、绕行或组合操作规避，导致删除文件、泄露密钥、执行恶意脚本等风险。
- 用户需要一种比 `--dangerously-skip-permissions` 更安全、同时又不频繁打断正常开发流程的权限控制方式。

## Approach
- 在每次工具调用执行前，通过 PreToolUse hook 拦截请求，先用**确定性结构分类器**在毫秒级判断该调用“实际在做什么”，而不是只看工具名。
- 将调用映射到约 20 个内置 action types（如文件删除、git 历史改写、网络访问等），再依据默认或用户自定义策略决定 `allow`、`ask` 或 `block`。
- 对文件读写结合**上下文信息**做判断，例如目标路径是否敏感、写入内容是否像私钥、命令是否包含危险模式（如 `curl ... | sh`、`git push --force`）。
- 对确定性规则无法消解的模糊案例，可选接入 LLM 只处理剩余 `ask` 决策；且 LLM 的权限上限可被限制为不能高于 `ask`。
- 配置采用全局配置 + 项目级 `.nah.yaml` 叠加，其中项目配置只能**收紧**策略、不能放松，降低恶意仓库借配置放行危险命令的风险。

## Results
- 文中未提供正式基准、论文式实验或准确率/误报率等量化结果，因此**没有可核验的定量性能数据**。
- 系统声称对每个工具调用先运行确定性分类，规则执行耗时为**毫秒级**，并覆盖 **20** 个内置 action types。
- 提供一个安全演示：**25** 个实时案例，覆盖 **8** 类威胁（如远程代码执行、数据外泄、混淆命令等），完整演示约 **5 分钟**。
- 给出的定性示例显示其能区分相似但风险不同的操作：如 `git push` 可放行，而 `git push --force` 会询问/阻断；`rm -rf __pycache__` 可允许，而 `rm ~/.bashrc` 会阻断；读取 `./src/app.py` 可允许，而读取 `~/.ssh/id_rsa` 会拒绝或确认。
- 声称“开箱即用、零配置可运行”，同时支持最小化或空白策略模式，以及多家 LLM 提供方级联作为模糊决策后备。

## Link
- [https://github.com/manuelschipper/nah/](https://github.com/manuelschipper/nah/)
