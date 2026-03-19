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
language_code: en
---

# Async React: The Full Story

## Summary
This article systematically explains the full mental model of “Async React”: the Suspense, transitions, actions, optimistic updates, and routing capabilities in React 18/19 are all fundamentally built on Fiber’s interruptible, schedulable rendering. The core argument is that asynchronous work should be coordinated inside React’s rendering system, rather than continuing to rely on `useEffect` to manually stitch together loading, error, and state transitions.

## Problem
- The article aims to solve this problem: **how React should natively coordinate asynchronous work such as data fetching, navigation, and user input with UI rendering**, instead of forcing developers to orchestrate it themselves outside the component with `useEffect`, loading/error state, and imperative updates.
- This matters because the old stack reconciler was **synchronous and non-interruptible**; long renders would block the main thread and could not be paused, reprioritized, or have stale work discarded, leading to input latency, jank, and a fragmented mental model in complex applications.
- The author also points out that React 18/19’s new features are often understood in isolation as “loading,” “performance optimization,” or “form” features, but what is really missing is a unified async-first architectural perspective.

## Approach
- The core mechanism is **React Fiber**: it represents the component tree as independently processable fiber units and breaks rendering into small incrementally executable steps, allowing React to **pause, resume, yield control back to the browser, schedule by priority, and discard uncommitted render work when necessary**.
- On that foundation, React separates **reconciliation/render** from **commit**: the former is interruptible and discardable, while the latter is not; this allows React to prepare multiple UI versions first and only commit the one ultimately needed.
- Developers use **transitions (`startTransition`, `useTransition`)** to mark non-urgent updates as low priority, so high-priority interactions such as input can respond first while the rest of the UI is prepared in the background.
- Through **Suspense + `use(promise)` + Error Boundary**, components can “assume data is available”; if the data is not ready, a promise is thrown during rendering, React shows a fallback, rendering automatically resumes after the promise resolves, and failures are handed off to the error boundary to display error UI.
- The article further extends this pattern to **async-first component libraries, action props, and suspense-enabled routers**: for example, a button can directly accept an `action`, and the router can wrap navigation in a transition while handling loading/error fallbacks uniformly at the routing level.

## Results
- Quantitative results: **the article does not provide formal experiments, benchmark tests, or quantitative metrics on datasets**, and there are no precise comparisons of throughput, latency, or performance numbers.
- Clear versioning claim: the author argues that React **16** laid the foundation with the Fiber rewrite, React **18** exposed part of the concurrent/async API surface, and only by React **19/19.2** was the full capability map of “Async React” completed.
- Concrete example number: in the article’s Suspense demo, the component throws a promise during rendering that resolves after **3 seconds**; during that time a `Loading` fallback is shown, and after resolution rendering resumes and the final content is displayed.
- Structural improvement claim: compared with the traditional `useEffect` data-fetching pattern, the async-first example simplifies the user list component to directly reading data via `use(userDataPromise)`, with loading/error coordinated uniformly by **1 Suspense boundary + 1 Error Boundary**.
- Breakthrough claim at the experience level: Fiber lets React insert high-priority tasks while low-priority updates are in progress; high-priority work can proceed **ahead of** low-priority rendering, and navigation can also **cancel** stale route preparation when users switch quickly, keeping the current UI visible and interactions uninterrupted.
- The article’s strongest conclusion is not a numeric SOTA result but a paradigmatic one: React can now treat asynchrony as the default way of building, with developers declaring more of “how the UI should behave,” while React takes responsibility for coordinating across loading, pending, error, and navigation.

## Link
- [https://www.nonsoo.com/posts/async-react](https://www.nonsoo.com/posts/async-react)
