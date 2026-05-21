---
source: arxiv
url: https://arxiv.org/abs/2605.00244v1
published_at: '2026-04-30T21:25:20'
authors:
- Yajvan Ravan
- Adam Rashid
- Alan Yu
- Kai McClennen
- Gio Huh
- Kevin Yang
- Zhutian Yang
- Qinxi Yu
- Xiaolong Wang
- Phillip Isola
- Ge Yang
topics:
- robot-data-scaling
- sim2real
- dexterous-manipulation
- synthetic-data
- xr-teleoperation
- vision-language-action
relevance_score: 0.86
run_id: materialize-outputs
language_code: zh-CN
---

# Lucid-XR: An Extended-Reality Data Engine for Robotic Manipulation

## Summary
## 摘要
Lucid-XR 是一个面向机器人操作的 XR 合成数据系统。它在基于浏览器的 MuJoCo 仿真中收集人类示范，再将示范转换为逼真的多视角训练图像。论文称，只用这些数据训练的策略可以迁移到真实机器人的抓取放置场景，并且比用真实遥操作数据训练的策略更能处理视觉变化。

## 问题
- 机器人操作策略需要多样的、接触密集的数据，但真实遥操作速度慢，因为每次试验都需要人工复位、安全检查和物理布置。
- 浏览器或云端 VR 设置可能引入延迟，这会影响包含可变形物体、颗粒、紧密接触或快速运动的灵巧任务。
- 普通 3D 场景中的合成示范难以训练出良好的视觉策略，除非视觉数据覆盖杂乱程度、光照、相机姿态和物体外观。

## 方法
- Lucid-XR 通过 WebAssembly 在 XR 头显浏览器内运行 MuJoCo，使用 WebGL 渲染，并通过 web-XR 输入手部和控制器数据。
- 用户在虚拟场景中收集示范；系统以 25 Hz 记录 SE(3) 动捕姿态，并可用一个按钮重置场景。
- 系统使用 MuJoCo 逆运动学，以及动捕站点与机器人部件之间的用户自定义绑定，将人手或控制器运动重定向到机器人夹爪或灵巧手。
- 生成式图像流水线使用仿真掩码、深度、相机姿态和文本提示，将简单虚拟示范转换为逼真的多视角图像。
- 额外数据来自采集后改变相机视角，以及通过轨迹变形来移动物体、机器人和初始状态。

## 结果
- 基于浏览器的仿真器在 Apple Vision Pro 上以 90 fps 运行，以 25 fps 记录数据，并在测试设置中报告每个仿真步低于 12 ms。
- 在 3 个任务的 30 分钟采集会话中，参与者在 Lucid-XR 中收集的示范数量约为真实世界遥操作的 2 倍。
- 经过增强后，Lucid-XR 数据集的有效规模达到真实世界遥操作基线的约 5 倍。
- 在使用未见过的真实生活网格的厨房清理评估中，ACT 在基础环境、低杂乱环境、高杂乱加噪声环境中的得分分别为 100%、0% 和 0%；ACT + LucidSim 在相同设置中的得分分别为 100%、90% 和 25%。
- sim-to-real 测试使用 10、20 和 30 分钟的 Lucid-XR 数据，并与时长匹配的真实遥操作数据比较；论文报告了相近的真实机器人抓取放置表现，但摘录未给出图 11 中的具体成功率。
- 论文报告称，在仅使用 Lucid-XR 合成数据训练后，策略可以零样本迁移到未见过、杂乱且光照较差的评估环境，示例涵盖积木堆叠、倾倒颗粒、球分类、打结、厨房清理和杯架放置。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.00244v1](https://arxiv.org/abs/2605.00244v1)
