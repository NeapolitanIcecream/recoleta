---
source: hn
url: https://github.com/alex-reysa/glueRun-go
published_at: '2026-06-20T23:58:18'
authors:
- alexreysa
topics:
- code-intelligence
- multi-agent-software-engineering
- automated-software-production
- agent-orchestration
- git-worktrees
relevance_score: 0.86
run_id: materialize-outputs
language_code: zh-CN
---

# Show HN: Agentic coding workflows built on Git worktrees and task evidence

## Summary
## 摘要
GlueRun-go 是一个本地编排引擎，用于在一个 Git 仓库中运行多个 AI 编码代理，并提供 worktree 隔离、租约、门禁、审计和已记录的任务证据。

## 问题
- 并行编码代理可能相互覆盖改动、留下过期工作，或在完成时没有提供足够证据，导致人工或另一个代理难以判断变更。
- 长时间运行的代理任务可能阻塞 import、integrate、status 和 stop 等仓库控制操作。
- 为每个仓库复制脚本，会让多个仓库中的升级和项目特定行为更难管理。

## 方法
- 该引擎使用三层调度器：L0 origin loop、L1 area planners 和 L2 worker agents。
- 每个任务都在自己的 Git worktree 中运行，并持有一个 JSON 租约，记录 owner、retry count 和 expiry。
- Worker 会写入结构化状态包，包含 owned files、changed files、commands、tests 和 evidence；auditor 会检查该包和 gate result。
- 确定性 decider 会根据失败类别和剩余重试次数映射到 retry、amend-scope、escalate 或 park；只有在回退时才调用模型。
- 仓库会固定一个已安装的引擎版本，并把仓库特定行为保存在配置、本地覆盖或可选模块中。

## 结果
- 摘录给出的是工程实现层面的说明，不是标准数据集上的基准测试结果。
- Detached dispatch 默认开启，使 `gluerun reconcile --actuate` 在数秒内返回，同时 worker 继续在后台运行；旧的同步路径会等待每个 worker。
- 通过 dispatch records、worker exit files 和 PID 存活检查，崩溃检测从 60 分钟的过期租约窗口缩短到大约一个 reconcile 周期。
- 该系统包含 23 个回归测试，由 `bash tests/run.sh` 运行。
- 运行时会话恢复使用 10 个陈旧性门禁；如果任何门禁失败，或 runner 拒绝恢复，就回退到一次全新运行。

## Problem

## Approach

## Results

## Link
- [https://github.com/alex-reysa/glueRun-go](https://github.com/alex-reysa/glueRun-go)
