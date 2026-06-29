---
source: hn
url: https://github.com/Totes-MickGOATs/mcgoats-game-template
published_at: '2026-05-24T22:21:25'
authors:
- lastdong
topics:
- ai-assisted-development
- game-development
- ci-cd
- code-agents
- tdd
- github-automation
relevance_score: 0.78
run_id: materialize-outputs
language_code: zh-CN
---

# Mcgoats AI-powered game development template

## Summary
## 摘要
Mcgoats 是一个 GitHub 模板，用 Claude Code、CI、分支保护、自动合并和 TDD 规则来搭建 AI 辅助的游戏开发。它面向那些希望项目从一开始就带着受控自动化，而不是临时拼接仓库配置的团队。

## 问题
- 新的游戏仓库常常缺少 CI、分支规则、测试习惯和 AI 代理说明，导致合并不安全，项目结构也不一致。
- AI 编码代理需要仓库专用命令、文档、钩子和约束，才能在不绕过审查的情况下完成有用改动。
- 这个模板之所以重要，是因为游戏项目很容易在早期积累构建和工作流债务，尤其是引擎配置、测试和 GitHub 规则放到后面再补时。

## 方法
- Claude Code 里的 `/setup` 流程会引导选择引擎、设置 GitHub、配置分支保护、验证 CI，以及创建第一个特性分支。
- 仓库使用 3 层主分支保护：Claude Code 的 PreToolUse hook、git pre-commit hook，以及 GitHub 分支保护。
- 开发通过基于 worktree 的特性分支、pull request、由 `ready-to-merge` 标签触发的 FIFO squash 自动合并，以及合并后的测试检查来进行。
- 引擎模块会为 Godot、Unity 或 Unreal 复制 CI、lint、hooks、skills 和配置，然后删除 setup 模块。
- 面向 Claude 的文件包括 `CLAUDE.md`、按目录的文档、系统清单、hooks、commands、statusline 支持，以及按需加载的 agent skills。

## 结果
- 文本没有提供基准研究结果；摘要只给出了实现声明和设置功能，没有准确率、生产力或缺陷率数据。
- 这个模板支持 3 个引擎：Godot、Unity 和 Unreal；Godot 支持据称已经用于一个已发售的游戏项目，而 Unity 和 Unreal 只是起始模块。
- 它列出了 3 层主分支保护路径：Claude Code hook、git pre-commit hook 和 GitHub 分支保护。
- 它包含 5 个与引擎无关的 skills，以及按引擎区分的 skills、可复用的 CI workflows、合并后完整测试运行，以及在合并失败时自动创建 issue。
- 版本要求包括 Python 3.14+、Godot 4.x、Unity 2022+ 和 Unreal 5.x。

## Problem

## Approach

## Results

## Link
- [https://github.com/Totes-MickGOATs/mcgoats-game-template](https://github.com/Totes-MickGOATs/mcgoats-game-template)
