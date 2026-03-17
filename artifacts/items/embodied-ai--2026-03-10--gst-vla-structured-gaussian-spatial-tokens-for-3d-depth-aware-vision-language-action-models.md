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
---

# GST-VLA: Structured Gaussian Spatial Tokens for 3D Depth-Aware Vision-Language-Action Models

## Summary
GST-VLA提出一种把单目深度和语义特征压缩成3D高斯空间token的VLA框架，并加入可监督的深度感知思维链，以在动作生成前显式推理3D几何。论文声称这种结构比传统2D patch或标量深度表示更适合高精度操作，并在LIBERO和SimplerEnv上取得更高成功率。

## Problem
- 现有VLA通常只用2D图像patch token，缺少显式3D几何、表面朝向和几何置信度，导致精细抓取、插入等高精度任务容易失败。
- 仅加入稠密深度图的方法仍是“每像素一个标量”，不能表达局部表面法向/曲率，也会把token预算平均浪费在无关区域。
- 从视觉到动作的空间推理过程通常完全隐式，缺少可检查、可监督的中间3D理解步骤。

## Approach
- 用Gaussian Spatial Tokenizer把冻结的语义patch特征和冻结单目深度转换成3D各向异性高斯原语；每个token包含3D均值残差、3轴协方差和不透明度，分别表达位置细化、表面方向/形状、几何置信度。
- 先从256个raw spatial tokens构造高斯场，再通过learned spatial attention pooling压缩到128个token，把固定token预算集中到几何上更重要的区域。
- 在VLM中加入Depth-Aware Chain-of-Thought，显式生成四类中间空间推理结果：3D目标定位、抓取接触几何、物体间度量距离、粗SE(3)路径点，并把它们作为监督目标训练。
- 在DA-CoT生成时，每层VLM都可交叉注意到未压缩的256个raw Gaussian tokens，从而直接查询细粒度几何区域，而不是只依赖压缩后的表示。
- 动作端使用300M参数的flow-matching专家，通过双重cross-attention同时条件于VLM隐藏状态和DA-CoT输出，预测10步7-DoF delta action chunks。

## Results
- 论文声称在**LIBERO**上达到**96.4%**成功率，较基线提升**+2.0个百分点**。
- 在**SimplerEnv**上达到**80.2%**，较基线提升**+5.4个百分点**。
- 关键GST组件消融：去掉残差均值\(\mu_k\)损失**1.9个百分点**；各向异性改成各向同性协方差损失**1.6个百分点**；固定不透明度\(\alpha=1\)损失**1.5个百分点**；3D Fourier位置编码改成2D learned PE损失**2.8个百分点**；spatial attention pooling改成平均池化损失**2.1个百分点**。
- DA-CoT组件消融：去掉3D object grounding \(c_1\)损失**1.9个百分点**；去掉SE(3) waypoint thought \(c_4\)损失**2.3个百分点**，为四个thought中影响最大。
- 动作专家消融：移除来自DA-CoT action tokens的条件分支损失**3.1个百分点**；MoE前馈改为单一dense FFN损失**1.7个百分点**。
- 作者还声称这些收益在高精度任务上更集中，尤其体现在抓取精度、避碰和整体任务成功率，但摘录中未给出更细分的逐任务数字。

## Link
- [http://arxiv.org/abs/2603.09079v1](http://arxiv.org/abs/2603.09079v1)
