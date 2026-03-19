---
source: arxiv
url: http://arxiv.org/abs/2603.02194v1
published_at: '2026-03-02T18:54:28'
authors:
- Mateus Karvat
- Bram Adams
- Sidney Givigi
topics:
- code-quality
- autonomous-vehicles
- static-analysis
- software-security
- production-readiness
relevance_score: 0.78
run_id: materialize-outputs
language_code: zh-CN
---

# From Leaderboard to Deployment: Code Quality Challenges in AV Perception Repositories

## Summary
这篇论文研究自动驾驶感知模型代码库从“榜单高分”走向“可部署系统”时面临的软件质量鸿沟。作者对 178 个 KITTI 与 NuScenes 榜单仓库做了大规模静态分析，发现多数代码在错误、安全和可维护性上远未达到生产要求。

## Problem
- 论文要解决的问题是：**高榜单精度的 AV 感知代码库，是否真的具备生产部署与长期维护能力**；这很重要，因为自动驾驶属于安全关键系统，代码缺陷会直接影响真实道路安全与合规。
- 现有评测几乎只看检测精度，不衡量代码错误、安全漏洞、CI/CD、可维护性等工程质量，因此研究代码与工业部署之间存在明显断层。
- 此前缺少针对公开 AV 感知研究仓库的**大规模、系统性**软件质量实证分析。

## Approach
- 作者从 KITTI 和 NuScenes 3D 目标检测榜单收集并清洗仓库，最终得到 **178 个唯一代码库**，规模范围 **600 到 184.9k SLOC**。
- 用三类静态分析工具做评估：**Pylint** 查代码错误，**Bandit** 查安全漏洞，**Radon** 算 SLOC 和可维护性指标 **MI**。
- 他们把“生产就绪”简单定义为：**0 个关键错误 + 0 个高危安全漏洞**，并据此统计每个仓库是否达标。
- 进一步分析代码规模、错误数、漏洞数、MI、GitHub 指标、团队规模、测试与 **CI/CD** 采用情况之间的相关关系。
- 对最常见的 5 类安全问题提炼出预防指南，重点包括 **unsafe torch.load、silent exception suppression、shell injection、eval、unsafe yaml load** 等模式。

## Results
- **生产就绪率仅 7.3%（13/178）**；按结论部分口径，**仅 2.8%** 仓库完全无错误，**6.7%** 完全无安全漏洞，说明榜单表现与部署准备度明显脱钩。
- **97.2%** 的仓库至少有一个错误；错误中位数 **29**、均值 **55.7**、范围 **0–1,263**。Pylint 共识别 **1,612** 个错误，其中 **1,424** 个为关键错误，**90.4%** 仓库至少有一个关键错误。
- **93.3%** 的仓库至少有一个安全问题；漏洞中位数 **9**、范围 **0–62**。Bandit 共发现 **2,031** 个安全问题，其中 **403 个高危（19.8%）**、**1,180 个中危（58.1%）**、**448 个低危（23.1%）**；**51.7%** 的仓库含高危漏洞。
- 安全问题高度集中：前 **5** 类问题占 **79.3%** 的全部漏洞。最常见的是 **B614 unsafe PyTorch load：713 次、影响 144 个仓库（80.9%）**；其后包括 **B110 try-except-pass：273 次（38.8%）**、**B605 shell injection：239 次（44.4%）**、**B307 eval：222 次（59.6%）**、**B602 shell=True：163 次（15.7%）**。
- 仓库越大，问题越多：**错误数与 SLOC 的 Spearman ρ=0.453，p=0.0000**；**安全问题数与 SLOC 的 ρ=0.607，p=0.0000**。可维护性越高，安全问题密度越低：**MI 与安全问题密度 ρ=-0.547，p=0.0000**；与错误密度也负相关：**ρ=-0.397，p<0.001**。
- **CI/CD 仅被 7.3% 仓库采用**，但采用者的平均可维护性更高：**MI 73.0 vs 65.9**，**Mann-Whitney U=429, p=0.0003, r=0.600**。同时，GitHub stars 与错误数**无显著相关**（**ρ=0.04, p=0.56**），说明“受欢迎”不等于“可部署”。

## Link
- [http://arxiv.org/abs/2603.02194v1](http://arxiv.org/abs/2603.02194v1)
