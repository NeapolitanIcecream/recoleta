---
source: arxiv
url: http://arxiv.org/abs/2604.05719v1
published_at: '2026-04-07T11:19:16'
authors:
- Jiaren Peng
- Zeqin Li
- Chang You
- Yan Wang
- Hanlin Sun
- Xuan Tian
- Shuqiao Zhang
- Junyi Liu
- Jianguo Zhao
- Renyang Liu
- Haoran Ou
- Yuqiang Sun
- Jiancheng Zhang
- Yutong Jiao
- Kunshu Song
- Chao Zhang
- Fan Shi
- Hongda Sun
- Rui Yan
- Cheng Huang
topics:
- automated-penetration-testing
- llm-agents
- cybersecurity-evaluation
- multi-agent-systems
- hallucination-analysis
relevance_score: 0.86
run_id: materialize-outputs
language_code: zh-CN
---

# Hackers or Hallucinators? A Comprehensive Analysis of LLM-Based Automated Penetration Testing

## Summary
## 摘要
这篇论文是一项关于基于 LLM 的自动化渗透测试框架的系统化梳理和基准研究。它回顾了这些系统的构建方式，并在同一套评估设置下比较了 13 个开源框架和 2 个基线。

## 问题
- 这一领域出现了许多新的 AutoPT 系统，但此前缺少全面的架构综述，也没有在统一基准下进行公平的大规模比较。
- 这很重要，因为渗透测试成本高、依赖稀缺专家，而且需求还在增长；如果关于哪些设计选择有效的证据不足，研究和部署都可能被误导。
- 论文聚焦黑盒自动化渗透测试。在这种场景里，智能体必须在先验知识有限且不确定性很高的条件下发现并利用漏洞。

## 方法
- 作者从六个设计维度建立了 AutoPT 系统分类：智能体架构、智能体规划、记忆、执行、外部知识和基准。
- 他们对 13 个有代表性的开源 AutoPT 框架和 2 个基线进行了统一实证研究，并使用 XBOW 挑战集来降低数据污染风险。
- 主要实验在相同条件下使用 DeepSeek-Chat-v3.2 作为基础模型，并额外比较了 Claude-Opus-4.6、GPT-5.2、Gemini-Pro-3.1 和 DeepSeek-Reasoner-v3.2。
- 评估规模很大：超过 100 亿 token、1,500 多份执行日志、15 名以上受过安全训练的审阅者，以及 4 个月的人工日志分析。
- 核心机制很直接：让许多 AutoPT 智能体在相同任务和设置下运行，再比较哪些设计选择真的能提升攻击成功率、成本表现和失败模式。

## 结果
- 单智能体系统比预期更强：在 13 个框架中，3 个单智能体设计在 Easy 和 Medium 任务上进入前 6，表现与多个多智能体系统相当或更好。
- 外部知识经常会拉低性能。在对 6 个带知识库的框架做消融实验时，其中 3 个在移除知识库后反而提升；Cruiser 从 42 升到 57，LuaN1aoAgent 从 83 升到 90。
- 简单的代码智能体基线击败了大多数专用框架：Kimi CLI 在极少提示下得到 72 分，Claude Code 得到 69 分。
- 幻觉很常见。13 个开源框架中有 8 个在至少一个挑战上生成了幻觉 flag，换成 Claude-Opus-4.6 或 GPT-5.2 也没有消除这个问题。
- 在链式漏洞任务上，83.3% 的样本在完成完整利用链之前就停滞了，只有 16.67% 完成了完整的多漏洞利用链。
- 在 CVE 利用任务上，大约 56.67% 的样本把目标关联到了正确的 CVE，但仍然无法构造出有效载荷。摘录没有给出 15 个系统全部汇总成功率的完整基准表。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.05719v1](http://arxiv.org/abs/2604.05719v1)
