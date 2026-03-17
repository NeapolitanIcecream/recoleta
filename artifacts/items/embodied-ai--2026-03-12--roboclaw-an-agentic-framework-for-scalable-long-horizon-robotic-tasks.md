---
source: arxiv
url: http://arxiv.org/abs/2603.11558v1
published_at: '2026-03-12T05:22:59'
authors:
- Ruiying Li
- Yunlang Zhou
- YuYao Zhu
- Kylin Chen
- Jingyuan Wang
- Sukai Wang
- Kongtao Hu
- Minhui Yu
- Bowen Jiang
- Zhan Su
- Jiayao Ma
- Xin He
- Yongjian Shen
- Yangyang
- Guanghui Ren
- Maoqing Yao
- Wenhao Wang
- Yao Mu
topics:
- vision-language-action
- long-horizon-robotics
- agentic-framework
- autonomous-data-collection
- skill-orchestration
relevance_score: 0.95
run_id: materialize-outputs
---

# RoboClaw: An Agentic Framework for Scalable Long-Horizon Robotic Tasks

## Summary
RoboClaw 是一个面向长时程机器人操作的统一代理框架，把数据采集、策略学习和部署执行放进同一个 VLM 驱动闭环中。其关键思想是让机器人用成对的“执行-复位”动作自我重置，并在部署时由同一代理动态调度技能与恢复策略。

## Problem
- 现有 VLA 机器人系统在长时程任务上容易失效，因为数据采集、训练和部署通常彼此割裂，导致任务语义和状态分布不一致。
- 真实机器人数据采集严重依赖人工：示教、环境重置、故障监控、轨迹筛选和部署监督都很耗时，难以扩展。
- 长链条多技能执行中，早期小错误会级联放大；缺少运行时监督和恢复机制会让多策略系统非常脆弱。

## Approach
- 用一个现成的视觉语言模型作为元控制器，结合视觉观测与结构化记忆，进行高层推理、子任务选择、工具调用和技能编排。
- 设计三层结构：Policies 负责底层动作生成，Tools 提供启动/切换策略与环境查询接口，Skills 负责把工具组织成可复用过程。
- 提出 **Entangled Action Pairs (EAP)**：把一个正向操作策略和一个逆向恢复/复位策略配成一对，形成“做完再撤回”的自重置循环，从而持续在线采集数据。
- 部署时沿用同一个代理闭环，持续检查子任务是否完成；若失败则重试、切换策略、调用恢复技能，必要时再请求人工介入。
- 执行阶段产生的轨迹也回流到训练集，形成统一语义下的生命周期闭环学习。

## Results
- 论文声明：在真实世界长时程任务上，相比基线方法，RoboClaw 的任务成功率提升 **25%**。
- 论文声明：在机器人全生命周期中，人工时间投入减少 **53.7%**。
- 在相同数据量下，纯人工数据采集基线需要约 **2.16×** 的人工时间；在 rollout 期间需要约 **8.04×** 的人工干预，而 RoboClaw 大部分过程可自主完成。
- 逆向复位策略在 4 个单技能任务上的成功率分别为 **36/50、38/50、43/50、39/50**（Body Lotion、Primer、Lipstick、Tissue Wipe）。
- 正向操作策略经过 5 轮迭代后，4 个任务成功率从第 1 轮的 **21/50、23/50、2/50、11/50** 提升到第 5 轮的 **43/50、40/50、23/50、26/50**，显示在线采集与迭代优化有效。
- 图中还声称在 vanity table organization 长时程任务上，RoboClaw 明显优于端到端 VLA 基线以及“独立子任务成功率乘积”得到的期望成功率；结果基于 **20 次试验**，但摘录未给出完整基线数值。

## Link
- [http://arxiv.org/abs/2603.11558v1](http://arxiv.org/abs/2603.11558v1)
