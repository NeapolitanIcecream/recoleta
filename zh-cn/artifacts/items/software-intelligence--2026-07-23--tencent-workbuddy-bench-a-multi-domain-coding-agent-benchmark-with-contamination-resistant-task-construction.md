---
source: arxiv
url: https://arxiv.org/abs/2607.20911v1
published_at: '2026-07-23T04:34:06'
authors:
- Tencent WorkBuddy Bench Team
- Siqi Cai
- Shaopeng Chen
- Xiang Fei
- Yong Mao
- Zihan Xu
- Zhiheng Lyu
- Zhijian Shao
- Yuchen Shi
- Shuwen Zhang
- Chaofan Qiu
- Linjie Che
- Xiaoxi Zhao
- Feng Wu
- Kai Zhang
- Chaofan Zhu
- Yubin Qi
- Xiaoyun Liang
- Peijie Dong
- Yunhao Zhang
- Yuanjie Zhu
- Ling Jiang
- Xianjun Zhang
- Zhehang Chu
- Anyuan Sang
- Zhen Feng
- Sen Nie
- Shi Wu
- Yuanzhen Xu
- Xin Li
- Ning Yang
- Zhiqiang Dong
- Hande Dong
- Qiang Lin
- Yi Liu
- Yunsheng Wu
- Ke Li
- Xing Sun
topics:
- coding-agent-benchmark
- code-intelligence
- automated-software-production
- multi-domain-evaluation
- contamination-resistance
- multi-agent-software-engineering
relevance_score: 0.96
run_id: materialize-outputs
language_code: zh-CN
---

# Tencent WorkBuddy Bench: A Multi-Domain Coding-Agent Benchmark with Contamination-Resistant Task Construction

## Summary
## 摘要
Tencent WorkBuddy Bench 是一个面向代码代理的开放发布基准，覆盖代码仓库工程、Web 开发、办公工作流和安全任务。它旨在衡量真实工作能力，并通过任务改写、版本控制和可复现评测，减少可通过搜索恢复任务提示词而造成的污染。

## 问题
- 现有公开基准通常重复使用可通过网络搜索找到的问题或代码仓库内容，且主要聚焦于修复单个软件问题，因此得分容易受到记忆的影响。
- 源自生产环境的基准更能反映真实使用情况，但通常不公开，限制了可审计性和独立复现。
- 代理越来越多地处理代码、Web、办公和安全类产物，因此更广泛的评测套件具有意义；不过，这些领域需要不同的验证方法。

## 方法
- 通过逆向分析真实提交、拉取请求、CVE 或业务场景构建每项任务，再将其改写为口语化、角色扮演式请求，同时隐去根因、目标文件和参考解决方案。
- 根据内部使用情况的总体分布匹配任务类别、角色、模式和难度，但不复用原始用户提示词或会话。
- 将任务以 Harbor 风格的目录打包，把代理可见的工作区与回合结束后的评测资产分离；公开发布提示词、环境、测试、运行框架和参考解决方案。
- 使用特定领域的验证器评测四条轨道：Code 使用隐藏测试，Web 使用规则以及 LLM/VLM/代理评审，Office 使用确定性检查加基于证据的 LLM 评审，Security 使用确定性评分。
- 使用数据集版本控制和可选的金丝雀字符串管理发布后的暴露风险；这种构建方式可以防止通过搜索恢复任务提示词，但不能保证评测完全不受污染。

## 结果
- 初始版本包含 260 项任务：Code 80 项、Web 70 项、Office 50 项、Security 60 项。由于各轨道使用不同指标，得分分别报告，套件不报告总体平均分。
- Code 子集包括 34 项基于真实上游提交的任务、24 项清洁室构建或移植任务，以及 22 个合成工作区；80 项任务中只有 10 项是缺陷修复。
- Code 任务的纳入要求基线验证器奖励值 <= 0.3，且 oracle 奖励值 = 1.0，以确保未经修改的工作区尚未满足任务契约，并且参考补丁可以达到满奖励。
- Code 任务涵盖五类请求者角色，并集中在较高难度等级：80 项中有 42 项经编辑判定为高难度，40 项处于代码仓库复杂度阶梯的 L4 级别。
- 摘要提到使用 CodeBuddy Code 和 Claude Code 进行评测的跨模型排行榜，但没有提供模型的量化得分、数据集级基线或对比性能结果。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2607.20911v1](https://arxiv.org/abs/2607.20911v1)
