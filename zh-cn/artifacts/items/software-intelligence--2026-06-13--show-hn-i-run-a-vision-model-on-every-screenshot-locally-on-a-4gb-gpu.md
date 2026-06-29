---
source: hn
url: https://github.com/ayushh0110/ScreenMind
published_at: '2026-06-13T23:12:54'
authors:
- skye0110
topics:
- screen-memory
- local-ai
- multimodal-llm
- privacy
- search
- agent-automation
relevance_score: 0.71
run_id: materialize-outputs
language_code: zh-CN
---

# Show HN: I run a vision model on every screenshot, locally, on a 4GB GPU

## Summary
ScreenMind 是一款本地屏幕记忆应用。它会截取屏幕，用 Gemma 4 分析，然后让你基于活动历史进行搜索、聊天，并在其上构建自动化。它之所以重要，是因为它瞄准了和 Recall 这类屏幕感知助手相同的用例，但数据保留在设备上，还加入了脱敏、加密和本地搜索。

## Problem
- 屏幕感知助手需要记录并理解你在电脑上跨应用、会议和语音笔记中的操作。
- 如果系统把数据明文存储，或发送到云服务，就会带来隐私和信任问题。
- 用户还需要一种方式，按含义搜索过去的屏幕活动，而不只是按文件名或精确文本搜索。

## Approach
- 只在屏幕内容发生变化时截取屏幕，再用感知哈希和按应用感知的缓存跳过重复内容。
- 将每张截图和 OCR 文本一起发送给 Gemma 4 E2B，做结构化视觉分析，包括应用名称、活动类别、摘要、情绪、场景描述和布局区域。
- 把 EasyOCR、MiniLM 向量和 SQLite FTS5 结合起来，让搜索同时支持语义相似度和关键词匹配。
- 用 Gemma 4 的音频编码器加入语音备忘和会议转写，然后把摘要和元数据保存在本地。
- 通过聊天、REST API、MCP 和插件代理公开这些历史记录，供自定义自动化使用。

## Results
- 该项目声称在初始模型下载后可实现 100% 本地处理，没有云依赖。
- 它给出了三种分析模式：Accurate 约每张截图 76 秒，Balanced 约 40 秒，Fast 约 12 秒。
- 它称系统可在 4GB 以上 GPU 上运行，模型大约需要 5GB 磁盘空间。
- 它声称通过三层、按应用的 pHash 缓存减少推理调用，并更快释放 GPU；聊天会在 1 秒内取消正在进行的分析。
- 摘录中没有基准表或外部评测数据，所以最强的主张是本地私有的工作流、多模态屏幕理解和自动化支持。

## Link
- [https://github.com/ayushh0110/ScreenMind](https://github.com/ayushh0110/ScreenMind)
