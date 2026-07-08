---
source: arxiv
url: https://arxiv.org/abs/2607.05155v1
published_at: '2026-07-06T14:39:22'
authors:
- Deyao Zhu
- Xin Zhou
- Shengling Qin
- Xuekai Zhu
- Hangliang Ding
- Shu Zhong
- Zixin Wen
- Zhonglin Xie
- Chenhui Gou
- Linxuan Ren
- Yueyang Wang
- Junfeng Zhong
- Rui Liu
- Tian Gao
- Yangguang Lin
- Jingyuan Zhang
- Maojia Song
- Xuan Qi
- Jinhong Wu
- Chenyang Zhang
- Yinzhu Piao
- Ziru Niu
- Hongbin Lin
- Lingxiang Meng
- Peng Tang
- Chengyao Tang
- Shanyu Wu
- Huanyu Zheng
- Yu Liu
- Liya Zhu
- He Wang
- Ming Ding
- Ziyu Wan
- Hao Liu
- Sibo Wang
- Haotian Zhu
- Xintian Zhang
- Nan Chai
- Yipeng Liu
- Panhao Lai
- Sihang Yuan
- Zixin Su
- Ge Zhang
- Wangchunshu Zhou
- Yantao Du
- Wenhao Huang
- Guang Shi
topics:
- agent-learning
- scaling-laws
- real-world-benchmarks
- software-engineering-agents
- long-horizon-evaluation
relevance_score: 0.73
run_id: materialize-outputs
language_code: zh-CN
---

# EdgeBench: Unveiling Scaling Laws of Learning from Real-World Environments

## Summary
## 摘要
EdgeBench 是一个包含 134 个任务的基准，用于衡量智能体在可执行环境中的长时间运行期间如何改进。论文称，在约 38,000 小时交互中，智能体总体性能符合 log-sigmoid 曲线，平均 R² = 0.998。

## 问题
- 已部署的智能体需要学习私有数据、工具行为、隐藏测试和任务反馈，而预训练无法完全覆盖这些内容。
- 许多现有基准使用短任务或弱反馈，因此主要衡量初始能力，较少衡量单次运行中的学习。
- 这影响软件工程、研究、优化和专业工作。在这些场景中，用户需要智能体在许多小时内把失败和评审反馈转化为更好的成果。

## 方法
- EdgeBench 包含 134 个任务，覆盖六类：39 个科学/机器学习任务、36 个系统/软件工程任务、19 个组合优化任务、19 个专业知识工作任务、13 个形式化数学任务，以及 8 个游戏/模拟器任务。
- 每个任务支持至少 12 小时的智能体工作。该设置使用独立的工作容器和评审容器，因此智能体可以在本地测试，提交成果供隐藏评审，并在结果返回期间继续工作。
- 研究评估了五个智能体：Claude Opus 4.8、GPT-5.5、GPT-5.4、GLM-5.1 和 DeepSeek-V4-Pro preview。每个任务-模型组合进行三次独立的 12 小时试验。
- 核心曲线为 S(t) = S_max / (1 + (t_mid / t)^β)。直观地说，分数起初缓慢上升，在有用反馈积累后加速，随后随着可达到的收益减少而放缓。
- 论文提出的机制把任务建模为由隐藏得分单元组成的图。已解决的部分帮助解锁相邻的未解决部分；在对许多不同任务取平均后，进展会变得平滑。

## 结果
- 在全部 134 个任务上，五个智能体的 12 小时平均学习曲线都符合 log-sigmoid 形式，R² ≥ 0.997，平均 R² = 0.998。
- 更长运行仍保持同样的拟合：80 个任务和四个模型的 28 小时曲线，以及 18 个任务和两个模型的 72 小时曲线，均达到 R² ≥ 0.993。
- 仅用前 6.5 小时训练的预测器，可以预测 6.5 到 12 小时的表现，R² ≥ 0.997，RMSE 低于 1.0 分。
- 在 0–100 分制的完整窗口曲线比较中，log-sigmoid 的 RMSE 为 0.390；log-probit 为 0.398，log-Gompertz 为 0.402，Weibull CDF 为 0.404，log-linear 为 0.717。
- 论文报告称，自 2025 年 9 月以来发布的模型中，前沿智能体的学习速度约每三个月翻一倍。
- 该基准报告每个任务的人类专家投入平均为 57.2 小时，最高为 320 小时，并发布了 51 个任务和评估代码。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2607.05155v1](https://arxiv.org/abs/2607.05155v1)
