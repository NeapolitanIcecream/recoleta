---
source: arxiv
url: http://arxiv.org/abs/2604.05150v1
published_at: '2026-04-06T20:25:20'
authors:
- Geert Trooskens
- Aaron Karlsberg
- Anmol Sharma
- Lamara De Brouwer
- Max Van Puyvelde
- Matthew Young
- John Thickstun
- Gil Alterovitz
- Walter A. De Brouwer
topics:
- llm-code-generation
- workflow-automation
- deterministic-execution
- code-intelligence
- enterprise-ai
- document-intelligence
relevance_score: 0.91
run_id: materialize-outputs
language_code: zh-CN
---

# Compiled AI: Deterministic Code Generation for LLM-Based Workflow Automation

## Summary
## 摘要
本文研究“编译式 AI”：先用 LLM 一次性生成工作流代码，验证这段代码，然后像普通确定性软件一样运行工作流。核心观点是，这种做法用较少的运行时灵活性，换来更低成本、更低延迟、更强审计性和更好的可靠性，适合企业工作流。

## 问题
- 运行时 LLM 代理在每笔事务上都要调用模型，这会带来 token 成本、延迟和输出波动，即使温度设为 0 也一样。
- 在医疗预授权、计费和文档处理这类受监管的工作流里，部署前就需要确定性行为、审计轨迹和安全控制。
- 现有研究表明，代理在多步任务上的可靠性会下降，所以把模型使用前移到构建阶段，更适合高吞吐、规格明确的工作流。

## 方法
- 系统接收工作流规格，选择经过验证的模板和模块，然后只让 LLM 生成一个小的业务逻辑函数，通常是模板内 20 到 50 行代码。
- 生成的产物随后要经过四个必需的验证阶段：安全扫描、语法和类型检查、沙箱执行测试，以及与标准数据对比的输出准确性检查。
- 任何阶段失败后，系统都会带着错误上下文重新生成代码并重试，然后才部署。
- 工作流通过验证后，生产执行使用静态代码，在主编译设置下不再进行运行时 LLM 调用。
- 对于仍然需要处理杂乱输入并做判断的任务，论文加入了一个受限变体 Code Factory；它可以在严格 schema 约束下进行窄范围的 LLM 调用，并带有回退逻辑和监控。

## 结果
- 在 BFCL 函数调用任务（n=400）上，编译式 AI 在一次性 9,600 token 编译成本后，实现了 96% 的任务完成率（384/400），运行阶段使用 0 个 token。
- 在 BFCL 上，相比直接 LLM 的盈亏平衡点约为 17 笔事务；在 1,000 笔事务时，它的 token 使用量比直接 LLM 少 57 倍，比 AutoGen 少 84 倍。
- 在每月 100 万笔事务时，报告的总体拥有成本为：编译式 AI 555 美元，直接 LLM 22,000 美元，LangChain 29,400 美元，AutoGen 31,900 美元。
- 在 BFCL 延迟上，编译式 AI 的 P50 为 4.5 ms，直接 LLM 为 2,004 ms；它的可复现性为 100%，输出熵为 0。直接运行时推理的可复现性为 95%。
- 在 DocILE（5,680 张发票）上，Code Factory 在 KILE 上达到 80.0%，与 Direct LLM 持平，并在 LIR 上更高，分别是 80.4% 和 74.5%；中位延迟为 2,695 ms，而 Direct LLM 为 6,339 ms。纯确定性的正则表达式速度更快，只有 0.6 ms，但 KILE 只有 20.3%。
- 在安全测试中，提示注入检测对 30 个对抗输入的召回率为 95.8%，精确率为 100%；代码安全门控在 20 个有漏洞样本和 20 个无害样本上的召回率为 75%，精确率为 100%。摘要还报告，在 135 个测试用例上，提示注入准确率为 96.7%，静态代码安全准确率为 87.5%。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.05150v1](http://arxiv.org/abs/2604.05150v1)
