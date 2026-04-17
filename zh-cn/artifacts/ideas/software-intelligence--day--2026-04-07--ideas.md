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

# 补丁质量关卡

## Summary
三个地方已经出现了明确变化：代码仓库修复代理可以围绕具名代码实体工作，并按小而有效的 diff 来评估；补丁评估需要在测试通过率之外加入设计约束检查；AI 编写的安全敏感代码需要一道评审关卡，用可利用性检查来替代对提示词或自主攻击循环的单独信任。

## 面向代码仓库修复代理的 AST 级补丁与编辑规模评审
代码仓库修复代理现在可以围绕 AST 级别的读取和编辑工具来构建，评审重点放在具名代码实体和补丁大小上。CodeStruct 报告称，这种接口让前沿模型在 SWE-Bench Verified 上的 Pass@1 提高了 1.2 到 5.0 个点，GPT-5-nano 也从 19.6 提升到 40.4，同时空补丁失败率从 46.6% 降到 7.2%。PRepair 在训练侧指向同一类操作变化：奖励小而正确的编辑，因为只看 pass rate 会掩盖过度编辑。在 HumanEvalFix 上，Qwen2.5-Coder-7B 的 fix_1@1 从 47.44 提高到 81.62，而 pass@1 只增加了 1.37 个点。对于交付内部代码代理的团队，落地方式很明确：把函数、类和方法作为可编辑单元暴露出来；在工具层拒绝会破坏语法的编辑；记录每个成功补丁的编辑距离；评审代理时看最小可接受 diff，而不只看测试是否通过。最先会用的是代码仓库维护团队，因为糟糕补丁通常会出现在格式错误、改动过多无关代码或拉长评审周期这些问题上。

### Evidence
- [CODESTRUCT: Code Agents over Structured Action Spaces](../Inbox/2026-04-07--codestruct-code-agents-over-structured-action-spaces.md): AST 级别的读写操作提升了代码仓库修复准确率，并减少了空补丁失败。
- [QiMeng-PRepair: Precise Code Repair via Edit-Aware Reward Optimization](../Inbox/2026-04-07--qimeng-prepair-precise-code-repair-via-edit-aware-reward-optimization.md): 编辑感知训练在精确修复上带来大幅提升，而 pass rate 变化很小。

## 代理补丁验收中的设计约束验证
问题修复评估需要在测试通过率之外再加一道设计约束关卡。SWE-Shield 说明了原因：代理在 verified split 上的 pass rate 达到 70.25% 到 75.95%，但设计满足率只有 32.64% 到 50.20%，而且论文发现功能正确性与设计合规性之间几乎没有统计关系。这支持一种直接的流程调整，适用于已经在跑 SWE-Bench 风格评估或用代理辅助修 bug 的团队。可以从已合并的 pull request 和评审讨论中提取设计规则，把它们关联到问题类型，再运行一个验证器，在补丁被标记为可接受之前检查架构选择、错误处理、API 一致性和可维护性条件。短期内需要的不是一个新的 benchmark 品牌，而是一道内部验收检查，用来拦住那些测试通过但仍然违反仓库约定的补丁。最先在意这件事的会是代码评审队列活跃的团队，因为这类失败在那里最容易暴露，也最费钱。

### Evidence
- [Does Pass Rate Tell the Whole Story? Evaluating Design Constraint Compliance in LLM-based Issue Resolution](../Inbox/2026-04-07--does-pass-rate-tell-the-whole-story-evaluating-design-constraint-compliance-in-llm-based-issue-resolution.md): 在代码仓库问题修复中，pass rate 与设计满足率明显分离。

## 面向 AI 生成安全敏感代码的可利用性评审关卡
AI 生成代码在合并前需要增加一步生成后的安全评审，对高风险代码路径做可利用性检查。Broken by Default 报告称，在 3,500 个生成程序中有 55.8% 存在漏洞，其中 1,055 个发现通过 Z3 witness 被形式化证明可利用。整数运算的漏洞率达到 87%，内存分配达到 67%。同一篇论文还给工作流设计提供了一个有用的不对称现象：模型在评审模式下能识别自己脆弱输出的概率是 78.7%，而安全提示词在测试子集上只把平均漏洞率降低了 4 个点。AutoPT 的证据也指向同一方向，说明进攻型安全代理并不可靠：很多系统会产生幻觉，13 个框架里有 8 个生成了幻觉 flag，而且在链式漏洞样本中，只有 16.67% 完成了完整利用链。一个可执行的落地方案是为代理编写的代码设置合并关卡，把内存管理、算术、auth、输入处理和加密相关改动送入模型评审，并在可用时加入形式化或符号检查；只要出现已证明的 witness 或结果不确定，就交给人工升级处理。

### Evidence
- [Broken by Default: A Formal Verification Study of Security Vulnerabilities in AI-Generated Code](../Inbox/2026-04-07--broken-by-default-a-formal-verification-study-of-security-vulnerabilities-in-ai-generated-code.md): 形式化验证研究发现，生成代码的可利用漏洞率很高，而且评审模式下的检测收益高于安全提示词。
- [Hackers or Hallucinators? A Comprehensive Analysis of LLM-Based Automated Penetration Testing](../Inbox/2026-04-07--hackers-or-hallucinators-a-comprehensive-analysis-of-llm-based-automated-penetration-testing.md): 自动渗透测试代理在多步骤攻击链上仍然不可靠，并且经常产生幻觉。
