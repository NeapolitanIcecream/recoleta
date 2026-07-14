---
source: arxiv
url: https://arxiv.org/abs/2607.11111v1
published_at: '2026-07-13T05:41:01'
authors:
- Haotian Lin
- Silin Chen
- Xiaodong Gu
- Yuling Shi
- Chengxi Pan
- Jiaqi Ge
- Mengfan Li
- Jianghong Huang
- Mengchieh Chuang
- Beijun Shen
- Haibing Guan
topics:
- software-foundation-model
- code-intelligence
- automated-software-production
- multi-agent-software-engineering
- repository-knowledge
- human-ai-interaction
relevance_score: 0.96
run_id: materialize-outputs
language_code: zh-CN
---

# Know Before Fix: QA-Driven Repository Knowledge Acquisition for Software Issue Resolution

## Summary
## 摘要
ACQUIRE 在生成补丁前通过定向问答获取仓库知识，从而改进自动化软件问题解决。在 SWE-bench Verified 上，与 Mini-SWE-Agent 相比，它将 Pass@1 最高提高 4.4 个百分点，同时仅增加少量成本和时间。

## 问题
- 编码代理通常缺乏关于跨模块依赖、API 契约、数据流和外部协议的仓库特定知识，因此会生成错误补丁。
- 现有修复前方法主要定位可疑代码或生成宽泛摘要，没有先识别代理自身的具体知识缺口。
- 这些知识不足的失败尝试消耗的 token 成本超过成功解决方案的四倍，执行步骤也接近两倍。

## 方法
- ACQUIRE 将仓库理解与修复分为两个阶段：先获取知识，再生成补丁。
- Questioner 在四个类别中生成有针对性且不重复的问题：机制与行为、设计与使用、定位与结构、生态与标准。
- 独立的只读 Answerer 代理并行探索仓库，并生成基于证据的答案，引用相关文件、函数和代码行为。
- Resolver 在开始常规的导航、编辑和测试循环前，接收问题描述以及收集到的问答对。

## 结果
- 在 500 个 SWE-bench Verified 问题上，ACQUIRE 搭配 GPT-5-mini 达到 62.2% 的 Pass@1，而 Mini-SWE-Agent 为 58.4%，提高 3.8 个百分点；搭配 DeepSeek-V3.2 时达到 70.8%，而对照结果为 66.4%，提高 4.4 个百分点。
- ACQUIRE 在每个 GPT-5-mini 实例上的平均成本和耗时分别为 $0.054 和 302 秒，在每个 DeepSeek-V3.2 实例上分别为 $0.073 和 1,042 秒。SWE-Debate 等成本更高的基线方法成本为 $0.738 和 $0.382，耗时分别为 1,552 秒和 2,517 秒。
- 人工评审发现，232 个问答对中有 230 个得到仓库证据支持，占 99.1%；只有 2 个问答对包含缺乏依据的核心主张。
- 在全部 500 个问题上，注入问答知识使平均修复轮次减少 7.1%；在 44 个由失败转为成功的实例上，平均修复轮次减少 17.1%。
- 在此前失败的 116 个 SWE-bench Lite 实例上进行的 oracle 实验中，单个特权问答对使 26 个实例成功修复。这表明，定向仓库知识可以帮助基础代理完成原本无法生成的修复。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2607.11111v1](https://arxiv.org/abs/2607.11111v1)
