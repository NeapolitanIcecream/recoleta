---
source: arxiv
url: https://arxiv.org/abs/2605.28231v1
published_at: '2026-05-27T09:44:46'
authors:
- Seungsu Kim
- Jinyoung Choi
- Seungmin Baek
- Jean-Michel Renders
topics:
- vision-language-action
- robot-manipulation
- progress-estimation
- token-compression
- flow-matching
- long-horizon-control
relevance_score: 0.94
run_id: materialize-outputs
language_code: zh-CN
---

# ProgVLA: Progress-Aware Robot Manipulation Skill Learning

## Summary
## 摘要
ProgVLA 是一个参数量为 0.1B 的视觉-语言-动作策略，面向算力和内存受限条件下的长时程机器人操作。它把视觉、语言和本体感觉输入压缩成一小组 token，并训练辅助进度头，用这些预测结果重新加权 flow-matching 模仿学习。

## 问题
- 大型 VLA 机器人策略通常使用数十亿参数的主干网络和大规模机器人预训练数据集，这会提高训练和部署成本。
- 小型 VLA 策略可以在普通硬件上运行，但论文指出，它们在长时程任务上仍然吃力，因为机器人必须跟踪自己已经完成了多少进度。
- 这个问题很重要，因为很多操作任务都需要在本地算力和机器人数据有限的条件下，可靠地完成多步执行。

## 方法
- ProgVLA 在视觉部分使用 DUNE ViT-Small，指令部分使用冻结的 T5 文本编码器，本体感觉部分使用 MLP。
- 两级 Perceiver 重采样压缩变长输入：第一阶段对每种模态分别重采样，Transformer 融合这些 token，第二个重采样器再生成一组固定的控制 token。
- 一个类似 SmolVLA 的 flow-matching 动作专家根据压缩后的上下文生成动作块，推理时使用 10 步 Heun 迭代。
- 进度头从同一组上下文 token 预测归一化剩余进度、状态-动作价值，以及接近完成时的成功信号。
- 预测得到的优势值和成功概率会被 detach，并作为逐样本权重用于模仿损失，因此训练会更偏向那些和后续任务进度相关的示范和时间步。

## 结果
- 在 LIBERO 上，ProgVLA 以 0.1B 参数达到 91.1% 的平均成功率；SmolVLA 2.25B 为 88.75%，SmolVLA 0.24B 为 82.75%，OpenVLA 7B 为 76.5%，pi0 3.3B 为 86.0%。论文说明这些基线分数来自先前工作，因此这是公开数值的对比。
- 在 LIBERO Long 上，ProgVLA 得分 88.6%；SmolVLA 2.25B 为 77%，SmolVLA 0.24B 为 63%，OpenVLA 7B 为 53.7%，pi0 3.3B 为 73%。
- 在 Meta-World MT50 LeRobot 上，ProgVLA 在 49 个任务上的平均成功率为 78.5%；SmolVLA 2.25B 为 68.24%，SmolVLA 0.24B 为 56.95%，pi0 Paligemma-3B 为 50.5%，pi0 3.3B 为 47.9%。
- 对 LIBERO 的消融实验显示，融合后的上下文重采样器影响最大：去掉它后，平均成功率从 91.1% 降到 75.1%，Long 成功率从 88.6% 降到 51.2%。
- 冻结 DUNE 会让 LIBERO 平均成功率从 91.1% 降到 77.6%；把 DUNE 换成 DINOv3 会降到 88.7%；去掉进度目标会降到 88.8%。
- 在 6 自由度 PiPER 机械臂上的真实世界同分布测试中，每个任务用 50 个示范、共 10 个任务训练，ProgVLA 在 100 次试验中达到 68% 的成功率；失败包括 10 次杂乱物遮挡、8 次夹爪打开超时和 4 次抓错物体。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.28231v1](https://arxiv.org/abs/2605.28231v1)
