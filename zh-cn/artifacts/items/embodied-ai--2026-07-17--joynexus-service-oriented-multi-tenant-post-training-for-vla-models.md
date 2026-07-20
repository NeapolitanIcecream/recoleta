---
source: arxiv
url: https://arxiv.org/abs/2607.16074v1
published_at: '2026-07-17T15:58:20'
authors:
- Haoran Sun
- Wentao Zhang
- Junyang Hua
- Hedan Yang
- Yongjian Guo
- Yifei Zhang
- Xiaolong Xiang
- Mingxi Luo
- Jing Long
- Chen Zhao
- Chen Zhou
- Wanting Xu
- Qiming Yang
- Hui Zhang
- Song Wang
- Xiaodong Bai
- Shuai Di
- Xu Chu
- Xiaotie Deng
- Yicheng Gong
- Junwu Xiong
topics:
- robot-foundation-model
- vision-language-action
- robot-data-scaling
- sim2real
- generalist-robot-policy
relevance_score: 0.93
run_id: materialize-outputs
language_code: zh-CN
---

# JoyNexus: Service-Oriented Multi-Tenant Post-Training for VLA Models

## Summary
## 摘要
JoyNexus 提出一个面向服务的视觉-语言-动作模型多租户后训练平台。该平台在监督微调、强化学习、轨迹生成和评估工作负载之间共享常驻 VLA 骨干模型，同时隔离每个租户可训练的模块及其状态。

## 问题
- VLA 后训练涉及异构的机器人本体、模拟器、数据集、动作模式和目标，使个人用户难以管理基础设施。
- 独占 GPU 分配和固定卡时计费模式可能在轨迹生成、数据加载、评估或其他突发阶段造成资源浪费。
- 现有面向服务的后训练系统主要面向语言模型，无法直接提供 VLA 特有的环境交互、策略同步和评估工作流。

## 方法
- JoyNexus 将训练模型服务、推理模型服务和环境服务分离，并由主服务通过 API 进行协调。
- 共享基础 VLM 常驻内存，而每个租户特有的动作模块、优化器状态、检查点和策略版本则占用彼此隔离且可分别寻址的槽位。
- 高层 API 将 SFT、RL 和评估规范编译为服务工作流；底层 API 允许用户组合自定义算法。
- 全局训练队列和推理队列调度并发的租户工作负载；故障隔离、监控和弹性轨迹生成扩展则支持长时间运行的作业。
- 分组批处理将具有兼容模型输入前缀的异构样本组合起来，使多个租户能够复用一次共享骨干模型前向计算。

## 结果
- 工作负载模拟和真实具身场景中的分组批处理流水线据称相较于隔离的单租户执行减少了 GPU 总耗时，并提高了服务利用率。
- 所提供的文本没有报告 GPU 耗时减少量、利用率、延迟、吞吐量或对比工作负载规模的数值，因此无法根据该摘录确定效率提升的幅度。
- 该论文评估的是系统效率，而非提出新的 VLA 策略、训练目标或机器人控制基准。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2607.16074v1](https://arxiv.org/abs/2607.16074v1)
