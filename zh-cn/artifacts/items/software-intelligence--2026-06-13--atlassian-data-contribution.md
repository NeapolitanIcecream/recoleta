---
source: hn
url: https://news.ycombinator.com/item?id=48522482
published_at: '2026-06-13T23:21:20'
authors:
- yells_jovially
topics:
- software-foundation-model
- code-intelligence
- automated-software-production
- human-ai-interaction
relevance_score: 0.71
run_id: materialize-outputs
language_code: zh-CN
---

# Atlassian "Data Contribution"

## Summary
## 总结
这段文字认为，Atlassian 的“Data Contribution”政策允许 Rovo 用客户内容训练模型，并引发隐私和知识产权担忧，尤其影响小型组织。文中说，Jira 和 Confluence 的数据价值异常高，因为它们同时包含公司知识、工作历史和最新的运营细节。

## 问题
- Atlassian 计划使用客户数据训练 Rovo，这引发了隐私和知识产权方面的担忧。
- 该功能的推出方式不一致：小型客户只能通过手动步骤选择退出数据贡献，而 Enterprise 客户可以完全退出。
- 文中说，Jira 和 Confluence 包含高价值的组织知识，所以这种数据暴露比普通的 SaaS 遥测政策影响更大。

## 方法
- 文中把 Atlassian 的收集内容分成“Metadata”和“Data”，并认为公司的“Metadata”类别包含的不只是传统意义上的元数据。
- 文中举了 story points、dates、SLAs、similarity scores 和 readability scores 等例子，说明这些都可能被 Atlassian 使用。
- 文中解释了为什么 Jira 和 Confluence 组合后会形成很强的训练集：前者包含计划、任务和执行历史，后者包含文档和内部知识。
- 文中把这项政策描述为一种单向转移，小型组织把流程知识和知识产权贡献给 Atlassian，以改进它的 AI 产品。

## 结果
- 摘录中没有提供定量实验结果。
- 具体说法是，Atlassian 拥有来自 30 多万组织的数据，除非客户选择退出，否则会用这些客户数据训练 Rovo。
- 文中说，只有 Enterprise 客户可以完全退出；对其他客户来说，数据退出需要手动操作，而且 metadata contribution 仍然开启。
- 文中声称 Atlassian 对元数据的定义包括数值字段和计算特征，所以默认贡献覆盖的不只是简单的系统日志。
- 主要结论是政策批评，而不是测量得到的技术结果：这次推出会带来隐私和知识产权风险，并且更偏向大型企业，而不是小型客户。

## Problem

## Approach

## Results

## Link
- [https://news.ycombinator.com/item?id=48522482](https://news.ycombinator.com/item?id=48522482)
