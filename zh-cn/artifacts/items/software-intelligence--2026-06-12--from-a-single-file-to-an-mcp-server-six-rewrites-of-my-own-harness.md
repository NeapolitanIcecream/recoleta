---
source: hn
url: https://pub.towardsai.net/from-a-single-file-to-an-mcp-server-six-rewrites-of-my-own-harness-74b4d67b5373?source=friends_link&sk=9e8b13e4920771b5d414db224901bf0e
published_at: '2026-06-12T23:25:57'
authors:
- tacoda
topics:
- mcp
- agentic-tools
- code-intelligence
- software-foundations
- configuration-management
relevance_score: 0.88
run_id: materialize-outputs
language_code: zh-CN
---

# From a Single File to an MCP Server: Six Rewrites of My Own Harness

## Summary
## 摘要
这篇文章讲了一个个人 Claude harness 的六次重写，最后变成一个 MCP 服务器，让 agent 可以把规则、技能和实时状态当作结构化数据获取。核心观点是：对一个可用系统反复整理，能暴露它真正的形态；结构应该随代码移动，项目特定内容应留在本地。

## 问题
- 一个 1,800 行的 `CLAUDE.md` 文件变得难以记住、容易冲突，也难以修改。
- 全局规则会渗入不适用的项目，导致 agent 载入无关上下文，并执行混杂的指令。
- 只有文件的 harness 无法在团队间共享默认值、跟踪版本，也不能把实时状态暴露给 agent。

## 方法
- 把一个大配置拆成按主题划分的文件，然后把规则移到有作用范围的路径里，让位置决定是否生效。
- 将始终加载的规则、命名技能和 slash 命令分到不同的目录和文件类型。
- 先把 Sellier 做成一个用于项目 harness 的 CLI 脚手架，再用 Keystone 取代它；Keystone 支持项目类型、agent 选择、迁移、插件、团队/组织/项目分层，以及严格的级联规则。
- 把 Keystone 重新打包成 `keystone-mcp`，提供用于上下文查询和脚手架生成的工具，提供 bootstrap 和 audit 等工作流提示词，以及用于状态、验证和预算数据的资源。

## 结果
- 作者说，在把作用域移到子目录文件后，全局配置缩小到原来的大约三分之一。
- 当互相矛盾的规则不再放在同一个文件里后，agent 的行为变好了，规则之间也不再互相冲突。
- Sellier 暴露出三个明显限制：一个初始集合不适合不同项目类型，它不支持团队定制，也没有更新路径。
- Keystone 增加了类型化脚手架、迁移、插件、级联解析，以及按 agent 渲染；文章没有给出这些变化的基准数据。
- `keystone-mcp` 让 agent 可以调用 `keystone_get_context(topic)`、`keystone_list_topics()`、`keystone_harness_bootstrap()`，并获取像 `keystone://harness/verify` 这样的资源，但文章没有提供速度、准确率或采用率的量化评估。

## Problem

## Approach

## Results

## Link
- [https://pub.towardsai.net/from-a-single-file-to-an-mcp-server-six-rewrites-of-my-own-harness-74b4d67b5373?source=friends_link&sk=9e8b13e4920771b5d414db224901bf0e](https://pub.towardsai.net/from-a-single-file-to-an-mcp-server-six-rewrites-of-my-own-harness-74b4d67b5373?source=friends_link&sk=9e8b13e4920771b5d414db224901bf0e)
