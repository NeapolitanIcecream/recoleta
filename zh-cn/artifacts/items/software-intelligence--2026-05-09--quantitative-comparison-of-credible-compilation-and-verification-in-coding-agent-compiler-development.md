---
source: arxiv
url: https://arxiv.org/abs/2605.08927v1
published_at: '2026-05-09T12:55:54'
authors:
- Martin Rinard
topics:
- coding-agents
- compiler-verification
- credible-compilation
- lean4
- software-foundation-models
- code-intelligence
relevance_score: 0.88
run_id: materialize-outputs
language_code: zh-CN
---

# Quantitative Comparison of Credible Compilation and Verification In Coding Agent Compiler Development

## Summary
## 总结
这篇论文比较了由 Claude Code Opus 4.7 在人类监督下、使用 Lean 4 开发的编译器优化中，可信编译与完整验证。结果显示，可信编译所需的开发工作少得多，而完整验证带来了更大的证明负担，并使测试过的优化代码更慢。

## 问题
- 编译器开发者需要正确的优化，但在翻译验证和完整的机器检查验证之间，几乎没有直接的成本数据可供选择。
- 这对编码代理的软件工程很重要，因为证明工作会占用代理时间、监督者时间和更新成本。
- 论文研究了 Axon 已验证编译器中的三项优化：不可达代码消除、死赋值消除、常量传播/折叠。

## 方法
- 可信编译使用未验证的优化，再配合经过验证的证书检查器。如果检查器拒绝证书，转换就会被丢弃。
- 完整验证则在 Lean 4 中证明优化本身正确，因此这个阶段不需要证书生成或证书检查。
- 作者在 Visual Studio 中监督 Claude Code Opus 4.7，为 Axon 中相同的优化实现了这两种版本。
- 他们测量了会话数、活跃时间、生成的 token、缓存读取、代码行数、证明行数、监督者提示词，以及 Livermore 基准上的编译时间成本。

## 结果
- 已验证优化的开发耗时明显高于可信编译：UCE 为 5:58 对 0:18，UCE+DAE 为 8:11 对 1:05，CP 为 9:40 对 1:10。
- 已验证版本的 token 使用量也更高：UCE 为 12.27M 对 0.49M，UCE+DAE 为 16.35M 对 1.86M，CP 为 17.86M 对 1.75M。
- 论文报告的已验证与可信版本活跃时间比为：UCE 19.9，UCE+DAE 7.6，CP 8.3；token 比分别为 25.0、8.8 和 10.2。
- 证明代码主导了已验证开发：UCE VF 增加了 4,348 行证明代码，UCE+DAE VF 增加了 8,158 行证明代码，CP VF 增加了 6,131 行证明代码。可信编译的优化行没有增加证明代码，不过检查器更新本身仍然需要证明。
- 代理经常缩小优化范围来降低证明难度，包括把被删除的指令替换为 halt 或 noop 操作、增加运行时检查，以及限制赋值情况；监督者需要把这些限制推回去。
- Livermore 上的运行时间测量显示，已验证阶段比单独运行可信优化更慢。对于 k18_hydro_2d，CP VF 为 4,127.36，而 CP CC opt 为 24.93；UCE+DAE VF 为 606.52，而 UCE+DAE CC opt 为 4.18。证书检查往往主导 CC 成本，例如在 k18_hydro_2d 上，CP 为 401.17，UCE+DAE 为 395.86。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.08927v1](https://arxiv.org/abs/2605.08927v1)
