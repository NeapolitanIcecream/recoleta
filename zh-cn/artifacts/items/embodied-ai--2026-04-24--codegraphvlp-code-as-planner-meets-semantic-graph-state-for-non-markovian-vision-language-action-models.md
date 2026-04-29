---
source: arxiv
url: http://arxiv.org/abs/2604.22238v1
published_at: '2026-04-24T05:27:27'
authors:
- Khoa Vo
- Sieu Tran
- Taisei Hanyu
- Yuki Ikebe
- Duy Nguyen
- Bui Duy Quoc Nghi
- Minh Vu
- Anthony Gunderman
- Chase Rainwater
- Anh Nguyen
- Ngan Le
topics:
- vision-language-action
- long-horizon-manipulation
- non-markovian-planning
- semantic-graph-state
- code-as-planner
relevance_score: 0.95
run_id: materialize-outputs
language_code: zh-CN
---

# CodeGraphVLP: Code-as-Planner Meets Semantic-Graph State for Non-Markovian Vision-Language-Action Models

## Summary
## 摘要
CodeGraphVLP 面向长时程机器人操作任务，这类任务的下一步动作依赖更早的观察，而不只是当前相机画面。它把持久化语义图、一次性生成的代码规划器和面向对象的提示结合到一个 VLA 策略中。

## 问题
- 标准 Vision-Language-Action 模型通常只根据最新观察来动作；在非马尔可夫任务中，这种方式会失效，因为关键信息可能被遮挡，或只在更早的时刻出现。
- 基于历史的扩展可能漏掉稀疏的过去证据；随着上下文窗口变大，还会增加延迟和计算成本。
- 将 VLM 放在闭环中的分层规划器可以改善长时程推理，但反复调用模型速度较慢，而且仅用语言编写的子任务提示在杂乱场景中仍然难以稳定完成视觉定位。

## 方法
- 该系统会随时间构建并更新一个持久化语义图，其中包含与任务相关的对象、属性和关系；构建过程使用了分割、相关性过滤、跨视角关联、跟踪和基于规则的关系归纳。
- 系统在任务开始时调用一次 LLM，生成一个任务专用的 Python 规划器。这个规划器读取语义图，用简单谓词检查进度，保存轻量级任务记忆，并输出下一步子任务和相关对象。
- 执行器 VLA 不会看到完整的杂乱场景。它接收一条简短的子任务指令，以及经过掩码处理、只保留规划器所选对象的图像。
- 训练过程与部署一致：记录的演示会被转换成带子任务条件、经过掩码的观察，随后用这些输入通过模仿学习对 VLA 进行微调。

## 结果
- 在三个真实世界桌面任务上，CodeGraphVLP 报告的平均成功率为 **81.7%**，高于 **Gr00T N1.5 + Multi-frame: 56.7%**、**Gr00T N1.5: 31.7%**、**π0: 30.0%**、**π0.5: 5.0%** 和 **π0 FAST: 0.0%**。
- 在 **Pick-and-Place Twice** 任务上，CodeGraphVLP 的完整成功率为 **80%**，中间指标 **"PnP Once"** 为 **100%**；相比之下，Gr00T N1.5 + Multi-frame 为 **75% / 100%**，Gr00T N1.5 为 **35% / 50%**。
- 在 **Place-and-Stack** 任务上，CodeGraphVLP 的成功率为 **80%**，中间指标 **"Drop Cube"** 为 **95%**；相比之下，Gr00T N1.5 + Multi-frame 为 **50% / 50%**，Gr00T N1.5 为 **40% / 40%**。
- 在 **Swap Cups** 任务上，CodeGraphVLP 的成功率为 **85%**，中间指标 **"Stage Cup"** 为 **100%**；相比之下，Gr00T N1.5 + Multi-frame 为 **45% / 90%**，Gr00T N1.5 为 **20% / 70%**。
- 论文还称，与 VLM-in-the-loop 规划相比，其规划延迟显著更低，但给出的摘录没有包含具体延迟数值。
- 真实世界实验中的训练数据规模为：Pick-and-Place Twice **100** 条演示，Place-and-Stack **100** 条，Swap Cups **200** 条。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.22238v1](http://arxiv.org/abs/2604.22238v1)
