---
source: arxiv
url: https://arxiv.org/abs/2606.13578v1
published_at: '2026-06-11T17:03:53'
authors:
- Baochang Ren
- Xinjie Liu
- Xi Chen
- Yanshuo Liu
- Chenxi Li
- Daqi Gao
- Zeqin Su
- Jintao Xing
- Zirui Xue
- Rui Li
- Xiangyu Zhao
- Shuofei Qiao
- Minting Pan
- Wangmeng Zuo
- Lei Bai
- Dongzhan Zhou
- Ningyu Zhang
- Huajun Chen
topics:
- vision-language-action
- robot-foundation-model
- scientific-lab-automation
- simulation-data-generation
- cross-embodiment
relevance_score: 0.92
run_id: materialize-outputs
language_code: zh-CN
---

# LabVLA: Grounding Vision-Language-Action Models in Scientific Laboratories

## Summary
## 摘要
LabVLA 面向书面实验室流程的机器人执行，现有视觉-语言-动作策略在实验器材、液体和多步骤台面工作流上表现不好。它把一个合成实验室数据引擎和一个两阶段策略结合起来，让预训练视觉语言模型可以把实验室指令映射为跨不同机器人形态的动作。

## 问题
- 现有 VLA 策略大多在家庭和桌面数据上训练，因此学不到实验室特有对象、接触精度和流程工作流。
- 真实实验室数据采集成本高，因为它需要专门仪器、安全检查和领域监督。
- 同一条实验室流程必须在不同机器人形态上运行，而这些机器人在相机、夹爪、工作空间和动作空间上都不同。

## 方法
- RoboGenesis 在模拟中用生成的 3D 资产、经过验证的布局和可配置的机器人配置文件构建实验室场景。
- 它把 pick、pour、press、stir、open 和 close 这类原子技能组合成长时程工作流。
- 它在工作流验证后应用领域随机化，这样同一流程可以在光照、杂乱程度、相机位姿、物体外观和摆放位置上变化，而不改变任务语义。
- 它只导出成功的 rollouts 作为 LabEmbodied-Data，并包含多相机观测、机器人状态、动作和步骤级标注。
- LabVLA 先用 FAST 动作 token 对 Qwen3-VL-4B-Instruct 主干进行训练，再在停止梯度的知识隔离下用 flow matching 和一个 DiT 动作专家继续训练。

## 结果
- RoboGenesis 生成了一个 LabAssetLibrary，包含 2,947 个带标注资产和 1,000 多种纹理，然后用它们构建了 10,000 个实验室场景。
- 支持的机器人池覆盖 16 个机器人平台，包括单臂、双臂和移动操作臂配置。
- 论文报告称，包含 20 多个技能步骤的复合工作流，其采集成功率仍高于 75%。
- 在 LabUtopia 上，LabVLA 在所有评测基线中报告了最高的平均成功率，且在分布内和分布外设置下都是如此。
- 摘要没有给出 LabUtopia 的具体成功率数字或基线数值，所以最强的明确结果只能写成这个排序结论和报告的数据规模。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.13578v1](https://arxiv.org/abs/2606.13578v1)
