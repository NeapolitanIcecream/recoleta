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
## 摘要
BenchCAD 测试多模态模型能否把图像、代码和编辑指令转成可执行、可编辑的工业 CAD 程序。该基准显示，当前模型通常能匹配粗略形状，但仍会漏掉工程细节、参数和 CAD 操作。

## 问题
- 工业 CAD 自动化需要工程师可编辑、可制造、可检查的参数化程序，不能只生成外观看起来接近的渲染形状。
- 现有 CAD 基准通常按端到端几何相似度评分，这可能掩盖错误操作、参数恢复能力弱和编辑表现差等问题。
- 这个差距会影响齿轮、弹簧、钻头和紧固件等零件，因为这些零件依赖标准尺寸、局部特征和操作选择。

## 方法
- BenchCAD 包含 17,900 个经过执行验证的 CadQuery 程序，覆盖 106 个具名工业零件族。
- 数据集在 106 个零件族中包含 52 个基于标准的零件族，关联 47 项 ISO、DIN、EN、ASME 或 IEC 规范。
- 它测试四项任务：图像到 CadQuery 生成、图像问答、代码问答和指令引导的代码编辑。
- 它使用多视角渲染、成对的图像/代码数值问答项和人工整理的编辑对，用于区分视觉识别、CAD 操作理解、参数化抽象和代码合成能力。
- 它的 CadQuery 覆盖 49 种操作，包括螺旋扫掠、放样、twistExtrude、polarArray 和参数化齿轮构造。

## 结果
- BenchCAD-QA 有 2,400 个成对的图像/代码数值问答项；BenchCAD-Edit 有 748 个经过验证的编辑对。
- 在 Vision QA 上，报告的最高总分是 Gemini 3.1 Pro 的 0.587，相比之下空白图像基线为 0.375。GPT-4o 得分 0.464，GPT-5.3 thinking 得分 0.514，Claude Opus 4.7 thinking 得分 0.530。
- 最佳模型在 Code QA 上约为 0.838，而 Vision QA 最高为 0.587，说明读取 CAD 代码与从渲染图推断相同信息之间存在较大差距。
- 在 BenchCAD-Edit 上，GPT-5.3 thinking 的归一化准确率为 0.865，Claude Opus 4.7 thinking 为 0.853，Gemini 3.1 Pro thinking 为 0.837，GPT-4o 为 0.615，无改动基线为 0.000。
- 在 Vision2Code 上，摘录中报告的最强闭源模型分数是 Gemini 3.1 Pro thinking，总分 0.318；CAD 专用模型取得较好的 IoU，但会漏掉非挤出操作。
- 在 BenchCAD 上进行微调和强化学习能提升分布内生成表现和操作覆盖率，但摘录报告的是对留出零件族的泛化能力有限，而非单一核心数字。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.10865v2](https://arxiv.org/abs/2605.10865v2)
