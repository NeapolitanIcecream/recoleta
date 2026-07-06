---
source: hn
url: https://fly.io/blog/building-agents-that-dont-break-themselves/
published_at: '2026-07-05T23:54:43'
authors:
- ryantsuji
topics:
- agent-sandboxing
- software-agents
- command-execution
- credential-isolation
- checkpoint-rollback
relevance_score: 0.74
run_id: materialize-outputs
language_code: zh-CN
---

# Building Agents That Don't Break Themselves

## Summary
## 摘要
文章建议让 agent 进程保持持久运行，同时把有风险的 shell 命令发送到独立的 Fly.io Sprite。这样的拆分可以保护 agent 主机，限制凭据暴露，并让失败的命令运行从检查点回滚。

## 问题
- Agent 需要 shell 访问权限来运行测试、编辑文件、安装依赖、应用迁移和检查系统，但模型生成的命令可能删除文件、破坏工具链，或影响其他用户。
- 把整个 agent 放进一个沙箱会带来生命周期冲突：agent 需要持久的记忆和历史，而命令执行环境应当可以丢弃。
- 多用户 agent 需要按用户隔离命令执行，同时避免把长期有效的用户凭据存到共享磁盘上。

## 做法
- 把 agent 循环放在稳定主机上，例如 Fly Machine、VPS、笔记本电脑或长期运行的 Sprite，并在独立的 Sprite 中运行 shell 命令。
- SpriteDoc 为每个用户会话创建 1 个 Sprite，在首次使用文件系统时上传源码树，安装所需 CLI，并在同一个隔离沙箱中运行该会话的后续命令。
- SpriteDoc 只在执行单个 `flyctl` 命令时把用户的 Fly token 注入环境变量，命令返回后就移除它。
- Hermes Agent 使用 Sprite 后端，每个任务都可以保留自己的 Sprite，因此已安装工具和任务状态可以跨会话保留。
- 有风险的步骤可以在执行前创建 Sprite 检查点；如果命令出错，再恢复之前的文件系统和工具链状态。

## 结果
- 摘录没有给出基准表、数据集、基线、准确率指标或任务成功率。
- SpriteDoc 使用 1 个共享的 Node.js agent 运行时，同时为每个用户会话提供自己的 Sprite 来执行命令。
- 凭据设计让 Sprite 内静态存储的长期用户 token 数量为 0；token 只在 1 条命令执行期间存在于环境变量中。
- Hermes 可以在 1 个 Sprite 内运行，同时把命令分发到第二个 Sprite，后者有不同的 machine id 和启动过程，这证明命令执行可以与 agent 自身运行时隔离。
- 在回滚示例中，agent 删除了 `/root/app`、`/usr/bin/python3` 和 `/usr/bin/git`；检查点恢复在约 9 秒内找回了 2 个迁移文件和 `git version 2.51.0`。
- 空闲 Sprite 会进入 warm 和 cold 状态，也可以被销毁，因此非活动会话不必为正在运行的机器付费。

## Problem

## Approach

## Results

## Link
- [https://fly.io/blog/building-agents-that-dont-break-themselves/](https://fly.io/blog/building-agents-that-dont-break-themselves/)
