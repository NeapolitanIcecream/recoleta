---
source: arxiv
url: https://arxiv.org/abs/2606.26859v1
published_at: '2026-06-25T10:42:28'
authors:
- Changxin Lao
- Fei Pan
- Guozhuang Ma
- Han Li
- Huihuang Lin
- Jijun Shi
- Kangzhi Zhao
- Kun Gai
- Mo Zhou
- Qinqin Zhou
- Quan Chen
- Ruochen Yang
- Shifu Bie
- Shuang Yang
- Shuo Yang
- Wenhao Li
- Wentao Xie
- Xiao Lv
- Xuming Wang
- Yijun Wang
- Yiming Chen
- Yusheng Huang
- Zhongyuan Wang
- Zibo Zhao
- Zijie Zhuang
- Baoning Xia
- Chao Liu
- Chaoyi Ma
- Chubo He
- Dawei Cong
- Feng Jiang
- Gang Wang
- Guilin Xia
- Hanwen Xu
- Jiahong Xie
- Jiahui Qiao
- Jian Liang
- Jiangfan Yue
- Jing Wang
- Jinghan Yang
- Jinghui Jia
- Kan Qin
- Lei Wang
- Ming Li
- Peilin Song
- Pengbo Xu
- Qiang Luo
- Ruiming Tang
- Shiyang Liu
- Shuxian Jin
- Tao Wang
- Tao Zhang
- Xiang Gao
- Xianghan Li
- Yingsong Luo
- Yiwen Ning
- Yongcheng Liu
- Yuan Guo
- Zhaojie Liu
- Zhenkai Cui
topics:
- agentic-recsys
- multi-agent-systems
- automated-code-generation
- online-ab-testing
- recommender-systems
- self-improving-agents
relevance_score: 0.86
run_id: materialize-outputs
language_code: en
---

# AgentX: Towards Agent-Driven Self-Iteration of Industrial Recommender Systems

## Summary
AgentX is a production multi-agent system that runs recommendation experiments from idea generation to code changes, A/B rollout, and learning from outcomes. Kuaishou reports that a three-worker deployment produced 10 launchable rollouts from 374 ideas in three weeks and generated a 0.561% app-time gain.

## Problem
- Industrial recommender iteration depends on engineers for hypotheses, code edits, A/B launches, and attribution, so experiment throughput scales with headcount.
- Offline ML-agent tests do not provide the online reward signal needed for recommender changes; a change must pass live business metrics and safety guardrails.
- The bottleneck matters because release cycles can take weeks, while repeated failures and launch reviews lose value if they are not stored as reusable experiment records.

## Approach
- AgentX uses a four-stage loop: Brainstorm Agent ranks evidence-grounded proposals, Developing Agent edits repository-grounded production code, Evaluation Agent manages rollout and A/B judgment, and Harness Evolution updates agent instructions from execution trajectories.
- Brainstorm Agent pulls evidence from Experiment KB, System KB, Data Analysis, and Model Research, then scores candidates by objective alignment, business validity, feasibility, handoff completeness, evidence, and risk.
- Developing Agent turns accepted proposals into code using repository context, verification loops, and quality scoring before launch.
- Evaluation Agent assigns traffic safely, applies guardrail vetoes to A/B results, and stores both wins and failures as reusable knowledge assets.
- Harness Evolution uses Semantic-Gradient-based Prompt Optimization (SGPO) to convert successful and failed trajectories into prompt and agent-spec updates, with paired replay before changes are accepted.

## Results
- In a three-week Kuaishou App deployment across main-feed and life-service recommendation, 3 AgentX workers generated 374 ideas and 10 launchable rollouts.
- The paper claims per-worker throughput doubled each week during the deployment after self-evolution updates.
- Compared with a manual engineer baseline, AgentX claims 8x concurrency and 3.7x business value.
- The reported online business impact is a 0.561% user app-time gain and more than RMB 100M in annualized revenue.
- The paper also claims the same loop can support model-side research tasks such as paper reproduction, module ablation, and cross-paper architecture composition, but the excerpt does not provide full quantitative results for those tasks.
- The evaluation signal is online A/B feedback with guardrail vetoes; the excerpt does not include statistical confidence intervals or a full ablation table.

## Link
- [https://arxiv.org/abs/2606.26859v1](https://arxiv.org/abs/2606.26859v1)
