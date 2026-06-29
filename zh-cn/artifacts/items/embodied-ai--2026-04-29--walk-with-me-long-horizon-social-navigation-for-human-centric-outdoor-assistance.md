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
Walk with Me 是一个用于户外辅助的机器人导航系统，输入是高层语言指令。它用公共地图中的兴趣点来定位用户意图，规划粗粒度航点，并用 VLM/VLA 模块完成局部运动和安全决策。

## 问题
- 它解决的是长距离的户外社交导航问题，用户给出的往往是抽象请求，例如“我想去散步”，而不是坐标目标。
- 这对末端配送和盲人引导很重要，因为机器人必须选出真实目的地、沿着长路线前进，并在路口、交通和人群附近保持安全。
- HD 地图导航的构建和维护成本很高，而很多学习型导航策略主要面向室内或短路线，只处理低层目标。

## 方法
- 高层 VLM 接收用户指令、GPS 上下文和来自公共地图 API 的候选 POI，然后选定具体目的地。
- 系统调用步行路线 API，并把路线重采样为带地理参考的航点，用于长距离引导。
- 每一步，机器人会把 RGB 图像、局部位姿、最近轨迹和下一个航点组成观测。
- 一个 VLM 路由器判断当前场景是常规还是复杂，以及机器人应继续前进还是停下等待。
- 如果继续前进是安全的，低层 VLA 会预测一段短的局部轨迹；如果安全置信度较低，机器人会等待并重新检查场景。

## 结果
- 真实世界评测包含 20 次户外试验：2 类应用、每类 2 个场景、每个场景 5 次独立试验。
- 两类应用是末端配送和盲人引导；示例指令包括“把奶茶送到 B 楼”和“我想去购物”。
- 论文声称，Athena 2.0 Pro AGV 机器人可以根据抽象指令完成公里级户外导航。
- 摘录没有给出成功率、路径长度分布、完成时间、碰撞率或社会合规性指标。
- 主要实验没有提供完整系统的基线对比；作者表示，现有方法与相同的输入输出设置不匹配。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2604.26839v1](https://arxiv.org/abs/2604.26839v1)
