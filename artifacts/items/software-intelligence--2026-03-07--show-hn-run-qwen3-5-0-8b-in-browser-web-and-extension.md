---
source: hn
url: https://tiny-whale.vercel.app/
published_at: '2026-03-07T23:07:46'
authors:
- tantara
topics:
- browser-llm
- webgpu
- local-inference
- privacy-preserving-ai
- multimodal-chat
relevance_score: 0.78
run_id: materialize-outputs
---

# Show HN: Run Qwen3.5 0.8B in browser (Web and Extension)

## Summary
这是一个把开源大模型直接运行在浏览器中的本地推理应用，依靠 WebGPU 实现无需服务器、无需 API 的聊天与多模态交互。它强调隐私、本地离线可用和低门槛体验，展示了端侧 LLM 在网页与扩展中的可行性。

## Problem
- 传统 AI 聊天产品通常依赖云端推理，带来**隐私泄露、网络依赖、延迟和使用成本**问题。
- 用户很难在**无需注册、无需部署后端**的情况下，直接体验本地大模型能力，尤其是在浏览器环境中。
- 多模态与可控生成参数通常需要复杂工具链，而普通用户缺少一个**即开即用的本地 AI playground**。

## Approach
- 使用 **WebGPU** 在用户本机 GPU 上执行全部模型推理，使模型在浏览器或扩展内本地运行。
- 采用**纯前端本地执行**方式：无服务器、无 API 调用、无遥测，模型加载后可离线使用。
- 支持**开源 LLM 聊天**以及**多模态输入**，例如上传图片并在本地完成理解与问答。
- 提供温度、top-p、top-k、重复惩罚等**生成参数控制**，让用户可细粒度调节输出行为。

## Results
- 作品声称可在浏览器中运行 **Qwen3.5 0.8B**，并支持 **Web 和浏览器扩展** 形态。
- 明确宣称 **100% 本地推理**：数据“不离开设备”，**无服务器、无 API calls、无 telemetry**。
- 明确宣称模型**加载完成后可离线工作**，这相比依赖在线云服务的方案更适合隐私敏感和弱网场景。
- 支持**多模态本地处理**：可上传图片并进行问答，且处理过程在本机完成。
- 文本未提供**定量基准结果**，没有给出延迟、吞吐、显存占用、准确率或相对 baseline 的具体数字比较。
- 最强的具体主张是：**免费、私密、快速、免注册**，并提供可调采样参数的本地 AI 交互体验。

## Link
- [https://tiny-whale.vercel.app/](https://tiny-whale.vercel.app/)
