---
source: hn
url: https://tiny-whale.vercel.app/
published_at: '2026-03-07T23:07:46'
authors:
- tantara
topics:
- webgpu-inference
- browser-llm
- on-device-ai
- multimodal-chat
- privacy-preserving
relevance_score: 0.1
run_id: materialize-outputs
---

# Show HN: Run Qwen3.5 0.8B in browser (Web and Extension)

## Summary
这是一个把开源多模态小模型直接运行在浏览器中的本地推理应用，依赖 WebGPU 实现无服务器、无遥测、可离线的聊天与看图问答。它主要强调隐私、本地化和易用性，而不是提出新的模型或学习算法。

## Problem
- 传统在线 LLM 服务通常依赖云端 API，带来隐私泄露、网络依赖、延迟和使用门槛问题。
- 用户如果想体验本地 AI，往往需要安装复杂环境，而浏览器端原生运行模型的可用产品仍较少。
- 对于图像问答等多模态能力，很多工具仍需要把数据上传到服务器，这对敏感数据场景很重要。

## Approach
- 使用 **WebGPU** 在用户本机 GPU 上直接执行模型推理，使所有计算都留在浏览器内完成。
- 提供浏览器端聊天界面，加载开源模型（标题中提到 **Qwen3.5 0.8B**）后即可本地对话，无需注册、无需 API。
- 支持 **multimodal input**，用户可上传图片并进行问答，图像处理同样在本地完成。
- 提供温度、top-p、top-k、repetition penalty 等生成参数控制，让用户像在本地 playground 中调试生成行为。
- 模型加载完成后可 **offline** 使用，核心机制就是把推理前端化，而不是把请求发往远程服务。

## Results
- 文本未提供任何标准基准测试结果，**没有**给出准确率、延迟、吞吐、内存占用或与其他系统的量化对比。
- 最强的具体声明是：**所有推理都在本地 GPU 上通过 WebGPU 运行**，且**没有 server、没有 API calls、没有 telemetry**。
- 声称模型加载后可**离线工作**，这意味着后续使用不依赖持续联网，但未给出离线性能数字。
- 声称支持**多模态输入**（上传图片并提问），且处理过程**本地完成**，但未给出支持的模型范围或视觉任务指标。
- 标题中的最具体实例是可在浏览器中运行 **Qwen3.5 0.8B**，但正文摘录未报告加载时间、帧率、token/s 或相对 baseline 提升。

## Link
- [https://tiny-whale.vercel.app/](https://tiny-whale.vercel.app/)
