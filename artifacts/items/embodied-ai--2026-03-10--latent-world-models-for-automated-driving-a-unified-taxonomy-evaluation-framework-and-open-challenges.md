---
source: arxiv
url: http://arxiv.org/abs/2603.09086v1
published_at: '2026-03-10T01:56:17'
authors:
- Rongxiang Zeng
- Yongqi Dong
topics:
- world-models
- autonomous-driving
- latent-representations
- evaluation-framework
- survey
relevance_score: 0.52
run_id: materialize-outputs
---

# Latent World Models for Automated Driving: A Unified Taxonomy, Evaluation Framework, and Open Challenges

## Summary
这是一篇面向自动驾驶潜在世界模型的综述/立场论文，提出统一分类体系、评测框架与开放问题清单。其核心价值在于把分散的生成、规划、强化学习与推理方法放到同一个“潜在表示”视角下比较，并强调闭环部署与资源约束。

## Problem
- 自动驾驶需要从高维多传感器输入中进行长时域决策，但真实长尾/危险场景稀缺、闭环验证昂贵，纯仿真又存在 sim-to-real 落差。
- 现有研究按任务或架构割裂（预测、规划、扩散、Transformer、开环/闭环），难以解释哪些设计真正影响鲁棒性、泛化与安全。
- 开环感知或生成指标与闭环驾驶表现经常不一致，因此缺少能面向“可部署决策”的统一分析和评测原则。

## Approach
- 论文提出一个统一的潜在空间框架，按**latent targets**（worlds/actions/generators）、**latent forms**（continuous/discrete/hybrid）和**structural priors**（geometry/topology/semantics）整理自动驾驶世界模型。
- 用四大范式组织方法：神经仿真与世界建模、潜在空间规划与强化学习、生成式数据合成与场景编辑、认知推理与 latent chain-of-thought。
- 提炼五个跨方法的内部机制：结构同构、长时域时间稳定性、语义/推理对齐、价值对齐目标与后训练、自适应计算与审慎推理。
- 进一步提出评测建议：强调闭环指标套件，并加入资源感知的 deliberation cost，以缩小开环分数与闭环安全之间的错配。

## Results
- 这篇论文**没有报告新的实验性定量结果**；从给定摘要与节选看，它的主要贡献是框架化总结与评测主张，而不是提出并验证一个新模型。
- 明确声称的贡献有 **5 项**：统一 taxonomy、总结 **5** 个内部机制、提出闭环评测套件与资源代价、给出设计建议与研究议程、汇总代表性基准与方法。
- 覆盖的方法版图至少包含 **4** 大类：neural simulation、latent planning/RL、data synthesis/editing、cognitive reasoning/latent CoT。
- 评测层面的核心主张是：应减少 **open-loop / closed-loop mismatch**，并把“资源开销下的审慎推理”纳入评价，而不仅看视觉逼真度或开环预测误差。
- 文中列举了大量代表方法（如 BEVWorld、OmniGen、Think2Drive、WorldRFT、LCDrive、FutureX 等），但在所给文本中**未提供统一数值对比、具体数据集成绩或提升百分比**。

## Link
- [http://arxiv.org/abs/2603.09086v1](http://arxiv.org/abs/2603.09086v1)
