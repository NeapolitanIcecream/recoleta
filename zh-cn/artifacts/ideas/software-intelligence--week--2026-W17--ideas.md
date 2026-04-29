---
kind: ideas
granularity: week
period_start: '2026-04-20T00:00:00'
period_end: '2026-04-27T00:00:00'
run_id: materialize-outputs
status: succeeded
topics:
- coding-agents
- evaluation
- repo-level-codegen
- execution
- agent-harness
tags:
- recoleta/ideas
- topic/coding-agents
- topic/evaluation
- topic/repo-level-codegen
- topic/execution
- topic/agent-harness
language_code: zh-CN
---

# 可执行的仓库就绪性

## Summary
本周的编码代理工作指向三个实际变化：把仓库搭建视为独立的可执行阶段，用按规模区分的可运行测试来评估仓库生成，并把 harness 特性纳入明确的基准控制。共同模式很清楚：可运行的证明不只取决于底座模型。环境配置、仓库规模和 flag 之间的相互作用，都会改变代理是否能完成真实的软件任务。

## 带可执行搭建日志的仓库引导 worker
仓库级编码代理需要一个独立的环境搭建阶段，并为它单独设定预算、遥测和通过标准。本周的证据表明，搭建失败是一个独立的运维问题，不是代码生成前的一小段准备工作。RAT 在一个覆盖 2,000+ 个仓库的基准上报告了可执行环境搭建成功率：Python 为 63.2%，Java 为 41.3%，Rust 为 98.7%，JS/TS 为 68.7%，并且相对使用相同底座模型的 SWE-agent 有明显提升。成本也很明确：在一个 Python 设定下，完整 RAT 平均使用约 421.9K tokens，耗时 24.3 分钟。在内部仓库中部署编码代理的团队可以把这转成一个具体的流程变化：把环境配置当作一级步骤来运行，记录仓库是否变为可运行状态，并且当搭建从未成功时，不再继续评估下游补丁质量。

这里可落地的构建是一个仓库引导 worker：检测语言、选择基础镜像、在沙箱中安装依赖，并输出机器可读的搭建记录，其中包含尝试过的命令、修改过的文件、测试或 smoke check 状态，以及失败类别。这类输出既能用于评测，也能驱动面向用户的产品行为。一个低成本测试方法是，从内部仓库中抽取一个混合样本，测量这个 worker 在任何代码编辑代理启动前，把仓库带到可运行状态的比例。如果这个比例很低，那么补丁生成指标就在掩盖主要失败模式。

### Evidence
- [RAT: RunAnyThing via Fully Automated Environment Configuration](../Inbox/2026-04-25--rat-runanything-via-fully-automated-environment-configuration.md): RAT 按语言量化了环境搭建成功率，与基线方法做了比较，并报告了可执行环境搭建的 token 和时延成本。
- [RAT: RunAnyThing via Fully Automated Environment Configuration](../Inbox/2026-04-25--rat-runanything-via-fully-automated-environment-configuration.md): 论文指出，仓库级任务需要可执行环境，否则代码既无法验证，也无法在功能上成立。

## 按规模分桶计分的仓库级评测 harness
仓库级代码生成的评测现在可以围绕结构化设计输入和可运行的仓库测试来构建，并按仓库规模分开评估。RealBench 给出了修改评测 harness 的直接理由：当前模型在完整仓库生成上的平均 Pass@1 只有 19.39%；在低于 500 LOC 的仓库上，表现还能保持在 40% 以上；超过 2000 LOC 后，则降到 15% 以下。它还报告称，整体式生成在较小仓库上效果更好，而仓库变大后，增量式生成效果更好。

对模型团队和应用平台团队来说，一个具体可做的构建是内部基准：从需求说明加包图和类图开始，再按测试通过率、覆盖率和规模分桶来给生成仓库打分。关键的流程变化是停止只报告一个覆盖整个仓库的总分。小仓库和大仓库的行为差异已经大到足以让单一混合指标掩盖系统真正可用的范围。这也能形成一个直接的产品门槛：对小型、低依赖代码库允许端到端仓库生成；对更大的代码库，则要求按文件或按模块逐步规划。一个低成本检查方法是，在同一组任务上重新运行现有编码代理，分别对低于 1000 LOC 和高于 1000 LOC 的仓库单独计分，并比较整体式生成与增量式生成。

### Evidence
- [RealBench: A Repo-Level Code Generation Benchmark Aligned with Real-World Software Development Practices](../Inbox/2026-04-24--realbench-a-repo-level-code-generation-benchmark-aligned-with-real-world-software-development-practices.md): RealBench 报告了仓库级 Pass@1、按仓库规模划分的表现，以及整体式与增量式生成策略的差异。
- [RealBench: A Repo-Level Code Generation Benchmark Aligned with Real-World Software Development Practices](../Inbox/2026-04-24--realbench-a-repo-level-code-generation-benchmark-aligned-with-real-world-software-development-practices.md): 论文写明，较小仓库更适合整仓生成，而复杂仓库需要分阶段生成。

## 面向编码代理的 harness flag 注册表与基准回放
在继续加入更多记忆、反思或自评特性之前，代理团队有理由先建立一个独立的 harness 调参循环。HARBOR 在 Terminal-Bench 2 上的手动调参研究显示，这些组合很不稳定：全部 flag 关闭的基线通过了 89 个任务中的 15 个；一个包含 5 个原生 flag 的配置达到 17/89；加入自评 gate 后降到 13/89；再加入 ACON、Reflexion 和 PASTE 后降到 12/89。论文还指出，在生产风格代理中，harness 代码占实现的大头，其中一个被引用的审计给出的 Claude Code 比例约为 98.4%。

最直接的构建是为 harness 特性建立一个 flag 注册表和实验运行器，覆盖缓存模式、上下文压缩、轨迹回放、工具预测和自评 gate 等功能。每次运行都应记录启用的 flags、任务集版本、运行成本，以及在固定可执行基准上的通过数。这对那些不断给编码代理加特性、却只看最新版本在演示里是否感觉更好的团队很有用。一个低成本检查方法是，在一个稳定的终端或仓库基准上回放最近几次 harness 发布，看看最近新增特性到底提高了通过率，还是只增加了时延和上下文占用。

### Evidence
- [HARBOR: Automated Harness Optimization](../Inbox/2026-04-22--harbor-automated-harness-optimization.md): HARBOR 报告了四轮手动调参研究，并显示额外的 harness 特性可能降低任务成功率。
- [HARBOR: Automated Harness Optimization](../Inbox/2026-04-22--harbor-automated-harness-optimization.md): 论文写到，生产风格代理主要由 harness 代码和运维复杂性构成。
