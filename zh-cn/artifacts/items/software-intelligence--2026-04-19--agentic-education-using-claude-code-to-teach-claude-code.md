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
本文提出 **cc-self-train**，这是一套 50 个模块的课程，用 Claude Code 本身来教开发者如何使用 Claude Code。核心主张是，代理式编码工具需要结构化、可自动更新的教学方式；试点研究报告称，在所有测量的技能领域中，自我效能都显著提高。

## 问题
- 开发者可以使用强大的代理式编码工具，但现有学习材料彼此割裂，按功能零散组织，而且往往在几天内就过时，因为这些工具变化很快。
- 现有文档、博客文章和课程没有提供从入门到 hooks、skills、subagents 和多代理工作流等高级功能的渐进路径。
- 这很重要，因为高级代理式功能需要组合式理解；没有结构化路径，采用和有效使用都会受限。

## 方法
- 该系统是一套名为 **cc-self-train** 的实操课程，共 **50 个模块**，组织为 **5 条项目路径**，每条路径包含 **10 个顺序模块**：Canvas、Forge、Nexus、Sentinel 和 BYOP。
- 它通过让学习者在同一环境中与 Claude Code 作为讲师互动，边构建真实软件项目边学习 Claude Code。
- 教学会根据渐进式责任转移的 **4 个角色** 变化：**Guide → Collaborator → Peer → Launcher**。前期模块解释更多，后期模块让位给学习者，要求更多自主控制。
- 自适应层通过基于 hook 的启发式规则监控学习者参与度，使用连击检测进行模块中途干预，并在模块边界调整角色安排。
- 系统还包括步调控制、跨会话状态跟踪、用于所有模块结构一致性的参数化测试套件，以及一个上手代理；该代理会检查上游 Claude Code 的变化，并在教学开始前更新教学材料。

## 结果
- 论文报告了一项 **27 名参与者** 的试点评估。
- 它声称，在评估的 **10 个技能领域** 中，自我效能报告都出现了 **统计显著提升**，其中 **p < 0.001**。
- 报告中提升幅度最大的，是更高级的 Claude Code 功能，包括 **hooks** 和 **custom skills**。
- 课程包含 **50 个模块文件**、**5 个项目领域**、**每条路径 10 个渐进模块**、**22 个上下文文档** 和 **8 个测试文件**，用于一致性检查。
- 摘录中 **没有提供任务表现指标、完成率、节省时间，或与基线课程或其他工具培训方法的比较**。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.17460v1](http://arxiv.org/abs/2604.17460v1)
