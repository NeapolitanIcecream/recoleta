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
## 摘要
这是一个提示词 Skill，用来把简单的支持性任务分配给一名叫“多比”的人类助手。它把这名人类设定为低技能的执行者，负责搬运文件、手动测试、搜集资料、整理格式和复制粘贴等杂务。

## 问题
- 这个项目针对的是一个协作问题：AI 或操作员应当怎样把简单、边界明确的任务交给人类助手。
- 这和人机协作流程有关，因为很多软件工作仍然需要模型无法直接控制的人工执行、浏览、测试或格式整理。
- 摘录里没有给出可衡量的研究空白、正式任务定义或评测设置。

## 方法
- 核心方法是一个可复用的“Skill”，用户通过 `npx skills add littlelittlecloud/dobby` 安装。
- 这个 skill 提供了管理名为 Dobby 的人类助手的行为指令，并划定了明确的任务边界：Dobby 负责简单的体力或文书工作，而编程和架构工作由主代理或用户自己处理。
- 允许的工作示例很具体：搬运文件、手动测试、搜集资料、整理格式，以及复制粘贴。
- 其机制是在提示词层面分配角色，不是训练后的模型、 新算法，也不是具备自主规划能力的系统。

## 结果
- 摘录中没有提供定量结果。
- 没有报告基准、数据集、准确率、任务成功率、延迟，或与基线的比较。
- 最明确的具体主张是功能范围：这个 skill 用来帮助 AI 指挥人类完成简单执行任务，并避免把编程或架构设计这类需要高水平智能的工作分配出去。
- 这个产物似乎可以通过 `npx skills add littlelittlecloud/dobby` 安装，但摘录没有提供使用指标或结果数据。

## Problem

## Approach

## Results

## Link
- [https://github.com/LittleLittleCloud/Dobby](https://github.com/LittleLittleCloud/Dobby)
