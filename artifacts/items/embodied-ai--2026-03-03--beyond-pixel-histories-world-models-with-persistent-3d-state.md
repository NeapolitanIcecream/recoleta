---
source: arxiv
url: http://arxiv.org/abs/2603.03482v1
published_at: '2026-03-03T19:58:31'
authors:
- Samuel Garcin
- Thomas Walker
- Steven McDonagh
- Tim Pearce
- Hakan Bilen
- Tianyu He
- Kaixin Wang
- Jiang Bian
topics:
- world-model
- persistent-3d-state
- interactive-video-generation
- 3d-consistency
- spatial-memory
relevance_score: 0.85
run_id: materialize-outputs
---

# Beyond Pixel Histories: World Models with Persistent 3D State

## Summary
PERSIST提出一种带有**持久化3D潜状态**的交互式世界模型，不再只依赖像素历史来续写视频。它把“记忆”放进会随时间演化的3D场景表示中，从而提升长时程生成中的空间一致性、几何一致性与稳定性。

## Problem
- 现有交互式视频/世界模型通常基于自回归像素历史，受限于上下文窗口，只能记住几秒钟的过去，长序列中容易遗忘已见区域。
- 像素是视角相关、信息冗余且局部可见的，靠检索关键帧来恢复3D世界状态越来越难，导致回访场景时几何不一致、空间记忆差。
- 这会直接影响沉浸式交互体验，也妨碍把世界模型作为训练智能体的可靠模拟器。

## Approach
- 核心思路：显式维护一个**持续演化的3D latent world state**，把世界建模拆成三部分：3D世界帧预测、相机状态预测、以及从3D到像素的渲染生成。
- 世界帧模型在体素化的3D latent空间里预测环境如何随动作变化；相机模型预测代理视角；随后把3D世界投影到屏幕，形成按深度排序的2D特征栈。
- 像素生成器把这些投影后的3D特征当作主要条件输入，像“可学习的deferred renderer/shader”一样生成当前帧，从而把几何一致性显式注入视频生成。
- 训练上使用rectified flow / diffusion-forcing来做自回归生成，并加入噪声增强以减轻训练时真值条件、推理时模型预测条件之间的曝光偏差。
- 重要的是，推理时可仅由单张RGB图像初始化；虽然训练用到了3D世界帧和相机监督，但测试时不必依赖真实3D条件。

## Results
- 在Craftium/Luanti程序化3D世界上训练，数据规模约**4000万次交互、10万条轨迹、460小时、24Hz**；评测使用**148条**来自未见测试世界的轨迹。
- 相比基线**Oasis**与**WorldMem**，PERSIST在FVD上大幅更优：**PERSIST-S 209**、**PERSIST-XL 181**、**PERSIST-XL+w0 116**，而**Oasis 706**、**WorldMem 596**。这表明长时程视频分布质量明显提升。
- 用户研究（1-5分）显示空间/时间/整体质量全面更好：例如**Overall Score**从**Oasis 1.9±0.1**、**WorldMem 1.5±0.07**提升到**PERSIST-S 2.6±0.09**、**PERSIST-XL 2.6±0.08**，若给定初始3D世界帧则达**3.0±0.1**。
- 在**3D Consistency**上，**Oasis 1.9±0.1**、**WorldMem 1.7±0.09**，而**PERSIST-S 2.7±0.1**、**PERSIST-XL+w0 2.8±0.1**；在**Temporal Consistency**上，**Oasis 1.8±0.1**、**WorldMem 1.5±0.08**，而PERSIST达到**2.5-2.8**。
- 论文还声称实现了新的能力：可从**单张图像**合成多样3D环境、支持**600步**自回归长序列、可直接在3D空间做场景编辑，并能维持屏幕外动态过程继续演化。
- 除表1外，摘录中未提供更多细粒度任务成功率数字；最强结论是：显式持久化3D状态显著优于滚动窗口和记忆检索式像素基线。

## Link
- [http://arxiv.org/abs/2603.03482v1](http://arxiv.org/abs/2603.03482v1)
