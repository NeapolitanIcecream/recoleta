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
这篇论文没有用一整套基准来测模型，而是拿五个开权重代码模型做一个具体的应用生成任务。结果表明，SWE-Bench 排名并不能预测哪一个模型能在 GH200 上生成最好、能跑起来的 React Native 应用。

## 问题
- 论文想回答的是：SWE-Bench 上的领先模型，是否真的能从一个自然语言产品需求里生成可用的多文件应用。
- 这个问题对选择自托管代码模型的团队很重要，因为硬件成本很高，而基准分数可能看不出会把最终产物弄坏的失败。
- 任务包含一些基准常常漏掉的实际要求：登录认证、按用户隔离、按天计数语义，以及网页兼容性。

## 方法
- 作者用同一条提示词运行了五个开权重代码模型：Kimi-K2.5 Q3、Kimi-K2.5 Q4、GLM-5.1、Qwen3-Coder-480B 和 DeepSeek-V3.2。
- 所有模型都部署在一台 NVIDIA GH200 576GB 节点上，使用 llama.cpp 和 Unsloth Dynamic 2.0 GGUF 量化，然后通过 aider 的 whole-edit 模式调用。
- 提示词要求每个模型生成一个 React Native 应用，包含账号创建、登录、每天的袋鼠计数和网页支持。
- 评估标准是应用是否能开箱运行，以及关键功能是否正常：凭证校验、按用户隔离数据、按天分桶、保留历史、登出和网页安全行为。
- 论文还记录了使用时遇到的部署问题，包括对温度敏感的采样卡死、推理 token 泄漏到文件路径解析，以及 React Native 的 `Alert.alert` 在网页上的普遍误用。

## 结果
- Kimi-K2.5 Q3 是整体表现最好的模型。除所有模型共有的网页 `Alert.alert` 问题外，它被描述为在应用层面完全符合规格。它能开箱运行，通过认证校验、按用户隔离、按天计数、7 天历史和登出测试，速度约 **17 tok/s**，输出约 **4.8k tokens**。
- Kimi-K2.5 Q4 也能开箱运行，并且大部分功能一致，但它把按天语义退化成了 **“仅今天”** 计数。它的生成速度约 **7.9 tok/s**，比 Q3 慢约 **2.2 倍**，输出也约 **4.8k tokens**。
- GLM-5.1 在文中引用的 SWE-Bench Pro 分数最高，为 **58.4%**，但它在实际任务里失败了：应用不能开箱运行，因为缺少 `firebaseConfig.js`。它的生成速度约 **15 tok/s**，输出约 **5.5k tokens**。
- Qwen3-Coder-480B 能开箱运行，也处理了认证和按用户隔离，但它没完成核心要求中的按天计数：**没有按天分桶，也没有历史记录**。它的生成速度约 **20 tok/s**，输出约 **4.2k tokens**。
- DeepSeek-V3.2 因为推理文本泄漏进了解析后的文件路径，导致 `App.js` 放错位置，所以不能开箱运行。它也没通过凭证校验、按用户隔离、按天语义和登出测试。它的生成速度约 **14 tok/s**，输出约 **5.1k tokens**。
- 在五个模型里，**0/5** 正确处理了网页适配：每个模型都依赖 `Alert.alert`，而它在 `react-native-web` 上是空操作。论文还指出，效率路线的模型如果有 **10-15B active parameters**，可以用大约 **1/7** 的硬件成本，达到规模路线 **32-40B active** 模型相近的 SWE-Bench 结果。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.17187v1](http://arxiv.org/abs/2604.17187v1)
