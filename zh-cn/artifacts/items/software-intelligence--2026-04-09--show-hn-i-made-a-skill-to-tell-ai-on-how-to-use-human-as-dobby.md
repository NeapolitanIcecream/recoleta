---
source: hn
url: https://github.com/LittleLittleCloud/Dobby
published_at: '2026-04-09T23:01:07'
authors:
- BigBigMiao
topics:
- human-ai-interaction
- agent-workflow
- task-delegation
- prompt-skill
relevance_score: 0.72
run_id: materialize-outputs
language_code: zh-CN
---

# Show HN: I made a skill to tell AI on how to use human as Dobby

## Summary
这是一个用于分配简单支持任务的提示技能，对象是名为“多比”的人类助手。它把人类定位为执行琐事的低技能执行者，例如搬运文件、手动测试、收集资料、格式整理和复制粘贴。

## Problem
- 这个项目针对的是一个协调问题：AI 或操作者应该怎样把简单、边界清楚的任务交给人类助手。
- 它与人机协作有关，因为很多软件任务仍然需要模型直接控制之外的手动执行、浏览、测试或格式处理。
- 摘要没有定义可衡量的研究缺口、正式任务或评估设置。

## Approach
- 核心方法是一个可复用的“Skill”，用户可以用 `npx skills add littlelittlecloud/dobby` 安装。
- 这个技能给出管理名为多比的人类助手的行为指令，并划出明确的任务边界：多比负责简单的体力活或文书工作，而编码和架构留给主要代理或用户。
- 允许的工作示例很具体：移动文件、手动测试、收集材料、整理格式，以及复制和粘贴。
- 这里的机制是提示词层面的角色分配，而不是训练好的模型、新算法或带自主规划的系统。

## Results
- 摘要没有提供定量结果。
- 没有报告基准、数据集、准确率、任务成功率、延迟，或与基线的比较。
- 最明确的具体主张是功能范围：这个技能的目的，是帮助 AI 指示人类做简单执行任务，并避免把编码或架构设计这类高智能工作交给他。
- 这个项目似乎可以通过 `npx skills add littlelittlecloud/dobby` 安装，但摘要没有给出使用指标或结果数据。

## Link
- [https://github.com/LittleLittleCloud/Dobby](https://github.com/LittleLittleCloud/Dobby)
