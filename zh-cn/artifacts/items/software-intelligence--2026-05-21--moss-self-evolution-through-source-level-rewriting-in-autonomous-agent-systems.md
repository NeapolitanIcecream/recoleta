---
source: arxiv
url: https://arxiv.org/abs/2605.22794v1
published_at: '2026-05-21T17:48:33'
authors:
- Qianshu Cai
- Yonggang Zhang
- Xianzhang Jia
- Wei Xue
- Jun Song
- Xinmei Tian
- Yike Guo
topics:
- software-foundation-model
- code-intelligence
- agent-self-improvement
- multi-agent-software-engineering
- automated-software-production
- human-ai-interaction
relevance_score: 0.93
run_id: materialize-outputs
language_code: zh-CN
---

# MOSS: Self-Evolution through Source-Level Rewriting in Autonomous Agent Systems

## Summary
## 概述
MOSS 让已部署的智能体系统在收集到生产故障证据后，连 harness 代码在内一起重写自己的源代码。论文声称，在 OpenClaw 上，经过一次进化循环，四项任务的平均评分从 0.25 提升到 0.61，而且没有人工改代码。

## 问题
- 已部署的智能体常常会反复出现同样的失败，直到人工发布更新。
- 早期的自进化智能体只改提示词、技能、记忆或工作流图，所以它们无法修复路由、钩子顺序、会话状态、分发或并发中的代码级故障。
- 这会影响线上用户；随着智能体底座加入更多通道、插件、持久状态和多步执行，这类 harness 缺陷也更容易出现。

## 方法
- MOSS 从真实用户会话中构造故障批次。定期扫描和用户标记会加入缺失或较弱的对话片段；默认开放批次在 8 个 chunk 时封存。
- 它运行一个迭代循环，先做基线评估，然后按顺序执行 7 个阶段：Locate、Plan、Plan-Review、Implement、Code-Review、Task-Evaluate 和 Verdict。
- 源码修改由外部 coding-agent CLI 完成，包括 Claude Code、OpenAI Codex、DeepSeek-TUI 和 OpenCode。MOSS 控制阶段顺序、评审门控、判定和部署。
- 候选镜像会在临时试运行 worker 容器中测试，先重放故障批次，再决定是否推进。
- 推进需要通过 `moss evo apply` 获得用户同意，然后执行原地容器切换，并依靠健康探针和回滚机制。

## 结果
- 在 OpenClaw 上，使用 4 个 claweval 合规审计任务后，经过 1 个进化循环，平均评分从 0.25 升到 0.61，绝对提升 0.36 倍，达到基线的 2.44 倍。
- 表 1 将 MOSS 与 4 个先前的应用层自进化系统做了比较。MOSS 是列表中唯一一个会同时修改 4 个作用域的系统：skills、prompts、memory 和 harness code。
- 控制面暴露了 9 个 `moss evo` 子命令：status、batches、batch、start、stop、restart、apply、flag 和 catch-up。
- Task-Evaluate 会按 4 级量表给每个任务的 4 到 7 个 keypoint 打分：strong、adequate、weak 和 missing。
- 切换安全路径每 2 秒轮询一次，使用 90 秒探测窗口，每 5 秒探测一次，并且在提交前要求 4 项健康检查连续 3 次通过；否则会回滚。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.22794v1](https://arxiv.org/abs/2605.22794v1)
