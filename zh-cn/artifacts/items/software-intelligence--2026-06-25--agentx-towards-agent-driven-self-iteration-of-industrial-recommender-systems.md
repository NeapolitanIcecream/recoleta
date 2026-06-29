---
source: arxiv
url: https://arxiv.org/abs/2606.26859v1
published_at: '2026-06-25T10:42:28'
authors:
- Changxin Lao
- Fei Pan
- Guozhuang Ma
- Han Li
- Huihuang Lin
- Jijun Shi
- Kangzhi Zhao
- Kun Gai
- Mo Zhou
- Qinqin Zhou
- Quan Chen
- Ruochen Yang
- Shifu Bie
- Shuang Yang
- Shuo Yang
- Wenhao Li
- Wentao Xie
- Xiao Lv
- Xuming Wang
- Yijun Wang
- Yiming Chen
- Yusheng Huang
- Zhongyuan Wang
- Zibo Zhao
- Zijie Zhuang
- Baoning Xia
- Chao Liu
- Chaoyi Ma
- Chubo He
- Dawei Cong
- Feng Jiang
- Gang Wang
- Guilin Xia
- Hanwen Xu
- Jiahong Xie
- Jiahui Qiao
- Jian Liang
- Jiangfan Yue
- Jing Wang
- Jinghan Yang
- Jinghui Jia
- Kan Qin
- Lei Wang
- Ming Li
- Peilin Song
- Pengbo Xu
- Qiang Luo
- Ruiming Tang
- Shiyang Liu
- Shuxian Jin
- Tao Wang
- Tao Zhang
- Xiang Gao
- Xianghan Li
- Yingsong Luo
- Yiwen Ning
- Yongcheng Liu
- Yuan Guo
- Zhaojie Liu
- Zhenkai Cui
topics:
- agentic-recsys
- multi-agent-systems
- automated-code-generation
- online-ab-testing
- recommender-systems
- self-improving-agents
relevance_score: 0.86
run_id: materialize-outputs
language_code: zh-CN
---

# AgentX: Towards Agent-Driven Self-Iteration of Industrial Recommender Systems

## Summary
## 概要
AgentX 是一个已在生产环境部署的多智能体系统，负责运行推荐实验，覆盖从生成想法、修改代码、A/B 发布到从结果中学习的流程。快手报告称，3 个 worker 在三周部署中从 374 个想法产出 10 个可上线发布，并带来 0.561% 的 App 使用时长提升。

## 问题
- 工业推荐系统迭代依赖工程师提出假设、修改代码、发起 A/B 实验并做归因，因此实验吞吐量随人力规模增长。
- 离线 ML-agent 测试无法提供推荐变更所需的在线奖励信号；一次变更必须通过实时业务指标和安全护栏。
- 这个瓶颈会带来实际影响，因为发布周期可能需要数周；如果反复失败和上线评审没有存为可复用的实验记录，其价值会流失。

## 方法
- AgentX 使用四阶段闭环：Brainstorm Agent 对有证据支撑的提案排序，Developing Agent 修改基于代码仓库上下文的生产代码，Evaluation Agent 管理发布和 A/B 判断，Harness Evolution 根据执行轨迹更新智能体指令。
- Brainstorm Agent 从 Experiment KB、System KB、Data Analysis 和 Model Research 提取证据，然后按目标一致性、业务有效性、可行性、交接完整性、证据和风险对候选方案评分。
- Developing Agent 使用代码仓库上下文、验证循环和质量评分，将已接受的提案转化为上线前代码。
- Evaluation Agent 安全分配流量，对 A/B 结果应用护栏否决机制，并将成功和失败都存为可复用的知识资产。
- Harness Evolution 使用基于语义梯度的提示优化（SGPO），把成功和失败轨迹转换为提示词和智能体规格更新；变更被接受前会经过配对回放。

## 结果
- 在快手 App 主信息流和生活服务推荐的三周部署中，3 个 AgentX worker 生成了 374 个想法和 10 个可上线发布。
- 论文称，在自演化更新后，部署期间每个 worker 的吞吐量每周翻倍。
- 与人工工程师基线相比，AgentX 声称并发能力提升 8 倍，业务价值提升 3.7 倍。
- 报告的在线业务影响是用户 App 使用时长提升 0.561%，年化收入超过人民币 1 亿元。
- 论文还称，同一闭环可支持模型侧研究任务，例如论文复现、模块消融和跨论文架构组合，但摘录没有提供这些任务的完整定量结果。
- 评估信号是带护栏否决的在线 A/B 反馈；摘录没有包含统计置信区间或完整消融表。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.26859v1](https://arxiv.org/abs/2606.26859v1)
