---
source: arxiv
url: http://arxiv.org/abs/2604.17187v1
published_at: '2026-04-19T01:21:02'
authors:
- Alex Potanin
topics:
- open-weight-llms
- code-generation
- react-native
- benchmark-evaluation
- self-hosting
relevance_score: 0.94
run_id: materialize-outputs
language_code: zh-CN
---

# React-ing to Grace Hopper 200: Five Open-Weights Coding Models, One React Native App, One GH200, One Weekend

## Summary
## 摘要
这篇论文没有用一套基准测试来评估，而是让五个开源权重代码模型完成同一个具体的应用构建任务。结果显示，SWE-Bench 排名无法预测哪个模型能在 GH200 上生成最好用、可运行的 React Native 应用。

## 问题
- 论文要回答的是：在 SWE-Bench 上排名靠前的模型，是否真的能根据自然语言产品需求构建一个可用的多文件应用。
- 这对选择自托管代码模型的团队很重要，因为硬件成本很高，而基准分数可能看不出那些会让最终交付产物直接失效的问题。
- 这个任务包含了基准测试经常忽略的实际要求：身份验证、按用户隔离、按天计数语义，以及 Web 兼容性。

## 方法
- 作者在同一个提示词上运行了五个开源权重代码模型：Kimi-K2.5 Q3、Kimi-K2.5 Q4、GLM-5.1、Qwen3-Coder-480B 和 DeepSeek-V3.2。
- 所有模型都部署在同一台 NVIDIA GH200 576GB 节点上，使用 llama.cpp 和 Unsloth Dynamic 2.0 GGUF 量化，并通过 aider 的 whole-edit 模式使用。
- 提示词要求每个模型创建一个 React Native 应用，包含账户创建、登录、每日袋鼠计数和 Web 支持。
- 评估标准包括：应用是否开箱即用，以及关键功能是否正常，包括凭据校验、按用户数据隔离、按天分桶、历史保留、登出和 Web 安全行为。
- 论文还记录了使用过程中出现的部署问题，包括对温度敏感的采样卡死、推理 token 泄漏到文件路径解析，以及所有模型都错误地在 Web 上使用 React Native 的 `Alert.alert`。

## 结果
- Kimi-K2.5 Q3 是整体表现最好的模型。除去所有模型共有的 `Alert.alert` Web bug 之外，它是唯一一个在应用层面被描述为完全符合规格的模型。它可以开箱运行，并通过了身份验证校验、按用户隔离、按天计数、7 天历史记录和登出测试，生成速度为 **17 tok/s**，输出约 **4.8k tokens**。
- Kimi-K2.5 Q4 也可以开箱运行，并且大多数功能表现相同，但在按天语义上退化为只统计 **"今天"**。它的生成速度是 **7.9 tok/s**，比 Q3 **慢约 2.2 倍**，输出约 **4.8k tokens**。
- GLM-5.1 在论文中引用的 SWE-Bench Pro 分数最高，为 **58.4%**，但它在实际任务中失败了：应用**不能**开箱运行，因为缺少 `firebaseConfig.js`。它的生成速度约为 **15 tok/s**，输出约 **5.5k tokens**。
- Qwen3-Coder-480B 可以开箱运行，也处理了身份验证和按用户隔离，但没有满足按天计数这个核心要求：**没有按天分桶，也没有历史记录**。它的生成速度约为 **20 tok/s**，输出约 **4.2k tokens**。
- DeepSeek-V3.2 无法开箱运行，因为推理文本泄漏到了被解析的文件路径中，导致 `App.js` 被放错位置。它还未通过凭据校验、按用户隔离、按天语义和登出测试。它的生成速度约为 **14 tok/s**，输出约 **5.1k tokens**。
- 在这五个模型中，**0/5** 正确处理了 Web 适配：每个模型都依赖 `Alert.alert`，而它在 `react-native-web` 上不会生效。论文还指出，活跃参数规模在 **10-15B** 的效率派模型，可以用大约 **1/7** 的硬件成本，达到活跃参数 **32-40B** 的规模派模型在 SWE-Bench 上的结果。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.17187v1](http://arxiv.org/abs/2604.17187v1)
