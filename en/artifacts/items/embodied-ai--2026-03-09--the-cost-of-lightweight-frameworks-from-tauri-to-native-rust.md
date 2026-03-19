---
source: hn
url: https://www.gethopp.app/blog/hate-webkit
published_at: '2026-03-09T23:38:35'
authors:
- birdculture
topics:
- tauri
- webkit
- rust-native-ui
- webrtc
- cross-platform-apps
relevance_score: 0.03
run_id: materialize-outputs
language_code: en
---

# The Cost of 'Lightweight' Frameworks: From Tauri to Native Rust

## Summary
This article is not an academic paper, but an engineering retrospective: the author explains why a “lightweight” desktop stack based on Tauri/WebKit can actually create higher costs in low-latency remote collaboration scenarios, and argues for moving critical windows to native Rust. The core point is that for products that depend on WebRTC, audio/video, and cross-platform consistency, WebKit’s limitations can cancel out the advantages of lightweight frameworks.

## Problem
- The problem the article addresses is: **whether Tauri + WebKit is suitable for building an ultra-low-latency (target **<100ms**) remote pair programming / screen sharing app**, and what should replace it when it is not.
- This matters because products like Hopp are highly sensitive to **WebRTC, audio/video stability, codec support, cross-platform consistency, and resource usage**; once the browser engine behaves abnormally, users will immediately notice stuttering, crashes, or missing functionality.
- The pain points listed by the author include Safari/WebKit rendering issues, iOS pages crashing without logs, outdated user agent versions, audio problems, limited AV1 support, and the fact that **WebKitGTK does not support WebRTC by default**, which blocks Linux support.

## Approach
- The core approach is simple: **stop building critical real-time interactive interfaces on top of WebKit windows, and instead move critical windows and streaming logic to a native Rust (iced) implementation**.
- The mechanism is to **centralize the WebRTC/display/audio-video processing that was previously spread across multiple WebKit windows under unified backend management**, reducing synchronization complexity between frontend/backend and across multiple windows.
- Concretely, the author does not choose to switch directly to Electron, nor wait for Tauri’s CEF support, but instead opts for **partial native migration**: first converting the most critical screensharing/UI window into a native Rust window.
- After the migration, the author expects that each user will no longer need to generate **3 LiveKit tokens** for different windows or join as **3 participants**, but can instead be reduced to **1 participant per user**.
- In addition, once the backend directly receives the streams and buffers, it can bypass browser codec restrictions, use **any codec supported by libwebrtc**, and explore capabilities such as macOS Neural Engine image super-resolution.

## Results
- The article contains **no formal experiments, benchmark data, or systematic quantitative comparisons**, so there are no paper-style SOTA metrics to report.
- The only clear product target mentioned is that remote-control interaction latency must stay **<100ms**; the author cites Apple’s experiential threshold that above this level interactions start to feel “clunky.”
- The author reports one specific failure case: in iOS Safari, placing **3 GIFs** on a page could trigger the “**A problem repeatedly occurred**” crash, with **no console errors or traceable clues**; they worked around it by deferring rendering with **IntersectionObserver**.
- In the current architecture, each user needs **3 LiveKit tokens**, serving screen sharing, audio/camera, and camera view respectively, so **each person joins the call as 3 different participants**; after migration, this is claimed to drop to **1 person, 1 participant**.
- The author’s strongest engineering conclusion is that for complex desktop apps relying on WebRTC and low-latency streaming, the “lightweight” nature of Tauri/WebKit does not mean low total cost; **native Rust windows may improve code simplicity, codec freedom, Linux viability, and room for extensible features**.

## Link
- [https://www.gethopp.app/blog/hate-webkit](https://www.gethopp.app/blog/hate-webkit)
