---
source: hn
url: https://www.windowslatest.com/2026/03/06/microsoft-authenticator-will-crack-down-on-jailbroken-rooted-ios-and-android-phones-for-enterprises/
published_at: '2026-03-07T22:38:32'
authors:
- josephcsible
topics:
- mobile-security
- identity-management
- enterprise-authentication
- device-integrity
- entra
relevance_score: 0.11
run_id: materialize-outputs
---

# MS Authenticator will crack down on jailbroken/rooted iOS and Android phones

## Summary
这篇文章介绍了 Microsoft 将对企业版 Microsoft Authenticator 加强设备完整性管控：逐步识别并淘汰越狱/Root 的 iOS 和 Android 设备。其核心目标是降低受损设备上凭据、2FA 与无密码登录被窃取或滥用的风险。

## Problem
- 要解决的问题是：**企业用户仍可在越狱或 Root 的手机上使用 Microsoft Authenticator**，而这类设备绕过了系统原生安全保护，增加了凭据泄露与账户被盗风险。
- 这很重要，因为 Authenticator 承载了**工作/学校账户登录、双因素认证和无密码登录**；一旦运行环境被攻破，企业身份安全会受到直接影响。
- 文章还指出，这一变化**面向 Microsoft Entra 客户**，且不是可选择退出的功能，说明微软将其视为强制性的企业安全基线。

## Approach
- 核心机制很简单：**应用检测手机是否越狱/Root**；如果发现设备被修改，就按阶段逐步升级限制，直到完全不可用并清除本地数据。
- **Phase 1: Warning Mode**：先弹出警告，明确设备已绕过内建安全保护，但此阶段仍允许用户点击 Continue 继续使用。
- **Phase 2: Blocking Mode**：开始阻止工作/学校账户登录，且禁止使用 2FA 和无密码登录功能；应用可打开，但基本失去实际用途。
- **Phase 3: Wipe Mode**：自动登出并清除本地个人数据，不再允许访问已保存账户或使用 Authenticator 功能。
- 部署节奏上，**Android 从 2026 年 2 月最后一周开始，iOS 从 2026 年 4 月开始，整体计划在 2026 年年中/6 月前后完成**。

## Results
- 这不是学术论文，没有提供标准基准测试、实验数据或精确安全指标，因此**没有可报告的量化性能结果**。
- 最强的可验证结果性声明是：**Android 推送已于 2026 年 2 月最后一周开始**，**iOS 将于 2026 年 4 月开始**，并**在 2026 年年中（文中称约 6 月）完成 rollout**。
- 功能影响上，微软声称在 **Blocking Mode** 中会**阻止工作/学校账户登录**，并**禁用 2FA 与 passwordless sign-in**，使应用“打开但无法用于任何认证活动”。
- 在 **Wipe Mode** 中，微软声称应用将**自动登出并删除设备上的个人数据痕迹**，且**无选项恢复已保存账户访问**，除非联系组织支持团队。
- 相比此前允许在受损设备上继续运行的状态，这一更新的突破点是：**从提示风险升级为强制执行的设备完整性策略**，并且**不支持 opt-out**。

## Link
- [https://www.windowslatest.com/2026/03/06/microsoft-authenticator-will-crack-down-on-jailbroken-rooted-ios-and-android-phones-for-enterprises/](https://www.windowslatest.com/2026/03/06/microsoft-authenticator-will-crack-down-on-jailbroken-rooted-ios-and-android-phones-for-enterprises/)
