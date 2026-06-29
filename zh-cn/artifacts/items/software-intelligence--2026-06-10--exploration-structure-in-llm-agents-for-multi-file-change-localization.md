---
source: arxiv
url: https://arxiv.org/abs/2606.11976v1
published_at: '2026-06-10T11:54:14'
authors:
- Akeela Darryl Fattha
- Kia Ying Chua
- Lingxiao Jiang
- Laura Wynter
topics:
- software-agents
- code-localization
- multi-agent-systems
- swe-bench
- repository-analysis
- llm-code-intelligence
relevance_score: 0.94
run_id: materialize-outputs
language_code: zh-CN
---

# Exploration Structure in LLM Agents for Multi-File Change Localization

## Summary
## 总结
论文认为，按仓库子系统并行探索能提高 LLM 软件代理的多文件变更定位效果，尤其适合搜索预算有限的小模型。它评估了 SWE-bench Pro 中的 Ansible 问题，并比较了无工具 LLM、顺序 REPL 代理、按领域划分的代理、BM25 和 Codex 5.5 High。

## 问题
- 这项任务是在补丁生成开始前预测 GitHub 问题需要改动哪些仓库文件；这很重要，因为 SWE-bench Pro 中 80% 的实例涉及多文件，漏掉一个子系统就可能让正确修复无法完成。
- 大多数 LLM 代理每一步只检查一个文件、一个目录或一个 grep 结果，这会把预算消耗在仓库的某一部分，而真实修复可能跨越代码、插件、CLI 路径、测试或文档。
- 直接访问文件系统会增加误报，尤其是测试文件和变更日志文件。它们可能出现在修复 PR 中，但不在整理后的 SWE-bench Pro gold 集里。

## 方法
- 该方法为 Ansible 仓库中连贯的领域区域建立持久代理，例如 `lib/ansible/cli/`、`lib/ansible/module_utils/`、`lib/ansible/galaxy/`、plugins 和 `docs/docsite/rst/`。
- 查询时，根协调器读取问题，选择相关的领域代理，并行运行它们，再合并候选文件列表。
- 每个领域代理只搜索分配到的仓库区域，并返回候选文件及简短理由。
- 有界 I/O 层通过预览、行范围读取、搜索结果、紧凑目录列表和持久 Python 环境中的句柄，把大文件和目录排除在提示之外。
- 评估使用一个持久会话的 Ansible 切片：基于基准提交 `01e7915b0a97` 的 19 个 SWE-bench Pro 实例，其中有 15 个困难的多文件案例、4 个简单案例、63 个整理后的 gold 文件，以及 9 个包含文档文件的案例。

## 结果
- 摘要中提到，Haiku 级领域代理在 Haiku 级方法里以明显优势取得最高的 micro-F1；摘录没有给出具体 micro-F1 数值。
- 在作者扩展的、包含 2025 和 2026 年 PR 的基于 PR 基准上，领域代理排在第二位，仅次于 Codex 5.5 High；摘录没有给出具体分数。
- 在原始、整理过的 2020 SWE-bench Pro 切片上，更大的 Sonnet 纯 LLM 基线通过预测更少文件获得更高的 micro-F1，这提高了 precision，但降低了 all-gold recall；摘录没有给出具体 precision、recall 和 F1 数值。
- 该基准切片包含 19 个 Ansible 问题、63 个整理后的 gold 文件，以及一个包含 171 个被触及文件的 PR 参考集；在整理后的 gold 集中缺失的 108 个 PR 触及文件里，有 52 个集成测试文件、27 个单元测试文件、10 个其他测试文件和 16 个变更日志片段。
- 有界 I/O 大幅降低提示成本：一个大型源文件的上下文从 29,895 个 token 降到 719 个，减少 97.6%；一个大型文档文件从 14,366 个 token 降到 121 个，减少 99.2%。
- 紧凑目录列表把路径还原准确率保持在 50/50，同时把平均输入 token 从 1,540 降到 910，减少 40.8%。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.11976v1](https://arxiv.org/abs/2606.11976v1)
