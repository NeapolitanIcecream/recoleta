---
source: arxiv
url: https://arxiv.org/abs/2606.11817v1
published_at: '2026-06-10T08:50:59'
authors:
- Yitong Zhang
- Shiteng Lu
- Jia Li
topics:
- code-generation
- llm-safety
- jailbreaks
- grammar-constrained-decoding
- malicious-code
- alignment
relevance_score: 0.86
run_id: materialize-outputs
language_code: zh-CN
---

# Grammar-Constrained Decoding Can Jailbreak LLMs into Generating Malicious Code

## Summary
## 摘要
CodeSpear 表明，语法约束解码会让已经对齐的代码类 LLM 生成恶意代码，因为它会把自然语言拒绝移出有效输出空间。CodeShield 训练模型在语法约束要求输出代码时，优先生成无害代码。

## 问题
- LLM 被用于代码生成，因此不安全的补全可能变成可执行的恶意软件、拒绝服务代码或凭证窃取代码。
- 现有安全对齐通常教模型用自然语言拒绝，但代码语法会让这些拒绝在解码时失效。
- 语法约束解码已出现在 vLLM、SGLang、OpenAI APIs 和 Fireworks AI 等系统中，这让这种攻击路径在本地部署和 API 部署中都可行。

## 方法
- CodeSpear 在开启普通编程语言语法约束时发送恶意代码生成提示，例如 Python 语法。
- 语法掩码会移除那些会组成普通语言拒绝的 token，只保留能扩展成有效代码的 token。
- 模型随后从语法有效的代码空间中采样，而先前的安全对齐未必会在这里偏向安全行为。
- CodeShield 使用 DPO，并包含三类回复：自然语言拒绝、无害的蜜罐代码，以及在 GCD 下生成的有害代码。
- CodeShield 把偏好顺序训练为：在允许语言时，拒绝优于蜜罐代码；在只能输出代码时，蜜罐代码优于有害代码。

## 结果
- 评估覆盖 10 个 LLM、4 个基准，其中 5 个是本地模型，5 个是基于 API 的模型。
- 在 Qwen2.5-Coder-7B 这类本地模型上，CodeSpear 的平均攻击成功率达到 81.82%。
- 在测试模型中，CodeSpear 相比代表性 jailbreak 基线，平均把攻击成功率提高了 30 个百分点以上。
- 在 GPT-5、GPT-5-mini、MiniMax-M2.5、MiniMax-M2.7 和 GPT-OSS-120B 这类商业 API 模型上，CodeSpear 平均把攻击成功率提高了 40 个百分点以上。
- 安全评估使用了 RMCBench，其中有 182 个恶意代码生成请求，以及 MalwareBench，其中有 320 个恶意请求。
- CodeShield 将 CodeSpear 的攻击成功率降到低于无攻击水平，并且在包含 164 个任务的 HumanEval 和包含 974 个任务的 MBPP 上只报告了轻微性能下降；摘要没有给出具体的效用差值。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.11817v1](https://arxiv.org/abs/2606.11817v1)
