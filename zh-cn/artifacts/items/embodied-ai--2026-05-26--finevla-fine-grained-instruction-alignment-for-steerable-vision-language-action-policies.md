---
source: arxiv
url: https://arxiv.org/abs/2605.27284v1
published_at: '2026-05-26T17:01:10'
authors:
- Xintong Hu
- Xuhong Huang
- Jinyu Zhang
- Yutong Yao
- Yuchong Sun
- Qiuyue Wang
- Mingsheng Li
- Sicheng Xie
- Yitao Liu
- Junhao Chen
- Yixuan Chen
- Yingming Zheng
- Shuai Bai
- Tao Yu
topics:
- vision-language-action
- robot-foundation-models
- steerable-robot-policy
- robot-data-scaling
- fine-grained-annotation
- dual-arm-manipulation
relevance_score: 0.94
run_id: materialize-outputs
language_code: zh-CN
---

# FineVLA: Fine-Grained Instruction Alignment for Steerable Vision-Language-Action Policies

## Summary
## 总结
FineVLA 给机器人轨迹加入与动作对齐的细粒度指令，让 VLA 策略能遵循执行细节，例如选哪只手臂、从哪个方向接近、接触哪个区域以及最终姿态。论文报告说，这种做法在仿真和真实双臂操作中都带来提升，同时没有降低任务级成功率。

## 问题
- 开源机器人数据集通常只给每条轨迹配一个简短的目标标签，策略就缺少对执行选择的监督，而这些选择会影响操作结果。
- 这很重要，因为同一个任务可以有多种都正确的执行方式，例如用左臂、从特定方向接近，或者接触物体的某个区域。
- 这个领域也缺少一个留出集基准和一个已训练的标注器，用来检查 VLM 是否理解机器人动作的过程层面信息。

## 方法
- FineVLA-Tool 把 10 个开源机器人数据集中的 972,247 条轨迹转换为统一的 LeRobot 风格格式，并清理不一致的动作-状态日志。
- 它先在标准化后的动作序列上做动态时间规整，再对演示进行聚类，挑选出 47,159 条有代表性的轨迹用于标注。
- 每条选中的轨迹都会得到人类核验的细粒度指令，覆盖 10 个维度：动作序列、主动执行者、目标物体、初始和最终构型、接触与接近、轨迹与朝向、物体交互、失败与恢复，以及身体运动。
- RoboFine-Bench 留出 500 个视频，包含 10,816 个原子事实和 1,030 个 VQA 问题，用来测试机器人视频理解。
- FineVLA-Policy 训练 StarVLA-OFT 和 StarVLA-GR00T 变体，只改变语言混合方式：原始目标级指令、细粒度指令，或受控的 FG:Raw 比例。

## 结果
- FineVLA-Data 覆盖 47,159 条轨迹和 220,606 个步骤；平均指令长度从 9.3 个词增加到 96.8 个词，比粗粒度标签长 10.4 倍。
- 只用细粒度指令训练时，在测试的架构和数据规模设置中，比只用原始指令高出 +1.4 到 +8.1 个成功率百分点。
- 细粒度和原始指令混合训练在 FG:Raw = 1:2 到 1:1 附近达到峰值；最好的 AlohaMix-OFT 设置在 RoboTwin 上达到 86.8% Easy 和 82.5% Hard，而只用原始指令时分别是 71.8% 和 71.4%。
- 在真实世界的双臂操作中，FG:Raw = 1:1 得到 62.7/100，而只用原始指令是 49.9。
- 相比只用原始指令，真实世界提升最大的项目是姿态 +23、颜色 +18 和接近方向 +18，这些都和指令指定的执行因素有关。
- RoboFine-VLM 在 RoboFine-Bench 上达到 71.0% 的 VQA 准确率和 83.6% 的困难描述得分，领先于列出的通用 VLM 基线。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.27284v1](https://arxiv.org/abs/2605.27284v1)
