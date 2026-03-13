---
source: hn
url: https://www.nonsoo.com/posts/async-react
published_at: '2026-03-09T23:36:41'
authors:
- nonsootoh
topics:
- react
- fiber-reconciler
- suspense
- transitions
- async-ui
relevance_score: 0.02
run_id: materialize-outputs
---

# Async React: The Full Story

## Summary
这篇文章系统解释了“Async React”的完整心智模型：React 18/19 的 Suspense、transitions、actions、optimistic updates 与路由能力，本质上都建立在 Fiber 的可中断、可调度渲染之上。核心主张是把异步工作纳入 React 渲染系统内部协调，而不是继续依赖 `useEffect` 手工拼接加载、错误和状态流转。

## Problem
- 文章要解决的问题是：**React 应该如何原生协调数据获取、导航、用户输入等异步工作与 UI 渲染**，而不是让开发者在组件外部用 `useEffect`、loading/error 状态和命令式更新自行编排。
- 这很重要，因为旧的 stack reconciler 是**同步且不可中断**的；长渲染会阻塞主线程，无法暂停、重排优先级或丢弃过时工作，导致复杂应用中输入延迟、卡顿和心智模型碎片化。
- 作者还指出，React 18/19 的新特性常被分散理解为“加载”“性能优化”“表单”功能，但真正缺失的是一个统一的异步优先架构视角。

## Approach
- 核心机制是 **React Fiber**：把组件树表示为可独立处理的 fiber 单元，将渲染拆成可增量执行的小步骤，使 React 能**暂停、恢复、让出浏览器控制权、按优先级调度，必要时丢弃未提交的渲染工作**。
- 在这个基础上，React 将 **reconciliation/render** 与 **commit** 分离：前者可中断、可放弃，后者不可中断；因此 React 可以先准备多个 UI 版本，只提交最终需要的那个。
- 开发者通过 **transitions (`startTransition`, `useTransition`)** 把非紧急更新标记为低优先级，让输入等高优先级交互先响应，再在后台准备其余 UI。
- 通过 **Suspense + `use(promise)` + Error Boundary**，组件可以“假设数据可用”；若数据未就绪则在渲染时抛出 promise，由 React 显示 fallback，promise resolve 后自动恢复渲染；若失败则交给错误边界显示错误 UI。
- 文章进一步把这种模式扩展到 **async-first 组件库、action props、以及 suspense-enabled routers**：例如按钮直接接收 `action`，路由把导航包进 transition，并在路由级统一处理 loading/error fallback。

## Results
- 定量结果：**文中没有提供正式实验、基准测试或数据集上的量化指标**，没有准确的吞吐、延迟或性能数字对比。
- 明确的版本性主张：作者认为 React **16** 的 Fiber 重写奠定基础，React **18** 暴露了部分并发/异步 API，而到 React **19/19.2** 才补齐“Async React”的完整能力版图。
- 具体示例数字：文中的 Suspense 演示里，组件在渲染时抛出一个 **3 秒**后 resolve 的 promise；这期间显示 `Loading` fallback，resolve 后恢复并展示最终内容。
- 结构性改进主张：相较传统 `useEffect` 数据获取范式，async-first 示例将用户列表组件简化为直接 `use(userDataPromise)` 读取数据，并把 loading/error 交由 **1 个 Suspense 边界 + 1 个 Error Boundary** 统一协调。
- 体验层面的突破性声明：Fiber 使 React 能在低优先级更新进行中插入高优先级任务；高优先级工作可**先于**低优先级渲染，导航还可在用户快速切换时**取消**过时路由准备，从而保持当前 UI 可见、交互不中断。
- 文章的最强结论不是数值 SOTA，而是范式性结论：React 现在可以把异步当默认构建模式，开发者更多声明“UI 应该如何表现”，由 React 负责跨 loading、pending、error 和 navigation 的协调。

## Link
- [https://www.nonsoo.com/posts/async-react](https://www.nonsoo.com/posts/async-react)
