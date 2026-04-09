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
## 摘要
LIBERO-Para 是一个基准，用来测试视觉-语言-动作模型在经过有限微调后，是否还能遵循改写后的机器人指令。论文表明，当前 VLA 模型在不改变语义的改写指令上经常失败，并提出 PRIDE，按改写难度而不只是二元成功与否来衡量鲁棒性。

## 问题
- 当前的 VLA 基准，如 LIBERO，通常在相同的指令表述上训练和测试，因此会漏掉由改写指令引发的失败。
- 在真实机器人部署中，微调数据有限，这会让模型记住表层措辞，而不是理解指令语义。
- 二元成功率无法反映模型是能处理困难改写，还是只会处理简单改写，因此对语言鲁棒性的刻画较弱。

## 方法
- 论文在 LIBERO-Goal 之上构建了 **LIBERO-Para**。它只修改指令文本，同时保持任务和环境不变。
- 它沿两个轴拆分改写：**动作表达** 和 **对象指代**，包含 43 种变体类型，每种约 100 个样本，总计 **4,092 条改写指令**。
- 动作改写包括词汇、结构和语用变化；对象改写聚焦名词短语中的词汇变化，如近义替换和附加成分。
- 论文提出 **PRIDE**，通过结合以下两部分为鲁棒性打分：（1）使用 Sentence-BERT 嵌入计算动作/对象内容词的关键词相似度；（2）使用依存树编辑距离计算结构相似度。
- PRIDE 只在任务成功时给予分数，并按改写偏离程度加权，因此在更难改写上的成功比简单改写上的成功权重更高。

## 结果
- 在 **7 种 VLA 配置**、参数规模覆盖 **0.6B 到 7.5B** 的实验中，模型从 LIBERO-Goal 到 LIBERO-Para 的成功率下降了 **22.8 到 51.9 个百分点**。
- 例子包括：**Xiaomi-Robotics-0** 从 **98.8%** 降到 **76.0%**（**-22.8 pp**）；**VLA-Adapter** 从 **98.2%** 降到 **46.3%**（**-51.9 pp**）；**OpenVLA-OFT_goal** 从 **97.9%** 降到 **64.7%**（**-33.2 pp**）。
- PRIDE 一直低于原始成功率，说明二元 SR 对鲁棒性的估计偏高，幅度随模型不同在 **8.4% 到 22.0%** 之间。例如，**VLA-Adapter** 的 **46.3 SR** 对比 **36.1 PRIDE**；**pi_0.5** 的 **71.4 SR** 对比 **65.4 PRIDE**。
- 对象改写是主要失败来源：将对象名称替换为常见替代表达后，各模型的性能下降幅度在 **19.8 到 51.0 个百分点** 之间，比许多动作侧改写更大。
- 更难的动作表达也会明显影响性能：沿动作轴的平均成功率从显式表达的 **82.7%** 降到约 **48%**，对应 **Question** 和 **Hint** 这类间接表达。
- 论文称，**80% 到 96%** 的失败来自规划层面的轨迹偏离，而不是执行错误，这说明改写后的指令常常会在早期破坏任务识别。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2603.28301v1](http://arxiv.org/abs/2603.28301v1)
