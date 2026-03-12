---
source: arxiv
url: http://arxiv.org/abs/2603.02345v1
published_at: '2026-03-02T19:28:27'
authors:
- Sami Abuzakuk
- Lucas Crijns
- Anne-Marie Kermarrec
- Rafael Pires
- Martijn de Vos
topics:
- llm-agents
- configuration-drift
- infrastructure-as-code
- multi-agent-systems
- tool-reliability
relevance_score: 0.88
run_id: materialize-outputs
---

# RIVA: Leveraging LLM Agents for Reliable Configuration Drift Detection

## Summary
RIVA提出了一个面向基础设施即代码（IaC）配置漂移检测的多智能体系统，重点解决“工具返回结果本身可能是错的”这一现实问题。核心贡献是让两个LLM代理通过不同工具路径交叉验证同一属性，从而在不可靠工具存在时提升检测可靠性。

## Problem
- 要解决的问题是：已部署云基础设施是否偏离了IaC规格，即配置漂移检测与验证。
- 这很重要，因为漂移可能来自IaC缺陷、人工热修复、系统更新或云API异常，进而导致服务中断、安全风险和高昂的人工排查成本。
- 现有LLM agent通常默认外部工具输出可信；一旦工具静默返回错误、过时或空结果，agent就无法分辨是真实漂移还是工具故障，导致漏报或误报。

## Approach
- RIVA使用两个专门代理协作：**Verifier Agent**负责从IaC规格中选出要验证的属性并判断是否合规，**Tool Generation Agent**负责为该属性生成并执行工具调用。
- 核心机制很简单：**不要相信单次工具结果，而是用不同工具/不同诊断路径对同一属性做交叉验证**；如果多个独立路径结果一致，结论更可信。
- 系统维护一个共享的**Tool Call History**，按属性记录最多K次、且彼此不同的工具执行，包括命令、结果和简短分析；Verifier只有在同一属性拿到K条独立证据后才下结论。
- Tool Generation Agent会查看历史，专门生成“未用过”的新验证路径，并在调用失败时修正参数或语法后重试，以提高工具多样性和鲁棒性。
- 论文主要采用K=2；K=1时几乎退化为普通单路径agent，K=3在AIOpsLab中因可用诊断路径不足而失败。

## Results
- 在AIOpsLab上、**存在错误工具输出**时，RIVA将所有任务平均准确率从基线ReAct的**27.3%提升到50.0%**。
- 在**无错误工具输出**时，RIVA也把平均任务成功率从**28.0%提升到43.8%**，说明收益不只来自容错，也来自多智能体职责分离。
- 具体例子：定位任务中，ReAct在正确工具下为**22.2%**，在错误`get_logs`下掉到**11.1%**；RIVA在相同错误工具条件下达到**20.0%**。论文还指出RIVA在全部任务上的表现“始终大于或等于”ReAct在正确工具条件下的表现。
- 效率方面，正确工具下**80%**的RIVA任务在**15步内**完成，而ReAct只有**60%**；RIVA步数峰值**17**，而**33%**的ReAct运行触达**45步**上限。
- token开销方面，正确工具下RIVA峰值约**38,000 tokens**，ReAct约**78,000**；错误工具下RIVA峰值约**50,000**，ReAct约**90,000**。
- 超参数K的消融：**RIVA(K=1)**平均成功率与ReAct接近（正确工具**27.67** vs ReAct **28.00**）；**RIVA(K=2)**最佳（正确工具**43.75**，错误`get_logs` **46.67**，错误`read_metrics` **53.33**）；**RIVA(K=3)**在三种设置下均为**0%**，因为基准环境缺少3条可区分的诊断路径。

## Link
- [http://arxiv.org/abs/2603.02345v1](http://arxiv.org/abs/2603.02345v1)
