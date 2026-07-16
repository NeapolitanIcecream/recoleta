---
kind: ideas
granularity: day
period_start: '2026-06-02T00:00:00'
period_end: '2026-06-03T00:00:00'
run_id: materialize-outputs
status: succeeded
topics:
- agentic software engineering
- LLM training
- code repair
- terminal agents
- multi-agent orchestration
- developer tooling
- agent trust
tags:
- recoleta/ideas
- topic/agentic-software-engineering
- topic/llm-training
- topic/code-repair
- topic/terminal-agents
- topic/multi-agent-orchestration
- topic/developer-tooling
- topic/agent-trust
language_code: zh-CN
---

# Intermediate Evidence Gates for Coding Agents

## 摘要
当团队保留中间证据时，智能体编码工作会更容易改进：修复循环里的可疑行、多智能体执行中的明确依赖门禁，以及终端代理训练中的轨迹质量信号。实际工作是给现有代理加上小型评分和验证层，然后比较最近任务的通过率、评审负担和返工量。

## Line-ranked repair candidates for failed coding-agent runs
编码代理的修复循环可以在模型请求下一次编辑前，先给出一组按可能出错程度排序的代码行。FLARE 展示了具体做法：一个轻量诊断模型给词法单元打分，把分数汇总到行级可疑度，再围绕 top-k 可疑行生成修订，运行测试，并保留执行结果最好的候选。设置 k=10 时，FLARE 在 LiveCodeBench 和 BigCodeBench 上提高了五个基础模型的 Pass@1；它的诊断模型在 100 个 LiveCodeBench 任务上的定位准确率达到 Top-1 67% 和 Top-10 89%。

这个流程适合已经在 CI 中收集失败代理补丁的团队。可以保存失败程序、测试输出、如果有的话保存 token 概率、可疑行排名、生成的候选和测试结果。还可以为拟议修改加一个小的行为检查：Neural Change Prediction 报告说，变异-输出对可以训练模型预测代码修改的可能效果，微调后的 GPT-4.1 在单次 Python 变异上的输出变化预测准确率达到 95%。试点可以回放最近失败的生成结果，比较只看执行反馈的修复和按行排名的候选搜索，在通过率和每个接受修复所花的评审分钟数上的差异。

### 资料来源
- [FLARE: Fine-Grained Diagnostic Feedback for LLM Code Refinement](../Inbox/2026-06-02--flare-fine-grained-diagnostic-feedback-for-llm-code-refinement.md): FLARE reports line-level suspiciousness, top-k repair search, Pass@1 gains, and localization accuracy.
- [FLARE: Fine-Grained Diagnostic Feedback for LLM Code Refinement](../Inbox/2026-06-02--flare-fine-grained-diagnostic-feedback-for-llm-code-refinement.md): The paper abstract states that top-k suspicious-region search improves iterative LLM code refinement.
- [Neural Change Prediction: Relating Software Changes to Their Effects and Vice Versa](../Inbox/2026-06-02--neural-change-prediction-relating-software-changes-to-their-effects-and-vice-versa.md): Neural Change Prediction reports training on mutation-output pairs and high accuracy for predicting behavior effects of code changes.

## Dependency-graph dispatch with planning and code score gates for agent-written changes
多智能体编码运行应在实现开始前先暴露任务依赖。SPOQ 给出了一种具体做法：把一个史诗拆成 1-4 小时的任务，构建 DAG，将彼此独立的任务按并行波次派发，并在进入下一阶段前要求完成规划和代码验证门禁。它报告的收益对模型并发受限的团队很实用：SPOQ 在一个 2 槽位的真实 LLM 后端上测得稳定的 1.4x 加速，并通过双重验证把测试通过率从 91.25% 提高到 99.75%。

这对让代理从较大的需求单直接开 pull request 的团队最有用。采用上的改动是：先在代理写代码前加入一个人工规划检查点，再在每个任务后要求一个带评分的代码门禁。人的职责很具体：批准任务拆分、处理含糊需求、审查有风险的设计选择。一篇更广泛的综合研究引用了 456,535 个代理作者 pull request，覆盖 61,453 个仓库，同时也报告说代理作者 pull request 的合并率更低，结构性代码改动更少。这个模式支持在合并性和设计匹配很重要的地方给代理工作加门禁。

### 资料来源
- [SPOQ: Specialist Orchestrated Queuing for Multi-Agent Software Engineering](../Inbox/2026-06-02--spoq-specialist-orchestrated-queuing-for-multi-agent-software-engineering.md): SPOQ describes DAG task decomposition, parallel waves, validation gates, human participation, and reported speed and pass-rate results.
- [SPOQ: Specialist Orchestrated Queuing for Multi-Agent Software Engineering](../Inbox/2026-06-02--spoq-specialist-orchestrated-queuing-for-multi-agent-software-engineering.md): The abstract details 1.4x speedup on a 2-slot backend, dual validation gains, and deployment-scale results.
- [Human-AI Collaboration and the Transformation of Software Engineering Work](../Inbox/2026-06-02--human-ai-collaboration-and-the-transformation-of-software-engineering-work.md): The synthesis cites large-scale agent-authored pull request evidence and identifies human specification, verification, and governance needs.

## Trace quality gates for terminal-agent fine-tuning data
终端代理的训练数据应按轨迹是否显示有用的 inspect-act-verify 行为来筛选。终端代理研究发现，得分更低的教师模型 DeepSeek-V3.2 训练出的 Qwen3 学生模型，比 Claude Opus 4.6 训练出的更强，因为它的轨迹暴露了更多与环境相关的步骤。屏蔽观察-命令链接后，Targeted Observation Ratio 从 13.4% 降到 5.3%，Qwen3-32B 的表现从 20.6% 降到 13.8%。

训练团队可以把这变成一个轨迹门禁。记录文件检查、命令、测试运行、错误消息，以及每个命令依赖的路径或状态。给每条成功轨迹按 Targeted Observation Ratio 打分，在固定数据预算下保留高 TOR 轨迹，并标记那些动作没有可见支持性观察的轨迹。EvoTrainer 在长周期软件代理上也朝同一个操作方向前进：它的训练器读取 rollout、日志、配置、代码 diff 和指标，然后在现有证据无法解释结果时更新诊断。一个低成本验证办法，是在按 TOR 分组的匹配成功轨迹上跑一次 SFT，并在 Terminal-Bench 风格任务上测量结果。

### 资料来源
- [What Makes Interaction Trajectories Effective for Training Terminal Agents?](../Inbox/2026-06-02--what-makes-interaction-trajectories-effective-for-training-terminal-agents.md): The terminal-agent study defines Targeted Observation Ratio and reports stronger student performance from traces with inspect-act-verify behavior.
- [What Makes Interaction Trajectories Effective for Training Terminal Agents?](../Inbox/2026-06-02--what-makes-interaction-trajectories-effective-for-training-terminal-agents.md): The abstract describes environment-grounded supervision and data efficiency from Terminal-Lego trajectories.
- [EvoTrainer: Co-Evolving LLM Policies and Training Harnesses for Autonomous Agentic Reinforcement Learning](../Inbox/2026-06-02--evotrainer-co-evolving-llm-policies-and-training-harnesses-for-autonomous-agentic-reinforcement-learning.md): EvoTrainer describes training-side diagnostics over rollouts, logs, configs, and code diffs for agentic RL decisions.
