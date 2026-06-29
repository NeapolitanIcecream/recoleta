---
source: arxiv
url: http://arxiv.org/abs/2604.05399v2
published_at: '2026-04-07T03:49:12'
authors:
- Youngjoo Ahn
- Sangyeop Yeo
- Gijung Im
- Jongmin Lee
- Jinyoung Yeo
- Jieung Kim
topics:
- formal-verification
- automated-theorem-proving
- proof-search
- llm-for-code
- interactive-theorem-proving
relevance_score: 0.78
run_id: materialize-outputs
language_code: zh-CN
---

# PROMISE: Proof Automation as Structural Imitation of Human Reasoning

## Summary
## 摘要
PROMISE 面向大型形式化验证项目中的自动证明生成，现有基于 LLM 的方法在长而相互依赖的证明上准确率会下降。它用结构相似的证明状态迁移来引导证明搜索，而不是依赖与先前引理或脚本的表面文本匹配。

## 问题
- 形式化验证可以为安全关键软件提供机器检查的正确性保证，但证明构造仍然成本很高，需要专家级的交互式定理证明。
- 现有基于 LLM 的证明系统常把证明当作一次性生成、下一步战术预测，或对引理和证明做基于文本的检索；当证明在多个模块和文件之间存在深层依赖时，这些方法就会失效。
- 在 seL4 或 FSCQ 这类系统规模基准上，论文称以往方法对中层引理的证明覆盖率通常低于 30%，这限制了它们在已验证系统软件中的实际使用。

## 方法
- PROMISE 把证明建模为一系列证明状态和战术驱动的迁移，然后搜索与当前证明状态演化方式相似的历史迁移。
- 它根据证明状态演化模式检索结构兼容的证明片段，而不是只看定理陈述或证明文本的词面相似度。
- 它把这种结构化检索和来自当前证明环境的上下文感知引理检索结合起来，使用那些角色符合当前目标状态的可用引理。
- 该系统以迭代、带状态的证明搜索循环运行，提出简短的战术延续，用证明助手检查结果，并用检索到的迁移轨迹扩展搜索。
- 这个方法与模型无关，使用现成的 LLM，不需要额外训练；论文用 GPT-3.5-Turbo、Qwen2.5-Coder-7B-Instruct 进行评估，也讨论了 GPT-4.1 的设置。

## 结果
- 在 seL4 微内核验证基准上，PROMISE 相比以往基于 LLM 的证明自动化方法，最高提升 **+26 个百分点**，论文将其描述为 **186% 的相对提升**。
- 论文与 **Selene** 和 **Rango** 比较，并称在相同查询预算下，PROMISE 在**大多数设置**中优于先前方法。
- 在摘要中列出的唯一例外 **GPT-4.1/P2** 里，PROMISE 仍然与最强基线持平，而不是领先。
- PROMISE 在不同模型规模和能力下都保持较强性能；摘要称在 PROMISE 内部，**Qwen2.5-Coder-7B-Instruct** 和 **GPT-3.5-Turbo** 之间的差距很小，而其他方法对模型大小更敏感。
- 摘要没有给出完整结果表、各模型的精确成功率，或除 **+26 个百分点 / 186%** 之外的逐基准拆分。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.05399v2](http://arxiv.org/abs/2604.05399v2)
