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
## 概要
这篇综述认为，用于具身 AI 的 3D 生成必须产出可直接用于模拟器的资产和场景，包括几何、关节结构、物理参数和可执行格式。它围绕物体资产、交互环境和 sim-to-real 迁移来组织这一领域。

## 问题
- 机器人学习、VLA 模型和基于仿真的训练需要大量机器人可以操作的 3D 物体和场景，而不只是可观看的内容。
- 现有 3D 生成工作通常优化形状或外观，但缺少关节、质量、摩擦、材料行为、碰撞几何，以及与 URDF/MJCF/USD 的兼容性。
- 相关文献分散在图形学、视觉、机器人和模拟器领域，使评估和复用变得困难。

## 方法
- 这篇综述用 4 个要求定义仿真就绪性：几何有效性、物理参数化、运动学可执行性和模拟器兼容性。
- 它将文献分为 3 个角色：用于物体资产的 Data Generator（数据生成器）、用于交互场景的 Simulation Environments（仿真环境），以及用于重建、增强和迁移的 Sim2Real Bridge（仿真到现实桥接）。
- 它回顾了具身流水线中使用的 3D 表示，包括体素、点云、网格、场景图、SDF、NeRF 和 3D Gaussian Splatting。
- 它将生成内容连接到模拟器格式和引擎，包括 URDF、MJCF、USD、MuJoCo、Isaac Sim、Habitat、AI2-THOR、OmniGibson、PyBullet、ManiSkill3 和 Genesis。

## 结果
- 论文没有报告新的模型基准或机器人策略实验；它是一篇综述。
- 它声称的主要结果是用于具身 AI 中 3D 生成的三部分分类：Data Generator、Simulation Environments 和 Sim2Real Bridge。
- 它列出 4 项仿真就绪性标准：几何、物理参数、运动学和模拟器文件兼容性。
- 它在表 I 中比较了 8 个主要机器人仿真平台：MuJoCo、Isaac Sim、Habitat 3.0、AI2-THOR、OmniGibson、PyBullet、ManiSkill3 和 Genesis。
- 它按 4 类资产组织物体生成方法：关节式、物理 grounded、可变形和端到端仿真就绪流水线。
- 它认为主要未解决瓶颈是物理标注有限、视觉质量与物理有效性之间对齐较弱、评估分散，以及持续存在的 sim-to-real 差距。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2604.26509v3](https://arxiv.org/abs/2604.26509v3)
