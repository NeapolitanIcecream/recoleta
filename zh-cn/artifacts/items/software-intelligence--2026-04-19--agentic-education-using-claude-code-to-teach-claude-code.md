---
source: arxiv
url: http://arxiv.org/abs/2604.17460v1
published_at: '2026-04-19T14:20:09'
authors:
- Zain Naboulsi
topics:
- agentic-coding
- developer-education
- claude-code
- adaptive-learning
- multi-agent-workflows
relevance_score: 0.92
run_id: materialize-outputs
language_code: zh-CN
---

# Agentic Education: Using Claude Code to Teach Claude Code

## Summary
## 摘要
本文提出 **cc-self-train**，这是一个包含 50 个模块的课程，用 Claude Code 本身来教开发者如何使用 Claude Code。核心观点是，代理式编码工具需要结构化、可自动更新的教学；试点研究报告称，在所有测量的技能领域中，学习者的自我效能感都有较大提升。

## 问题
- 开发者已经可以使用强大的代理式编码工具，但当前的学习材料零散，按功能分散组织，而且工具变化很快，内容往往几天内就会过时。
- 现有文档、博客文章和课程没有提供从入门到高级功能的渐进式学习路径，例如 hooks、skills、subagents 和多代理工作流。
- 这很重要，因为高级代理功能需要组合式理解；如果没有结构化路径，采用率和有效使用都会受限。

## 方法
- 该系统是一个动手实践课程，名为 **cc-self-train**，包含 **50 个模块**，组织方式是 **5 条项目路径，每条路径 10 个顺序模块**：Canvas、Forge、Nexus、Sentinel 和 BYOP。
- 它通过让学习者构建真实的软件项目来教授 Claude Code，同时学习者在同一环境中把 Claude Code 当作教师进行交互。
- 教学会在 **4 种角色**之间变化，并与“逐步释放责任”模型对应：**Guide → Collaborator → Peer → Launcher**。前期模块讲解更多，后期模块减少引导，要求学习者承担更多控制。
- 自适应层通过基于 hook 的启发式规则观察学习者参与情况，使用连续状态检测在模块中途进行干预，并在模块边界调整角色安排。
- 系统还包括步骤节奏控制、跨会话状态跟踪、一个参数化测试套件，用于检查所有模块在结构上的一致性，以及一个入门代理，它会在教学开始前检查上游 Claude Code 的变更并更新教学材料。

## 结果
- 论文报告了一项 **27 名参与者的试点评估**。
- 论文称，在 **10 个被评估的技能领域**中，报告的自我效能感提升均具有 **统计显著性**，且 **p < 0.001**。
- 报告中提升最大的，是更高级的 Claude Code 功能，包括 **hooks** 和 **custom skills**。
- 该课程包含 **50 个模块文件**、**5 个项目领域**、**每条路径 10 个渐进式模块**、**22 个上下文文档**，以及 **8 个用于一致性检查的测试文件**。
- 该摘录 **没有提供任务表现指标、完成率、节省时间的数据，也没有与基线课程或其他工具培训方法进行比较**。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.17460v1](http://arxiv.org/abs/2604.17460v1)
