---
source: arxiv
url: http://arxiv.org/abs/2604.19305v1
published_at: '2026-04-21T10:11:59'
authors:
- Linhao Wu
- Yifei Pei
- Zhen Yang
- Kainan Li
- Zhonghang Lu
- Hao Tan
- Xiran Lyu
- Jia Li
- Yizhou Chen
- Pengyu Xue
- Kunwu Zheng
- Dan Hao
topics:
- automated-program-repair
- llm-debugging
- code-intelligence
- self-directed-debugging
- software-engineering
relevance_score: 0.95
run_id: materialize-outputs
language_code: zh-CN
---

# DebugRepair: Enhancing LLM-Based Automated Program Repair via Self-Directed Debugging

## Summary
## 摘要
DebugRepair 通过加入一个收集运行时状态的调试步骤来改进基于 LLM 的自动程序修复，而不是只依赖失败的测试结果和堆栈跟踪。论文报告说，它在 Java 和 Python 基准上取得了最先进的修复结果，并且在多个骨干 LLM 上都有提升。

## 问题
- 现有基于反馈的 LLM 修复方法主要使用失败测试和堆栈跟踪这类结果级信号，它们能显示 bug 的症状，但常常隐藏导致问题的运行时状态。
- 没有中间执行证据时，模型可能猜错根因，生成的补丁只能掩盖失败，而不能修复 bug。
- 这在自动程序修复中很重要，因为它只有在能为真实 bug 找到正确补丁时才有用，尤其是在静态代码和测试结果都不够的更难案例上。

## 方法
- DebugRepair 先做 **测试语义纯化**：它切分失败测试，只保留触发失败的最小语句和所需的类级依赖，从而减少无关上下文和噪声调试日志。
- 然后它进行 **模拟插桩**：LLM 预测要检查的有用变量和位置，插入类似 print 的调试语句，并执行插桩后的代码来收集中间运行时轨迹。
- 为了保证插桩安全，系统会检查去掉调试输出和注释后，插桩函数是否与原始逻辑一致，同时检查是否能编译；如果 LLM 插桩失败，就使用基于规则的 AST 插桩回退方案。
- 最后，**调试驱动的对话式修复** 以迭代层级方式运行：外层循环负责插桩和轨迹收集，内层循环把先前的修复尝试和新观察到的运行时状态一起用于细化补丁，直到测试通过或预算用尽。

## 结果
- 在 **Defects4J** 上使用 **GPT-3.5** 时，DebugRepair 正确修复了 **224 个 bug**，比最先进的基于 LLM 的基线平均提升 **26.2%**。
- 在 **Defects4J** 上使用 **DeepSeek-V3** 时，DebugRepair 正确修复了 **295 个 bug**，比第二好的基线多 **59 个**。
- 在来自不同家族和规模的另外 **五个骨干 LLM** 上，DebugRepair 相比各模型的原始设置，平均将修复性能提高了 **51.3%**。
- 评估覆盖 **两个语言** 的 **三个基准**：**Defects4J (v1.2 和 v2.0)**、**QuixBugs** 和 **HumanEval-Java**，并与 **15 种代表性方法** 进行了比较。
- 论文称消融研究显示所有主要组件都有帮助，尤其是测试纯化和模拟调试，但摘录没有给出详细的消融数值。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.19305v1](http://arxiv.org/abs/2604.19305v1)
