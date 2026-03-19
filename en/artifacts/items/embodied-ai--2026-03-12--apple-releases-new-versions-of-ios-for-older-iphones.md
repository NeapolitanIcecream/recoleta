---
source: hn
url: https://www.macrumors.com/2026/03/11/apple-ios-16-7-15-release/
published_at: '2026-03-12T23:32:50'
authors:
- mgh2
topics:
- apple-security-update
- ios
- ipad-os
- legacy-device-support
- mobile-security
relevance_score: 0.0
run_id: materialize-outputs
language_code: en
---

# Apple Releases New Versions of iOS for Older iPhones

## Summary
This article describes Apple releasing the iOS/iPadOS 15.8.7 and 16.7.15 security updates for older iPhones and iPads that cannot upgrade to newer systems, with the focus on fixing the disclosed sophisticated Coruna exploit. Its significance is that it shows Apple continues to provide long-term security support for older devices, but this is not a robotics or AI research paper.

## Problem
- Older iPhones and iPads cannot run the latest versions of iOS/iPadOS, but they still face risks from known security vulnerabilities.
- The sophisticated **Coruna exploit** disclosed by Google last week needs to be patched; otherwise, users of older devices will remain exposed to attack.
- Long-term device security support is important because many users are still using hardware released many years ago.

## Approach
- Apple released **iOS 16.7.15, iPadOS 16.7.15, iOS 15.8.7, and iPadOS 15.8.7**, specifically for older devices that cannot upgrade to newer major versions.
- The core mechanism is simple: backport the security patches that were previously fixed in **iOS 16 / iOS 17** to older system branches.
- Users can install them manually via **Settings > General > Software Update**, or wait for automatic update rollout.
- Apple positions these versions as maintenance updates containing “important security fixes,” rather than feature updates.

## Results
- **4** software update versions for older devices were released: **iOS 16.7.15, iPadOS 16.7.15, iOS 15.8.7, and iPadOS 15.8.7**.
- Apple explicitly states that these updates fix issues related to the **Coruna exploit**; those issues had previously been fixed in multiple **iOS 16 / iOS 17** updates and are now being brought to older devices as well.
- The long-term support figures given in the article include: Apple promises at least **5 years** of security updates after a device launches; it also gives the example that the **iPhone 5s still received an update 13 years after launch**.
- It does not provide the experimental metrics, datasets, baseline models, or percentage performance gains typical of a traditional research paper; the strongest concrete claim is that Apple is extending known critical security fixes to older devices that cannot upgrade to newer systems.

## Link
- [https://www.macrumors.com/2026/03/11/apple-ios-16-7-15-release/](https://www.macrumors.com/2026/03/11/apple-ios-16-7-15-release/)
