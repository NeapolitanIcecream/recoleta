---
source: arxiv
url: https://arxiv.org/abs/2604.26509v3
published_at: '2026-04-29T10:17:55'
authors:
- Tianwei Ye
- Yifan Mao
- Minwen Liao
- Jian Liu
- Chunchao Guo
- Dazhao Du
- Quanxin Shou
- Fangqi Zhu
- Song Guo
topics:
- 3d-generation
- robotic-simulation
- sim2real
- embodied-ai
- simulation-assets
- scene-generation
relevance_score: 0.82
run_id: materialize-outputs
language_code: zh-CN
---

# 3D Generation for Embodied AI and Robotic Simulation: A Survey

## Summary
## 摘要
这篇综述认为，面向具身 AI 的 3D 生成必须生成可直接用于模拟器的资产和场景，包括几何、关节结构、物理参数和可执行格式。它把这一领域分成三部分：对象资产、交互环境和 sim-to-real 迁移。

## 问题
- 机器人学习、VLA 模型和基于模拟的训练需要大量 3D 对象和场景，机器人要能操作这些内容，而不只是观察。
- 现有 3D 生成工作往往只优化形状或外观，却缺少关节、质量、摩擦、材料行为、碰撞几何，以及与 URDF/MJCF/USD 的兼容性。
- 相关研究分散在图形学、视觉、机器人和模拟器社区，评估和复用都更难。

## 方法
- 这篇综述把模拟就绪定义为 4 个要求：几何有效性、物理参数化、运动学可执行性和模拟器兼容性。
- 它把文献分成 3 类角色：用于对象资产的数据生成器、用于交互场景的模拟环境，以及用于重建、增强和迁移的 Sim2Real Bridge。
- 它回顾了具身流程中使用的 3D 表示，包括体素、点云、网格、场景图、SDF、NeRF 和 3D Gaussian Splatting。
- 它把生成内容和模拟器格式及引擎对应起来，包括 URDF、MJCF、USD、MuJoCo、Isaac Sim、Habitat、AI2-THOR、OmniGibson、PyBullet、ManiSkill3 和 Genesis。

## 结果
- 这篇论文没有报告新的模型基准或机器人策略实验；它是一篇综述。
- 它的主要结论是一个用于具身 AI 中 3D 生成的三分法：Data Generator、Simulation Environments 和 Sim2Real Bridge。
- 它列出 4 项模拟就绪标准：几何、物理参数、运动学和模拟器文件兼容性。
- 它在表 I 中比较了 8 个主要机器人模拟平台：MuJoCo、Isaac Sim、Habitat 3.0、AI2-THOR、OmniGibson、PyBullet、ManiSkill3 和 Genesis。
- 它按 4 类资产类型整理对象生成方法：有关节、物理约束、可变形，以及端到端模拟就绪流程。
- 它指出，主要未解决的瓶颈是物理标注有限、视觉质量与物理有效性之间的对齐不足、评估割裂，以及持续存在的 sim-to-real 差距。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2604.26509v3](https://arxiv.org/abs/2604.26509v3)
