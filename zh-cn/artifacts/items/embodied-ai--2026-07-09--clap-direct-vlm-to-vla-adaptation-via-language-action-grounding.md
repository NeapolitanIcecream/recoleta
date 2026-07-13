---
source: arxiv
url: https://arxiv.org/abs/2607.08974v1
published_at: '2026-07-09T22:34:11'
authors:
- Yuri Ishitoya
- Jeremy Siburian
- Masashi Hamaya
- Kuniaki Saito
- Cristian C. Beltran-Hernandez
- Mai Nishimura
topics:
- vision-language-action
- robot-foundation-model
- language-action-grounding
- robot-data-scaling
- sim-to-real
- dexterous-manipulation
relevance_score: 0.96
run_id: materialize-outputs
language_code: zh-CN
---

# CLAP: Direct VLM-to-VLA Adaptation via Language-Action Grounding

## Summary
## 摘要
CLAP 在精确的数值动作 token 前加入自然语言动作描述，将预训练视觉语言模型适配为可执行的机器人策略。经过一个 epoch 的微调且不增加架构组件后，2B 模型在 LIBERO 上达到 90.8% 的平均成功率，比匹配的 VLA-0 基线高 14.9 个百分点。

## 问题
- VLA 微调通常让语言模型输出没有自然语言描述的数值动作 token，这会造成输出分布与预训练所使用的自然语言数据不匹配。
- 这种不匹配可能削弱语义泛化能力，也使研究者难以衡量预训练 VLM 对机器人控制的贡献。
- 对于紧凑型 VLA，这个问题影响更大，因为有限的模型容量和较短的训练预算会放大能力损失的代价。

## 方法
- CLAP 先生成动作片段的简短语言描述，例如“向前移动、向右倾斜并闭合夹爪”，再生成数值动作 token。
- 模型在同一个因果序列中生成这两部分，因此每个数值动作 token 都以上文的语言描述为条件。
- 描述由应用于现有动作标签的固定模板生成，因此该方法不需要人工标注、动作专家、词表扩展或架构改动。
- 动作仍可直接执行：每个 7-DoF 动作使用 1,000 个离散化区间，输出保留精确的数值控制能力。
- 可选的动作掩码增强会将部分输入动作 token 替换为占位符，但默认的 CLAP 模型不使用掩码。

## 结果
- 经过一个 epoch 的训练后，0.8B、2B 和 4B CLAP 模型在 LIBERO 上的平均成功率分别为 89.6%、90.8% 和 84.9%，相较匹配的 VLA-0 基线分别提高 13.5、14.9 和 20.7 个百分点。
- 2B 模型在 LIBERO 的每个测试套件上都超过 VLA-0：Spatial 从 77.8% 提升到 93.0%，Object 从 86.6% 提升到 97.4%，Goal 从 77.0% 提升到 90.8%，Long 从 62.4% 提升到 82.0%。
- 在 LIBERO-PRO 上，未使用掩码的 CLAP 相比 VLA-0，在 0.8B、2B 和 4B 规模下的平均分布外成功率分别提高 5.5、11.1 和 10.9 个百分点。对于包含新视觉实例的 4B Spatial 任务，提升幅度为 42.6 个百分点；使用掩码后提升幅度达到 54.4 个百分点。
- 动作掩码对分布内性能的影响不一致：在 0.8B、2B 和 4B 规模下，LIBERO 平均成绩分别变化 -3.9、-1.7 和 +3.2 个百分点。
- 报告的训练成本约为在 8 个 GPU 上训练 6.5 小时，计划发布 0.8B、2B 和 4B 规模的开放权重模型。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2607.08974v1](https://arxiv.org/abs/2607.08974v1)
