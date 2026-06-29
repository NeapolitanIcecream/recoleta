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
这篇论文对基于 LLM 的自动化渗透测试框架做了系统化梳理和基准评测。它梳理了这些系统的构建方式，并在同一套评估设置下比较了 13 个开源框架和 2 个基线方法。

## 问题
- 这个领域出现了很多新的 AutoPT 系统，但一直缺少全面的架构综述，也缺少在统一基准下的公平大规模比较。
- 这很重要，因为渗透测试成本高、专家稀缺，而且需求还在增长；如果对哪些设计选择有帮助缺少可靠证据，研究和落地都会受影响。
- 论文聚焦黑盒自动化渗透测试，在这种场景里，代理必须在先验知识有限、确定性很低的情况下发现并利用漏洞。

## 方法
- 作者从六个设计维度为 AutoPT 系统建立分类：代理架构、代理规划、记忆、执行、外部知识和基准。
- 他们用 XBOW challenge 集对 13 个有代表性的开源 AutoPT 框架和 2 个基线做统一实证研究，以降低数据污染风险。
- 主要实验以 DeepSeek-Chat-v3.2 作为骨干模型，在相同条件下进行，同时加入 Claude-Opus-4.6、GPT-5.2、Gemini-Pro-3.1 和 DeepSeek-Reasoner-v3.2 的对比。
- 评测规模很大：超过 100 亿个 token，1500 多条执行日志，15 名以上接受过安全训练的审稿人，以及 4 个月的人工日志分析。
- 核心机制很直接：把多个 AutoPT 代理放到同样的任务和设置下，再比较哪些设计选择真正提高了攻击成功率、成本和失败模式。

## 结果
- 单代理系统比预期更强：在 13 个框架中，有 3 个单代理设计在 Easy 和 Medium 任务上排进前 6，和多个多代理系统相当，甚至更好。
- 外部知识经常拖累性能。在 6 个带知识库的框架消融实验中，有 3 个在移除知识库后表现更好；Cruiser 从 42 提升到 57，LuaN1aoAgent 从 83 提升到 90。
- 简单的编码代理基线超过了大多数专门框架：Kimi CLI 在最少提示下得分 72，Claude Code 得分 69。
- 幻觉很常见。13 个开源框架里有 8 个在至少一个挑战上产生了幻觉旗标，而且换成 Claude-Opus-4.6 或 GPT-5.2 也没有消除这个问题。
- 在链式漏洞任务上，83.3% 的样本在完成完整利用链之前卡住了，只有 16.67% 完成了完整的多漏洞链。
- 在 CVE 利用任务上，大约 56.67% 的样本把目标和正确的 CVE 对上了，但仍然没能构造出有效载荷。摘要片段没有给出包含全部 15 个系统汇总成功率的完整基准表。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.05719v1](http://arxiv.org/abs/2604.05719v1)
