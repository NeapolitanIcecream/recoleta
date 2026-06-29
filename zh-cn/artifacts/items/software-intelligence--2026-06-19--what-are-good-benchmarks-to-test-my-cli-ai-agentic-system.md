---
source: hn
url: https://www.minovativemind.dev/
published_at: '2026-06-19T23:22:50'
authors:
- daniel_ward
topics:
- code-agent
- cli-agent
- multi-agent-coding
- codebase-context
- software-verification
- human-ai-interaction
relevance_score: 0.82
run_id: materialize-outputs
language_code: zh-CN
---

# What are good benchmarks to test my CLI AI agentic system?

## Summary
## 摘要
Minovative Mind CLI 是一个编码代理 CLI，结合了代码库搜索、多代理任务执行、代码编辑、构建检查、修复循环和回滚控制。摘录提供了功能声明和系统限制，但没有提供基准分数、数据集、基线或准确率测量。

## 问题
- 自主编码代理在编辑代码前需要可靠的项目上下文，因为遗漏依赖和过期文件可能导致变更破坏项目。
- 多文件编辑需要协调、语法检查、验证和回滚，这样代理才不会让代码仓库处于错误状态。
- CLI 代理还需要安全控制，以防止不安全路径、提示注入和不受控的文件变更。

## 方法
- 上下文引擎会检查文件时间戳，在文件级别压缩并缓存源文件，为语义代码搜索构建本地向量索引，追踪依赖，并用基于 AST 的行范围映射符号。
- 系统把工作拆分成并行的子代理线程任务，并使用互斥锁注册表来减少编辑冲突。
- 它在一个回合内把工作路由到专用 Gemini 模型，包括 Gemini 3.1 Pro、Gemini 3.5 Flash 和 Flash-Lite。
- 写入变更前，它会运行语法验证、意图分类、批量编辑、模糊补丁匹配和事务日志记录。
- 编辑后，它会运行沙盒构建试验，把编译器错误反馈到代理循环，并通过 `/revert` 命令支持回滚。

## 结果
- 没有提供基准结果。摘录中没有 SWE-bench、HumanEval、RepoBench、通过率、延迟、成本或基线对比数字。
- 依赖追踪声明覆盖 11 种语言。
- 编排声明称该 CLI 可以在一个回合内协调最多 4 个专用模型。
- 沙盒构建验证每次试验最长可运行 120 秒。
- 自动纠错循环可在编译器错误或性能回退后最多重试修复 5 次。
- 安全声明包括拒绝绝对路径、用 CDATA 包装文件内容、GitHub Device Flow 身份验证，以及 Server-Sent Events 令牌流式传输。

## Problem

## Approach

## Results

## Link
- [https://www.minovativemind.dev/](https://www.minovativemind.dev/)
