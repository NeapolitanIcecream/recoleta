---
kind: ideas
granularity: day
period_start: '2026-04-07T00:00:00'
period_end: '2026-04-08T00:00:00'
run_id: materialize-outputs
status: succeeded
topics:
- code-agents
- software-repair
- security
- benchmarks
- formal-verification
- agent-orchestration
tags:
- recoleta/ideas
- topic/code-agents
- topic/software-repair
- topic/security
- topic/benchmarks
- topic/formal-verification
- topic/agent-orchestration
language_code: zh-CN
---

# Patch Quality Gates

## Summary
具体变化已经出现在三个地方：仓库修复代理可以围绕命名代码实体工作，并根据小而有效的 diff 来评估；补丁评估需要在测试通过率之外加入设计约束检查；AI 编写的安全敏感代码需要一个检查可利用性的审查门，而不是只信任提示词或自动攻击循环。

## AST-level patching with edit-size review for repository repair agents
仓库修复代理现在可以围绕 AST 级别的读取和编辑工具来组织，审查重点放在命名代码实体和补丁大小上。CodeStruct 报告称，这种接口让前沿模型在 SWE-Bench Verified 上的 Pass@1 提升 1.2 到 5.0 个点，GPT-5-nano 从 19.6 跳到 40.4，同时空补丁失败率从 46.6% 降到 7.2%。PRepair 在训练侧指向了同样的操作变化：奖励小而正确的编辑，因为只看通过率会掩盖过度编辑。在 HumanEvalFix 上，Qwen2.5-Coder-7B 的 fix_1@1 从 47.44 升到 81.62，pass@1 只提高 1.37 个点。对交付内部代码代理的团队来说，这个做法很具体：把函数、类和方法暴露为可编辑单元；在工具层拒绝会破坏语法的编辑；记录每个成功补丁的编辑距离；审查代理时看最小的可接受 diff，而不只看测试是否通过。最先受影响的是仓库维护团队，因为坏补丁会在格式上出错、碰到太多无关代码，或者拉长审查周期。

### Evidence
- [CODESTRUCT: Code Agents over Structured Action Spaces](../Inbox/2026-04-07--codestruct-code-agents-over-structured-action-spaces.md): AST-level read/edit actions improved repository repair accuracy and cut empty-patch failures.
- [QiMeng-PRepair: Precise Code Repair via Edit-Aware Reward Optimization](../Inbox/2026-04-07--qimeng-prepair-precise-code-repair-via-edit-aware-reward-optimization.md): Edit-aware training shows large gains in precise repair with minimal change to pass rate.

## Design-constraint verification in agent patch acceptance
问题修复评估需要在测试通过率之外，再加一道设计约束检查。SWE-Shield 说明了原因：在 verified 划分上，代理的通过率是 70.25% 到 75.95%，而设计满意率只有 32.64% 到 50.20%，论文还发现功能正确性和设计合规性之间几乎没有统计关系。这支持一个对已经在做 SWE-Bench 风格评估或代理辅助修 bug 的团队很实用的流程改动。把合并请求和 review 线程里的设计规则挖出来，关联到问题类型，然后在补丁被标记为可接受之前，运行一个检查架构选择、错误处理、API 一致性和可维护性条件的验证器。短期内要做的不是一个新的基准品牌，而是内部验收检查，用来拦住那些能过测试、却仍然违背仓库约定的补丁。活跃的代码审查队列最先需要这个机制，因为这些失败在那里最容易被看到，也最费成本。

### Evidence
- [Does Pass Rate Tell the Whole Story? Evaluating Design Constraint Compliance in LLM-based Issue Resolution](../Inbox/2026-04-07--does-pass-rate-tell-the-whole-story-evaluating-design-constraint-compliance-in-llm-based-issue-resolution.md): Pass rate and design satisfaction diverge sharply on repository issue resolution.

## Exploitability review gates for AI-generated security-sensitive code
AI 生成的代码在合并前需要一层生成后的安全审查，对高风险代码路径做可利用性检查。Broken by Default 报告，在 3,500 个生成程序中有 55.8% 存在漏洞，并且 1,055 个发现被 Z3 证明确实可利用。整数运算的漏洞率达到 87%，内存分配是 67%。同一篇论文还显示了一个对流程设计很有用的差异：模型在 review 模式下能识别自己生成的脆弱输出，命中率是 78.7%，而安全提示词只让测试子集上的平均漏洞率下降 4 个点。AutoPT 的证据也指向同一方向，针对进攻性安全代理：很多系统会产生幻觉，13 个框架里有 8 个输出过幻觉标记，而且只有 16.67% 的链式漏洞样本完成了完整利用链。一个可落地的做法是给代理写的代码加一道合并门禁，把内存管理、算术、认证、输入处理和加密相关改动交给模型审查，并在可用时结合形式化或符号检查；对任何已证明的证据或不确定结果都交给人工升级处理。

### Evidence
- [Broken by Default: A Formal Verification Study of Security Vulnerabilities in AI-Generated Code](../Inbox/2026-04-07--broken-by-default-a-formal-verification-study-of-security-vulnerabilities-in-ai-generated-code.md): Formal verification study finds high exploitability rates in generated code and shows review-mode detection exceeds secure prompting gains.
- [Hackers or Hallucinators? A Comprehensive Analysis of LLM-Based Automated Penetration Testing](../Inbox/2026-04-07--hackers-or-hallucinators-a-comprehensive-analysis-of-llm-based-automated-penetration-testing.md): Automated penetration-testing agents remain unreliable on multi-step chains and often hallucinate.
