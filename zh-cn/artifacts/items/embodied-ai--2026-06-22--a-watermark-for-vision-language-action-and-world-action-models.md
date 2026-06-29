---
source: arxiv
url: https://arxiv.org/abs/2606.23574v1
published_at: '2026-06-22T16:39:28'
authors:
- Yule Liu
- Shuai Liu
- Jiaheng Wei
- Xinlei He
topics:
- vla-watermarking
- world-action-models
- robot-policy-provenance
- latent-noise-watermark
- black-box-verification
relevance_score: 0.82
run_id: materialize-outputs
language_code: zh-CN
---

# A Watermark for Vision-Language-Action and World Action Models

## Summary
## 摘要
本文提出一种用于 VLA 和 WAM 机器人策略的潜在噪声水印，使所有者能通过已执行动作验证已部署的黑盒服务。论文称，该方法在 π0.5 和 LingBot-VA 上实现了可靠的所有权检测和多密钥识别，且任务性能变化很小。

## 问题
- VLA 和 WAM 机器人策略是用专有数据训练出的高价值服务，但所有者可能只能审计发送给机器人的动作命令，无法审计权重或潜在种子。
- 现有后门水印需要修改权重，较难适配多用户识别；输出侧频率标记可能从动作流中被发现并过滤掉。
- 这个问题很关键，因为合作方可以包装或转售策略服务，同时隐藏权重，所以所有权证明必须能通过部分、经过后处理的机器人动作完成。

## 方法
- 所有者用带密钥的混合项替换选定的高斯采样器种子：z_fp = sqrt(1-β^2) z + β r_k。由于 z 和 r_k 都是高斯分布，z_fp 仍服从 N(0,I)。
- 一个秘密的带密钥选择器只标记部分动作块，并设置每个 episode 的上限 m 和最大间隔 P，使攻击者不知道哪些块携带信号。
- 审计期间，所有者只记录已执行的通道，例如单臂机器人 32 个通道中的 7 个，或双臂机器人的 14 个通道。
- 验证器通过基于梯度的 MAP 优化恢复每个潜在种子：它搜索一个种子，使其生成的动作匹配观测到的已执行通道，同时在高斯先验下保持高概率。
- 它用匹配滤波器将恢复的种子与候选密钥参考进行打分，用诱饵密钥归一化分数，汇总 rollout 分数，并为多用户识别对密钥排序。

## 结果
- 评估使用 2 个策略族 π0.5 和 LingBot-VA，覆盖 2 个机器人套件 LIBERO-10 和 RoboTwin，共 4 个策略-机器人组合。
- 使用 16 次审计 rollout 时，所有 4 个组合的二元所有权验证都在 1% FPR 下达到 TPR 1.00。
- 同一组证据在多密钥设置中识别出分配的密钥；摘录未给出准确的密钥识别准确率。
- 在 4 个组合中，任务成功率变化最多只有几个百分点。
- 在标准输出侧攻击和所有者侧变体下，汇总后报告的最弱结果仍在 1% FPR 下达到 TPR 0.84。
- π0.5/LIBERO-10 上的强平滑或抖动是失败案例，即使增加 rollout 预算，TPR 也低于 0.2。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.23574v1](https://arxiv.org/abs/2606.23574v1)
