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
- agentic-robotics
- long-horizon-planning
- vision-language-action
- autonomous-data-collection
- process-supervision
relevance_score: 0.74
run_id: materialize-outputs
language_code: zh-CN
---

# RoboClaw: An Agentic Framework for Scalable Long-Horizon Robotic Tasks

## Summary
RoboClaw 是一个面向长时程机器人操作的统一智能体框架，把数据采集、策略学习和部署执行放进同一个 VLM 驱动闭环中。其核心卖点是用可自复位的数据采集机制和部署时过程监督来提升长链任务鲁棒性并减少人工参与。

## Problem
- 现有 VLA 机器人流程通常把**数据采集、训练、部署**分开，导致语义不一致、训练-执行分布失配，长时程任务容易误差累积。
- 真实机器人数据采集高度依赖人工：示教、环境重置、失败监控、轨迹筛选和部署看护都很费时，难以扩展。
- 多策略顺序执行通常是开环或脆弱的，缺少运行时监督与恢复机制，导致复杂长链操作成功率偏低。

## Approach
- 用一个**VLM 元控制器**统一整个生命周期：根据视觉观察和结构化记忆做高层推理、选子任务、调用工具与策略。
- 提出 **Entangled Action Pairs (EAP)**：把“正向操作策略”和“逆向复位策略”成对绑定，形成**自复位循环**，让机器人能连续在线采数而不必频繁人工重置环境。
- 系统采用 **Skills–Tools–Policies** 分层：高层 skill 编排，中层 MCP 工具调用，底层 VLA 策略执行，从而把推理与控制连接起来。
- 部署时同一个智能体持续查询环境摘要与机器人状态，动态决定**继续、重试、换策略、恢复或请求人工介入**，相当于给多步任务加上过程监督。
- 执行轨迹会回流到训练数据集，形成闭环持续改进，使部署本身也成为学习来源。

## Results
- 论文主张在真实世界长时程任务上，RoboClaw 相比基线方法**成功率提升 25%**，同时**人工时间投入降低 53.7%**。
- 在数据采集效率上，若归一化 RoboClaw 的人工投入为 1，纯人工基线需要约 **2.16×** 更多人工时间，且 rollout 期间需要约 **8.04×** 更多人工干预。
- 逆向复位策略在 4 个任务上的成功率分别为：**Body Lotion 36/50、Primer 38/50、Lipstick 43/50、Tissue Wipe 39/50**。
- 正向操作策略经过 5 轮迭代后提升明显：Body Lotion **21/50 → 43/50**，Primer **23/50 → 40/50**，Lipstick **2/50 → 23/50**，Tissue Wipe **11/50 → 26/50**。
- 图 4 说明在 vanity table organization 长链任务上，RoboClaw 显著优于端到端 VLA 基线以及“4 个独立子任务成功率乘积”得到的期望成功率；结果基于 **20 次试验平均**，但摘录中未给出该图的完整数值。

## Link
- [http://arxiv.org/abs/2603.11558v1](http://arxiv.org/abs/2603.11558v1)
