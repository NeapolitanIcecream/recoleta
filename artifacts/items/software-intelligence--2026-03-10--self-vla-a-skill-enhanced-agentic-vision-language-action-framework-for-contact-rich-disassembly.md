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
- robotic-disassembly
- agentic-framework
- contact-rich-manipulation
- failure-recovery
relevance_score: 0.46
run_id: materialize-outputs
---

# SELF-VLA: A Skill Enhanced Agentic Vision-Language-Action Framework for Contact-Rich Disassembly

## Summary
SELF-VLA提出一种将显式“技能”嵌入VLA机器人策略的agentic框架，用于接触密集、长时程的电子废弃物拆解。它试图解决纯端到端VLA在精密工业拆解中几乎失效的问题，并通过技能调用与失败恢复显著提升成功率。

## Problem
- 电子废弃物拆解需要面对产品差异大、状态不确定、操作流程长且接触密集，传统人工成本高、效率低，还有安全与健康风险。
- 现有机器人拆解多依赖感知-规划-执行的分阶段流水线，工程复杂、误差累积、泛化差，难以应对实时不确定性。
- 现有端到端VLA虽在日常桌面操作上有效，但在CPU/RAM这类高精度、强约束拆解任务上成功率接近于零，因此限制了其工业落地价值。

## Approach
- 框架由三个部分组成：**VLA-planner**负责根据视觉+语言接近目标；到达合适姿态后输出一个特殊**stop token**；随后调用**skill library**执行预定义的接触密集拆解技能；若抓取失败，则由**VLA-corrector**重新抓取并恢复后续流程。
- 核心思想是：不要让单一VLA策略硬学完整个复杂拆解流程，而是让它先“走到位、看懂何时切换”，再把最精密、最程序化的部分交给显式技能执行。
- stop token被编码进夹爪动作维度中，使用超出物理范围的数值255，无需改造原有VLA输出头即可触发技能切换。
- 技能库使用相对/绝对路点序列实现：相对路点适配不同起始位姿进行拔出，绝对路点负责放置；并通过夹爪宽度差与50Hz连续掉落检测自动判断失败。
- 数据集包含528条真实演示（CPU 264、RAM 264），并将轨迹标注为approaching、skill execution、correction、skill resumption四阶段，用LoRA微调OpenVLA、OpenVLA-OFT、π0.5、π0.5-Droid。

## Results
- 数据规模：共**528**条真实演示，包含**264**条CPU extraction和**264**条RAM removal；训练/评估覆盖**8**种采集配置，测试使用**5**种未见过的组件位置/姿态，每个任务每模型设置评估**20**次。
- **RAM removal**上，最佳端到端基线为**π0.5-Droid FT-10Hz：7/20 final success (35%)**；SELF-VLA最佳为**π0.5-Droid FT-10Hz：12/20 (60%)**，比最佳端到端提升**+5/20 = +25个百分点**。
- **RAM removal**上，SELF-VLA在**π0.5 FT-10Hz**达到**9/20 (45%)** final success，而对应端到端仅**4/20 (20%)**；在**π0.5-Droid FT-30Hz**下，SELF-VLA为**11/20 (55%)**，端到端为**5/20 (25%)**。
- **CPU extraction**上，最佳端到端基线仅为**π0.5-Droid FT-30Hz：2/20 final success (10%)**；SELF-VLA最佳为**π0.5-Droid FT-10Hz：17/20 (85%)**，相对最佳端到端提升**+15/20 = +75个百分点**。
- **CPU extraction**上，SELF-VLA在**OpenVLA-OFT FT-10Hz**达到**10/20 (50%)** final success，而对应端到端为**0/20**；在**π0.5 FT-10Hz**达到**11/20 (55%)**，对应端到端为**0/20**。
- 预训练模型几乎全部失败：如OpenVLA、OpenVLA-OFT、π0.5、π0.5-Droid在两项任务上的多数**PT final success为0/20**，说明该论文的主要贡献在于“技能增强+恢复机制”对工业拆解场景的显著增益，而非单纯依赖现成VLA能力。

## Link
- [http://arxiv.org/abs/2603.11080v1](http://arxiv.org/abs/2603.11080v1)
