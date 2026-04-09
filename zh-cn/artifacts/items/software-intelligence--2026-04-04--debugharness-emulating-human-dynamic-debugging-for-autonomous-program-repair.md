---
source: arxiv
url: http://arxiv.org/abs/2604.03610v1
published_at: '2026-04-04T06:49:30'
authors:
- Maolin Sun
- Yibiao Yang
- Xuanlin Liu
- Yuming Zhou
- Baowen Xu
topics:
- automated-program-repair
- llm-agents
- dynamic-debugging
- software-security
- memory-safety
- c-cpp
relevance_score: 0.95
run_id: materialize-outputs
language_code: zh-CN
---

# DebugHarness: Emulating Human Dynamic Debugging for Autonomous Program Repair

## Summary
## 摘要
DebugHarness 是一个基于 LLM 的程序修复系统，面向困难的 C/C++ 安全漏洞。它不只读取静态代码，还使用实时调试。论文称，让代理访问运行时状态、逆向调试和补丁验证反馈后，在真实世界的内存安全漏洞上，修复成功率会提高。

## 问题
- 现有的 LLM 修复代理把漏洞修复当成静态代码生成任务，只使用源代码、崩溃报告和栈跟踪，缺少足够的运行时上下文。
- 这会在底层 C/C++ 缺陷上失效，例如释放后使用、堆损坏和陈旧指针问题，因为崩溃位置与根因在时间和代码位置上都可能相距很远。
- 这很重要，因为模糊测试器能发现很多安全漏洞，但打补丁仍然需要专家手动调试，导致修复变慢，也让系统暴露更久。

## 方法
- DebugHarness 从可复现的 PoC 崩溃和 sanitizer 报告开始，提取漏洞特征，并对错误类型分类，以加载适合该类漏洞的调试指导。
- 随后，代理运行交互式调试循环：它通过语言服务器检查源代码，通过 GDB 和 pwndbg 查询实时执行状态，并使用 `rr` 记录/重放，在执行过程中向后回溯，把内存损坏追踪到源头。
- 系统要求 LLM 形成一个具体的根因假设，用断点、观察点等调试器操作来验证，并根据观察到的运行时证据不断修正假设。
- 为了让调试器输出不超出上下文限制，系统会提炼原始跟踪结果，还可以在沙箱中运行 LLM 生成的 Python 脚本，汇总大型数据结构或内存转储。
- 在识别出可能原因后，系统会生成补丁，用一个确定性的对齐步骤修复格式错误的 diff，重新编译，重新运行 PoC 和测试，并把编译器或崩溃反馈送回下一轮迭代。

## 结果
- 评估使用 **SEC-bench**，这是一个基准，包含 **29** 个开源 **C/C++** 项目中的 **200 个真实世界安全漏洞**。
- DebugHarness 报告该基准上的总体漏洞解决率约为 **90%**。
- 论文与 **PatchAgent** 和 **VulnResolver** 对比，它们的解决率分别是 **57.5%** 和 **67.5%**。
- 论文声称，相比当前最先进的基线方法，提升幅度超过 **30% 相对改进**。
- 论文称，消融研究表明两个核心部分都对报告的性能有必要：**signature-driven investigation** 和 **interactive state introspection**，但摘录中没有给出消融实验的具体数字。
- 论文中的示例是 **mruby** 的 **CVE-2022-1286**，其中动态观察点和逆向追踪让代理发现了静态代理没有找到的 `mrb_mc_clear_by_class` 缓存失效遗漏。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.03610v1](http://arxiv.org/abs/2604.03610v1)
