---
source: hn
url: https://github.com/OoneBreath/claude-code-project-brain
published_at: '2026-06-02T23:12:59'
authors:
- Slav_fixflex
topics:
- ai-coding
- project-memory
- claude-code
- code-intelligence
- developer-tools
relevance_score: 0.74
run_id: materialize-outputs
language_code: zh-CN
---

# Project Brain – Persistent memory index for AI coding

## Summary
## 总结
Project Brain 是一个 Claude Code 技能，用一个小型 Markdown 索引和链接的详情文件保存项目记忆。它针对的是 AI 编码会话里反复做上下文准备、混淆项目和浪费 token 的问题。

## 问题
- Claude Code 用户常常在每次会话开始时重新解释架构、部署、技术栈、历史和已知坑。
- 长篇的、始终加载的笔记或 README 会浪费上下文，包括用户为常规任务贴入一份 1000 行 README 的情况。
- 多项目并行工作时，模型会把不同仓库里的技术栈、既有决策和已完成工作混在一起。

## 方法
- 这个技能会创建一个 `.project-brain/` 文件夹，其中 `index.md` 是一个小地图，`projects/<project>/<topic>.md` 下放每个项目的主题文件。
- Claude 先读索引，只有在用户问到某个领域时才打开一个链接的主题文件。
- `init` 会根据 `git`、`package.json` 和 `pyproject.toml` 之类的信号检测项目，然后在 `CLAUDE.md` 里加一个指针，让后续会话加载这张地图。
- `verified`、`failed` 和 `in-progress` 这类状态值记录结果，而 `superseded` 备注会保留先前决定，不会把它们覆盖掉。
- `brain-check` 校验器会发现损坏的指针、格式错误的 frontmatter，以及索引和主题之间的状态漂移。

## 结果
- 摘录没有提供基准测试、消融实验、用户研究或可测量的 token 减少数据。
- 声称的 token 收益：只有 `index.md` 会被预先加载，所以每次会话的上下文上限由索引大小决定，而不是整段历史或一份 1000 行 README。
- 声称的回忆收益：离开某个项目 3 个月后，Claude 可以直接使用保存的技术栈、部署、决策、失败尝试和已验证工作，不需要用户再贴一遍上下文。
- 声称的导航行为：像“我们是怎么解决缓存问题的？”这样的问题，应该只通过 1 个索引指针加载 1 个主题文件，而不是读取整个知识库。
- 设置说明：每台机器运行一次 `install.sh`，每个工作区运行一次 `init`，一个 brain 就能在服务器上编目多个项目。

## Problem

## Approach

## Results

## Link
- [https://github.com/OoneBreath/claude-code-project-brain](https://github.com/OoneBreath/claude-code-project-brain)
