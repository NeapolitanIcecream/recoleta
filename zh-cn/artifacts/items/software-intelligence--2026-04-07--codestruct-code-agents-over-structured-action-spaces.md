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
CodeStruct 改变了代码代理与代码仓库交互的方式：它们不再读取和编辑原始文本片段，而是直接操作有名称的 AST 实体，比如函数、类和方法。这减少了脆弱的字符串匹配失败，并在软件工程基准上同时提升任务成功率和 token 效率。

## 问题
- 现有的 LLM 代码代理把代码仓库当作平面文本处理，所以它们要么读取整个文件，要么读取行区间，再通过字符串替换来编辑代码。
- 基于文本的编辑会在格式变化、目标字符串出现多次，或者模型必须逐字复现未修改代码时失败；这些失败很重要，因为它们会在仓库级 bug 修复中浪费调用、token 和补丁尝试。
- 现有辅助工具，比如 repo map 或符号索引，可以帮助代理找到代码，但实际的读取和编辑动作仍然使用文本，失败模式也没有变。

## 方法
- CodeStruct 通过抽象语法树（AST）把代码仓库暴露为一个结构化动作空间，其中代码元素有稳定名称，例如 `file.py::ClassName::method`。
- 它增加了 `readCode`，返回完整的语法单元或结构化摘要，而不是任意文本切片。对于大型文件，代理可以先读取签名，再用选择器请求某个具体函数或方法。
- 它增加了 `editCode`，对选中的实体执行 AST 级别的插入、替换或删除操作。这个工具会保留缩进，并拒绝会产生语法错误的编辑。
- 这意味着代理只需要说明目标实体和预期修改，工具负责把它落实为源文本。论文说，这样就不再依赖行号和精确字符串匹配。
- 该接口通过 MCP 暴露，因此作者可以把它接入现有的 SWE-Agent 风格工作流，而不用改动规划器。

## 结果
- 在 **SWE-Bench Verified** 上，跨六个模型测试时，CodeStruct 将 **Pass@1 提高了 1.2 到 5.0 个百分点，适用于前沿模型**，增幅包括 **GPT-5: 66.0 -> 67.2 (+1.2)**、**GPT-5-mini: 60.4 -> 62.0 (+1.6)**、**Qwen3-Coder: 61.2 -> 66.2 (+5.0)** 和 **Qwen3-32B: 14.8 -> 16.0 (+1.2)**。
- SWE-Bench 上最大的提升来自 **GPT-5-nano: 19.6 -> 40.4 (+20.8 个百分点)**。摘要把这一点归因于无效或空补丁更少，其中 **empty-patch failures 从 46.6% 降到 7.2%**。
- SWE-Bench 的效率通常也会同步提升：**大多数模型的输入 token 下降了 12% 到 38%**。例如：**GPT-5 成本 -19.1%**、**GPT-5-mini 成本 -32.6%**、**Qwen3-32B 成本 -17.4%**。有一个例外是 **GPT-5-nano**，虽然准确率上升，但 **成本增加了 40.8%**。
- 在 **CodeAssistBench** 上，所有测试模型的准确率都提高了 **0.8 到 4.4 个百分点**：**GPT-5 53.3 -> 54.1 (+0.8)**、**GPT-5-mini 51.1 -> 51.9 (+0.8)**、**GPT-5-nano 46.7 -> 48.1 (+1.4)**、**Qwen3-Coder 31.1 -> 31.9 (+0.8)**、**Qwen3-32B 15.6 -> 20.0 (+4.4)**、**Qwen3-8B 13.3 -> 14.1 (+0.8)**。
- CodeAssistBench 的成本也经常下降，例子包括 **GPT-5 -14.5%**、**GPT-5-mini -33.3%** 和 **Qwen3-8B -17.6%**。一个明显例外是 **Qwen3-32B**，它的准确率提高了 **4.4 个百分点**，但 **成本上升了 23.7%**。
- 核心结论是，具备结构感知的读写原语，比基于文本的工具更适合代码代理，尤其适合那些主要瓶颈是补丁格式失败而不是推理能力的模型。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.05407v3](http://arxiv.org/abs/2604.05407v3)
