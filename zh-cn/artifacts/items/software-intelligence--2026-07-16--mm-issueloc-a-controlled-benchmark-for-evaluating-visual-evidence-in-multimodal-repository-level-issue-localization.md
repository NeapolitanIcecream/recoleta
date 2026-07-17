---
source: arxiv
url: https://arxiv.org/abs/2607.15205v1
published_at: '2026-07-16T17:02:25'
authors:
- Shaoxiong Zhan
- Shi Hu
- Boyu Feng
- Hai Lin
- Andrew Gong
- Zhengda Zhou
- Jiaying Zhou
- Yunyun Hou
- Hao Su
- Hai-Tao Zheng
topics:
- code-intelligence
- automated-software-production
- multimodal-reasoning
- repository-search
- software-engineering-benchmarks
relevance_score: 0.86
run_id: materialize-outputs
language_code: zh-CN
---

# MM-IssueLoc: A Controlled Benchmark for Evaluating Visual Evidence in Multimodal Repository-Level Issue Localization

## Summary
## 摘要
MM-IssueLoc 提出了一项受控基准，用于衡量视觉证据是否能帮助系统在真实软件仓库中定位相关文件和函数。该基准通过成对的纯文本评测与图像条件评测，将定位与补丁生成分离开来。

## 问题
- 现有的仓库级软件工程基准主要基于文本，而真实问题通常包含屏幕截图、错误对话框、渲染状态和日志。
- 多模态修复基准将定位与补丁合成结合在一起，因此无法说明图像是否改善了定位，或是否被系统忽略。
- 这一点很重要，因为定位错误会进一步影响自动补丁生成和问题解决。

## 方法
- 从关联的 GitHub issue 和修复 pull request 构建基准，使用修复前的仓库快照，为 652 个实例提供文件级金标准标签，为 343 个实例提供函数级标签。
- 按七种证据类别和四个相关性等级标注 1,050 张图像，其中包括一个由人工审查、包含 55 个实例的有害图像压力测试集。
- 比较纯文本、原始图像、视觉内容证据（Visual Content Evidence，VCE）以及 VCE 加图像模式。VCE 将图像转换为结构化文本，其中包含 OCR、错误信号、界面元素和代码提示等字段。
- 使用严格的 Acc@K 指标评估 LLM 代理和检索器；MM-IssueLoc-VL-Embedding 检索器采用对比学习、困难负样本和文件到函数的训练课程。

## 结果
- 在 652 个文件级实例上，最强的总体结果来自使用 GPT-5.2 的 OpenHands，其 File Acc@5 为 38.96；其 File Acc@1 和 Acc@3 分数分别为 23.93 和 36.35。
- 在 343 个函数级实例上，MM-IssueLoc-VL-Embedding-8B 取得了最佳检索结果，Function Acc@10 为 33.86；最强代理的得分为 22.45。
- 移除图像后，2B 受控检索器的 File Acc@5 下降 4.91 个百分点，8B 版本下降 4.44 个百分点；图像对代理的影响则更小且不一致。
- 在困难的多编辑问题上，性能大幅下降：OpenHands GPT-5.2 在简单实例上的 Acc@10 为 83.10，在困难实例上降至 2.84；8B 检索器则从 74.18 降至 3.98。
- 以文本为主的基准表现无法直接迁移：OpenHands 在 SWE-bench-Lite 上的 File@5 为 94.53，在 SWE-bench-Verified 上为 90.20，而 SWE-bench-MM 上最佳系统的得分为 43.14。
- 文中同时报告了 23 种和 24 种编程语言，以及 608 个仓库和 650 个仓库快照；这一统计差异不改变基准的核心规模，但限制了对数据集范围的精确解读。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2607.15205v1](https://arxiv.org/abs/2607.15205v1)
