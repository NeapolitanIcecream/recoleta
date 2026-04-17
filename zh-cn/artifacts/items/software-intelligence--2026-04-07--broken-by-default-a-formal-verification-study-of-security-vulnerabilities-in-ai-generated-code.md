---
source: arxiv
url: http://arxiv.org/abs/2604.05292v2
published_at: '2026-04-07T00:55:42'
authors:
- Dominik Blain
- Maxime Noiseux
topics:
- code-security
- formal-verification
- llm-code-generation
- static-analysis
- software-engineering
relevance_score: 0.95
run_id: materialize-outputs
language_code: zh-CN
---

# Broken by Default: A Formal Verification Study of Security Vulnerabilities in AI-Generated Code

## Summary
## 摘要
这篇论文衡量主流 LLM 在安全敏感的编程任务中生成不安全代码的频率，并用形式化方法而不是关键词规则来检查这些代码是否可利用。在来自七个模型的 3,500 个生成程序中，作者报告说，易受攻击的代码很常见，而且往往可以被形式化证明。

## 问题
- 论文研究了一个实际缺口：AI 编程助手已被用于生成生产代码，但此前的评估通常依赖模式匹配或人工审查，这些方法无法证明缺陷是否真的可以被利用。
- 这对安全关键代码很重要，因为静态规则发出的警告弱于一个具体的见证输入；后者可以实际触发溢出、内存破坏、注入或弱认证行为。
- 核心问题是：当前的 LLM 默认会多频繁地生成可利用漏洞，以及提示词或标准安全工具是否能降低这种风险。

## 方法
- 作者构建了一个包含 500 个安全导向提示词的基准集，覆盖五类 CWE：内存分配、整数运算、认证、密码学和输入处理。他们以 temperature 0 查询七个生产级 LLM，得到 3,500 个代码产物。
- 他们用 COBALT 分析输出结果。COBALT 会定位候选漏洞点，将缺陷条件编码为 Z3 SMT 公式，并请求 Z3 给出满足赋值。如果 Z3 返回 SAT，论文将其视为可利用性的形式化证明，并附带一个具体输入见证。
- 他们将结果分为 Z3 SAT、模式匹配或干净，并用 CVSS v3 基础分评定严重性。
- 他们用概念验证 harness 和 GCC AddressSanitizer 运行时检查验证了 7 个代表性案例。
- 他们还在一个包含 50 个提示词的子集上加入了三个附加实验：安全提示词消融、与六种静态分析工具比较，以及自我审查，即每个模型检查自己生成的脆弱输出。

## 结果
- 在全部 3,500 个产物中，55.8% 至少包含一个由 COBALT 识别的漏洞。论文报告了 1,055 个带有可满足性见证的 Z3 证明结果。
- 在这个 500 提示词基准上，各模型的漏洞率从 Gemini 2.5 Flash 的 48.4% 到 GPT-4o 的 62.4% 不等。没有任何模型达到 C 或更高等级；Gemini 2.5 Flash 为 D，48.4%；GPT-4o 为 F，62.4%；GPT-4.1 为 54.0%；Mistral Large 为 57.8%；Llama 3.3 70B 为 58.4%；Llama 4 Scout 为 60.6%；Claude Haiku 4.5 为 49.2%。
- 按类别看，整数运算的平均漏洞率最高，为 87%；内存分配为 67%；输入处理为 56%；认证为 44%；密码学为 25%。
- 运行时验证在 7 个选定案例中确认了其中 6 个存在实际故障或可利用行为，包括 heap-buffer-overflow、alloc-size-too-big、越界读取、SQL 注入和弱密码哈希。一个 Zip Slip 案例虽然生成了脆弱模式，但在运行时被 Python 3.12 阻止。
- 在 50 个提示词的安全提示词消融实验中，平均漏洞率从 64.8% 降到 60.8%，下降 4 个百分点。五个模型中仍有四个得到 F，Llama 3.3 70B 还从 68% 升到 70%。
- 在 50 提示词子集上的工具比较中，Semgrep 加 Bandit 标记了 250 个产物中的 19 个，即 7.6%。论文称，六种行业工具合起来漏掉了 97.8% 的 Z3 已证明结果，而 CodeQL 在 90 个形式化证明案例中检出 0 个。
- 在自我审查中，模型在 89 次中有 70 次识别出自己生成的脆弱代码，即 78.7%。论文据此认为，模型在审查模式下通常知道如何发现这些缺陷，但在生成代码时仍会默认产生它们。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.05292v2](http://arxiv.org/abs/2604.05292v2)
