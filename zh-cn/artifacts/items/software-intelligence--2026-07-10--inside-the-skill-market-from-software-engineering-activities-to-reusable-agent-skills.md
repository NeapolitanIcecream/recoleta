---
source: arxiv
url: https://arxiv.org/abs/2607.09065v1
published_at: '2026-07-10T03:21:16'
authors:
- Jialun Cao
- Xinru Yan
- Songqiang Chen
- Yaojie Lu
- Zhongxin Liu
- Shing-Chi Cheung
topics:
- agent-skills
- software-engineering
- skill-marketplaces
- software-lifecycle
- artifact-reuse
- empirical-study
relevance_score: 0.96
run_id: materialize-outputs
language_code: zh-CN
---

# Inside the Skill Market: From Software Engineering Activities to Reusable Agent Skills

## Summary
## 摘要
本文研究了从四个公开市场和代码仓库收集的 11,497 个软件工程代理技能。结果显示，可复用技能主要覆盖编码、测试和代码审查，而需求、发布和部署活动的覆盖率较低。

## 问题
- 代理技能市场正在增长，但目前还没有系统说明这些市场将哪些软件工程活动封装为可复用技能。
- 这一缺口使研究人员难以评估生命周期覆盖范围、比较不同市场中的技能、推荐技能，或判断某项技能能否迁移到不同项目。
- 这个问题很重要，因为技能会封装指令、工作流、工具、文档和可执行资产，代理可以在软件生产过程中复用这些内容。

## 方法
- 作者抓取了 ClawHub、SkillHub、SkillNet 和 SkillsMP，在去重和筛选前收集到 775,790 条记录。
- 作者依据市场标识符和代码仓库 URL 去重，应用基于规则和 GPT-5.5 的相关性筛选，移除无法访问的代码仓库，最终得到包含 11,497 个软件工程相关技能的数据集。
- 作者分析了技能长度、结构、来源市场、更新历史、版本管理、评估实践和生命周期覆盖范围。
- 作者使用 Qwen3.6-35B-A3B 将每项技能映射到八个生命周期阶段之一：需求、规划与设计、实现、代码审查、测试、发布、部署，以及维护与运维。
- 作者将技能资产分为指令、文档、脚本、代理工作流、库和应用，用于衡量除自然语言指导之外封装了多少工程功能。

## 结果
- 实现阶段包含 2,875 项技能（25.0%），测试阶段包含 2,446 项（21.3%），代码审查阶段包含 2,198 项（19.1%）；三者合计占数据集的 65.4%。
- 需求阶段包含 255 项技能（2.2%），发布阶段包含 363 项（3.2%），部署阶段包含 609 项（5.3%），说明部分生命周期阶段的覆盖率较低。
- SkillsMP 提供了 5,322 项技能（46.3%），而在不同市场之间重复出现的技能只有 722 项（6.3%）。
- SKILL.md 的平均长度为 2,078 个 token；90% 的文件不超过 4,150 个 token，最长文件包含 37,499 个 token。
- 仅包含指令的技能占数据集的 63.8%。只有 13.6% 的技能包含代码级可执行资产，其中脚本占 10.5%、库占 2.0%、应用占 1.1%。
- 论文没有报告任务性能基准测试，也没有与基线进行准确率比较。主要证据来自所收集语料库的规模和分析，包括 2026 年 1 月的 2,042 次技能更新，以及 Frontmatter 为 97.8%、Commands 为 79.3%、Verification 为 73.7% 等结构覆盖率。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2607.09065v1](https://arxiv.org/abs/2607.09065v1)
