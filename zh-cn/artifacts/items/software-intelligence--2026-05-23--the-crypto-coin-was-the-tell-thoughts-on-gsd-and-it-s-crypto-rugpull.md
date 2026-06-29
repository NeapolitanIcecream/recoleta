---
source: hn
url: https://vexjoy.com/posts/the-crypto-coin-was-the-tell/
published_at: '2026-05-23T22:13:04'
authors:
- AndyNemmity
topics:
- ai-agent-security
- npm-supply-chain
- code-agents
- claude-code
- developer-tools
relevance_score: 0.64
run_id: materialize-outputs
language_code: zh-CN
---

# The Crypto Coin was the tell – thoughts on GSD, and it's crypto rugpull

## Summary
## 总结
这篇文章提醒用户卸载原始的 Get Shit Done npm 包，因为创建者先发行并抽走了 $GSD 代币，随后消失，但仍保留 npm 发布权限。主要风险来自本地 AI 代理的更新通道，这类代理可以在开发者机器上运行 shell 命令。

## 问题
- 在据称的 rug pull 之后，原始维护者仍然控制着 `get-shit-done-cc` 和 `@gsd-build/sdk` 的发布路径。
- GSD 代理可以获得 shell 和 bash 权限，所以恶意的包更新可能在用户机器上执行代码。
- npm 不会在信任关系破裂时撤销包凭据，社区分支也挡不住继续安装旧包名的用户。

## 方法
- 文章给出了全局 npm 安装、`npx` 使用和本地安装的卸载命令。
- 它建议用户检查 `~/.npm/_npx/` 和 `.claude`，看看是否还留有 GSD 目录。
- 它把仍想保留这套工作流的用户引向 `open-gsd/get-shit-done-redux`，这个版本把原始创建者移出了更新路径。
- 它把 npm 包的信任模式和基于 git 的安装方式作比较，后者让用户在运行前可以查看文件和变更。
- 作者主张使用更小、由用户自己掌控的 Claude Code 配置，基于本地 markdown、脚本和针对工作流的代理文件。

## 结果
- 这段文字没有基准、数据集或模型性能结果；它是一篇事件分析和安全建议文章。
- 具体说法：社区分支 `open-gsd/get-shit-done-redux` 在 $GSD 事件后连夜创建，并完成了审计。
- 具体说法：原始 npm 包在发布时并未被认为有恶意，但原始维护者仍保留发布权限。
- 具体系统细节：作者的 `vexjoy-agent` 配置有 44 个领域专家代理、121 个工作流技能和 77 个生命周期钩子。
- 具体安装细节：作者的配置使用 `git clone`、`cd` 和 `./install.sh`，然后部署到 Claude Code、Codex、Gemini 和 Factory。

## Problem

## Approach

## Results

## Link
- [https://vexjoy.com/posts/the-crypto-coin-was-the-tell/](https://vexjoy.com/posts/the-crypto-coin-was-the-tell/)
