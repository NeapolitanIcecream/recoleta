---
source: arxiv
url: https://arxiv.org/abs/2607.08575v2
published_at: '2026-07-09T15:06:43'
authors:
- Shiyuan Yang
- Borong Zhang
- Jizheng Zhang
- Zhijia Tao
- Junfei Guo
- Donglai Ran
- Xu Bian
- Qingbiao Li
topics:
- vision-language-action
- robot-foundation-model
- generalist-robot-policy
- dexterous-manipulation
- flow-matching
- robot-data-scaling
relevance_score: 0.98
run_id: materialize-outputs
language_code: en
---

# FabriVLA: A Lightweight Vision-Language-Action Model for Precise Multi-Task Manipulation

## Summary
FabriVLA is a 0.89B-parameter vision-language-action model for multi-task robot manipulation. It combines flow-matching action generation, gated self-attention, and intermediate vision-language features, reaching 90.0% tier-average and 92.0% episode-level success on Meta-World MT50 without robotic data pretraining.

## Problem
- Large VLA models can perform generalist manipulation but require high compute and may have costly inference, limiting practical robot control.
- Precise tasks such as insertion, assembly, contact actuation, and object localization require both language grounding and fine spatial detail.
- The paper targets a compact model that retains strong multi-task performance without multi-billion-parameter VLA backbones or robotic pretraining.

## Approach
- FabriVLA uses the 1B-scale InternVL3.5-1B backbone with 14 retained layers. It fuses the final layer with layer 6 through a 2.1M-parameter projection so the action head receives semantic and spatial features.
- A flow-matching action head predicts a 50-step horizon with 24 action dimensions per step. It starts from uniform noise and learns the velocity that transports the noise toward expert actions.
- Eight transformer blocks use gated self-attention over action tokens before cross-attention to visual-language context. The gate starts at zero and opens during training, adding temporal action dependencies through a gradual optimization path.
- The model jointly fine-tunes the pretrained backbone and randomly initialized action head in one stage on 2,500 Meta-World demonstrations, with 50 trajectories for each of 50 tasks.

## Results
- On Meta-World MT50, FabriVLA achieves 90.0% tier-average success and 92.0% overall episode-level success across 500 evaluation episodes. Tier scores are 95.0% easy, 88.2% medium, 86.7% hard, and 90.0% very hard.
- Its 90.0% tier average exceeds LA4VLA at 87.5% and Evo-Depth at 84.4%, while using 0.89B parameters and no robotic data pretraining. The table reports results from the corresponding baseline papers.
- Layer 6 fusion improves tier-average success from 82.9% to 90.0% and episode-level success from 86.8% to 92.0%, gains of 7.1 and 5.2 percentage points.
- In the controlled 50k-step action-head ablation, gated self-attention raises tier-average success from 48.5% to 57.7% and episode-level success from 55.4% to 66.9%. Adding the token-residual head or temporal convolution reduces performance relative to gated self-attention alone.
- The strongest task-group scores are 95.7% for planar precision and sliding and 95.7% for articulated or contact actuation. Tool-mediated manipulation is weaker at 83.3%, indicating remaining difficulty with tool use and broad transport.

## Link
- [https://arxiv.org/abs/2607.08575v2](https://arxiv.org/abs/2607.08575v2)
