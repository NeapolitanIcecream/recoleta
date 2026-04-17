---
source: arxiv
url: http://arxiv.org/abs/2604.05407v3
published_at: '2026-04-07T03:58:10'
authors:
- Myeongsoo Kim
- Joe Hsu
- Dingmin Wang
- Shweta Garg
- Varun Kumar
- Murali Krishna Ramanathan
topics:
- code-agents
- ast-based-editing
- software-engineering-benchmarks
- code-intelligence
- llm-tool-use
relevance_score: 0.96
run_id: materialize-outputs
language_code: zh-CN
---

# CODESTRUCT: Code Agents over Structured Action Spaces

## Summary
## 摘要
CodeStruct 改变了代码智能体与代码仓库交互的方式：它们不再读取和编辑原始文本片段，而是直接作用于具名 AST 实体，例如函数、类和方法。这减少了脆弱的字符串匹配失败，并在软件工程基准上同时提升了任务成功率和 token 效率。

## 问题
- 当前的 LLM 代码智能体把代码仓库当作平面文本处理，因此它们读取整个文件或某些行范围，并通过字符串替换来编辑代码。
- 基于文本的编辑会在格式变化、目标字符串出现多次，或模型必须精确复现未改动代码时失败；这些失败会浪费调用次数、tokens 和补丁尝试，影响仓库级 bug 修复任务。
- 现有辅助工具，如 repo map 或 symbol index，可以帮助智能体定位代码，但实际的读取和编辑动作仍然基于文本，所以同样会遇到这些失败模式。

## 方法
- CodeStruct 将代码仓库暴露为一个基于抽象语法树（AST）的结构化动作空间，其中代码元素具有稳定名称，例如 `file.py::ClassName::method`。
- 它增加了 `readCode`，返回完整的语法单元或结构摘要，而不是任意文本切片。对于大文件，智能体可以先读取签名，再按选择器请求某个具体函数或方法。
- 它增加了 `editCode`，对选中的实体执行 AST 层级的插入、替换或删除操作。该工具会保留缩进，并拒绝会产生语法错误的编辑。
- 这意味着智能体只需说明目标实体和预期修改，由工具负责把修改落实到源文本。论文称，这消除了对行号和精确字符串匹配的依赖。
- 该接口通过 MCP 暴露，因此作者可以将其接入现有的 SWE-Agent 风格工作流，而无需修改规划器。

## 结果
- 在 **SWE-Bench Verified** 上，CodeStruct 在六个模型上都带来了提升，**前沿模型的 Pass@1 提高了 1.2 到 5.0 个点**，包括 **GPT-5: 66.0 -> 67.2 (+1.2)**、**GPT-5-mini: 60.4 -> 62.0 (+1.6)**、**Qwen3-Coder: 61.2 -> 66.2 (+5.0)**，以及 **Qwen3-32B: 14.8 -> 16.0 (+1.2)**。
- SWE-Bench 上最大的一次提升来自 **GPT-5-nano: 19.6 -> 40.4 (+20.8 个点)**。摘要将其归因于无效补丁或空补丁更少，**空补丁失败率从 46.6% 降到 7.2%**。
- SWE-Bench 上的效率通常也会同步提升：**大多数模型的输入 tokens 降低了 12% 到 38%**。例如：**GPT-5 -19.1% cost**、**GPT-5-mini -32.6% cost**、**Qwen3-32B -17.4% cost**。一个例外是 **GPT-5-nano**，它的准确率上升，但 **cost 增加了 40.8%**。
- 在 **CodeAssistBench** 上，所有测试模型的准确率都提高了 **0.8 到 4.4 个点**：**GPT-5 53.3 -> 54.1 (+0.8)**、**GPT-5-mini 51.1 -> 51.9 (+0.8)**、**GPT-5-nano 46.7 -> 48.1 (+1.4)**、**Qwen3-Coder 31.1 -> 31.9 (+0.8)**、**Qwen3-32B 15.6 -> 20.0 (+4.4)**、**Qwen3-8B 13.3 -> 14.1 (+0.8)**。
- CodeAssistBench 上的成本也经常下降，例如 **GPT-5 -14.5%**、**GPT-5-mini -33.3%** 和 **Qwen3-8B -17.6%**。一个明显的例外是 **Qwen3-32B**，它的准确率提高了 **4.4 个点**，但 **cost 上升了 23.7%**。
- 核心结论是，具备结构感知的读取和编辑原语，为代码智能体提供了比文本工具更可靠的接口，尤其适用于主要瓶颈在补丁格式失败而不是推理能力的模型。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.05407v3](http://arxiv.org/abs/2604.05407v3)
