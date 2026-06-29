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
Lucid-XR 是一个用于机器人操作的基于 XR 的合成数据系统。它在基于浏览器的 MuJoCo 仿真中采集人工演示，然后把这些演示转换成逼真的多视角训练图像。论文声称，只用这些数据训练的策略可以迁移到真实机器人的抓取放置场景，并且比用真实遥操作数据训练的策略更能应对视觉变化。

## 问题
- 机器人操作策略需要多样的、包含接触的数据，但真实遥操作很慢，因为每次试验都要人工复位、安全检查和物理布置。
- 基于浏览器或云端的 VR 设置会增加延迟，这会影响涉及可变形物体、颗粒、紧密接触或快速运动的灵巧任务。
- 纯 3D 场景中的合成演示，只有在视觉数据覆盖杂乱背景、光照、相机位姿和物体外观时，才足以训练视觉策略。

## 方法
- Lucid-XR 通过 WebAssembly 在 XR 头显浏览器中运行 MuJoCo，使用 WebGL 渲染，并通过 web-XR 输入获取手部和控制器信号。
- 用户在虚拟场景中采集演示；系统以 25 Hz 记录 SE(3) mocap 位姿，并且可以一键重置场景。
- 系统用 MuJoCo 逆运动学，以及用户定义的 mocap 站点和机器人部件绑定，把人的手部或控制器动作重定向到机器人夹爪或灵巧手。
- 一个生成式图像流程使用仿真掩码、深度、相机位姿和文本提示，把简单的虚拟演示转换成逼真的多视角图像。
- 额外数据来自采集后改变相机视角，以及对轨迹做变形，以移动物体、机器人和初始状态。

## 结果
- 这个基于浏览器的模拟器在 Apple Vision Pro 上以 90 fps 运行，以 25 fps 记录数据，并且在测试配置下报告每个仿真步长少于 12 ms。
- 在 3 个任务、每次 30 分钟的采集会话中，参与者在 Lucid-XR 中收集到的演示数量大约是现实世界遥操作的 2 倍。
- 加上增强后，Lucid-XR 的有效数据集规模达到现实世界遥操作基线的约 5 倍。
- 在使用未见过的真实网格模型进行的厨房清理评估中，ACT 在基础环境中得分 100%，在低杂乱环境中得分 0%，在高杂乱加噪声环境中得分 0%；ACT + LucidSim 在相同设置下分别得分 100%、90% 和 25%。
- Sim-to-real 测试使用了 10、20 和 30 分钟的 Lucid-XR 数据，并与匹配的真实遥操作数据对照；论文报告真实机器人抓取放置性能相近，但这段摘要没有给出图 11 的具体成功率。
- 论文报告，只用 Lucid-XR 合成数据训练后，可以零样本迁移到未见过的、杂乱的、光线较差的评估环境，示例覆盖积木堆叠、颗粒倾倒、球分类、打结、厨房清理和杯树放置。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.00244v1](https://arxiv.org/abs/2605.00244v1)
