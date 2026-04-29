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
DebugRepair 通过加入一个收集运行时状态的调试步骤，提升了基于 LLM 的自动程序修复，而不是只依赖失败测试结果和堆栈跟踪。论文报告称，它在 Java 和 Python 基准测试上取得了当前最优的修复结果，并在多个基础 LLM 上都有提升。

## 问题
- 现有基于反馈的 LLM 修复方法主要使用结果层面的信号，例如失败测试和堆栈跟踪。这些信息能展示 bug 的症状，但往往看不到导致问题的运行时状态。
- 缺少执行过程中的中间证据时，模型可能会判断错根因，生成的补丁只是掩盖失败现象，而不是真正修复 bug。
- 这一点很重要，因为自动程序修复只有在能为真实 bug 找到正确补丁时才有价值，尤其是在更难的案例里，静态代码和测试结果本身并不够用。

## 方法
- DebugRepair 首先执行 **测试语义净化**：对失败测试进行切片，只保留触发失败所需的最小语句和必要的类级依赖，以减少无关上下文和带噪声的调试日志。
- 然后执行 **模拟插桩**：由 LLM 预测值得检查的变量和位置，插入类似 print 的调试语句，并运行插桩后的代码来收集中间运行时轨迹。
- 为了保证插桩安全，系统会在去除调试打印和注释后检查插桩函数是否与原始逻辑一致，同时检查能否编译；如果 LLM 插入的插桩失败，则使用基于规则的 AST 插桩回退方案。
- 最后，**调试驱动的对话式修复** 以迭代层级方式运行：外层循环负责插桩和轨迹收集，内层循环结合此前的修复尝试和新观察到的运行时状态来细化补丁，直到测试通过或预算耗尽。

## 结果
- 在 **Defects4J** 上使用 **GPT-3.5** 时，DebugRepair 正确修复了 **224 个 bug**，相比当前最优的基于 LLM 的基线方法，平均提升 **26.2%**。
- 在 **Defects4J** 上使用 **DeepSeek-V3** 时，DebugRepair 正确修复了 **295 个 bug**，比第二好的基线多 **59 个**。
- 在另外 **五个基础 LLM** 上，这些模型来自不同家族、规模各异，DebugRepair 相比各模型的原始设置，平均将修复表现提高了 **51.3%**。
- 评估覆盖了 **两种语言** 上的 **三个基准**：**Defects4J (v1.2 and v2.0)**、**QuixBugs** 和 **HumanEval-Java**，并与 **15 种代表性方法** 进行了比较。
- 论文称消融实验表明，各个主要组件都有帮助，尤其是测试净化和模拟调试，但这段摘录没有给出详细的消融数字。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.19305v1](http://arxiv.org/abs/2604.19305v1)
