---
source: arxiv
url: https://arxiv.org/abs/2606.03784v1
published_at: '2026-06-02T15:37:59'
authors:
- Nan Sun
- Yuan Zhang
- Yongkun Yang
- Wentao Zhao
- Peiyan Li
- Jun Guo
- Wenxuan Song
- Pengxiang Ding
- Runze Suo
- Yifei Su
- Xin Xiao
- Xinghang Li
- Huaping Liu
topics:
- vision-language-action
- embodied-cot
- robot-manipulation
- diffusion-policy
- robot-data-scaling
- generalist-robot-policy
relevance_score: 0.97
run_id: materialize-outputs
language_code: zh-CN
---

# Revisiting Embodied Chain-of-Thought for Generalizable Robot Manipulation

## Summary
## 总结
ERVLA 把具身 chain-of-thought 视为机器人动作表示的训练监督，而不是测试时必须提供的前缀。论文使用一个大规模自动标注的具身 CoT 语料库，报告了在 LIBERO-Plus 和 VLABench 上的领先成功率。

## 问题
- VLA 机器人策略能理解图像和语言，但在任务需要语义消歧、空间落地或长动作序列时，经常失败。
- 以往的具身 CoT 方法常让策略先生成推理再输出动作，这会增加延迟，也会让推理错误影响后续动作 token。
- 大规模具身 CoT 标签噪声很大，尤其是依赖检测器的坐标信息，比如边界框和夹爪位置；如果模型必须依赖显式 CoT，扩大数据规模反而可能损害控制效果。

## 方法
- 论文构建了一个具身 CoT 语料库，包含任务理解、规划、空间落地和动作级运动描述等结构化字段。
- ERVLA 以 Qwen3-VL-4B 作为视觉语言主干，并使用一个用 flow matching 训练的 diffusion transformer 动作头来生成连续机器人动作。
- 模型在训练时接收 CoT 监督，但 reasoning dropout 让它在推理时可以在有或没有显式 CoT 的情况下执行动作。
- 辅助的 action-query 回归让 VLM 隐状态预测动作块，把语言推理和控制对齐。
- knowledge truncation 让动作模型可以关注 semantic-prefix 的 KV cache，同时排除后续追加的状态和 action-query token，避免训练捷径。

## 结果
- 语料库包含 978,743 条轨迹、2.263 亿个样本和 2,592.5 小时机器人数据，来源包括 Bridge、Fractal、Droid、MolmoAct 和 AgiBot。
- ERVLA 在 LIBERO-Plus 上报告了 86.9% 的平均成功率，并在 LIBERO-Plus Spatial 轨道的背景和光照变化上达到 100% 成功率。
- ERVLA 在 VLABench 上报告了 53.2% 的平均成功率。这个基准包含类别、常识、指令和纹理变化的分布内与分布外轨道。
- 在不预训练的 CoT 字段消融中，只有高层字段时效果变差或几乎没有提升：Goal 为 -1.2，Planning 为 -0.8，Subtask 为 -0.6，Reasoning 为 -1.0；Movement 为 +4.1，Point trajectory 为 +4.8。
- 把语义和动作落地的 CoT 结合起来效果更好：Movement+Reasoning 为 +5.2，Subtask+Movement+Point trajectory 为 +7.4，完整 ECoT 在不预训练时为 +8.2。
- 在自回归 CoT+FAST 扩展下，加入 Bridge+Fractal+MolmoAct+Droid 会让 VLABench In-dist. 下降 -3.6，Cross-category 下降 -3.0，Texture 下降 -3.4，支持论文关于显式 CoT 前缀不适合稳定扩展用于动作解码的判断。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.03784v1](https://arxiv.org/abs/2606.03784v1)
