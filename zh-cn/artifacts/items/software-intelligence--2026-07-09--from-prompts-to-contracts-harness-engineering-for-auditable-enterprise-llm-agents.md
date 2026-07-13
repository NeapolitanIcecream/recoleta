---
source: arxiv
url: https://arxiv.org/abs/2607.08028v1
published_at: '2026-07-09T01:08:33'
authors:
- Joongho Ahn
- Moonsoo Kim
topics:
- llm-agents
- harness-engineering
- code-intelligence
- auditable-ai
- enterprise-software
- multi-agent-software-engineering
relevance_score: 0.86
run_id: materialize-outputs
language_code: zh-CN
---

# From Prompts to Contracts: Harness Engineering for Auditable Enterprise LLM Agents

## Summary
## 摘要
论文提出一种由代码负责执行的 harness，将基于提示词的企业 LLM 原型转化为可审计的智能体，并为来源、路由、输出和追踪记录建立契约。一个基于韩国企业数据的投资简报系统表明，这些控制在替换模型后仍然有效，其可用性高于外部防护机制。

## 问题
- 以提示词为主的原型无法稳定执行来源边界、实体路由、主张资格、答案结构、追踪完整性和推荐用语限制。
- 在企业场景中，这些缺陷会带来实际风险：缺乏依据的主张、混合实体的证据、泄露的内部字段和无法复现的答案，都会使系统难以安全部署或审计。

## 方法
- 在清单中登记获准来源，提取证据记录，只将原子化、限定实体范围且带有来源链的陈述纳入运行时可用的来源支持主张集合。
- 将来源准入、实体路由、主张选择、答案规划、后续问题过滤、追踪生成和验证交由代码、模式、清单及验证器执行。
- 将语言模型置于可替换的组合边界。模型负责表述受限的主张包，harness 检查结果，必要时切换到确定性组合器。
- 同时记录面向读者的答案和审计追踪，内容包括路由、来源状态、选定主张、验证结果及回退路径。
- 在 5 个韩国企业集团、25 家上市公司、113 条来源支持主张、30 个验证场景和 3 个托管模型上评估系统；每个场景重复 3 次。

## 结果
- 在固定验证场景中，harness 保持了来源依据、实体路由、追踪记录、输出清理和推荐用语契约；故障注入使验证器识别出被刻意破坏的契约。
- 3 个托管模型的 270 次实际组合边界运行全部通过 harness 契约。模型侧的失败由控制层捕获并记录。
- 在执行层消融实验中，仅靠提示词指令会让推荐用语违规和内部追踪泄露到达用户。由代码负责执行的控制阻止了这些违规。
- 外接防护机制的可用性为 88/120；harness 在阻止所测试违规的同时保持了 120/120 的可用性。
- 这项研究衡量的是系统可验证性和契约执行能力，不是投资决策质量；研究也没有提供大规模生产部署或用户质量基准的证据。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2607.08028v1](https://arxiv.org/abs/2607.08028v1)
