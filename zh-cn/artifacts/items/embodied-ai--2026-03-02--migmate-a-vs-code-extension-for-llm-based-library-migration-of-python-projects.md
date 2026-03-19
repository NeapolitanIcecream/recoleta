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
- llm-software-engineering
- library-migration
- vscode-extension
- developer-tools
- human-in-the-loop
relevance_score: 0.02
run_id: materialize-outputs
language_code: zh-CN
---

# MigMate: A VS Code Extension for LLM-based Library Migration of Python Projects

## Summary
MigMate 是一个将基于大语言模型的 Python 库迁移能力嵌入 VS Code 的插件，用于把原本繁琐的第三方库替换流程半自动化。它强调在人类确认环节下完成迁移，以减少工作流切换并提升开发者对 AI 修改的信任。

## Problem
- 论文解决的是 **Python 项目中第三方库迁移耗时、繁琐且易出错** 的问题；开发者不仅要理解旧库和新库 API，还要在整个代码库中做一致性修改，因此维护成本很高。
- 现有工具往往只做替代库推荐或 API 映射，**仍把大量代码改写工作留给开发者**；而纯 CLI 工具又会打断 IDE 内的正常开发流程。
- 这件事重要，因为库会过时、不再适用或需要替换；如果迁移成本过高，项目维护、升级与技术栈演进都会被拖慢。

## Approach
- 核心方法很简单：**把作者已有的 LLM 迁移工具 MigrateLib 封装进 VS Code 插件 MigMate**，让开发者可以直接在依赖文件里发起迁移，而不是离开 IDE 去命令行操作。
- 后端的 MigrateLib 会先跑原始测试建立基线，再让 LLM 生成迁移后的代码，然后再次运行测试；如果测试不一致，还会做若干后处理修正，再比较测试结果来判断迁移状态。
- MigMate 在前端增加了 **交互式预览与人工确认机制**：开发者可以逐条、逐文件或整批查看并批准代码改动，避免 LLM 引入无关编辑。
- 插件还提供 **测试结果视图**，把迁移前后测试摘要、错误信息和日志直接展示在 Webview 中，帮助定位失败原因。
- 设计上还包括懒加载激活、依赖文件悬停/右键触发、Quick Pick 选择源库与目标库、可配置模型与预览方式等，以尽量减少使用摩擦。

## Results
- 预实验用户研究包含 **8 名有效参与者**（原招募 9 人，1 人退出），比较手工迁移与插件辅助迁移的完成时间。
- 对 **requests → httpx** 任务，平均耗时从 **25:23**（手工）降到 **10:42**（插件）。
- 对 **tablib → pandas** 任务，平均耗时从 **27:51**（手工）降到 **10:48**（插件）。
- 论文声称插件平均可节省约 **60%** 的迁移时间。
- 可用性方面，MigMate 的平均 **SUS 分数为 80.9/100**，约位于 **第 90 百分位**，对应 **A 级** 可用性评价。
- 遥测数据显示最常见的触发方式是 **Hover Trigger 62.5%**，其次是 **Context Menu 33.3%**；但论文**没有报告迁移正确率的定量结果**，并明确说明本次用户研究不测 correctness。后端相关既有工作中，作者引用 MigrateLib 可实现 **32% 完全正确迁移**，其余案例平均仅剩 **14% 的迁移相关修改** 需开发者手动修复；更早的 LLM 基准中，GPT-4o 达到 **94% 至少部分正确、57% 完全正确**。

## Link
- [http://arxiv.org/abs/2603.01596v1](http://arxiv.org/abs/2603.01596v1)
