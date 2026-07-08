---
source: arxiv
url: https://arxiv.org/abs/2607.05471v1
published_at: '2026-07-06T08:14:02'
authors:
- Bo Huang
- Fengxiang Li
- Hao Xu
- Haoyang Huang
- Hongyi Fu
- Jinhua Hao
- Kun Yuan
- Minglei Zhang
- Pengcheng Xu
- Shiyang Liu
- Wenhao Zhuang
- Yuze Shi
- Zongxian Feng
- Chao Wang
- Cheng He
- Chongling Rao
- Deyu Cao
- Fan Yang
- Gang Xiong
- Haochen Liu
- Jiabao Li
- Jian Liang
- Jinghui Jia
- Jingwen Chang
- Jun Du
- Junyu Shi
- Min Li
- Mingqi Wu
- Qiang Gao
- Shangpeng Yan
- Shaotong Qi
- Shu Xu
- Shuo Zhou
- Tiankuo Xu
- Tong Zheng
- Weilun Zhao
- Xiancheng Meng
- Xianda Sun
- Xiaoyu Jiang
- Xunhao Jia
- Yao Xia
- Yimeng Xu
- Yinghan Cui
- Yingpeng Chen
- Yiwen Ning
- Yong Wang
- Yuxuan Sun
- Zhongsheng Liu
- Ming Sun
- Cheng Luo
- Chen Yang
- Han Li
- Kun Gai
topics:
- software-foundation-model
- code-intelligence
- agentic-coding
- repository-level-swe
- tool-use-agents
- reinforcement-learning
relevance_score: 0.96
run_id: materialize-outputs
language_code: zh-CN
---

# KAT-Coder-V2.5 Technical Report

## Summary
## 摘要
KAT-Coder-V2.5 是一个编码智能体，面向仓库级软件工程和可执行环境中的工具使用进行训练。论文的主要主张是，相比单纯扩大模型规模，改进可验证环境、轨迹过滤和长任务强化学习基础设施更能提升智能体式编码能力。

## 问题
- 编码智能体需要修改真实仓库、运行测试、从失败中恢复，并在长任务中使用工具；单轮代码生成难以训练出这些行为。
- 真实仓库很难大规模重建，因为依赖、构建工具、测试和运行时假设会随项目变化。
- 只看最终测试是否通过会产生较弱的训练数据，因为部分通过的轨迹使用了捷径，而部分失败的轨迹包含有用的搜索和修复行为。

## 方法
- AutoBuilder 在沙箱中重建多语言仓库，运行结构化测试验证，并且只在收集到超过 90% 的预期测试且结果能跨多次运行复现时接受环境。
- 系统根据黄金补丁和测试补丁重新生成自包含任务描述，然后过滤不清楚或不一致的样本。
- 一个过程感知的轨迹流水线会对探索、定位、补丁质量、验证、恢复和诚实性评分；它会移除脆弱的通过轨迹，并通过临时提示恢复接近成功的失败轨迹，随后重新生成无提示轨迹。
- KwaiClawEnv 通过 Service、Task 和 Eval 层创建工具使用训练数据，包含可执行服务、任务变体、并行 rollout 和多阶段过滤。
- 强化学习使用 harness 随机化、加固沙箱、非对称 actor-critic PPO、面向 harness 的奖励，以及跨 SWE、Claw、终端、Web 编码和通用专家的 Multi-Teacher On-Policy Distillation。

## 结果
- 在统一的 Claude Code harness 下，KAT-Coder-V2.5 在 6 个软件工程和智能体基准上报告了 PinchBench 的最高结果，并在受评模型中于 SWE-Bench Pro 和 KAT Code Bench 取得第二名；摘录没有提供准确的基准分数。
- 论文称，在报告的对比中，KAT-Coder-V2.5 在仓库级软件工程上仅次于 Opus 4.8，排名第二。
- AutoBuilder 将可执行环境构建成功率从 16.5% 提高到 57.2%，并在 12 种语言中产出超过 100,000 个可验证环境。
- 提示辅助恢复将此前零通过任务的通过率提高到约 20%，随后系统会重新生成无提示训练轨迹。
- KwaiClawEnv 报告服务生成成功率超过 90%，在验证后保留超过 100,000 个高质量任务实例，并生成平均包含 15 次工具调用的轨迹，最长轨迹超过 100 步。
- 强化学习基础设施报告，在使用聊天端点时，约 200 轮的智能体样本中大约 40% 出现 retokenization 漂移，因此它通过生成端点发送请求，以保持 rollout 和训练 token 完全一致。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2607.05471v1](https://arxiv.org/abs/2607.05471v1)
