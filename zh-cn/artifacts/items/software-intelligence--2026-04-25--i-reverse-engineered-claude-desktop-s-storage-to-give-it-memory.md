---
source: hn
url: https://github.com/Foued-pro/Mnemos
published_at: '2026-04-25T23:28:51'
authors:
- foufouadi
topics:
- code-intelligence
- memory-augmented-llm
- local-first-ai
- mcp
- retrieval-augmented-generation
relevance_score: 0.74
run_id: materialize-outputs
language_code: zh-CN
---

# I reverse-engineered Claude Desktop's storage to give it memory

## Summary
## 摘要
Mnemos 通过读取 Claude Desktop 磁盘上的对话存储、建立索引，并通过 MCP 暴露搜索，为 Claude Desktop 提供本地记忆层。它的目标是不用把所有内容都放进一个活跃对话里，而是按需取回相关的历史片段，从而避免长上下文带来的变慢和混乱。

## 问题
- Claude Desktop 没有历史或记忆 API，因此过去的对话很难以结构化方式复用。
- 很长的聊天会随着上下文增长而削弱模型表现，带来更慢的响应、更多混乱和更多幻觉；项目把这称为 context rot。
- 想要持久记忆且重视隐私的用户，可能不想要云同步或外部 API 调用。

## 方法
- Mnemos 逆向分析 Claude Desktop 的本地 Chromium 存储，实时监视文件，解压存储数据，并解析活动会话和历史记录中的对话条目。
- 它使用 MiniLM-L6-v2 的 ONNX 版本在本地生成嵌入，然后把文本和向量存入 SQLite，使用 FTS5 做关键词搜索，使用向量 BLOB 做语义搜索。
- 它通过基于 JSON-RPC 的 MCP server 把检索结果返回给 Claude，因此 Claude 可以按需查询相关的历史片段。
- 搜索使用混合检索：SQLite FTS5 的 BM25 关键词排序加上基于余弦相似度的语义排序，再用 Reciprocal Rank Fusion 合并。
- v1.1 增加了一个本地 GUI，用户可以在 3D 视图中浏览、搜索并可视化对话历史，使用 UMAP 和 K-Means。

## 结果
- 该系统声称完全离线运行：没有 API 调用、没有云同步，也没有数据离开机器。
- 它声称通过操作系统文件监视器和 semaphore debouncing 实现实时索引，没有轮询开销。
- 嵌入使用 MiniLM-L6-v2 的 384 维向量，可视化则用 UMAP 和 K-Means 聚类来投影这些嵌入。
- 这段论文摘录没有给出检索质量、延迟、内存节省、幻觉减少或用户结果的基准数据。
- 最明确的具体主张是架构上的：带有 Reciprocal Rank Fusion 的混合搜索，比单独使用语义搜索或关键词搜索有更好的召回率，但摘录里没有实测对比。

## Problem

## Approach

## Results

## Link
- [https://github.com/Foued-pro/Mnemos](https://github.com/Foued-pro/Mnemos)
