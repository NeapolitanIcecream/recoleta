---
source: arxiv
url: https://arxiv.org/abs/2604.26839v1
published_at: '2026-04-29T16:02:13'
authors:
- Lingfeng Zhang
- Xiaoshuai Hao
- Xizhou Bu
- Yingbo Tang
- Hongsheng Li
- Jinghui Lu
- Xiu-shen Wei
- Jiayi Ma
- Yu Liu
- Jing Zhang
- Hangjun Ye
- Xiaojun Liang
- Long Chen
- Wenbo Ding
topics:
- social-navigation
- outdoor-navigation
- vision-language-action
- human-robot-assistance
- map-free-navigation
- safety-reasoning
relevance_score: 0.74
run_id: materialize-outputs
language_code: zh-CN
---

# Walk With Me: Long-Horizon Social Navigation for Human-Centric Outdoor Assistance

## Summary
## 摘要
Walk with Me 是一个面向户外辅助的机器人导航系统，可根据高层语言指令导航。它使用公共地图 POI 来定位用户意图，规划粗略航点，并用 VLM/VLA 模块处理局部运动和安全决策。

## 问题
- 它解决长时程户外社交导航问题：用户给出的是抽象请求，例如“我想去散步”，而不是坐标目标。
- 这对最后一公里配送和盲人引导有用，因为机器人必须选择真实目的地，沿长路线行进，并在路口、车流和人群附近保持安全行为。
- 基于 HD 地图的导航构建和维护成本高，许多学习型导航策略则集中在室内或短路线，并依赖低层目标。

## 方法
- 高层 VLM 接收用户指令、GPS 上下文和公共地图 API 提供的候选 POI，然后选择一个具体目的地。
- 系统查询步行路线 API，并将路线重采样为带地理参考的航点，用于长时程引导。
- 在每一步，机器人根据 RGB 图像、局部位姿、近期轨迹和下一个航点形成观测。
- VLM 路由器判断场景是常规还是复杂，并决定机器人应继续前进还是停下等待。
- 如果继续前进是安全的，低层 VLA 会预测一段短的局部轨迹；如果安全置信度低，机器人会等待并重新检查场景。

## 结果
- 真实世界评估使用 20 次户外试验：2 个应用类别，每个类别 2 个场景，每个场景 5 次独立试验。
- 两个应用类别是最后一公里配送和盲人引导；示例指令包括“把奶茶送到 B 楼”和“我想去购物”。
- 论文称，该系统可在 Athena 2.0 Pro AGV 机器人上根据抽象指令完成公里级户外导航。
- 摘录没有给出成功率、路径长度分布、完成时间、碰撞率或社交合规指标。
- 主要实验没有报告完整系统的基线对比；作者说明，现有方法与该系统的输入输出设置不一致。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2604.26839v1](https://arxiv.org/abs/2604.26839v1)
