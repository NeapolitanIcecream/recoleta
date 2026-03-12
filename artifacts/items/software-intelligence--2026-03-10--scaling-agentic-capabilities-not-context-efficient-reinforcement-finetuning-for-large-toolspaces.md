---
source: hf_daily
url: https://huggingface.co/papers/2603.06713
published_at: null
authors: []
topics:
- agentic-systems
- reinforcement-finetuning
- tool-using-llms
- small-language-models
- context-control
relevance_score: 0.95
run_id: fa4f5d9d-bee2-47ee-b80f-c690622f57d0
---

# Scaling Agentic Capabilities, Not Context: Efficient Reinforcement Finetuning for Large Toolspaces

## Summary
### TL;DR: ATLAS 通过强化微调让小语言模型在超大工具空间中学会“按需取上下文 + 按结构执行工具”，从而在更小参数量和更紧上下文预算下，达到接近前沿智能体的工具使用能力。

### Problem:
- 目标问题：让小语言模型（SLM）在包含大量工具的环境中完成长流程、弱监督的 agent 任务，而不是依赖大模型的参数规模和超长上下文窗口。
- 关键困难：如果把工具说明一次性全塞进上下文，会迅速挤爆上下文；多步执行中错误会级联放大；任务奖励稀疏且往往难以直接验证，训练信号弱。
- 为什么重要：这关系到低成本、可部署的软件智能体能否在真实工具生态中稳定工作，直接影响自动化软件生产、代码智能体和多工具 agent 系统的实用性。

### Approach:
- 把**上下文控制**本身当成可学习决策：模型不再一次性加载所有工具，而是迭代式、按需加载相关工具信息，控制上下文增长。
- 把**执行结构**当成可学习决策：通过程序化的工具编排（programmatic tool orchestration）来约束多步执行过程，减少长轨迹中的失误累积。
- 提出 **rubric-based reinforcement finetuning**：把“任务是否成功”拆解为结构化、任务对齐的评分标准（rubrics），用更细粒度的奖励替代单一稀疏成功信号。
- 使用小型 judge models 进行可扩展打分，使弱/不可验证监督下的 RL 微调更可行、成本更低。

### Results:
- 在 **MCP benchmarks** 上，ATLAS 相比通用 RL 基线取得了**大且一致的提升**；摘要未给出具体分数或百分比。
- ATLAS 使 **4B** 级小语言模型能够在**更严格的参数与上下文预算**下，达到**接近 frontier-agent performance** 的水平。
- 论文的核心主张是：与其单纯扩上下文或模型规模，不如学习“何时取什么上下文、如何结构化执行”，这对大工具空间中的 agent 能力更关键。
- 提供文本中**没有具体定量指标**（如准确率、成功率、相对提升百分比、具体基线名称）。

## Links
- Canonical: https://huggingface.co/papers/2603.06713
