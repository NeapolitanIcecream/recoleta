---
source: arxiv
url: http://arxiv.org/abs/2603.28301v1
published_at: '2026-03-30T11:27:34'
authors:
- Chanyoung Kim
- Minwoo Kim
- Minseok Kang
- Hyunwoo Kim
- Dahuin Jung
topics:
- vision-language-action
- robot-benchmark
- paraphrase-robustness
- instruction-following
- language-grounding
relevance_score: 0.95
run_id: materialize-outputs
language_code: zh-CN
---

# LIBERO-Para: A Diagnostic Benchmark and Metrics for Paraphrase Robustness in VLA Models

## Summary
## 总结
LIBERO-Para 是一个基准，用来测试视觉-语言-动作模型在有限微调后能否跟随改写过的机器人指令。论文显示，当前 VLA 模型在保持语义不变的改写上经常失效，并提出 PRIDE，用偏义改写的难度来衡量鲁棒性，而不只看二元成功率。

## 问题
- 当前的 VLA 基准，如 LIBERO，通常用相同的指令措辞训练和测试，因此会漏掉由改写指令引起的失败。
- 在真实机器人部署中，微调数据有限，这会让模型记住表层措辞，而不是把指令语义和环境对应起来。
- 二元成功率看不出模型是能处理困难改写，还是只会处理简单改写，所以它对语言鲁棒性的刻画很弱。

## 方法
- 论文在 LIBERO-Goal 的基础上构建了 **LIBERO-Para**，这是一个受控基准，只改变指令文本，任务和环境保持不变。
- 它沿两个轴拆分改写：**动作表达** 和 **对象指代**，包含 43 种变化类型，每种约 100 个样本，总计 **4,092 条改写指令**。
- 动作变化包括词汇、结构和语用层面的变化；对象变化主要关注名词短语中的词汇变化，例如近义替换和添加。
- 论文提出 **PRIDE**，通过结合以下两项来给鲁棒性打分：(1) 用 Sentence-BERT 嵌入计算动作/对象内容词的关键词相似度；(2) 用依存树编辑距离计算结构相似度。
- PRIDE 只在任务成功时给分，并按改写偏离程度加权，所以在更难的改写上成功会比在更容易的改写上成功分值更高。

## 结果
- 在 **7 种 VLA 配置** 上，参数规模从 **0.6B 到 7.5B**，从 LIBERO-Goal 到 LIBERO-Para 的成功率下降了 **22.8 到 51.9 个百分点**。
- 例子：**Xiaomi-Robotics-0** 从 **98.8%** 降到 **76.0%**（**-22.8 pp**）；**VLA-Adapter** 从 **98.2%** 降到 **46.3%**（**-51.9 pp**）；**OpenVLA-OFT_goal** 从 **97.9%** 降到 **64.7%**（**-33.2 pp**）。
- PRIDE 一直低于原始成功率，说明二元 SR 会高估鲁棒性，高估幅度因模型而异，范围是 **8.4% 到 22.0%**。例如，**VLA-Adapter** 的 **46.3 SR** 对应 **36.1 PRIDE**；**pi_0.5** 的 **71.4 SR** 对应 **65.4 PRIDE**。
- 对象改写是主要失败来源：把对象名替换成常见替代表达，会让各模型的成功率下降 **19.8 到 51.0 个百分点**，比许多动作侧变化更大。
- 更难的动作形式也会拉低表现：沿动作轴的平均成功率从显式形式的 **82.7%** 降到间接形式（如 **Question** 和 **Hint**）的约 **48%**。
- 论文称，**80% 到 96%** 的失败来自规划层面的轨迹偏离，而不是执行错误，这说明改写往往会在早期打乱任务识别。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2603.28301v1](http://arxiv.org/abs/2603.28301v1)
