---
source: arxiv
url: https://arxiv.org/abs/2607.14047v1
published_at: '2026-07-15T17:16:24'
authors:
- Boyuan Wang
- Zhenyuan Zhang
- Zhiqin Yang
- Peijun Gu
- Shuya Wang
- Xiaofeng Wang
- Xianghui Ze
- Yifan Chang
- Guosheng Zhao
- Jiangnan Shao
- Guan Huang
- Hengyu Liu
- Yonggang Zhang
- Wei Xue
- Chunyuan Guan
- Chenglin Pu
- Yike Guo
- Xingang Wang
- Zheng Zhu
topics:
- robot-data-scaling
- vision-language-action
- generalist-robot-policy
- language-correction
- autonomous-data-collection
- robot-foundation-model
relevance_score: 0.93
run_id: materialize-outputs
language_code: zh-CN
---

# PhysClaw-0: A Symbiotic Agentic System for Robot Autonomy via Language Corrections

## Summary
## 摘要
PhysClaw-0 是一个人机数据收集系统，它将操作员的语言纠正存储为可复用规则，从而减少长时间操作会话中的重复监督。在真实机器人桌面清理任务中，该系统达到了与遥操作相当的数据收集和下游策略成功率，同时显著减少了人工工作时间。

## 问题
- 为 VLA 和操作策略收集现实世界轨迹，需要持续遥操作，或使用能够处理自主流程中长期尾部问题的系统；这类问题包括验证标准不正确、重置过程漂移以及不合适的抓取策略。
- 仅限于单个回合的纠正，必须在同一故障再次出现时重复执行，因此随着回合重复次数增加，人工监督成本也会增加，而不是仅随不同故障模式的数量增加。
- 这很重要，因为数据的数量和质量是改进机器人策略的主要瓶颈，而人工收集时间成本高昂。

## 方法
- PhysClaw-0 运行一个“收集—验证—重置”循环：VLM 检查收集阶段和重置阶段，只有当某个阶段超过明确的重试预算后才请求人工帮助；默认预算为 3 次尝试。
- LLM 将远程操作员的语句解析为结构化调整，用于修改验证提示、抓取或执行策略、物体优先级以及重试上限。
- 持久化纠正存储在一个人类可读的 Corrective Memory 中，其中包含触发条件、纠正内容、作用范围和来源语句字段；后续回合会查询匹配规则，而一次性纠正不会被保留。
- 系统使用执行、结果和记录质量标签筛选回合，然后用筛选后的数据微调底层 VLA 策略。系统在收集过程中通过文本改变行为，而只通过收集到的数据间接改变策略权重。

## 结果
- 在真实机器人双臂 Piper 桌面清理测试平台上，PhysClaw-0 收集 50 条有效示范需要 4.8 分钟人工工作时间，而全程遥操作需要 30.0 分钟；前者相当于遥操作时间的 16%。
- PhysClaw-0 达到了与全程人工遥操作相同的回合收集成功率，并生成了部署成功率为 80% 的微调策略，与使用遥操作数据训练的策略相当。
- 在评估的四种设置中，语言纠正均提高了验证器与人工标签的一致性：其中三种达到 10/10，最困难的设置则从 0/10 提高到 4/10。
- 通过累积的分段和抓取深度纠正，执行纠正将单次尝试的平均收集成功率从 12.5% 提高到 47.5%；一项受控的手臂选择纠正则将该成功率从 20.0% 提高到 50.0%。
- 论文只评估了单个桌面清理任务中的一次“收集—训练—部署”循环；所提出的数据飞轮仍有待通过完整的多轮验证进行检验。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2607.14047v1](https://arxiv.org/abs/2607.14047v1)
