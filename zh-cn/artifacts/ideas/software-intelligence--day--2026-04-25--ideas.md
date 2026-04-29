---
kind: ideas
granularity: day
period_start: '2026-04-25T00:00:00'
period_end: '2026-04-26T00:00:00'
run_id: materialize-outputs
status: succeeded
topics:
- agent-evaluation
- coding-agents
- benchmarks
- software-engineering
- repository-execution
tags:
- recoleta/ideas
- topic/agent-evaluation
- topic/coding-agents
- topic/benchmarks
- topic/software-engineering
- topic/repository-execution
language_code: zh-CN
---

# 可执行的代码证据

## Summary
可执行证据正成为代理评估和代码工作流中的实际标准。近期最清晰的落地方向，是一个检查真实状态和工具轨迹的可重放评估器，一个在补丁生成前先证明环境可运行的仓库接入层，以及一个在尚无测试用例时使用教师示例的科学代码工作流。

## 面向工具使用代理的可重放 episode 评估
构建客服、运维或浏览器代理的团队，现在有充分理由搭建一种评估框架：记录完整运行过程，并对状态变化、工具使用和用户可见产物打分。这比只看对话转录更可靠。sim/eval 论文给出了一套具体方案：把场景设计、模拟运行和评分分开；记录世界状态、工具调用轨迹、对话转录，以及截图或遥测数据；对最终状态和执行过程优先使用确定性检查；只在范围很窄的问题上使用模型裁判。CUJBench 提供了一个更贴近运维的例子。它把浏览器和后端证据冻结成确定性的事故快照，但六个前沿模型的准确率仍只有 19.7%，主要问题是跨模态综合推理。这里一个可落地的产品是面向单一狭窄流程的可重放 episode 运行器，比如退款、订单修改或结账失败诊断，并对后端状态和必需的工具调用设置通过/失败门槛。一个低成本的初步检查方法是，拿最近十个客服或事故案例，在沙箱里重放，并比较只看转录的评分与基于结果和工具轨迹的检查结果。如果排名不同，说明当前评估栈漏掉了生产环境里真正重要的失败。

### Evidence
- [Simulating and Evaluating Agentic Systems](../Inbox/2026-04-25--simulating-and-evaluating-agentic-systems.md): 定义了围绕完整运行产物、确定性断言、工具轨迹和状态变化的 sim/eval 方案。
- [CUJBench: Benchmarking LLM-Agent on Cross-Modal Failure Diagnosis from Browser to Backend](../Inbox/2026-04-25--cujbench-benchmarking-llm-agent-on-cross-modal-failure-diagnosis-from-browser-to-backend.md): 展示了确定性浏览器到后端诊断中的低准确率，并指出跨模态综合推理是持续存在的失败模式。

## 代码生成前的仓库环境就绪检查
仓库级代码代理在进入任何补丁基准测试或部署流程前，都需要一个独立的环境搭建阶段，并且要有单独的成功指标。RAT 报告称，在一个覆盖 2000 多个仓库的基准上，自动化环境搭建在真实仓库中可以达到较高成功率：Python 的 ESSR 为 63.2%，Java 为 41.3%，Rust 为 98.7%，JS/TS 为 68.7%。开源提交研究说明了为什么这个阶段应当与补丁生成分开。即使在 C 项目的小型真实提交上，生成的修改仍会编译失败、触发静态分析警告，并且通不过测试。这指向一个明确的产品空缺：在任何代码编辑代理启动前，先由一个仓库接入 worker 检测语言、选择基础镜像、安装依赖、运行冒烟测试，并输出机器可读的就绪报告。首批用户会是内部开发工具团队和基准构建者，因为他们经常把时间耗在那些还没进入执行阶段就已经失败的任务上。一个低成本的验证步骤是，把这个接入 worker 跑在一组混合的 50 个仓库上，衡量它在不需要人工修复的情况下，有多大比例能到达可复现的构建或测试命令。

### Evidence
- [RAT: RunAnyThing via Fully Automated Environment Configuration](../Inbox/2026-04-25--rat-runanything-via-fully-automated-environment-configuration.md): 提供了基准证据，说明自动化仓库环境配置在多种语言上既可行也可度量。
- [Can LLMs be Effective Code Contributors? A Study on Open-source Projects](../Inbox/2026-04-25--can-llms-be-effective-code-contributors-a-study-on-open-source-projects.md): 表明即使在真实仓库任务中完成代码生成后，编译失败、静态分析失败和测试失败仍然常见。

## 无测试用例时面向科学工作流的教师引导代码生成
科学计算代码团队可以测试一种适用于“还没有输入/输出测试集”的代码生成流程。MOSAIC 给出了一种具体模式：用领域内教师示例生成推理模板和伪代码，保留只包含先前函数签名和摘要的紧凑滚动上下文，并把自动调试限制在语法和 import 修复上。在 SciCode 上，这种做法在 GPT-4o、Claude Sonnet 4 和 Gemini 2.5 Flash 上都提升了结果；紧凑上下文窗口也很关键，因为在消融实验中，保留全部历史代码会让性能明显下降。这对实验室和研究软件团队有用，因为他们常常根据方法描述编写数值计算或仿真代码，而验证更多依赖领域审查，不是固定测试答案。一个可行的试点是先搭一个脚手架，让领域负责人为某个子领域整理一小组教师示例，再生成带有明确中间步骤和人工审查交接点的工作流代码。第一步检查很直接：在一小组内部任务上，对比有无紧凑上下文和教师示例时生成代码的质量，再看审查者是否花更少时间修正算法结构。

### Evidence
- [No Test Cases, No Problem: Distillation-Driven Code Generation for Scientific Workflows](../Inbox/2026-04-25--no-test-cases-no-problem-distillation-driven-code-generation-for-scientific-workflows.md): 展示了科学工作流中一种不依赖 I/O 测试驱动生成的具体替代方案，并报告了多个模型骨干上的提升。
