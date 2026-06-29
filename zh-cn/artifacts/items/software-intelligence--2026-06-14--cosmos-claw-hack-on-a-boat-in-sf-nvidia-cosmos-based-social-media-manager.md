---
source: hn
url: https://github.com/manas15/cosmos-claw
published_at: '2026-06-14T23:57:59'
authors:
- manas95
topics:
- agentic-video-generation
- social-media-automation
- multimodal-ai
- self-hosted-inference
- venue-marketing
relevance_score: 0.83
run_id: materialize-outputs
language_code: zh-CN
---

# Cosmos Claw: Hack on a Boat in SF (Nvidia Cosmos Based Social Media Manager)

## Summary
## 总结
Cosmos Claw 是一个面向场馆的代理式社交视频生成器。它把现有照片和场馆事实转成带品牌风格的短视频帖子、配音、文案和视频剪辑，不需要人工摄制团队。

## 问题
- 场馆需要持续产出短视频，才能在 Reels、TikTok、Shorts 以及类似信息流里保持曝光。
- 人工制作速度慢、成本高，而且很难在不同格式和不同帖子之间保持一致。

## 方法
- 它从上传的场馆照片和事实开始，然后用 GPT-4o 视觉模型给素材打标，并建立一个带稳定假设的品牌档案。
- 一个管理代理会调研场馆和周边区域，然后为每个帖子写新的活动方案：角度、钩子、素材顺序、格式、音乐、配音和文案。
- NVIDIA Cosmos 3 Nano 从选定照片生成短的第一人称运动片段，通过 vLLM-Omni 自托管在 Nebius H200 NVLink GPU 上。
- 这个流程还会加入 GPT 生成的配音、按氛围匹配的音乐、交叉淡入淡出和画幅适配，然后输出可直接发布的成品包。
- 系统以循环方式运行，每个场馆一个 worker，品牌档案里保存持久记忆，网络短暂中断后可以自动恢复。

## 结果
- 论文没有报告基准测试数字、准确率分数或用户研究结果。
- 它称系统可以并行生成多个场馆的可直接发布的社交视频。
- 它说当时有两个 worker 同时运行，分别为旧金山的两个场馆生成各自的可直接发布 Reels 和 TikToks。
- 它说系统在 Wi-Fi 或隧道中断后可以自动暂停并恢复继续运行。
- 它称一组上传照片就足以驱动跨格式的重复品牌视频生成，例如 9:16、1:1、4:5 和 16:9。

## Problem

## Approach

## Results

## Link
- [https://github.com/manas15/cosmos-claw](https://github.com/manas15/cosmos-claw)
