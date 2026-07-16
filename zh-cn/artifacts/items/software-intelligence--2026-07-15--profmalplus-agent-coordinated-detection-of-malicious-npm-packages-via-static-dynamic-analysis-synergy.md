---
source: arxiv
url: https://arxiv.org/abs/2607.13965v1
published_at: '2026-07-15T15:52:11'
authors:
- Yiheng Huang
- Zhijia Zhao
- Bihuan Chen
- Susheng Wu
- Zhuotong Zhou
- Yiheng Cao
- Kun Hu
- Xin Hu
- Xin Peng
topics:
- code-intelligence
- software-supply-chain-security
- malware-detection
- multi-agent-software-engineering
- static-dynamic-analysis
relevance_score: 0.88
run_id: materialize-outputs
language_code: zh-CN
---

# ProfMalPlus: Agent-Coordinated Detection of Malicious NPM Packages via Static-Dynamic Analysis Synergy

## Summary
## 摘要
ProfMalPlus 结合对象敏感的行为图、源代码级代码切片、静态与动态证据以及协同工作的 LLM 代理来检测恶意 NPM 软件包。论文报告了较强的基准测试和现实场景结果，包括 98.1% 的 F1 分数，以及在为期三个月的监测中识别出 597 个此前未知的恶意软件包。

## 问题
- 恶意 NPM 软件包威胁软件供应链，而软件包注册表的规模使人工检查难以开展。
- 现有检测器可能漏掉经过混淆处理或通过对象介导的 JavaScript 行为，无法有效结合静态与动态证据，并且只能提供有限的解释或代码定位信息。

## 方法
- 脚本分析器检查安装命令，并识别安装时和导入时执行的文件。
- 对象敏感的静态分析器构建行为图，其中包含控制流、控制依赖、数据依赖、敏感 API、第三方调用和未解析调用；代码切片器将可疑的图区域转换为保留源代码结构并带有注释的切片。
- 本地判断代理评估代码切片，全局判断代理汇总各切片的结果；一致性自检则减少多次 LLM 判断之间的差异。
- 当证据不足时，路由代理会选择基于注册表的第三方信息增强或沙箱动态增强，然后重复推理过程。
- 定位代理将确认的恶意行为映射到具体代码片段，并生成解释。

## 结果
- ProfMalPlus 获得了 98.1% 的 F1 分数，在评估的检测器中表现最佳；相比先进系统，其结果高出 3.5 至 52.6 个百分点。
- 其行级恶意代码定位 F1 分数为 88.9%；在抽样的恶意软件包中，有 86.9% 的解释被评为高质量。
- 在为期三个月的监测中新发布的 NPM 软件包期间，它检测出 597 个此前未知的恶意软件包；论文称这些软件包均已得到确认并从 NPM 中移除。
- 报告的现实场景误报率为 16.5%，在比较的检测器中最低。
- 摘要未说明基准数据集的规模，也未说明所报告 F1 分数比较背后的确切实验方案，因此仅凭所提供的文本无法对这些结果进行独立的背景化解读。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2607.13965v1](https://arxiv.org/abs/2607.13965v1)
