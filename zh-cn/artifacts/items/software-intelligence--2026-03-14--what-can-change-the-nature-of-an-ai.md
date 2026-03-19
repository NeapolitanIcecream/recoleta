---
source: hn
url: https://onatm.dev/2026/03/14/what-can-change-the-nature-of-an-ai/
published_at: '2026-03-14T22:52:48'
authors:
- onatm
topics:
- prompt-engineering
- ai-agents
- model-alignment
- anthropomorphism
- code-intelligence
relevance_score: 0.7
run_id: materialize-outputs
language_code: zh-CN
---

# What can change the nature of an AI?

## Summary
这篇文章主张：通过提示词、`AGENTS.md`、`PERSONALITY.md` 等上下文配置，并不能真正改变 AI 的“本性”，只能短暂改变其表面行为与话语风格。作者强调，模型的实质能力与倾向主要只能在训练、后训练或微调阶段发生变化。

## Problem
- 文章批评一种常见误解：人们把提示工程中的“角色设定”当成了对模型本体的改变。
- 这种误解之所以重要，是因为它会夸大 AI 的自主性、人格性与道德能动性，进而误判其风险、能力和适用边界。
- 对软件代理场景而言，把“像资深工程师那样说话”误当成“真的具备资深工程师的判断与责任感”，会导致错误信任。

## Approach
- 核心观点非常直接：`AGENTS.md`、`PERSONALITY.md`、技能说明等，本质上只是额外上下文，不是对模型参数或内部机制的修改。
- 作者将真正的“改变”限定为三类：训练（training）、后训练（post-training）和微调（fine-tuning）。
- 文中通过对比“角色扮演/语气变化”和“本性变化”，说明前者只是脚本、声音、服装层面的模仿，不是认知或良知的形成。
- 作者进一步指出，模型在会话中表现出的“个性”只是一次推理期间由上下文暂时诱导出的行为模式，会随会话结束而消失。

## Results
- 这不是一篇实验论文；**文段未提供任何定量结果、数据集、基线或评测数字**。
- 最强的具体主张是：提示词文件只能改变**表面行为**，不能改变模型“nature”；真正改变只能发生在 **3** 个阶段：training、post-training、fine-tuning。
- 作者声称，所谓 coding agent 的“人格”只会在一次会话中、短暂地出现在某个推理实例上，属于“context”而非持久属性。
- 文章还提出一个强烈但非量化的判断：把模仿当成 conscience（良知/自我）是严重错误，因而不应把模型拟人化为会“懊悔”或“负责”的主体。

## Link
- [https://onatm.dev/2026/03/14/what-can-change-the-nature-of-an-ai/](https://onatm.dev/2026/03/14/what-can-change-the-nature-of-an-ai/)
