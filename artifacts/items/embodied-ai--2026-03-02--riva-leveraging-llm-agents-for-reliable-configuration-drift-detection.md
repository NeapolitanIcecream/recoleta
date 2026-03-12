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
relevance_score: 0.03
run_id: materialize-outputs
---

# RIVA: Leveraging LLM Agents for Reliable Configuration Drift Detection

## Summary
RIVA提出了一个面向云基础设施配置漂移检测的多智能体LLM系统，重点解决“工具返回静默错误结果”时代理系统不可靠的问题。其核心贡献是通过多工具交叉验证与历史追踪，在AIOpsLab上显著提升了任务成功率与效率。

## Problem
- 论文解决的是**IaC（基础设施即代码）环境中的配置漂移检测**问题：线上云资源可能因为代码缺陷、人工修改或系统更新而偏离声明式配置。
- 这很重要，因为配置漂移会导致**服务中断、安全漏洞和运维复杂度上升**，而人工持续核对大规模日志、指标和状态十分费力且容易出错。
- 现有LLM代理通常默认外部工具总是正确；一旦工具返回**错误但看似正常**的结果，代理就无法区分是真实漂移还是工具坏了，从而产生漏报或误报。

## Approach
- RIVA使用两个专门代理协作：**Verifier Agent**负责从IaC规范中挑选要验证的属性并判断是否满足；**Tool Generation Agent**负责为该属性生成并执行不同的验证工具调用。
- 核心机制很简单：**不要相信单次工具结果，而是让多个不同工具/不同诊断路径去验证同一个属性**；如果结果一致，更可信；如果冲突，就继续推理和交叉检查。
- 系统维护一个共享的**Tool Call History**，按属性记录不同工具的命令、输出和简短分析；只有当同一属性积累到K个不同工具结果后，Verifier才下结论。
- Tool Generation Agent会查看历史，刻意生成**不同于之前方法**的新工具调用，从另一个角度验证同一问题，以提高对错误工具输出的鲁棒性。
- 作者将该方法集成到AIOpsLab，并与标准**ReAct单代理**基线比较，在有/无错误工具两种条件下测试检测、定位和分析任务。

## Results
- 在**存在错误工具输出**时，RIVA将AIOpsLab上的**平均任务成功率**从ReAct的**27.3%提升到50.0%**，恢复了大量因错误工具导致的性能损失。
- 在**没有错误工具输出**时，RIVA仍把平均成功率从**28.0%提升到43.8%**，说明收益不只是鲁棒性，还来自更好的多代理分工。
- 具体例子：**定位任务**中，ReAct在正确工具下为**22.2%**，遇到错误`get_logs`时降到**11.1%**；RIVA在相同错误工具条件下达到**20.0%**。同时，RIVA在定位任务的正确工具条件下达到**40.0%**，错误`get_logs`+`read_metrics`时为**20.0%**。
- **检测任务**中，ReAct在正确工具下为**50.0%**，在错误`get_logs`下反而到**62.5%**；论文解释为检测任务较简单，空日志促使代理更依赖更聚焦的指标信息。这表明工具错误对单代理行为可能产生偶然且不可控的影响，而RIVA更稳定。
- 在效率上，正确工具条件下，**80%** 的RIVA任务在**15步内**完成，而ReAct仅**60%**；RIVA步数峰值**17**，而**33%** 的ReAct运行撞到**45步**上限。RIVA峰值token约**38,000**，ReAct约**78,000**。
- 在错误工具条件下，RIVA仍最多约**17步**，而**37%** 的ReAct任务超过这一阈值；峰值token使用约**50,000**（RIVA）对比**90,000**（ReAct）。此外，超参数**K=2**最佳：平均成功率为**43.75%/46.67%/53.33%**（正确工具/错误`get_logs`/错误`read_metrics`），而**K=1**接近ReAct，**K=3**因诊断路径不足降到**0%**。

## Link
- [http://arxiv.org/abs/2603.02345v1](http://arxiv.org/abs/2603.02345v1)
