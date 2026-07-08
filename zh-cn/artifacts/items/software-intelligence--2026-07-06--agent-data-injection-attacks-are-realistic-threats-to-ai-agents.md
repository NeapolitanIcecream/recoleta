---
source: arxiv
url: https://arxiv.org/abs/2607.05120v1
published_at: '2026-07-06T14:07:49'
authors:
- Woohyuk Choi
- Juhee Kim
- Taehyun Kang
- Jihyeon Jeong
- Luyi Xing
- Byoungyoung Lee
topics:
- ai-agent-security
- prompt-injection
- coding-agents
- web-agents
- software-supply-chain
- llm-vulnerabilities
relevance_score: 0.84
run_id: materialize-outputs
language_code: zh-CN
---

# Agent Data Injection Attacks are Realistic Threats to AI Agents

## Summary
## 概要
这篇论文表明，AI 代理可能把攻击者控制的内容误认为可信元数据，从而导致点击、代码执行或不安全的代码合并。论文将这类攻击命名为代理数据注入，并说明常见的提示注入防御无法覆盖它。

## 问题
- 代理会把可信字段与不可信内容混在一起。可信字段包括发件人姓名、元素 ID、工具名称和工具历史；不可信内容包括评论、电子邮件和网页文本。
- 现有的间接提示注入防御主要区分指令和数据，因此无法保护工具响应内部的信任边界。
- 这点很关键，因为代理会在真实系统中执行操作：伪造的元素 ID 可能触发浏览器点击，伪造的维护者评论可能让编码代理运行命令。

## 方法
- 论文定义了代理数据注入（ADI）：攻击者控制的不可信数据被 LLM 读取为可信的代理数据。
- 它的核心技术是概率分隔符注入。攻击者把 JSON 大括号、引号、换行符、标签或类似分隔符放入不可信字段，使 LLM 读到伪造结构，而普通解析器会把这些内容当作纯文本处理。
- 作者通过注入复用可信元素标识符的虚假 UI 条目，测试 ADI 对 Web 代理的影响。
- 他们通过在 GitHub issue 评论中伪造可信元数据，以及在拉取请求审查期间注入伪造工具响应，测试 ADI 对编码代理的影响。
- 他们将 ADI 与指令注入进行对比，评估二者面对现有间接提示注入防御时的效果。

## 结果
- 在 6 个现成模型中，概率分隔符注入在 JSON 数据上的攻击成功率达到 31.3%–43.3%。
- 在同一组模型中，Web DOM 风格数据的攻击成功率达到 33.3%–100.0%。
- 面对前沿代理防御时，指令注入的攻击成功率只有 0.0%–0.7%，而 ADI 最高达到 50.0%。
- 作者报告了针对 Claude in Chrome、Antigravity 和 Nanobrowser 的任意点击攻击。
- 他们报告了针对 Claude Code、Codex 和 Gemini CLI 的远程代码执行和供应链攻击路径。
- OpenAI、Google 和 Anthropic 确认了报告的问题；作者发布了一个概率分隔符注入基准，以及一个加入 ADI 攻击的扩展版 AgentDojo 基准。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2607.05120v1](https://arxiv.org/abs/2607.05120v1)
