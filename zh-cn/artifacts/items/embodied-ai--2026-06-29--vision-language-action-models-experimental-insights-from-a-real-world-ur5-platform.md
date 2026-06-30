---
source: arxiv
url: https://arxiv.org/abs/2606.30456v1
published_at: '2026-06-29T15:23:34'
authors:
- Mathilde Hochedel
- Marc Lalonde
topics:
- vision-language-action
- openvla
- real-robot-deployment
- ur5e
- robot-data-pipeline
- imitation-learning
relevance_score: 0.86
run_id: materialize-outputs
language_code: zh-CN
---

# Vision-Language-Action Models: Experimental Insights from a Real-World UR5 Platform

## Summary
## 摘要
本文是在 UR5e 机械臂上测试 OpenVLA 和 OpenVLA-OFT 的真实机器人案例研究。主要发现是：当动作语义、时序、预处理、坐标系和数据覆盖不一致时，闭环 VLA 部署会失败或变得不稳定。

## 问题
- 论文研究开放 VLA 模型能否从基准测试环境迁移到本地 UR5e 机器人，并实现可复现的数据采集、微调和部署。
- 这一问题重要，因为 VLA 策略依赖完整的感知-动作闭环；图像、动作单位、坐标系或时序中的小偏差都可能改变机器人的物理行为。
- 摘要指出，关于如何把开放 VLA 模型适配到新的机器人配置，尤其是协作型工业机械臂，目前指导有限。

## 方法
- 作者搭建了一个 UR5e 系统，包含 Robotiq 2F-140 夹爪、Intel RealSense D435 第三人称相机，以及安装在腕部的 Logitech 网络摄像头。
- 他们采集真实机器人示教数据，将数据转换为兼容 RLDS 的格式，并为 OpenVLA 和 OpenVLA-OFT 准备微调和推理路径。
- OpenVLA 将图像和语言指令映射为离散化的机器人动作 token；每个动作维度被量化为 256 个 bin，并通过语言模型 token 路径解码。
- 论文把 OpenVLA-OFT 作为后续模型进行研究，该模型包含连续动作回归、并行动作解码、动作分块，以及可选的腕部相机和机器人状态输入。
- 部署采用客户端-服务器设置：机器人客户端将相机输入发送到 GPU 服务器，接收预测动作，并通过 UR RTDE 执行。

## 结果
- 摘要没有给出定量任务成功率、rollout 数量，也没有给出作者 UR5e 试验的基准表。
- 在他们的设置中，原始 OpenVLA 在 NVIDIA A100 上的推理速度约为 3 Hz，使模型推理成为主要速度限制，网络传输影响较小。
- 微调使用 4 块 NVIDIA A100 GPU；本地开发和仿真在 Ubuntu 22.04 上使用配备 16 GB VRAM 的 RTX 5080。
- 作者报告称，离线指标与实体 UR5e 系统上的不稳定闭环行为之间存在稳定差距。
- 最具体的成果是交付的工程流水线：真实机器人数据采集、RLDS 转换、VLA 微调、推理部署，以及 UR5e 平台上的动作/控制验证。
- 作为模型选择背景，论文引用了 OpenVLA-OFT 原始工作的结果，包括并行解码和动作分块带来的最高 26x 加速；这不是本项目在 UR5e 上得到的新结果。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.30456v1](https://arxiv.org/abs/2606.30456v1)
