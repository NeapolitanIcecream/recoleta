---
source: arxiv
url: https://arxiv.org/abs/2605.27360v1
published_at: '2026-05-26T17:58:43'
authors:
- Tamerlan Aghayev
- Maxime Elkael
- Michele Polese
- Minh Dat Nguyen
- Gabriele Gemmi
- Andrea Lacava
- Ali Saeizadeh
- Reshma Prasad
- Paolo Testolina
- Angelo Feraudo
- Soumendra Nanda
- Pedram Johari
- Salvatore D'Oro
- Tommaso Melodia
topics:
- multi-agent-software-engineering
- code-generation
- ran-engineering
- spec-to-code
- agentic-testing
- 6g-ran
relevance_score: 0.88
run_id: materialize-outputs
language_code: zh-CN
---

# GENESIS: Harnessing AI Agents for Autonomous 6G RAN Synthesis, Research, and Testing

## Summary
## 总结
Genesis 是一个多智能体系统，用来把 3GPP/O-RAN 意图转换成 RAN 代码、测试、补丁和实验，这些内容可以在模拟器、仿真器和真实无线电上运行。论文声称，在两个 RAN 功能实现案例中，它达到了 100% 成功率，而 Claude Code 搭配 Opus 4.7 没有产出任何可工作的实现。

## 问题
- RAN 研发速度很慢，因为特性合成、一致性测试、加固、优化、发现和安全工作在每次迭代中都要花费数月工程时间。
- 在一项被引用的 5G 栈分析中，一个较大的特性从平均进入 stable 分支用了 74 天，90 分位数是 207 天。
- 通用 LLM 编码代理在 RAN 任务上会失败，因为一个小的 API 错误或规范误读就会破坏与标准设备、无线电和 OTA 测试平台的互操作性。

## 方法
- Genesis 会把一个意图，比如规范条款、遥测异常或研究假设，路由到 6 条流水线之一：Synthesize、Test、Harden、Optimize、Discover 或 Secure。
- 核心机制很直接：代理决定做什么，确定性的技能执行 build、deploy、configure 和 experiment 这类动作，hooks 记录事件、强制安全门控并保存溯源信息。
- Synapse 存储整理过的 3GPP/O-RAN 规范、研究论文、参考代码、实验室库存、代码差异、日志、轨迹和实验输出，所以后续运行可以复用已验证的工件。
- 验证跨越 3 个层级：RFSIM 仿真、Colosseum 或硬件在环仿真，以及在 X5G 和 Arena 这类生产级测试平台上的 OTA 部署。
- 这个原型使用了大约 23 个参数化技能，可以运行商业和本地模型，包括 Claude Opus 4.7、Claude Sonnet 4.6、gpt-oss、Llama 4、Phi 和 Gemma。

## 结果
- 在多次统计独立运行中，Genesis 在实现 3GPP TS 28.552 中的 RRC.ConnMean KPM 和带闭环 E2SM-RC xApp 的 Conditional Handover 时都达到了 100% 成功率。
- 基线 Claude Code 搭配 Opus 4.7 在前 2 个案例研究的每次尝试中都没有产出可工作的实现。
- 评估覆盖 3 个端到端案例研究：RRC.ConnMean KPM 合成和 OTA 传播、CHO 合成/测试/加固，以及使用 ALLSTaR 循环的自主 RAN 调度器发现。
- 该系统通过 6 条流水线覆盖完整的 6 步 RAN 研发周期，并在把结果反馈到 Synapse 之前，先在 3 个基础设施层级上验证生成的变更。
- 论文报告了跨阶段的剖析结果，并说 6 个 Synthesize 阶段里有 2 个，即功能实现和测试执行，在成本和墙钟时间上都占主导。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.27360v1](https://arxiv.org/abs/2605.27360v1)
