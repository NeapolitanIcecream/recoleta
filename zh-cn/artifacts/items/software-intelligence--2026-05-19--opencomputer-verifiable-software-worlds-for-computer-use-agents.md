---
source: arxiv
url: https://arxiv.org/abs/2605.19769v1
published_at: '2026-05-19T12:40:29'
authors:
- Jinbiao Wei
- Qianran Ma
- Yilun Zhao
- Xiao Zhou
- Kangqi Ni
- Guo Gan
- Arman Cohan
topics:
- computer-use-agents
- desktop-benchmark
- verifiable-evaluation
- software-worlds
- agent-training
- gui-automation
relevance_score: 0.93
run_id: materialize-outputs
language_code: zh-CN
---

# OpenComputer: Verifiable Software Worlds for Computer-Use Agents

## Summary
## 摘要
OpenComputer 为面向电脑使用代理构建可验证的桌面软件任务，并把程序化检查绑定到真实应用状态。论文认为，即使代理已经取得部分进展，当前系统仍然会错过很多端到端任务。

## 问题
- 桌面代理基准很难构建，因为每个任务都需要一个真实的初始状态，例如文件、配置文件、设置、文档或浏览器数据。
- 基于截图或 LLM 裁判的评分，可能会漏掉文件、元数据、偏好设置、数据库或已保存应用状态中的隐藏错误。
- 更好的训练和评估需要可复现的任务，以及能在桌面环境内运行检查、并据此审计奖励的机制。

## 方法
- OpenComputer 为每个应用创建专用的 Python 验证器模块，并通过 CLI 端点输出 JSON，用于真实应用。
- 验证器通过应用专属通道检查状态，例如浏览器调试协议、D-Bus、LibreOffice UNO、SQLite 配置文件数据库、可访问性状态和已保存文件解析。
- 自我演进的验证器流程对每个应用运行约 15 个校准任务，把程序化验证器判断与按标准细分的 LLM 参考判断进行比较，并修正检查代码、端点代码或文档中的验证器侧错误。
- 任务生成器提出真实的用户目标，对任务的难度和数据生成进行筛选，保留结果可以检查的任务，并把每个任务封装为指令、沙盒初始化器和可执行的成功标准。
- 评估框架在新的沙盒中运行代理，记录截图和动作轨迹，并把每个任务记为通过的验证器检查比例。

## 结果
- 发布的基准包含 33 个桌面应用和 1,000 个最终任务，平均每个应用有 17.7 个验证器端点、每个任务有 6.9 个检查、每个任务有 1.3 个种子文件。
- GPT-5.4 的任务成功率为 68.3%，平均奖励为 88.4%，平均步数为 19.0，每步 16.5 秒。
- Claude-Sonnet-4.6 的成功率为 64.4%，平均奖励为 76.6%；Kimi-K2.6 的成功率为 58.8%，平均奖励为 70.7%。
- 开源模型低得多：Qwen-3.5-27B 的成功率为 32.3%，EvoCUA-8B 为 10.9%，Qwen-3.5-9B 为 7.8%，GUI-OWL-1.5-8B 为 5.7%。
- 论文报告，一些开源模型相对 OSWorld-Verified 出现大幅下降，例如 GUI-OWL-1.5-8B 从 52.3% 降到 5.7%，EvoCUA-8B 从 46.1% 降到 10.9%。
- 摘要没有给出确切的人类一致性百分比，但声称当成功取决于细粒度应用状态时，硬编码验证器比 LLM-as-judge 评分更接近人工裁定。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.19769v1](https://arxiv.org/abs/2605.19769v1)
