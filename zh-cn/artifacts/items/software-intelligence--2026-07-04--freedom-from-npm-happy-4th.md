---
source: hn
url: https://www.npmjs.com/package/donobu
published_at: '2026-07-04T22:40:30'
authors:
- vasusen
topics:
- ai-testing
- playwright
- code-intelligence
- autonomous-agents
- test-auto-healing
- developer-tools
relevance_score: 0.78
run_id: materialize-outputs
language_code: zh-CN
---

# Freedom from NPM. Happy 4th

## Summary
## 概要
Donobu 是一个 Playwright SDK 和 CLI，为 Web 测试加入 AI 驱动的浏览器操作、断言、失败分诊和自动修复。摘录描述的是开发者工具，未提供基准测试证据。

## 问题
- 当选择器、布局或内容变化时，Web UI 测试常会中断，开发者需要维护测试，发布检查也会变慢。
- 普通 Playwright 测试要求开发者编写底层操作和断言；Donobu 旨在让测试表达用户目标，例如导航到某个页面或检查地图结果。
- 失败诊断可能耗时，因为截图、DOM 状态、模型推理和修复步骤常分散在不同位置或缺失。

## 方法
- Donobu 通过类型化 fixture 扩展 Playwright：`import { test } from 'donobu'` 会加入 `page.ai` 辅助方法、智能选择器、持久化能力，以及 `page.runAccessibilityTest` 等预构建包装器。
- 测试可以用自然语言指令调用 `page.ai()`；可选的 Zod schema、工具 allow-list、缓存的工具调用回放和环境变量控制可约束该 agent。
- 每次 `page.ai()` 调用都会缓存在 spec 旁边的 `.cache-lock/<spec-file>.cache.js` 中，因此生成的操作或选择器可复用，也可用 `--clear-ai-cache` 重新生成。
- CLI 对应 Playwright 命令，并加入 Donobu 设置，用于分诊目录、缓存清理和自动修复重试。
- 失败时，Donobu 会保存证据，生成处理计划，并可重新运行自主修复流程，尝试更新选择器或测试代码。

## 结果
- 摘录未提供定量基准结果：没有报告准确率、通过率、延迟、成本、数据集或基线对比。
- 该包声称用单一依赖提供 Playwright fixture、Page.AI 编排层、CLI 包装器、失败分诊和插件系统。
- 运行要求包括 Node.js 18+、npm 8+ 或 pnpm 10+ 或 yarn、Playwright 浏览器，以及至少 1 个 LLM 凭据。
- 支持的模型路径包括 Donobu API、OpenAI、Anthropic direct、Google Gemini、通过 AWS Bedrock 使用 Anthropic，以及 `BASE64_GPT_CONFIG`。
- 失败证据写入 `test-results/donobu-triage/<timestamp>-<runId>/`，处理计划保存在证据旁边，并带有 `treatment-plan-` 前缀。
- 使用 `--auto-heal` 时，成功的修复会附加 `fixed-test.ts`，并用 `@self-healed` 标注运行，但摘录未给出成功率。

## Problem

## Approach

## Results

## Link
- [https://www.npmjs.com/package/donobu](https://www.npmjs.com/package/donobu)
