---
source: hn
url: https://mrzk.io/posts/qmlx-maximising-ai-psychosis-minmaxing-mac-studio/
published_at: '2026-07-11T22:54:06'
authors:
- marzukia
topics:
- local-inference
- long-context-caching
- code-intelligence
- apple-silicon
- model-serving
relevance_score: 0.93
run_id: materialize-outputs
language_code: zh-CN
---

# Fixed three bugs that made Qwen3.5-122B a daily driver on Mac Studio

## Summary
## 摘要
qMLX 通过修复三个缓存和历史记录错误，让 Qwen3.5-122B 能在配备 M3 Ultra 的 Mac Studio 上用于长上下文本地编程。基于磁盘的 KV 恢复将重复 32k token 的预填充时间从 88 秒降至 0.64 秒，解码速度为每秒 28-55 token。

## 问题
- 长上下文追问需要等待 3-5 分钟才出现第一个 token，使本地结对编程难以使用。
- 由于系统提示词发生变化、被中断的回复未写入历史记录，以及无法匹配的检查点淘汰了有效的磁盘检查点，服务栈会反复重新计算对话内容。
- 122B 模型可以装入 96GB 统一内存，但每次都对完整上下文进行预填充会抵消本地推理的实际优势，因此这个问题很重要。

## 方法
- 将 rapid-mlx 分叉为 qMLX，为 Apple Silicon 上的 Qwen3.5 和 Qwen3.6 模型加入混合注意力支持。
- 从 SSD 恢复可复用的注意力 KV 状态，使每一轮只需对上一个检查点之后新增的 token 进行预填充。
- 从缓存的系统提示词中移除每轮都会变化的消息 ID，以保持逐字节一致的前缀匹配。
- 在生成被中断时保存流式输出的助手回复，使服务器状态与对话历史保持一致。
- 淘汰检查点时优先保留可匹配的检查点，并在启用恢复后禁用无效检查点写入。

## 结果
- 在配备 96GB 统一内存的 M3 Ultra Mac Studio 上，重复处理 32k token 提示词时，不使用缓存需要 88 秒，使用磁盘恢复后需要 0.64 秒，速度提升 137 倍。
- 同一基准测试显示，缓存加速比在 1k token 时为 13 倍，在 32k token 时为 137 倍。
- 在一个从 31k 增长到 57k token 的对话中，热启动轮次恢复了约 53k-56k 个缓存 token，只需对 33-1,869 个新增 token 进行预填充；实测预填充时间为 33-1,871 毫秒。
- 短上下文下的预填充吞吐量约为每秒 700 token，64k 上下文下为每秒 386 token；解码吞吐量则从每秒 55 token 降至每秒 28 token。
- 在 168k token 时，一个包含 67 个 token 的追问需要 2.6 秒才能出现第一个 token；额外加入包含 1,800 个 token 的工具结果后，预填充需要约 17 秒。
- 这些数据来自一台 M3 Ultra 系统，尚未在其他 Apple Silicon 配置上复现。

## Problem

## Approach

## Results

## Link
- [https://mrzk.io/posts/qmlx-maximising-ai-psychosis-minmaxing-mac-studio/](https://mrzk.io/posts/qmlx-maximising-ai-psychosis-minmaxing-mac-studio/)
