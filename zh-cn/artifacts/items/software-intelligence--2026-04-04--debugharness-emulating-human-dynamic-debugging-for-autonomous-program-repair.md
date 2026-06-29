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
DebugHarness 是一个基于 LLM 的程序修复系统，面向难修的 C/C++ 安全漏洞，依赖实时调试，而不只是静态读代码。论文声称，让代理访问运行时状态、反向调试和补丁验证反馈后，修复真实世界内存安全漏洞的成功率会提高。

## 问题
- 现有的 LLM 修复代理把漏洞修复当作静态代码生成任务，只用源代码、崩溃报告和堆栈跟踪，缺少足够的运行时上下文。
- 这类方法在处理 use-after-free、堆损坏和过期指针等低层级 C/C++ 缺陷时会失效，因为崩溃点和根因可能在时间和代码位置上相距很远。
- 这很重要，因为 fuzzers 可以发现很多安全漏洞，但修补它们仍然需要专家手工调试，修复速度会变慢，系统也会继续暴露在风险中。

## 方法
- DebugHarness 从可复现的 PoC 崩溃和 sanitizer 报告开始，提取 bug 特征，并对错误类型分类，以加载针对该类漏洞定制的调试指导。
- 然后代理进入交互式调试循环：它通过语言服务器查看源代码，通过 GDB 和 pwndbg 查询实时执行状态，并使用 `rr` 录制/回放向后回溯执行，追踪内存损坏的源头。
- 系统要求 LLM 形成具体的根因假设，用断点和观察点等调试操作验证假设，并根据观测到的运行时证据修正假设。
- 为了让调试器输出保持在上下文限制内，它会压缩原始跟踪信息，也可以在沙箱里运行 LLM 生成的 Python 脚本，用来总结大型结构或内存转储。
- 找到可能原因后，它生成补丁，用确定性的对齐步骤修复格式不正确的 diff，重新编译，重新运行 PoC 和测试，并把编译器或崩溃反馈带回下一轮迭代。

## 结果
- 评估使用 **SEC-bench**，这是一个包含 **29** 个开源 **C/C++** 项目、共 **200** 个真实世界安全漏洞的基准。
- DebugHarness 在这个基准上的整体漏洞修复率约为 **90%**。
- 论文把它和 **PatchAgent** 的 **57.5%** 以及 **VulnResolver** 的 **67.5%** 修复率作比较。
- 论文声称，相比当前最好的基线，提升超过 **30% 的相对改进**。
- 论文说消融实验表明，两个核心部分，**签名驱动的调查** 和 **交互式状态内省**，对报告中的性能都必不可少，但节选没有给出消融数值。
- 动机案例是 **mruby** 中的 **CVE-2022-1286**，动态观察点和反向追踪让代理找到静态代理会漏掉的 `mrb_mc_clear_by_class` 缓存失效缺失。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.03610v1](http://arxiv.org/abs/2604.03610v1)
