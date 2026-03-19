---
source: arxiv
url: http://arxiv.org/abs/2603.09079v1
published_at: '2026-03-10T01:39:38'
authors:
- Md Selim Sarowar
- Omer Tariq
- Sungho Kim
topics:
- vision-language-action
- 3d-representation
- depth-aware-reasoning
- robot-manipulation
- gaussian-tokens
relevance_score: 0.96
run_id: materialize-outputs
language_code: en
---

# GST-VLA: Structured Gaussian Spatial Tokens for 3D Depth-Aware Vision-Language-Action Models

## Summary
GST-VLA proposes a VLA framework that compresses monocular depth and semantic features into 3D Gaussian spatial tokens, and adds a supervisable depth-aware chain of thought to explicitly reason about 3D geometry before action generation. The paper claims this structure is better suited than traditional 2D patch or scalar-depth representations for high-precision manipulation, and achieves higher success rates on LIBERO and SimplerEnv.

## Problem
- Existing VLA models typically use only 2D image patch tokens and lack explicit 3D geometry, surface orientation, and geometric confidence, causing fine-grained tasks such as grasping and insertion to fail more easily.
- Methods that only add dense depth maps still use “one scalar per pixel,” which cannot express local surface normals/curvature and also waste the token budget uniformly on irrelevant regions.
- The spatial reasoning process from vision to action is usually entirely implicit, lacking inspectable and supervisable intermediate 3D understanding steps.

## Approach
- Use a Gaussian Spatial Tokenizer to convert frozen semantic patch features and frozen monocular depth into 3D anisotropic Gaussian primitives; each token contains a 3D mean residual, 3-axis covariance, and opacity, representing position refinement, surface direction/shape, and geometric confidence, respectively.
- First construct a Gaussian field from 256 raw spatial tokens, then compress it to 128 tokens through learned spatial attention pooling, concentrating the fixed token budget on geometrically more important regions.
- Add Depth-Aware Chain-of-Thought to the VLM to explicitly generate four types of intermediate spatial reasoning outputs: 3D object grounding, grasp contact geometry, pairwise metric distances, and coarse SE(3) waypoints, and train them as supervised targets.
- During DA-CoT generation, every VLM layer can cross-attend to the uncompressed 256 raw Gaussian tokens, enabling direct querying of fine-grained geometric regions rather than relying only on the compressed representation.
- On the action side, a 300M-parameter flow-matching expert is used, conditioned simultaneously on VLM hidden states and DA-CoT outputs through dual cross-attention, to predict 10-step 7-DoF delta action chunks.

## Results
- The paper claims **96.4%** success on **LIBERO**, an improvement of **+2.0 percentage points** over the baseline.
- It reaches **80.2%** on **SimplerEnv**, an improvement of **+5.4 percentage points** over the baseline.
- Key GST component ablations: removing the residual mean \(\mu_k\) loses **1.9 percentage points**; changing anisotropic to isotropic covariance loses **1.6 percentage points**; fixing opacity at \(\alpha=1\) loses **1.5 percentage points**; replacing 3D Fourier positional encoding with 2D learned PE loses **2.8 percentage points**; replacing spatial attention pooling with average pooling loses **2.1 percentage points**.
- DA-CoT component ablations: removing 3D object grounding \(c_1\) loses **1.9 percentage points**; removing the SE(3) waypoint thought \(c_4\) loses **2.3 percentage points**, the largest effect among the four thoughts.
- Action expert ablations: removing the conditioning branch from DA-CoT action tokens loses **3.1 percentage points**; replacing the MoE feedforward with a single dense FFN loses **1.7 percentage points**.
- The authors also claim these gains are more concentrated on high-precision tasks, especially in grasp accuracy, collision avoidance, and overall task success rate, but the excerpt does not provide finer-grained per-task numbers.

## Link
- [http://arxiv.org/abs/2603.09079v1](http://arxiv.org/abs/2603.09079v1)
