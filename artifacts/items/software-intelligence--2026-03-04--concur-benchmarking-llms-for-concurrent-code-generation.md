---
source: arxiv
url: http://arxiv.org/abs/2603.03683v1
published_at: '2026-03-04T03:22:26'
authors:
- Jue Huang
- Tarek Mahmud
- Corina Pasareanu
- Guowei Yang
topics:
- llm-code-generation
- concurrent-programming
- benchmarking
- model-checking
- code-evaluation
relevance_score: 0.95
run_id: materialize-outputs
---

# CONCUR: Benchmarking LLMs for Concurrent Code Generation

## Summary
CONCUR 是一个专门评测大语言模型生成并发代码能力的基准与验证框架，填补了现有代码生成评测主要面向顺序程序的空白。它把并发题目数据集与基于模型检查的自动判定结合起来，用来更严格地发现死锁、竞态和“看似并发其实单线程”的错误。

## Problem
- 现有代码生成基准大多评估**顺序代码**，无法有效衡量 LLM 生成**并发程序**的能力。
- 并发代码更难，因为会出现顺序程序没有的错误，如**deadlock、race condition、starvation**，且传统静态相似度或单元测试很难覆盖不同线程交错执行。
- 如果没有专门基准，就无法真实了解 LLM 在软件工程中生成并发代码的上限与短板，这对代码智能和自动化软件生产很重要。

## Approach
- 构建 **CONCUR** 数据集：从经典并发教材整理出 **43** 个基础并发问题，并加入 **72** 个经人工验证的 mutant 变体，共 **115** 个任务，均配有结构化提示和 Java 真值实现。
- 使用**结构化 prompt** 约束输出为单个 Java 8 文件、限定线程数和迭代次数、禁止第三方库，从而保证可编译并适合形式化验证。
- 用 **Java Pathfinder (JPF)** 做模型检查，而不是只靠单元测试：系统性遍历有界线程交错，检测 **deadlock、race condition、starvation、uncaught exception** 等问题。
- 增加自定义监听器和规则，把错误映射为固定标签，包括 **No Entry Method**、**Single Thread**、**Termination Error** 等，特别识别“使用并发库但没有真正创建并发执行”的伪并发解。
- 采用双重有界策略保证可扩展性：题目层面限制线程/迭代，验证层面将 JPF 深度限制设为真值程序最大深度的 **10 倍**，并设置统一超时。

## Results
- 基准规模：**43** 个基础题 + **72** 个 mutant = **115** 个并发代码生成任务；作者称这是**首个**面向 LLM 并发代码生成的专用基准。
- 评测范围：对 **23** 个当前 LLM（含闭源 API 与开源模型）进行了实验，论文称结果揭示了现有模型在并发代码生成上的明显局限。
- 自动验证有效性：其基于 JPF 的错误检测框架在人工核验中达到 **92% precision**，说明自动发现并发错误具有较高可靠性。
- 验证设置示例：JPF 配置中使用 **9000 ms** 时间限制，并把 `search.depth_limit` 设为对应真值程序深度的 **10x**；这体现了其“有界但系统”的并发验证策略。
- 论文明确声称：常用代码生成指标 **CodeBLEU** 不能可靠反映并发程序正确性，但文段未给出该结论对应的具体相关系数或数值比较。
- 提供文本中**没有**给出各个模型在 CONCUR 上的具体通过率、分模型排名、或相对基线提升数字；最强的定量主张主要是数据集规模、评测模型数和 **92%** 的人工验证精度。

## Link
- [http://arxiv.org/abs/2603.03683v1](http://arxiv.org/abs/2603.03683v1)
