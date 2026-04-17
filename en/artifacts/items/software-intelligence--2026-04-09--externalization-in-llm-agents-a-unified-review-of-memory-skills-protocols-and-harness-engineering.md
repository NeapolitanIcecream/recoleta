---
source: arxiv
url: http://arxiv.org/abs/2604.08224v1
published_at: '2026-04-09T13:19:41'
authors:
- Chenyu Zhou
- Huacan Chai
- Wenteng Chen
- Zihan Guo
- Rong Shan
- Yuanyi Song
- Tianyi Xu
- Yingxuan Yang
- Aofan Yu
- Weiming Zhang
- Congming Zheng
- Jiachen Zhu
- Zeyu Zheng
- Zhuosheng Zhang
- Xingyu Lou
- Changwang Zhang
- Zhihui Fu
- Jun Wang
- Weiwen Liu
- Jianghao Lin
- Weinan Zhang
topics:
- llm-agents
- agent-infrastructure
- memory-systems
- tool-protocols
- multi-agent-systems
- software-engineering-agents
relevance_score: 0.93
run_id: materialize-outputs
language_code: en
---

# Externalization in LLM Agents: A Unified Review of Memory, Skills, Protocols and Harness Engineering

## Summary
This paper is a review that argues current LLM agent progress comes from moving key burdens out of model weights and into runtime infrastructure. It unifies four parts of that shift: memory, skills, protocols, and the harness that coordinates them.

## Problem
- LLM agents are weak at long-term state, repeatable procedures, and reliable coordination with tools or other agents when those burdens stay inside prompts and model weights.
- Existing work often studies memory, tool use, agent protocols, or architectures separately, which makes it hard to explain why these threads are converging in practical systems.
- This matters because many deployed agent gains come from system design around the model, especially for long-horizon tasks such as software engineering, workflow automation, and multi-agent execution.

## Approach
- The paper gives a unified review through the idea of **externalization**: move cognitive burdens into explicit external artifacts that the model can query or follow.
- It splits externalization into three parts: **memory** for state across time, **skills** for reusable procedures, and **protocols** for structured interaction with tools, services, users, and other agents.
- It defines **harness engineering** as the runtime layer that orchestrates these parts with control logic, constraints, observability, approval loops, and recovery mechanisms.
- It frames the field's history as a shift from **weights -> context -> harness**, where capability moves from model parameters to prompt/context design and then to persistent infrastructure.
- It uses examples from prior systems such as RAG, ReAct, AutoGen, MetaGPT, SWE-agent, and OpenHands to show how external modules change the task the model has to solve.

## Results
- This is a survey/review paper. The excerpt provides **no new benchmark numbers or experimental metrics**.
- The main claim is conceptual: reliable agent behavior comes less from changing model weights and more from externalizing three burdens: continuity into memory, procedure into skills, and coordination into protocols.
- It claims the harness is the integrating runtime that makes these modules usable in practice through sequencing, validation, sandboxing, observability, and feedback loops.
- It claims the strongest practical gains in agent systems often come from infrastructure changes such as persistent memory, tool registries, protocolized interfaces, and multi-step orchestration rather than from a new base model alone.
- It identifies open issues in evaluation, governance, trade-offs between parametric and externalized capability, and future directions such as self-evolving harnesses and shared agent infrastructure.

## Link
- [http://arxiv.org/abs/2604.08224v1](http://arxiv.org/abs/2604.08224v1)
