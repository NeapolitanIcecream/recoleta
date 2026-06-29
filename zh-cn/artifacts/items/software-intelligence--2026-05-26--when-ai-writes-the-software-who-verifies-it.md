---
source: hn
url: https://leodemoura.github.io/blog/2026-2-28-when-ai-writes-the-worlds-software-who-verifies-it/
published_at: '2026-05-26T22:57:02'
authors:
- fagnerbrack
topics:
- formal-verification
- ai-generated-code
- lean-theorem-proving
- code-intelligence
- software-foundation-models
- verified-software
relevance_score: 0.93
run_id: materialize-outputs
language_code: zh-CN
---

# When AI Writes the Software, Who Verifies It?

## Summary
## 摘要
文章认为，AI 生成的软件需要机器可检查的证明，因为人工审查和测试跟不上代码生成速度。文章把 Lean 作为主要平台，并引用了 AI 辅助验证在 zlib、分布式协议和数学上的早期结果。

## 问题
- AI 正在生成大量新代码：Google 和 Microsoft 报告新代码中有 25–30% 由 AI 生成，AWS 用 AI 为 Toyota 将 4000 万行 COBOL 现代化，Microsoft 的 CTO 预测到 2030 年 95% 的代码都将由 AI 生成。
- 当模型生成的代码看起来合理时，人工审查会变弱。文章引用了 Karpathy 的“Accept All”模式，并说接近一半的 AI 生成代码没有通过基本安全测试。
- 测试和审查花了几年时间才发现 Heartbleed 这类漏洞。在 AI 生成代码的速度下，这类缺陷和供应链攻击会比现有验证流程更快扩散到关键基础设施。

## 方法
- 先用形式化规格说明定义正确行为，再接受 AI 生成的代码。
- 让 AI 在 Lean 中生成代码、证明和证明步骤；一个小而可信的内核逐条机械检查每个证明。
- 让验证器独立于 AI 生成器，这样信任落在证明检查器上，而不是模型或供应商上。
- 在可能时，用简单、显然正确的模型作为规格。然后让 AI 写出更快的实现，并证明两个版本的行为一致。
- 利用 Lean 的 tactic 反馈、Mathlib 和领域扩展，让 AI 智能体能一步步构造证明，而不是只依赖黑盒求解器结果。

## 结果
- Anthropic 据报道用并行 AI 智能体在两周内、花费不到 20,000 美元构建了一个 10 万行的 C 编译器；它能启动 Linux，并编译 SQLite、PostgreSQL、Redis 和 Lua，但文章说它没有经过形式化验证。
- 一个基于 Claude 的实验在几乎没有人工指导、也没有专门定理证明工具的情况下，把 zlib（包括 DEFLATE）转换到了 Lean。文章声称的定理证明了对每个压缩级别，`decompressSingle (compress data level) = .ok data`，前提是 `data.size < 1024 * 1024 * 1024`。
- 文章提到 Lean 的 Mathlib 有超过 200,000 个形式化定理和 750 名贡献者。
- 文章给出的 Lean 采用数据包括超过 8,000 个 GitHub 仓库、超过 200,000 次编程环境安装，以及 Lean Zulip 上每天超过 700 名活跃用户。
- 基于 Lean 的分布式协议验证器 Veil 据报道能验证任意节点数下的 Rabia 一致性和有效性，并在两个独立工具之间发现了先前 Rabia 验证中的一个不一致。
- 一名数学家与 AI 智能体合作，在三周内把素数定理形式化到 Lean 中，产出 25,000 行代码和超过 1,000 个定理；文章说，之前的形式化花了超过一年和几十名贡献者。

## Problem

## Approach

## Results

## Link
- [https://leodemoura.github.io/blog/2026-2-28-when-ai-writes-the-worlds-software-who-verifies-it/](https://leodemoura.github.io/blog/2026-2-28-when-ai-writes-the-worlds-software-who-verifies-it/)
