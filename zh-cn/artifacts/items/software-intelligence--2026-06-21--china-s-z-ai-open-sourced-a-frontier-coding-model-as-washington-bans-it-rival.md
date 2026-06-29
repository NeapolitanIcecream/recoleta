---
source: hn
url: https://startupfortune.com/chinas-zai-open-sourced-a-frontier-coding-model-the-same-day-washington-banned-its-american-rival/
published_at: '2026-06-21T23:28:26'
authors:
- insanetech
topics:
- code-intelligence
- open-weight-models
- software-agents
- self-hosted-ai
- ai-policy-risk
relevance_score: 0.88
run_id: materialize-outputs
language_code: zh-CN
---

# China's Z.ai open-sourced a frontier coding model as Washington bans it rival

## Summary
## 摘要
GLM-5.2 是 Z.ai 以 MIT 许可证发布的 753B 参数开放权重代码模型，并宣称具备前沿级代码代理能力。核心判断很实际：当美国闭源模型 API 可能因政府命令受限时，自托管权重可以降低访问风险。

## 问题
- 美国以外的团队如果让产品依赖美国闭源前沿模型，就会面临政策风险；文章引用了 2026 年 6 月 13 日的一项命令，要求 Anthropic 停用外国国民对 Claude Fable 5 和 Claude Mythos 5 的访问。
- 长周期代码代理需要能在庞大、混乱的代码库中连续工作数小时的模型，其上下文需求远超短聊天提示。
- 对敏感源代码和客户数据来说，托管 API 仍会带来数据处理、合规和可用性风险。

## 方法
- Z.ai 以 MIT 许可证发布了可下载的 GLM-5.2 权重，允许检查、修改和自托管。
- 模型卡列出该模型有 7530 亿参数，并支持 100 万 token 的上下文窗口。
- 机制很简单：如果团队负担得起算力，就可以在自己的基础设施中运行或提供下载后的模型，而不是调用托管 API。
- Z.ai 仍提供托管访问，但开放权重让团队在地区或国籍访问规则变化时多了一条路径。

## 结果
- 在 Z.ai 的表格中，GLM-5.2 在 SWE-bench Pro 上得分 62.1，高于 GPT-5.5 的 58.6，低于 Claude Opus 4.8 的 69.2。
- 在 Z.ai 的 Terminus-2 运行中，GLM-5.2 在 Terminal-Bench 2.1 上得分 81.0，Claude Opus 4.8 为 85.0。
- 发布时间接近政策事件：Anthropic 的限制于 2026 年 6 月 13 日被报道，Z.ai 于 2026 年 6 月 17 日发布了 GLM-5.2 的 Hugging Face 文章。
- 文章称权重可下载且采用 MIT 许可证，这是最强的部署层面主张，因为已复制的权重比 API 访问更难被撤回。
- 基准证据由厂商发布，因此在用这些数字指导生产模型选择之前，最强的量化主张需要独立复现。

## Problem

## Approach

## Results

## Link
- [https://startupfortune.com/chinas-zai-open-sourced-a-frontier-coding-model-the-same-day-washington-banned-its-american-rival/](https://startupfortune.com/chinas-zai-open-sourced-a-frontier-coding-model-the-same-day-washington-banned-its-american-rival/)
