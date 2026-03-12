---
source: arxiv
url: http://arxiv.org/abs/2603.01596v1
published_at: '2026-03-02T08:26:31'
authors:
- Matthias Kebede
- May Mahmoud
- Mohayeminul Islam
- Sarah Nadi
topics:
- llm-for-code
- ide-plugin
- library-migration
- python
- human-in-the-loop
- developer-tools
relevance_score: 0.86
run_id: materialize-outputs
---

# MigMate: A VS Code Extension for LLM-based Library Migration of Python Projects

## Summary
MigMate 是一个开源 VS Code 插件，把基于 LLM 的 Python 库迁移能力嵌入开发环境，并通过人工确认预览来降低自动迁移的风险。论文重点是工具设计与初步可用性评估，而不是提出全新的底层迁移算法。

## Problem
- Python 项目经常需要把一个第三方库迁移到功能相近的另一个库，但手工迁移很耗时，因为开发者要同时理解旧库和新库 API，并在整个代码库中改代码。
- 现有推荐或 API 映射工具通常只帮助“找替代库”或“找对应 API”，仍把大量实际代码修改留给开发者完成。
- 纯命令行自动化工具会打断开发工作流；而 LLM 生成的修改也可能包含无关改动，因此需要在 IDE 内提供可审查、可拒绝的人工在环机制来建立信任。

## Approach
- 核心方法很简单：MigMate 在 VS Code 中调用其已有后端 MigrateLib，让 LLM 先自动生成库迁移修改，再把这些修改以交互式 diff 预览展示给开发者，由开发者逐条、逐文件或整体批准后再应用。
- 插件从依赖文件（如 `requirements.txt`、`pyproject.toml`）中触发迁移，允许用户选择源库与目标库，并在后台启动 MigrateLib 子进程执行迁移。
- 后端流程包括：迁移前先跑测试建立基线；调用 LLM 生成迁移代码；如果迁移后测试结果变化，则执行若干后处理修正步骤，再次运行测试以检查是否恢复正确性。
- 插件提供两类关键界面：迁移预览（Refactor Preview 或 Webview）用于显式确认代码变更；测试结果视图用于比较迁移前后测试并查看失败信息与日志。
- 设计重点不是完全替代开发者，而是把自动化和人工监督结合起来，减少上下文切换并提高可用性与可控性。

## Results
- 初步用户研究包含 **8 名**完成实验的参与者（原招募 9 人，1 人退出），采用被试内设计，对比手工迁移与插件辅助迁移。
- 在 **requests → httpx** 任务上，平均时间从手工 **25:23** 降到插件辅助 **10:42**；在 **tablib → pandas** 任务上，从 **27:51** 降到 **10:48**。
- 论文声称 MigMate 平均可节省约 **60%** 的迁移时间；不过研究只测时间与可用性，**未测迁移正确性**。
- 可用性方面，MigMate 的平均 **SUS = 80.9/100**，约处于 **90th percentile**，对应 **A-grade**。
- 遥测显示最常用的迁移触发方式是 **Hover Trigger 62.5%**，其次是 **Context Menu 33.3%**；Command Palette 仅使用 **1 次**。
- 论文还引用其前序工作作为背景：GPT-4o 在 PyMigBench 子集上达到 **94%** 迁移“至少部分正确”、**57%** “完全正确”；CLI 工具 MigrateLib 可使 **32%** 迁移完全正确，且其余迁移平均只剩 **14%** 的迁移相关改动需人工修复。这些数字主要证明后端基础能力，而非 MigMate 插件本身的新实验结果。

## Link
- [http://arxiv.org/abs/2603.01596v1](http://arxiv.org/abs/2603.01596v1)
