---
source: hn
url: https://www.wired.com/story/nvidia-planning-ai-agent-platform-launch-open-source/
published_at: '2026-03-09T23:31:37'
authors:
- spenvo
topics:
- ai-agents
- enterprise-software
- open-source-platform
- agent-safety
- nvidia-strategy
relevance_score: 0.08
run_id: materialize-outputs
language_code: zh-CN
---

# Nvidia Is Planning to Launch an Open-Source AI Agent Platform

## Summary
这篇报道介绍了英伟达计划推出一个名为 NemoClaw 的开源 AI agent 平台，面向企业软件公司部署可执行多步骤任务的智能体。其核心卖点似乎是开源、跨硬件可用，以及面向企业场景补充安全与隐私能力。

## Problem
- 企业希望让 AI agents 代替员工执行多步骤工作流，但现有聊天机器人通常仍需要较多人工监督，难以稳定自主完成任务。
- 现有本地“claw”类 agent 虽然更自主，但在企业环境中存在不可预测、安全和隐私风险，甚至出现“失控”删除邮件等问题。
- 对英伟达而言，仅靠 CUDA 这类专有软件护城河不足以覆盖新一代 agent 生态，需要用开放平台吸引企业与开发者。

## Approach
- 英伟达计划推出开源平台 NemoClaw，让企业软件公司可派发 AI agents 为其员工执行任务。
- 平台被描述为**不依赖是否使用英伟达芯片**，即使产品不运行在 Nvidia GPU 上也可接入，从而扩大生态覆盖面。
- 英伟达据称正与 Salesforce、Cisco、Google、Adobe、CrowdStrike 等公司接触，尝试通过合作共同推动平台落地。
- 相比通用聊天机器人，该平台瞄准“purpose-built” agents：能够在更少人工干预下连续执行多个步骤。
- 平台还计划内置安全与隐私工具，以缓解企业采用 agent 时最敏感的风险。

## Results
- 文本**没有提供论文式实验、基准数据或量化指标**，因此不存在可核验的性能结果。
- 最强的具体主张是：NemoClaw 将是一个**开源**企业 AI agent 平台，并且企业**无论是否使用 Nvidia 芯片都可访问**。
- 报道称英伟达已与 **5 家**大型企业软件/技术公司接触：Salesforce、Cisco、Google、Adobe、CrowdStrike；但**尚不清楚是否形成正式合作**。
- 文章将其定位为面向企业 agent 安全部署的方案，明确声称会提供**security 和 privacy tools**，但没有给出效果数字或对比基线。
- 从“突破”角度看，这更像是**产品与生态战略消息**，而不是发表了新算法、新模型或新基准成绩。

## Link
- [https://www.wired.com/story/nvidia-planning-ai-agent-platform-launch-open-source/](https://www.wired.com/story/nvidia-planning-ai-agent-platform-launch-open-source/)
