---
source: arxiv
url: http://arxiv.org/abs/2603.14191v1
published_at: '2026-03-15T03:01:13'
authors:
- Dectot--Le Monnier de Gouville Esteban
- Mohammad Hamdaqa
- Moataz Chouchen
topics:
- yara-rules
- threat-intelligence
- ecosystem-mining
- malware-detection
- detection-as-code
relevance_score: 0.42
run_id: materialize-outputs
---

# Mining the YARA Ecosystem: From Ad-Hoc Sharing to Data-Driven Threat Intelligence

## Summary
本文对开源 YARA 生态进行了首个大规模、数据驱动的系统刻画，显示其虽然被广泛用于“Detection as Code”，但整体更像陈旧、复制扩散的规则仓库，而非高质量情报源。研究结合仓库挖掘、静态分析与动态基准测试，揭示了中心化、滞后和检测有效性不足等系统性问题。

## Problem
- 论文解决的问题是：开源 YARA 规则生态长期依赖临时共享，但缺乏关于其结构、维护状态、传播机制和实际检测效果的系统证据。
- 这很重要，因为 YARA 已成为恶意软件检测和软件供应链防护的事实标准；如果共享规则过时、噪声高或覆盖偏斜，防御者会在 CI/CD 和安全运营中承担额外性能成本却得不到有效防护。
- 现有工作多关注单条规则质量、语法检查或自动生成，而没有从生态层面验证“公开规则库是否真的可靠可用”。

## Approach
- 作者对 **1,853 个 GitHub 仓库**中的 **840 万条规则**进行混合方法研究，构建了一个八阶段流水线来分析规则发现、提取、去重、传播、作者影响、质量和威胁覆盖。
- 他们先做仓库挖掘：从 GitHub 发现 YARA 项目、提取规则，并在 **10% 随机子集（约 84 万条）**上用 Plyara 交叉验证，报告与其正则提取结果 **100% 一致**。
- 为识别“逻辑相同但文本略有变化”的规则，论文使用 **ssdeep 模糊哈希**和层次聚类，在 **65% 相似度阈值**下聚合近重复规则，得到 **9.44 万个 unique rule logics**。
- 为分析生态传播，他们根据首次出现时间、first-publisher ratio 和 technical lag 区分“源仓库”与“镜像仓库”，衡量规则从创建到被其他仓库采纳的延迟。
- 为评估实际可靠性，他们把静态质量分数（yaraQA）与动态检测表现对照，并在 **4,026 个恶意样本**和 **2,000 个良性样本**上测试误报、召回和覆盖偏差。

## Results
- 数据规模上，论文分析了 **1,853 个仓库、840 万条规则**，最终聚合为 **9.44 万个唯一规则逻辑**，说明生态中存在大规模复制和冗余。
- 作者影响高度集中：**前 10 位作者驱动了 80% 的规则采纳**，表明生态不是分散协作网络，而是由少数关键节点主导的中心化供应链。
- 生态更新明显停滞：仓库的**中位不活跃时间为 782 天**，**中位 technical lag 为 4.2 年**，说明公开仓库更像静态归档而非持续更新的情报 feed。
- 静态质量表面上很高：规则的**平均静态质量分数为 99.4/100**；但动态基准测试显示这与真实效果脱节，作者明确声称存在**显著误报（false positives）和低召回（low recall）**。
- 覆盖分布存在明显偏差：规则更偏向**Ransomware**等传统高曝光威胁，而对现代初始入侵向量如 **Loaders** 和 **Stealers** 的覆盖**严重不足**。
- 在方法验证上，ssdeep 阈值调优后的近重复检测在对抗性基准上达到 **F1 = 0.77**；规则提取在 **10% 子集**上与正式解析器达到 **100% agreement**。论文未在给定摘录中提供更细的误报率、召回率或按数据集分层的完整数值对比。

## Link
- [http://arxiv.org/abs/2603.14191v1](http://arxiv.org/abs/2603.14191v1)
