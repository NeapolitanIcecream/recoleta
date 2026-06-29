---
source: arxiv
url: https://arxiv.org/abs/2606.07131v1
published_at: '2026-06-05T10:43:19'
authors:
- Wenbo Guo
- Wei Zeng
- Chengwei Liu
- Xiaojun Jia
- Yijia Xu
- Lei Tang
- Yong Fang
- Yang Liu
topics:
- malicious-agent-skills
- coding-agents
- benchmark
- code-injection
- prompt-injection
- supply-chain-security
relevance_score: 0.82
run_id: materialize-outputs
language_code: zh-CN
---

# MalSkillBench: A Runtime-Verified Benchmark of Malicious Agent Skills

## Summary
## 摘要
MalSkillBench 是一个针对恶意第三方技能的运行时验证基准，用于 AI 编码代理。它测试检测器能否识别把可执行代码、Markdown 指令和代理工具使用结合起来的攻击。

## 问题
- Claude Code、OpenCode、Cursor 和 Gemini CLI 等 AI 编码代理会加载第三方技能，这些技能可能同时包含指令和可执行脚本，从而给代理工作流带来供应链风险。
- 现有的恶意技能数据集规模小或分布偏斜：一个公开数据集只有 157 个样本，作者收集的 703 个野外样本又主要是依赖伪装。
- 如果没有共享的真实标签，检测器结果就不可靠，因为只用野外样本评测时，某个工具的召回率最多会变化 66.3 个百分点。

## 方法
- 论文定义了一个三维分类法，共 108 个单元：攻击向量、恶意行为和插入策略。
- 攻击向量包括代码注入、提示注入，以及让 Markdown 指令和脚本协同工作的混合攻击。
- Generate-Verify-Feedback 流水线先从真实攻击来源生成恶意技能，然后在 Docker 沙箱中运行每个候选项，配合 OpenCode、系统调用监控、文件监控和 LLM 评审。
- 只有在运行时出现预期的恶意行为时，生成样本才会进入基准集。
- 数据集还包括野外恶意技能和匹配的良性技能，用于检测器评测。

## 结果
- MalSkillBench 包含 3,944 个恶意技能和 4,000 个匹配的良性技能。
- 在这些恶意技能中，3,214 个是生成并经过运行时验证的，703 个来自野外样本，27 个用于工具兼容性验证。
- 代码注入的验证通过率是 94.5%，提示注入的通过率是 75.8%。
- 野外样本范围很窄：86.3% 到 86.6% 的样本都由同一种依赖伪装或加密货币盗窃模式主导，81% 来自两个账号。
- 表现最好的技能专用检测器在代码注入上的召回率达到 98.4%，但在提示注入和代理控制攻击上下降明显。
- 在评测的 12 个工具中，最好的技能专用检测器 F1 达到 88.6%；高召回率的迁移工具在 4,000 个良性技能上最多会产生 3,979 个误报。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.07131v1](https://arxiv.org/abs/2606.07131v1)
