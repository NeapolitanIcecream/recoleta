---
source: hn
url: https://www.theregister.com/2026/03/14/cortical_labs_biological_cloud/
published_at: '2026-03-14T22:43:59'
authors:
- spzb
topics:
- biological-computing
- neuromorphic-cloud
- brain-computer-interface
- wetware-systems
- experimental-computing
relevance_score: 0.17
run_id: materialize-outputs
language_code: zh-CN
---

# The datacenter where the day starts with topping up cerebrospinal fluid

## Summary
这篇文章介绍了 Cortical Labs 将由活体神经元驱动的生物计算设备 CL1 组成云服务，使外部用户可通过 API、Jupyter Notebook 和 Python 代码远程访问这类新型计算资源。其意义在于把仍然高度实验性的生物计算，从实验室演示推进到可租用的基础设施阶段。

## Problem
- 文章要解决的问题是：**生物计算虽然被宣称具备学习能力、潜在低能耗和不同于传统 AI 的计算特性，但目前极难获取、部署和维护，外部研究者几乎无法实际使用。**
- 这很重要，因为若没有类似云平台的交付方式，生物计算将停留在少数实验室内部，无法形成可重复实验、应用探索和产业生态。
- 另一个核心障碍是供应链和运维：细胞来源稀缺、需要定制细胞系，还要持续管理液体、氧气、氮气和二氧化碳等生存环境。

## Approach
- Cortical Labs 将其 CL1 生物计算机集中部署在数据中心中，构建了一个“biological cloud”，让用户像调用云算力一样提交作业。
- 每台机器以放置在高密度多电极阵列上的生物神经网络为核心，通过**电刺激与电信号记录**把硅基系统和活体神经元连接起来，简单说就是“用电子设备向神经元发信号，再读回神经元的反应”。
- 用户侧接口被做成更熟悉的软件形态：可创建 Jupyter Notebook 或上传 Python 代码，通过 API 在生物计算设备上运行实验。
- 运行前需要按任务准备特定细胞系，并人工维护“类脑脊液”营养液与约 **5% 氧气** 的气体环境；目前每个任务的准备周期约 **一周**。
- 其技术来源可追溯到 2022 年论文《In vitro neurons learn and exhibit sentience when embodied in a simulated game-world》，该工作展示了体外神经元学习玩 Pong，后续被工程化为 CL1，并进一步用于学习玩 DOOM。

## Results
- 文章本身**没有提供严格的基准测试表或同行评审的量化云性能数据**，因此无法确认其相对传统计算的实际吞吐、准确率或成本优势。
- 明确披露的基础设施规模是：Cortical Labs 已经部署了 **120 台 CL1 单元** 组成云服务。
- 明确披露的运维参数包括：营养液**每 24 小时更换/补充一次**；设备周围气体环境维持在约 **5% 氧气**；每个用户作业的机器准备时间约 **1 周**。
- 典型用户配置上，公司称多数用户会租用 **3 到 4 台 CL1**，以便做重复实验和设置对照组。
- 文章引用的既有能力展示是：2022 年论文中的体外神经元系统学会了玩 **Pong**；Cortical Labs 后续声称其机器还学会了玩 **DOOM**，但本文未给出分数、样本效率或与经典算法/LLM 的定量对比。
- 公司层面的 strongest claims 是：神经元可在模拟环境中学习并形成新策略，可能比经典计算机学习更快、比传统数据中心更省能，并且不只是像 LLM 那样重组已有信息；但这些主张在本文摘录中**没有量化证据支撑**。

## Link
- [https://www.theregister.com/2026/03/14/cortical_labs_biological_cloud/](https://www.theregister.com/2026/03/14/cortical_labs_biological_cloud/)
