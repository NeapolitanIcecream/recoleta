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
这篇论文研究“编译式 AI”：先用一次 LLM 生成工作流代码，验证这段代码，再把工作流当作普通的确定性软件运行。论文的核心观点是，这种方式牺牲了一部分运行时灵活性，换来更低的成本、更低的延迟、更强的可审计性和更好的企业工作流可靠性。

## 问题
- 运行时 LLM 代理会在每笔交易上调用模型，因此会带来 token 成本、延迟，以及即使在 temperature 0 下仍然存在的输出波动。
- 在医疗预授权、计费和文档处理这类受监管工作流中，运营方在部署前需要确定性行为、审计轨迹和安全控制。
- 现有研究表明，代理在多步骤任务上的可靠性会下降，因此把模型使用移到构建阶段的系统，更适合高吞吐、规格明确的工作流。

## 方法
- 系统接收工作流规范，选择已验证的模板和模块，然后只调用一次 LLM，在模板内部生成一个小型业务逻辑函数，通常为 20 到 50 行。
- 生成的产物随后必须经过四个验证阶段：安全扫描、语法和类型检查、沙箱执行测试，以及基于黄金数据的输出准确性检查。
- 如果任何阶段失败，系统会带着错误上下文重新生成代码，并在部署前重试。
- 工作流通过验证后，生产执行在主要的编译式设置中使用静态代码，运行时不再调用 LLM。
- 对于仍然需要对复杂输入做判断的任务，论文加入了一种有边界的变体，叫做 Code Factory。在这种模式下，编译后的代码可以发起范围很窄、受 schema 约束的 LLM 调用，并带有回退逻辑和监控。

## 结果
- 在 BFCL function calling（n=400）上，编译式 AI 在一次性 9,600 token 编译成本之后，以零执行 token 达到 96% 的任务完成率（384/400）。
- 在 BFCL 上，与直接调用 LLM 相比，盈亏平衡点约为 17 笔交易；在 1,000 笔交易时，它的 token 使用量比 direct LLM 少 57 倍，比 AutoGen 少 84 倍。
- 在每月 100 万笔交易时，报告的总拥有成本为：compiled AI 555 美元，direct LLM 22,000 美元，LangChain 29,400 美元，AutoGen 31,900 美元。
- 在 BFCL 延迟上，compiled AI 的 P50 为 4.5 ms，direct LLM 为 2,004 ms；前者可复现性为 100%，输出熵为 0；直接运行时推理的可复现性为 95%。
- 在 DocILE（5,680 张发票）上，Code Factory 在 KILE 上与 Direct LLM 持平，都是 80.0%；在 LIR 上更高，为 80.4%，而 Direct LLM 为 74.5%；中位延迟为 2,695 ms，而 Direct LLM 为 6,339 ms。纯确定性的 regex 速度快得多，仅 0.6 ms，但 KILE 只有 20.3%，明显更差。
- 在安全测试中，prompt injection 检测在 30 个对抗输入上达到 95.8% recall 和 100% precision；代码安全关卡在 20 个有漏洞样例和 20 个良性样例上达到 75% recall 和 100% precision。摘要还报告，在 135 个测试用例上，prompt injection 准确率为 96.7%，静态代码安全分析准确率为 87.5%。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.05150v1](http://arxiv.org/abs/2604.05150v1)
