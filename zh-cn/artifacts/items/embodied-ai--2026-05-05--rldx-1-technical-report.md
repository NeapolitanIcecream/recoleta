---
source: arxiv
url: https://arxiv.org/abs/2605.03269v2
published_at: '2026-05-05T01:40:15'
authors:
- Dongyoung Kim
- Huiwon Jang
- Myungkyu Koo
- Suhyeok Jang
- Taeyoung Kim
- Beomjun Kim
- Byungjun Yoon
- Changsung Jang
- Daewon Choi
- Dongsu Han
- Donguk Lee
- Heeseung Kwon
- Hojin Jeon
- Jaehyun Kang
- Jaekyoung Bae
- Jihyuk Lee
- Jimin Lee
- John Won
- Joonwoo Ahn
- Junhyeong Park
- Junyoung Sung
- Kyungmin Lee
- Minseong Han
- Minsung Yoon
- Sejune Joo
- Seonil Son
- Seungcheol Park
- Seunggeun Cho
- Seungjun Moon
- Seungku Kim
- Yonghoon Dong
- Yongjin Cho
- Youngchan Kim
- Chang Hwan Kim
- Dohyeon Kim
- Heecheol Kim
- Heewon Lee
- Hensen Ahn
- Hyungkyu Ryu
- Hyunsoo Choi
- Hyunsoo Shin
- Jaeheon Jung
- Jaewoo Kim
- Jinwook Kim
- Joochul Chang
- Joonsoo Kim
- Junghun Park
- Jungwoo Park
- Junho Cho
- Junhyeok Park
- Junwon Lee
- Kangwook Lee
- Kwanghoon Kim
- Kyoungwhan Choe
- Manoj Bhadu
- Nayoung Oh
- Sangjun Kim
- Sangwoo Kim
- Seunghoon Shim
- Seunghyun Kim
- Seungjun Lee
- Seungyup Ka
- Sungryol Yang
- Wook Jung
- Yashu Shukla
- Yeonjae Lee
- Yeonwoo Bae
- Jinwoo Shin
topics:
- vision-language-action
- dexterous-manipulation
- generalist-robot-policy
- robot-data-scaling
- multimodal-transformer
- real-robot-evaluation
relevance_score: 0.96
run_id: materialize-outputs
language_code: zh-CN
---

# RLDX-1 Technical Report

## Summary
## 摘要
RLDX-1 是一个用于灵巧操作的 VLA 机器人策略，它在基于 Qwen3-VL 的策略上加入了运动、记忆和触觉/扭矩输入。报告称，它在仿真和真实机器人任务上，相比 π_{0.5} 和 GR00T N1.6 有大幅提升，尤其是在高自由度类人机器人任务上。

## 问题
- 现有 VLA 往往能处理场景理解和语言指令，但在操作需要运动跟踪、长期任务状态或接触感知时表现不足。
- 这对真实机器人很重要，因为传送带接物、抽牌式选择、可变形物体抓取和插入等任务，在策略只能看到当前图像和指令时容易失败。

## 方法
- RLDX-1 以 Qwen3-VL 8B 作为 VLM 基座，并用机器人 VQA 数据微调，覆盖空间关系、子任务推断和低层动作落地。
- 模型加入了一个用于多帧视频的运动模块、一个保存过去 3 个认知特征块的记忆模块，以及一个处理触觉和扭矩信号的物理流。
- 其 Multi-Stream Action Transformer 将认知、动作/本体感觉和物理信息分成独立流处理，再通过联合自注意力交换信息，同时用 flow matching 预测动作块。
- 训练分 3 个阶段：多载体预训练、结合内部和合成数据的载体特定中期训练，以及可选强化学习的任务特定后训练。
- 合成数据流程包括图像/视频生成、通过逆动力学标注动作、视频质量过滤，以及通过模拟器回放进行运动一致性过滤。

## 结果
- 在 ALLEX 类人任务上，RLDX-1 的成功率为 86.8%，而 π_{0.5} 和 GR00T N1.6 约为 40%。
- 在传送带高速物体抓取任务上，RLDX-1 的成功率超过 87.5%，而 π_{0.5} 低于 29.2%。
- 在 GR-1 Tabletop 上，RLDX-1 的成功率为 58.7%，GR00T N1.6 为 47.6%。
- 在 OpenArm 的通用智能测试中，RLDX-1 将未见过物体的成功率从 π_{0.5} 的 37.5% 提升到 54.2%，将未见过任务的成功率从 45.8% 提升到 54.2%。
- 在需要长期记忆的 ALLEX Object-in-Box Selection 任务上，RLDX-1 的成功率为 91.7%，而 GR00T N1.6 和 π_{0.5} 都在 30% 左右。
- 合成数据让 GR-1 Tabletop 的结果比只用真实数据训练高 9.1 个百分点；推理优化把 RTX 5090 上的单步延迟从 71.2 ms 降到 43.7 ms，速度提升 1.63 倍。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.03269v2](https://arxiv.org/abs/2605.03269v2)
