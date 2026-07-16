---
kind: trend
trend_doc_id: 1317
granularity: day
period_start: '2026-06-02T00:00:00'
period_end: '2026-06-03T00:00:00'
topics:
- agentic software engineering
- LLM training
- code repair
- terminal agents
- multi-agent orchestration
- developer tooling
- agent trust
run_id: materialize-outputs
aliases:
- recoleta-trend-1317
tags:
- recoleta/trend
- topic/agentic-software-engineering
- topic/llm-training
- topic/code-repair
- topic/terminal-agents
- topic/multi-agent-orchestration
- topic/developer-tooling
- topic/agent-trust
language_code: zh-CN
---

# Evidence-rich control loops are the center of agentic coding work

## 概览
这一时期把大语言模型（LLM）代理当作可训练、可检查的软件系统。EvoTrainer、FLARE 和 SPOQ 的证据最强：更好的代理来自诊断、带门控的执行和任务结构，人类判断出现在规划和验证环节。

## 研究发现

### Training harnesses and interaction traces
代理训练工作关注训练期间可用的证据，而不只看最终任务分数。EvoTrainer 让策略分支和读取 rollout、日志、配置、代码 diff 的诊断代码一起演化。它报告的最强提升来自仓库级软件工程：SWE-9B 的 Avg@8 BC% 达到 38.16，而人工设计的强化学习方案为 33.77。

终端代理研究通过监督微调得到相近结论。DeepSeek-V3.2 的 Terminal-Bench 2.0 单独分数低于 Claude Opus 4.6，但它的轨迹训练出更强的 Qwen3 学生，因为这些轨迹展示了更多 inspect-act-verify 行为。屏蔽 observation-command 关联后，Targeted Observation Ratio 从 13.4% 降到 5.3%，Qwen3-32B 的表现从 20.6% 降到 13.8%。

#### 资料来源
- [EvoTrainer: Co-Evolving LLM Policies and Training Harnesses for Autonomous Agentic Reinforcement Learning](../Inbox/2026-06-02--evotrainer-co-evolving-llm-policies-and-training-harnesses-for-autonomous-agentic-reinforcement-learning.md): EvoTrainer summary, mechanism, and SWE-9B result against human-engineered RL.
- [What Makes Interaction Trajectories Effective for Training Terminal Agents?](../Inbox/2026-06-02--what-makes-interaction-trajectories-effective-for-training-terminal-agents.md): Terminal-agent teacher comparison, trace properties, and TOR ablation results.

### Fine-grained code repair signals
代码修复论文把调试反馈做得更局部，也更容易验证。FLARE 给执行反馈加上线级可疑度分数，然后在 top-k 行上搜索候选修改。k=10 时，它在 LiveCodeBench 和 BigCodeBench 上让五个基础模型的 Pass@1 都有所提升，而它自己的诊断模型在 100 个 LiveCodeBench 任务上达到 67% 的 Top-1 定位准确率和 89% 的 Top-10 定位准确率。

Neural Change Prediction 用合成突变和观察到的输出变化来学习修改行为关系的两个方向。微调后的 GPT-4.1 在 CSS 变化预测上达到 95% 准确率，在单次突变的 Python 变化位置预测上达到 82.6%，在从单个 Python 代码突变预测输出变化上达到 95%。实际价值很明确：先按预期行为给候选修复排序，再用测试检查。

#### 资料来源
- [FLARE: Fine-Grained Diagnostic Feedback for LLM Code Refinement](../Inbox/2026-06-02--flare-fine-grained-diagnostic-feedback-for-llm-code-refinement.md): FLARE approach, benchmark gains, candidate search, and localization results.
- [Neural Change Prediction: Relating Software Changes to Their Effects and Vice Versa](../Inbox/2026-06-02--neural-change-prediction-relating-software-changes-to-their-effects-and-vice-versa.md): Neural Change Prediction data construction and CSS/Python accuracy results.

### Multi-agent task orchestration with human gates
SPOQ 把软件工作看作依赖图。它把一个 epic 拆成原子任务，把独立任务按并行波次调度，并用 95% 的总阈值来做规划和代码验证门控。报告结果包括：在无界合成图上最高 14.3x 的加速，在带 2 个槽位的真实 LLM 后端上 1.4x 的加速，以及在使用双重验证时测试通过率从 91.25% 升到 99.75%。

一篇更广泛的综合论文解释了这些门控的组织原因。它引用了 61,453 个仓库中的 456,535 个代理作者 pull request，但也指出代理作者 pull request 的合并率更低，而且往往带来的结构性代码改动更少。这组文献里对人的角色描述是：在需求说明、审查、治理，以及规划含糊或改动风险高时做升级处理。

#### 资料来源
- [SPOQ: Specialist Orchestrated Queuing for Multi-Agent Software Engineering](../Inbox/2026-06-02--spoq-specialist-orchestrated-queuing-for-multi-agent-software-engineering.md): SPOQ task graph, validation gates, human-as-agent design, and reported execution results.
- [Human-AI Collaboration and the Transformation of Software Engineering Work](../Inbox/2026-06-02--human-ai-collaboration-and-the-transformation-of-software-engineering-work.md): Evidence on agent-authored pull requests and the proposed human competency model.

### Runtime cost, memory, and trust metadata
面向开发者的工具关注编码代理周边的运行成本。Cross-Lingual Token Arbitrage 在发往云端之前先在本地重写多语言提示词。On OMH-Polyglot，提示词 token 数下降 34–47%，同时在 gpt-3.5-turbo、gpt-4o 和 gemini-2.5-flash-lite 上准确率保持不变或有所提升，不过不同后端的美元节省幅度不同，因为输出 token 定价会抵消输入端节省。

Project Brain 用一个指向主题文件的小型 Markdown 索引来减少反复搭建上下文的开销。它没有基准测试，但设计很具体：先加载索引，只有在相关时才打开详细项目笔记，并检查失效指针或状态漂移。另一篇代理网络论文补上了信任这一层：能力广告应包含可靠性估计、基准名称、样本量、评测日期、版本限制、过期时间、测试和信誉更新。

#### 资料来源
- [Cross-Lingual Token Arbitrage: Optimizing Code Agent Context Windows via Local LLM Preprocessing](../Inbox/2026-06-02--cross-lingual-token-arbitrage-optimizing-code-agent-context-windows-via-local-llm-preprocessing.md): Local prompt rewriting design and token, accuracy, and cost results.
- [Project Brain – Persistent memory index for AI coding](../Inbox/2026-06-02--project-brain-persistent-memory-index-for-ai-coding.md): Project Brain memory layout, claimed token behavior, and lack of measured results.
- [Capability Advertisement as a Market for Lemons: A Trust Layer for Heterogeneous Agent Networks](../Inbox/2026-06-02--capability-advertisement-as-a-market-for-lemons-a-trust-layer-for-heterogeneous-agent-networks.md): Trust Layer proposal for evidence-backed capability claims and drift checks.
