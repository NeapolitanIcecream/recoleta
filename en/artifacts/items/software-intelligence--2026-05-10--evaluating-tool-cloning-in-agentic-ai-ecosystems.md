---
source: arxiv
url: https://arxiv.org/abs/2605.09817v2
published_at: '2026-05-10T23:39:44'
authors:
- Taein Kim
- David Jiang
- Yuepeng Hu
- Yuqi Jia
- Neil Gong
topics:
- agent-tools
- code-cloning
- mcp
- skills
- benchmark-contamination
- software-provenance
relevance_score: 0.86
run_id: materialize-outputs
language_code: en
---

# Evaluating Tool Cloning in Agentic-AI Ecosystems

## Summary
This paper measures code cloning across public MCP and Skills tool repositories and finds that duplicated implementations are common enough to distort tool counts, benchmark splits, and security review.

## Problem
- Public agent-tool platforms count many repositories and tools, but those counts can include copied code, lightly edited forks, and template-derived tools.
- Duplicate implementations can leak similar code across train/test splits, spread vulnerable scaffolds, and obscure provenance, attribution, and license obligations.
- The paper asks whether cloning in MCP and Skills repositories is rare or large enough to affect evaluation and governance.

## Approach
- The authors build a unified repository-level dataset with 7,508 MCP repositories and 1,353 Skills repositories, covering 100,011 tool entries in total.
- They normalize repository source code by removing dependencies, generated artifacts, binaries, comments, extra whitespace, and case differences.
- They compare repositories with token-level Jaccard similarity and `ssdeep` fuzzy hashing, then run pairwise comparisons for MCP-MCP, Skills-Skills, and MCP-Skills pairs.
- They exclude same-developer pairs for main cross-developer estimates and manually verify sampled pairs across similarity buckets to test whether high scores mean real cloning.

## Results
- The dataset contains 8,861 repositories: 7,508 MCP repositories with 87,564 extracted tools and 1,353 Skills repositories with 12,447 tools.
- In MCP-MCP comparisons, the highest Jaccard bucket, 80-100, contains 758 pairs; manual review labels 12 of 20 sampled pairs as clones, a 60% clone rate with a 95% CI of 0.39-0.78.
- In MCP-MCP comparisons, the highest `ssdeep` bucket, 80-100, contains 517 pairs; manual review labels 17 of 20 sampled pairs as clones, an 85% clone rate with a 95% CI of 0.64-0.95.
- In Skills-Skills comparisons, the 80-100 `ssdeep` bucket contains 94 pairs; 15 of 20 sampled pairs are clones, a 75% clone rate with a 95% CI of 0.53-0.89.
- Cross-domain MCP-Skills cloning is weaker but present: in the 60-80 Jaccard bucket, 4 of 8 sampled pairs are clones, a 50% clone rate with a 95% CI of 0.22-0.78.
- Metadata is concentrated: MCP data retrieval and API interaction account for 76.6% of MCP tools, while Skills developer tooling accounts for 59.1% of Skills tools; this supports the paper's claim that repeated wrapper patterns make code reuse likely.

## Link
- [https://arxiv.org/abs/2605.09817v2](https://arxiv.org/abs/2605.09817v2)
