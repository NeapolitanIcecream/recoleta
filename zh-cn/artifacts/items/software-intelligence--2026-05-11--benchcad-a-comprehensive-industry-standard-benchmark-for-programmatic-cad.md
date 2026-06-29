---
source: arxiv
url: https://arxiv.org/abs/2605.10865v2
published_at: '2026-05-11T17:13:36'
authors:
- Haozhe Zhang
- Kaichen Liu
- Miaomiao Chen
- Lei Li
- Shaojie Yang
- Cheng Peng
- Hanjie Chen
topics:
- programmatic-cad
- code-generation
- cad-benchmark
- multimodal-models
- engineering-automation
relevance_score: 0.86
run_id: materialize-outputs
language_code: zh-CN
---

# BenchCAD: A Comprehensive, Industry-Standard Benchmark for Programmatic CAD

## Summary
## 总结
BenchCAD 检验多模态模型能否把图像、代码和编辑指令转换成可执行、可编辑的工业 CAD 程序。基准结果显示，当前模型往往能匹配大致形状，但仍会遗漏工程细节、参数和 CAD 操作。

## 问题
- 工业 CAD 自动化需要可供工程师编辑、制造和检查的参数化程序，而不只是看起来相近的渲染形状。
- 现有 CAD 基准通常按端到端几何相似度打分，这会掩盖错误的操作、薄弱的参数恢复和较差的编辑表现。
- 这个差距很重要，因为齿轮、弹簧、钻头和紧固件等零件依赖标准尺寸、局部特征和操作选择。

## 方法
- BenchCAD 包含 17,900 个经过执行验证的 CadQuery 程序，覆盖 106 个命名的工业零件家族。
- 数据集里有 106 个家族中的 52 个以标准为锚定，对应 47 个 ISO、DIN、EN、ASME 或 IEC 代码。
- 它测试四项任务：图像到 CadQuery 生成、图像问答、代码问答和指令引导的代码编辑。
- 它使用多视角渲染、配对的图像/代码数值问答样本和人工筛选的编辑配对，用来区分视觉识别、CAD 操作理解、参数化抽象和代码合成。
- 其 CadQuery 覆盖 49 种操作，包括螺旋扫掠、放样、twistExtrude、polarArray 和参数化齿轮构造。

## 结果
- BenchCAD-QA 包含 2,400 个配对的图像/代码数值问答样本；BenchCAD-Edit 包含 748 对经过验证的编辑配对。
- 在视觉问答上，已报告的最佳总分是 Gemini 3.1 Pro 的 0.587，对比空白图像基线的 0.375。GPT-4o 得分 0.464，GPT-5.3 thinking 得分 0.514，Claude Opus 4.7 thinking 得分 0.530。
- 代码问答的最佳模型得分约为 0.838，而视觉问答最高只有 0.587，显示出从 CAD 代码读取信息和从渲染图推断同样信息之间有明显差距。
- 在 BenchCAD-Edit 上，GPT-5.3 thinking 的归一化准确率为 0.865，Claude Opus 4.7 thinking 为 0.853，Gemini 3.1 Pro thinking 为 0.837，GPT-4o 为 0.615，无修改基线为 0.000。
- 在 Vision2Code 上，摘录中报告的最强专有模型分数是 Gemini 3.1 Pro thinking，总分 0.318；CAD 专用模型的 IoU 很高，但会漏掉非挤出类操作。
- 在 BenchCAD 上进行微调和强化学习可以提升训练分布内的生成和操作覆盖，但摘录报告说，对留出的零件家族的泛化仍然有限，而不是给出单一的头条数字。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.10865v2](https://arxiv.org/abs/2605.10865v2)
