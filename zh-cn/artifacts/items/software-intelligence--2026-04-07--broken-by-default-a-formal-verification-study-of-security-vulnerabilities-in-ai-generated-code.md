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
本文测量主要 LLM 在安全敏感编程任务中生成不安全代码的频率，并用形式化方法而不是关键词规则检查这些代码是否可被利用。在七个模型生成的 3,500 个程序中，作者报告称，含漏洞代码很常见，而且很多都能被形式化证明。

## 问题
- 本文研究一个实际缺口：AI 编码助手已经被用于生产代码，但以往评估常依赖模式匹配或人工审查，无法证明缺陷是否真的可被利用。
- 这对安全关键代码很重要，因为静态规则发出的警告，远不如一个能触发溢出、内存破坏、注入或弱认证行为的具体输入见证。
- 主要问题是：当前 LLM 默认会在多大程度上生成可利用漏洞，以及提示词或常规安全工具能否降低这种风险。

## 方法
- 作者构建了一个基准，包含 500 个面向安全的提示，覆盖五个 CWE 组：内存分配、整数运算、认证、密码学和输入处理。他们以 temperature 0 询问七个生产级 LLM，得到 3,500 个代码工件。
- 他们用 COBALT 分析输出，定位候选漏洞位置，把错误条件编码成 Z3 SMT 公式，再让 Z3 寻找满足赋值。如果 Z3 返回 SAT，论文就把它视为可利用性的形式化证明，并附带一个具体输入见证。
- 他们把结果分为 Z3 SAT、模式匹配或干净，并用 CVSS v3 基础分数评估严重性。
- 他们用 7 个代表性案例做了概念验证脚本和 GCC AddressSanitizer 运行时检查。
- 他们在 50 个提示的子集上做了三项附加实验：安全提示消融、与六个静态分析工具比较，以及自检，即每个模型审查自己的含漏洞输出。

## 结果
- 在全部 3,500 个工件中，55.8% 至少包含一个由 COBALT 识别出的漏洞。论文报告了 1,055 个带满足性见证的 Z3 证明结果。
- 在 500 提示基准上，各模型结果从 Gemini 2.5 Flash 的 48.4% 到 GPT-4o 的 62.4% 不等。没有模型达到 C 级或更好；Gemini 2.5 Flash 以 48.4% 获得 D，GPT-4o 以 62.4% 获得 F，GPT-4.1 为 54.0%，Mistral Large 为 57.8%，Llama 3.3 70B 为 58.4%，Llama 4 Scout 为 60.6%，Claude Haiku 4.5 为 49.2%。
- 按类别看，整数运算的平均漏洞率最高，为 87%；内存分配为 67%，输入处理为 56%，认证为 44%，密码学为 25%。
- 运行时验证确认了 7 个选定案例中的 6 个，确实存在故障或可利用点，包括堆缓冲区溢出、分配大小过大、越界读取、SQL 注入和弱密码哈希。其中一个 Zip Slip 案例在运行时被 Python 3.12 拦截，尽管模型生成了有漏洞的模式。
- 在 50 个提示的安全提示消融实验中，平均漏洞率从 64.8% 降到 60.8%，下降 4 个百分点。5 个模型中有 4 个仍然得到 F，Llama 3.3 70B 反而从 68% 升到 70%。
- 在 50 个提示子集的工具比较中，Semgrep 和 Bandit 共标记了 250 个工件中的 19 个，即 7.6%。论文称，六个行业工具合起来漏掉了 97.8% 的 Z3 证明结果，CodeQL 对 90 个形式化证明案例检测为 0。
- 在自检中，模型 89 次里有 70 次识别出自己的含漏洞代码，比例为 78.7%。论文据此认为，模型在审查模式下往往知道如何发现这些缺陷，但在生成时仍然会产出它们。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.05292v2](http://arxiv.org/abs/2604.05292v2)
