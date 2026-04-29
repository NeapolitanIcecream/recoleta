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
Mnemos 通过读取 Claude 的本地对话存储、建立索引，并通过 MCP 提供搜索，为 Claude Desktop 增加了一层本地记忆。它的目标是用检索相关的历史片段来替代把所有内容都留在一个活动对话里，从而减少长上下文带来的变慢和混乱。

## 问题
- Claude Desktop 没有历史记录或记忆 API，因此很难以结构化方式复用过去的对话。
- 随着上下文变长，很长的聊天会削弱模型表现，导致响应更慢、混乱增加、幻觉更多；该项目将这种现象称为 context rot。
- 想要持久记忆且重视隐私的用户，可能不希望使用云同步或外部 API 调用。

## 方法
- Mnemos 对 Claude Desktop 本地的 Chromium 存储进行逆向分析，实时监控文件，解压已存储的数据，并从当前会话和历史记录中解析对话内容。
- 它使用 ONNX 版本的 MiniLM-L6-v2 在本地生成消息嵌入，然后将文本和向量存入 SQLite，使用 FTS5 做关键词搜索，使用 vector blobs 做语义搜索。
- 它通过基于 JSON-RPC 的 MCP 服务器把检索能力提供给 Claude，因此 Claude 可以按需查询相关的历史片段。
- 搜索采用混合检索：将来自 SQLite FTS5 的 BM25 关键词排序与基于余弦相似度的语义排序结合，再用 Reciprocal Rank Fusion 合并结果。
- v1.1 增加了一个本地图形界面，用户可以用 UMAP 和 K-Means 在 3D 视图中浏览、搜索并可视化对话历史。

## 结果
- 该系统声称可完全离线运行：没有 API 调用，没有云同步，数据也不会离开本机。
- 它声称通过操作系统文件监视器和信号量去抖实现实时索引，并且没有轮询开销。
- 嵌入使用 MiniLM-L6-v2，向量维度为 384；可视化则用 UMAP 对这些嵌入做投影，并结合 K-Means 聚类。
- 摘录中没有给出检索质量、延迟、内存节省、幻觉减少或用户结果的基准数据。
- 最明确的具体主张是架构层面的：使用 Reciprocal Rank Fusion 的混合搜索比单独使用语义搜索或关键词搜索有更好的召回率，但摘录中没有提供实测对比。

## Problem

## Approach

## Results

## Link
- [https://github.com/Foued-pro/Mnemos](https://github.com/Foued-pro/Mnemos)
