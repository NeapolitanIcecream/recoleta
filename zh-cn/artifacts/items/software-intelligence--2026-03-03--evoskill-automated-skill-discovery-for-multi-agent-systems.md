---
source: arxiv
url: http://arxiv.org/abs/2603.02766v1
published_at: '2026-03-03T09:07:22'
authors:
- Salaheddin Alzubi
- Noah Provenzano
- Jaydon Bingham
- Weiyuan Chen
- Tu Vu
topics:
- multi-agent-systems
- skill-discovery
- coding-agents
- evolutionary-optimization
- agent-skills
relevance_score: 0.92
run_id: materialize-outputs
language_code: zh-CN
---

# EvoSkill: Automated Skill Discovery for Multi-Agent Systems

## Summary
EvoSkill提出一种让多智能体系统自动“长出技能”的框架：它不微调模型，而是从失败案例中总结并生成可复用的技能模块。论文声称，这种基于技能层的进化比直接改提示词或代码更可迁移，并在多个问答/搜索基准上带来稳定提升。

## Problem
- 现有代码/智能体系统虽然通用，但缺少处理专业任务所需的**领域技能**，导致在复杂文档推理、搜索验证等任务上表现不稳。
- 今天多数agent skills依赖**人工手写**，扩展到更多任务时成本高、难维护，也难系统化迭代。
- 现有进化式方法多优化**低层工件**（prompt、代码），通常强绑定特定模型与任务，复用性和跨任务迁移较差。

## Approach
- EvoSkill把优化目标从prompt/代码提升到**skill层**：把技能表示成结构化技能文件夹，包含触发元数据、说明文档（SKILL.md）和可选辅助脚本。
- 系统由三个协作agent组成：**Executor**执行任务、**Proposer**分析失败轨迹并提出“新增/修改技能”的建议、**Skill-Builder**将建议落地成具体技能。
- 进化过程是**失败驱动**的：每轮从当前最优程序集合中选一个父程序，收集低分样本，基于失败分析提出技能变异，再在验证集上评估。
- 用一个固定容量的**Pareto/frontier**保存高分agent程序；只有在held-out验证集上真正提升性能的技能才会保留，底层模型始终冻结不变。
- 系统还维护**反馈历史**，记录过去提案、得分变化和成败，避免重复尝试，并帮助后续提案在已有经验上继续改进。

## Results
- **OfficeQA**（基于美国财政部文档的grounded reasoning）：基线精确匹配准确率 **60.6%**，EvoSkill最佳“merge-unique”配置达到 **67.9%**，提升 **+7.3 个百分点**。同表中不同训练比例也优于基线：**5%训练集 63.4%（+2.8）**，**10% 65.8%（+5.2）**，**15% 64.5%（+3.9）**。
- OfficeQA在更宽松容差下也有提升：例如**0.10%容差**从 **66.3% → 70.8%**，**1.00%容差**从 **72.8% → 77.1%**，**5.00%容差**从 **77.2% → 80.5%**。
- **SealQA**（带噪声检索的搜索增强QA）：准确率从 **26.6%** 提升到 **38.7%**，绝对提升 **+12.1 个百分点**。
- **零样本迁移**：在SealQA上进化出的技能迁移到 **BrowseComp**，无需修改，将准确率从 **43.5%** 提升到 **48.8%**，提升 **+5.3 个百分点**。
- 论文的最强主张是：仅用**小训练子集**、且**冻结底层模型**，通过自动发现可复用技能就能获得显著提升，并且部分技能具有跨任务迁移能力。
- 局限上，文中提到部分配置仅做**单次运行**，由于计算成本高，**多随机种子方差分析尚未提供**。

## Link
- [http://arxiv.org/abs/2603.02766v1](http://arxiv.org/abs/2603.02766v1)
