---
source: hn
url: https://www.ddmckinnon.com/2026/02/11/my-%f0%9f%8c%b6-take-on-vibe-coding-for-pms/
published_at: '2026-03-03T23:38:21'
authors:
- dmckinno
topics:
- product-management
- vibe-coding
- software-engineering-process
- prototyping
- human-ai-interaction
relevance_score: 0.42
run_id: materialize-outputs
language_code: zh-CN
---

# My spicy take on vibe coding for PMs

## Summary
这篇文章不是学术论文，而是一篇面向产品经理（PM）的观点文。作者认为，PM 不应把“亲自提交生产代码”当成高杠杆工作，但应利用编码与原型能力来更好地沟通、理解系统和做实验。

## Problem
- 文章讨论的问题是：在大公司环境下，PM 是否应该亲自写并上线生产代码，以及这种做法是否真的带来高价值。
- 作者认为这很重要，因为 PM 的核心职责是**推动优先级与资源协调**，如果把时间花在低效写代码上，可能造成机会成本、技术债和组织流程被绕过。
- 还涉及一个更广泛的问题：把“能落 prod diff”当成成就展示，可能制造“看起来在推进、实际上杠杆很低”的假象。

## Approach
- 核心观点很简单：**不要把 PM 编码用于正式生产交付，而要把它用于原型、沟通、实验和理解系统。**
- 作者首先从组织效率角度反对 PM 直接落生产代码：如果功能真的重要，应修复优先级系统，而不是绕过流程自己做。
- 其次从成本与风险角度论证：PM 编码速度可能低于专业工程师，同时人力成本更高，还容易引入技术债，甚至影响内部工具或生产环境稳定性。
- 然后给出“PM 为什么仍然应该会写代码”的正面用途：更直观地展示想法、加深对系统实现的理解、构建更真实的实验原型，以及临时利用自己独特的领域/API 经验。
- 其机制不是提出新算法，而是一种**角色分工与工作流优化原则**：把编码作为认知与实验工具，而不是作为 PM 的主要交付方式。

## Results
- 文中**没有提供任何定量实验、基准数据、数据集或指标**，因此不存在可核验的数值型结果。
- 最强的具体主张是：在 Meta 这类大规模组织里，PM 亲自上线生产功能通常是低杠杆行为，容易“绕过优先级系统”而不是修复系统性问题。
- 作者明确声称 PM 写生产代码会带来多重负效应：编码效率可能像“slow E3”，但公司承担的是接近“IC7 salary”的机会成本；不过这是一种修辞性比较，并非正式测量结果。
- 文章还提出具体风险判断：随机的 PM 宠物功能很容易积累技术债，且即便是 intern tools 的改动也可能影响生产系统。
- 正面结果层面，作者主张 PM 编码最有价值的场景包括：更好地演示功能、帮助与工程团队沟通、进行更真实的人类实验，而不是直接产出正式生产 diff。

## Link
- [https://www.ddmckinnon.com/2026/02/11/my-%f0%9f%8c%b6-take-on-vibe-coding-for-pms/](https://www.ddmckinnon.com/2026/02/11/my-%f0%9f%8c%b6-take-on-vibe-coding-for-pms/)
