---
source: arxiv
url: https://arxiv.org/abs/2607.01537v1
published_at: '2026-07-01T23:36:49'
authors:
- Hongbo Wang
topics:
- world-models
- active-perception
- certified-prediction
- sensing-scheduling
- equivariant-models
- conformal-calibration
relevance_score: 0.61
run_id: materialize-outputs
language_code: zh-CN
---

# Certified World Models as Sensing Clocks: Drift-Aware Deadlines for Active Perception

## Summary
## 摘要
这篇论文把认证世界模型的有效性时域转化为重新感知截止期限，用于依靠开环预测滑行的智能体。它的主要主张是一个漂移感知时钟：在冻结的 3D VN-JEPA 模型上控制区间证书违例，并明确说明谱项收益的边界。

## 问题
- 使用世界模型的智能体需要一条规则，决定在开环滑行期间何时再次感知；感知过晚可能破坏预测证书，感知过早会浪费感知预算。
- 固定感知周期忽略模型当前可靠性，残差监视器则在误差已经增长后才触发。
- 目标指标是区间同时证书违例：在一次滑行区间内任意位置，预测误差超过认证容差的概率。

## 方法
- 该方法把认证预测时域作为感知截止期限：感知重置信念后，智能体滑行到认证时钟到期，然后再次感知。
- 朴素谱截止期限使用 Lyapunov 式扩张率，近似为 `T ~ log(epsilon/e0) / lambda`，用于估计预测误差保持在容差以下的时长。
- 部署规则加入校准后的原生 rollout 漂移包络：`b_h^UCB + C exp(lambda h) e0 + eta_h <= epsilon_cert`。截止期限是满足该界限的最大时域 `h`。
- 在完整重新感知的 VN-JEPA 设置中，感知后误差接近零，因此部署截止期限简化为漂移包络时钟，时域约为 2 到 3 步。
- 校准在校准划分上固定证书容差、漂移包络和松弛项，然后在留出区间上评估一次。

## 结果
- 在冻结的 3D VN-JEPA 上，三项留出测试都达到预注册的 interval-ICV 上界目标 `<= 0.15`：r2 分片 000 到 001 为 `epsilon_cert=1.15`、`T_eq=3`、`U95=0.092`；r1 分片 000 到 001 为 `epsilon_cert=1.10`、`T_eq=2`、`U95=0.139`；r2 分片 000 到 002 为 `epsilon_cert=0.95`、`T_eq=2`、`U95=0.095`。
- 在合成 oracle 截止期限基准上，interval-ICV 上界为 `U95=0.040` 和 `0.073`，均低于 `0.15` 目标。
- 在有限数据谱审计中，有效性在估计误差下仍然保持，`U95 <= 0.073`，预算比 `<= 1.11`，审计样本数低至约 `n=5` 时仍成立。
- 在感知预算匹配、约为 `0.068` 的 cue-conditioned reactive-contrast 基准中，认证时钟的总体 ICV 为 `U95=0.042`，eventful-tail ICV 为 `0.163`；MB-EIG 的总体为 `0.062`，eventful tail 为 `0.364`；Uniform 的总体为 `0.131`，tail 为 `0.715`。
- MB-EIG 需要约 `3x` 更多感知预算才能恢复尾部保护；风险敏感 MB-CVaR（`0.165` tail ICV）和 MB-WorstCase（`0.169` tail ICV）与认证时钟接近。
- 论文报告了若干限制：在 VN-JEPA 上，非谱经验 conformal 时域在全部 3 个已确认划分上的有效性和预算都与部署时钟匹配；lead-time 基准给出空结果（`0.955` Eq-spec 对 `0.957` Uniform）；在 partial-reset exploration 中，谱项没有显示出清晰的预算匹配优势。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2607.01537v1](https://arxiv.org/abs/2607.01537v1)
