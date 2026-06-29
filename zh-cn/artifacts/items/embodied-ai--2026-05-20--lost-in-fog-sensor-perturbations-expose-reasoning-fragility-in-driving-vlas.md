---
source: arxiv
url: https://arxiv.org/abs/2605.21446v1
published_at: '2026-05-20T17:34:02'
authors:
- Abhinaw Priyadershi
- Jelena Frtunikj
topics:
- vision-language-action
- autonomous-driving
- sensor-corruption
- chain-of-causation
- runtime-monitoring
- planning-safety
relevance_score: 0.62
run_id: materialize-outputs
language_code: zh-CN
---

# Lost in Fog: Sensor Perturbations Expose Reasoning Fragility in Driving VLAs

## Summary
## 总结
这篇论文在摄像头噪声、光照变化和雾天条件下测试了 10B 参数的驾驶 VLA 模型 Alpamayo R1。论文认为，模型链式因果解释的变化，是轨迹大幅偏移的强预警信号。

## 问题
- 驾驶 VLA 可以解释自己的计划，但这些解释在摄像头受到雾、眩光、黑暗或传感器噪声影响时可能会变化。
- 这很重要，因为规划器可能输出看起来合理的文本，但预测轨迹会偏移，这会给自动驾驶验证带来安全问题。

## 方法
- 作者在 1,996 个 PhysicalAI 自动驾驶验证场景上评估 Alpamayo R1。
- 他们施加了 8 种同步多摄像头扰动：高斯噪声 σ=10、30、50、70，亮度 0.4× 和 1.6×，以及雾度 α=0.3 和 0.7。
- 他们运行了大约 18,000 次推理试验，并用 ADE、ADE 增量、L2 轨迹偏差和 CoC 精确匹配变化率比较干净输入与受扰动输出。
- 他们还做了一个 CoC 抑制消融实验，除 token budget 外，使用相同的 checkpoint 和解码设置，因此因果结论的范围有限。

## 结果
- 在干净输入上，Alpamayo R1 的 ADE 为 2.00 m，基线恒速模型为 6.32 m，在 1,996 个样本上下降 68.3%，p<10^-257。
- 当扰动后 CoC 解释发生变化时，平均 L2 轨迹偏差为 21.82 m；当解释保持不变时为 4.13 m，相差 5.3 倍；中位偏差分别为 15.39 m 和 2.16 m，相差 7.1 倍。
- 在全部 15,968 对受攻击样本中，CoC 变化与轨迹偏差的点二列相关系数 r=0.53，Cohen's d=1.12，p<10^-100；在 8 种攻击类型上，汇总相关系数 r=0.99。
- 噪声退化在 σ=10、30、50、70 上几乎线性上升，R²=0.957，斜率为每个 σ 单位增加 0.0048 m ADE；轨迹偏移超过 5 m 的比例从 σ=10 时的 18.8% 升至 σ=70 时的 70.6%。
- 最高测试噪声 σ=70 是最强的失真：ADE 升至 2.30 m，ΔADE 为 +0.30 m，52.7% 的样本出现 CoC 变化，p=2×10^-17。
- CoC 消融结果显示，在测试条件下启用 CoC 生成时，ADE 平均改善 11.8%，p<0.0001；常规预处理防御只带来很小、统计上较弱的改善。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.21446v1](https://arxiv.org/abs/2605.21446v1)
