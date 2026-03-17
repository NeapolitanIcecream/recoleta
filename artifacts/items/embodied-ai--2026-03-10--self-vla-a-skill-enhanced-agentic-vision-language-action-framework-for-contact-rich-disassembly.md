---
source: arxiv
url: http://arxiv.org/abs/2603.11080v1
published_at: '2026-03-10T22:30:28'
authors:
- Chang Liu
- Sibo Tian
- Xiao Liang
- Minghui Zheng
topics:
- vision-language-action
- robot-disassembly
- contact-rich-manipulation
- agentic-robotics
- skill-library
- failure-recovery
relevance_score: 0.95
run_id: materialize-outputs
---

# SELF-VLA: A Skill Enhanced Agentic Vision-Language-Action Framework for Contact-Rich Disassembly

## Summary
SELF-VLA提出一种面向接触丰富拆解任务的智能体式VLA框架，把端到端视觉-语言-动作策略与显式技能库和失败恢复结合起来。它旨在解决传统VLA在长时程、高精度工业拆解中成功率极低的问题，并在CPU与RAM拆解上显著优于端到端基线。

## Problem
- 现有机器人拆解系统通常依赖分阶段工程流水线，数据准备、建模和维护成本高，且对具体任务和零件过于特化，泛化差。
- 端到端VLA虽然在桌面日常操作上表现不错，但在拆解这类**长时程、接触丰富、需严格步骤约束**的工业任务上往往接近失效。
- 该问题重要，因为电子废弃物规模巨大、人工拆解成本高且有健康风险，而高价值部件回收依赖稳定自动化拆解能力。

## Approach
- 核心思想很简单：**让VLA负责“靠近与判断时机”，让显式技能负责“关键接触操作”，失败时再由校正VLA捡回并继续”**。
- 框架包含3部分：VLA-planner根据图像和语言把机械臂移动到合适预抓取状态，并输出一个特殊stop token；随后调用技能库执行接触丰富的拆解轨迹；若抓取/放置失败，则触发VLA-corrector重新抓取并恢复执行。
- 为避免改VLA输出头，作者把stop token编码进夹爪动作维度，使用超出物理范围的数值255来表示“切换到技能执行”。
- 技能库由人工遥操作记录的结构化waypoint组成：提取阶段用相对位姿waypoint适应不同起点，放置阶段用绝对位姿waypoint到固定目标；CPU技能含23个waypoints，RAM技能含8个。
- 数据集为真实桌面拆解演示，共528条示范（CPU 264、RAM 264），并对4个VLA基座模型做LoRA微调，同时训练planner、corrector和端到端基线，比较10Hz与30Hz版本。

## Results
- 在**RAM removal**上，最佳端到端结果为**π0.5-Droid FT-10Hz: 7/20 final success (35%)**；最佳SELF-VLA结果为**π0.5-Droid FT-10Hz: 12/20 (60%)**，相对该最强端到端基线提升**25个百分点**。
- 在**CPU extraction**上，最佳端到端结果仅为**π0.5-Droid FT-30Hz: 2/20 final success (10%)**；最佳SELF-VLA达到**π0.5-Droid FT-10Hz: 17/20 (85%)**，提升**75个百分点**，说明对更复杂接触操作收益更大。
- 对于OpenVLA-OFT，在CPU任务上，端到端最佳仅**0/20 final success (FT-10Hz)**，而SELF-VLA达到**10/20 (50%)**；在RAM任务上，端到端**0/20**提升到SELF-VLA **4/20 (20%)**。
- 对于π0.5，在CPU任务上，端到端最佳为**0/20**，SELF-VLA最佳为**11/20 (55%)**；在RAM任务上，端到端最佳为**4/20 (20%)**，SELF-VLA最佳为**9/20 (45%)**。
- 预训练未微调模型几乎全部为**0/20**，说明该场景对任务特定适配要求很高；同时作者报告**10Hz微调通常优于30Hz**，例如π0.5-Droid在CPU SELF-VLA上**17/20 vs 7/20**。

## Link
- [http://arxiv.org/abs/2603.11080v1](http://arxiv.org/abs/2603.11080v1)
