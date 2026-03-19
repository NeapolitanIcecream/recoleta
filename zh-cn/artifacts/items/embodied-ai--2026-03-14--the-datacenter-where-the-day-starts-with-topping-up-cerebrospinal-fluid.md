---
source: hn
url: https://www.theregister.com/2026/03/14/cortical_labs_biological_cloud/
published_at: '2026-03-14T22:43:59'
authors:
- spzb
topics:
- biological-computing
- neuromorphic-cloud
- in-vitro-neurons
- brain-computer-interface
relevance_score: 0.08
run_id: materialize-outputs
language_code: zh-CN
---

# The datacenter where the day starts with topping up cerebrospinal fluid

## Summary
这篇文章介绍了 Cortical Labs 将基于活体神经元的“生物计算机”做成可租用云服务的尝试。其核心卖点是：让培养神经元在模拟环境中学习任务，并通过 API 像云算力一样被远程调用。

## Problem
- 文章要解决的问题是：如何把目前高度实验性、依赖细胞培养和人工维护的生物计算，变成外部用户可访问的计算平台。
- 这很重要，因为公司声称生物神经元可能比传统计算机更快学会某些模拟任务、能耗更低，并可能产生更“原创”的策略，而不只是像 LLM 一样重组已有信息。
- 当前瓶颈在于生物计算基础设施极不成熟：需要特定细胞来源、每天更换类似脑脊液的培养液、调节气体环境，而且行业还缺少类似“cell foundry/TSMC”的标准化供给体系。

## Approach
- Cortical Labs 将人类和啮齿类干细胞培养出的生物神经网络放在高密度多电极阵列上，让硅基系统通过电刺激与电记录和神经元双向交互。
- 最简单地说，方法就是：把活神经元接到电子接口上，把模拟环境状态编码成电信号输入给它们，再把它们的放电活动读出来作为动作输出，让它们在闭环中学习任务。
- 公司把这一思路产品化为 CL1 设备，并进一步“云化”：部署了 120 台 CL1，提供 API、Jupyter Notebook 和 Python 代码上传接口，让用户远程在生物计算机上运行实验。
- 每次作业前仍需按客户需求准备细胞系，并配置氧气、氮气、二氧化碳和营养液环境；文章称通常用户会租 3–4 台机器用于重复实验和对照。
- 文中还将该平台与 2022 年论文的方法关联起来：该论文展示了体外神经元在模拟游戏世界中学习 Pong，后续又被公司扩展到学习 DOOM，并最终形成 CL1 产品。

## Results
- 基础设施层面：公司已在墨尔本数据中心部署 **120 台 CL1**，并开放云访问接口；这是文中最具体的产品化规模数据。
- 运维层面：培养液需要 **每 24 小时**更换一次，工作气氛维持在约 **5% 氧气**；为每个客户任务准备机器约需 **1 周**。
- 使用方式层面：公司称多数用户会租用 **3–4 台** CL1，以便做重复实验和控制组。
- 能力声明层面：文章引用 2022 年论文称体外神经元已学会玩 **Pong**，并提到公司后来展示其机器学会玩 **DOOM**；但本文未提供这些任务的定量指标、数据集分数、基线比较或统计显著性结果。
- 性能声明层面：CEO 声称这类系统能比经典计算机“更快”学会模拟环境中的挑战，并且比传统数据中心更省电，但本文没有给出可核验的数值结果或实验对照。

## Link
- [https://www.theregister.com/2026/03/14/cortical_labs_biological_cloud/](https://www.theregister.com/2026/03/14/cortical_labs_biological_cloud/)
