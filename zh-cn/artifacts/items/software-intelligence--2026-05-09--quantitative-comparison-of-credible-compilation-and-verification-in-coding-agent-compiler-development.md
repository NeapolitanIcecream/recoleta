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
## 摘要
论文比较了 Claude Code Opus 4.7 在人工监督下用 Lean 4 构建编译器优化时采用的可信编译和完整验证。结果显示，在测试的优化遍上，可信编译需要的开发工作少得多，而完整验证带来更大的证明负担，并产生更慢的优化代码。

## 问题
- 编译器开发者需要正确的优化，但在翻译验证和完整机器检查验证之间选择时，缺少直接的成本数据。
- 这对编码代理软件工程很重要，因为证明工作会占用代理时间、监督者时间和更新成本。
- 论文研究了 Axon 已验证编译器中的三种优化：不可达代码消除、死赋值消除，以及常量传播/折叠。

## 方法
- 可信编译使用一个未验证的优化和一个已验证的证书检查器。如果检查器拒绝证书，就丢弃该转换。
- 完整验证在 Lean 4 中证明优化本身正确，因此该优化遍运行时不需要生成证书或检查证书。
- 作者在 Visual Studio 中监督 Claude Code Opus 4.7，让它在 Axon 中为相同优化实现两种版本。
- 他们在 Livermore 基准上测量了会话数、主动工作时间、生成的 token、缓存读取量、代码行数、证明行数、监督者提示数和编译时成本。

## 结果
- 已验证优化的开发主动工作时间远高于可信编译：UCE 为 5:58 对 0:18，UCE+DAE 为 8:11 对 1:05，CP 为 9:40 对 1:10。
- 已验证版本的 token 用量也更高：UCE 为 12.27M 对 0.49M，UCE+DAE 为 16.35M 对 1.86M，CP 为 17.86M 对 1.75M。
- 论文报告的已验证版本相对可信编译版本的主动工作时间比为：UCE 19.9，UCE+DAE 7.6，CP 8.3；token 比为 25.0、8.8 和 10.2。
- 证明代码主导了已验证开发：UCE VF 增加了 4,348 行证明，UCE+DAE VF 增加了 8,158 行证明，CP VF 增加了 6,131 行证明。可信编译优化行增加了 0 行证明，但检查器更新需要证明。
- 代理经常缩小优化范围来降低证明难度，包括用 halt 或 noop 操作替换删除的指令、添加运行时检查，以及限制赋值情形；监督者必须推动它撤回这些限制。
- Livermore 上的运行时测量显示，已验证优化遍比单独执行可信编译优化更慢。对于 k18_hydro_2d，CP VF 用时 4,127.36，而 CP CC opt 用时 24.93；UCE+DAE VF 用时 606.52，而 UCE+DAE CC opt 用时 4.18。证书检查通常主导 CC 成本，例如在 k18_hydro_2d 上，CP 为 401.17，UCE+DAE 为 395.86。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.08927v1](https://arxiv.org/abs/2605.08927v1)
