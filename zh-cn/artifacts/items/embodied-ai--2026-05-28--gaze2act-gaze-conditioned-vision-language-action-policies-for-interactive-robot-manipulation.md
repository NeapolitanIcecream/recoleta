---
source: arxiv
url: https://arxiv.org/abs/2605.30282v1
published_at: '2026-05-28T17:37:16'
authors:
- Kuangji Zuo
- Gen Li
- Bofan Lyu
- Yanshuo Lu
- Boyu Ma
- Shijia Han
- Xinyu Zhou
- Xichen Yuan
- Chuhao Zhou
- Jiaqi Bai
- Geng Li
- Jianfei Yang
topics:
- vision-language-action
- gaze-conditioned-control
- robot-manipulation
- human-robot-interaction
- generalist-robot-policy
- robot-foundation-model
relevance_score: 0.93
run_id: materialize-outputs
language_code: zh-CN
---

# Gaze2Act: Gaze-Conditioned Vision-Language-Action Policies for Interactive Robot Manipulation

## Summary
## 摘要
Gaze2Act 把人类视线加入 Vision-Language-Action 机器人策略，让用户可以在执行过程中选定目标物体、目标部位，或者更换目标。论文称，相比只用语言和带语言约束的空间基线，它在真实 Unitree G1 操作任务上有明显提升。

## 问题
- 当场景里有多个相似物体、机器人必须作用在某个物体部位，或者用户在执行过程中更改目标时，语言指令常常不够用。
- 这对交互式操作很关键，因为机器人需要的是准确的空间意图信号，而不只是像“pick up the cup”这样的任务句子。
- 现有基于 mask 的 VLA 方法仍然从语言推断空间目标，因此在存在歧义或视觉困难时，可能会错过用户真正指向的对象。

## 方法
- 用户佩戴 Meta Aria 眼镜，视线在第一人称视角中给出一个二维点。
- Gaze2Act 通过无标记的跨视角语义匹配，把第一人称视线映射到机器人相机视角：SAM3 提议 mask，DINOv3 特征在不同视角间匹配被注视的物体，稠密特征匹配再在选中物体上找到对应的部位点。
- 匹配得到的物体 mask 和视线点会画到机器人观测上，作为视觉提示：轮廓用于物体选择，高斯热力图用于部位级动作。
- 同样的 mask 和点也会编码成 gaze token，并通过新增的 cross-attention 分支注入到 GROOT N1.5 扩散动作头中。
- 新增的 gaze 分支用零初始化开始时等同于不生效，参数只增加 4.95%，因此微调一开始可以保留预训练的动作先验。

## 结果
- 在 Unitree G1 人形机器人上，覆盖 7 个类别和 15 个主要真实机器人任务、每个任务 50 次试验时，Gaze2Act 的整体意图准确率为 88.8%，整体任务成功率为 83.5%。Vanilla GROOT 的意图准确率和成功率分别是 33.6% 和 23.2%，RoboGround 分别是 60.6% 和 39.6%，ControlVLA 分别是 68.0% 和 41.5%。
- 在 10 个物体级任务上，Gaze2Act 的意图准确率达到 93.0%，任务成功率达到 89.0%。最强基线 ControlVLA 的意图准确率为 68.0%，成功率为 46.4%。
- 在 5 个部位级任务上，Gaze2Act 的部位级意图准确率为 80.4%，任务成功率为 72.4%。基线任务成功率中，Vanilla GROOT 为 21.2%，RoboGround 为 29.6%，ControlVLA 为 31.6%。
- 在组合任务上，Gaze2Act 对“pick bread place bowl”的意图准确率为 96%，成功率为 94%；对“pick paper ball place bin”的意图准确率为 88%，成功率为 84%。
- 在执行过程中切换目标的动态意图控制任务上，Gaze2Act 在 30 次试验中成功 14 次。RoboGround 成功 4 次，ControlVLA 成功 5 次。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.30282v1](https://arxiv.org/abs/2605.30282v1)
