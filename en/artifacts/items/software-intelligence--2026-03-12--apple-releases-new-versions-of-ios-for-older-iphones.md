---
source: hn
url: https://www.macrumors.com/2026/03/11/apple-ios-16-7-15-release/
published_at: '2026-03-12T23:32:50'
authors:
- mgh2
topics:
- ios-security
- legacy-device-support
- software-update
- apple-ecosystem
relevance_score: 0.05
run_id: materialize-outputs
language_code: en
---

# Apple Releases New Versions of iOS for Older iPhones

## Summary
This is a product and security update news item, not a research paper. It mainly explains that Apple released security patch updates for iOS/iPadOS 15 and 16 for older iPhones and iPads that cannot upgrade to newer systems.

## Problem
- Older devices cannot run newer versions of iOS/iPadOS, but they still face security risks from disclosed vulnerabilities.
- If older devices do not receive patches, known vulnerabilities (such as the Coruna exploit-related issues mentioned in the article) may continue to expose users.
- Maintaining the security of older devices over the long term is important, because device lifecycles often exceed the support cycle of major OS versions.

## Approach
- Apple released point-version updates for older devices: iOS 16.7.15, iPadOS 16.7.15, iOS 15.8.7, and iPadOS 15.8.7.
- The core mechanism is simple: backport security fixes that were previously addressed in newer iOS 16 / iOS 17 updates to older devices that cannot upgrade to iOS 17 or later.
- The updates are distributed through the system path "Settings -> General -> Software Update," and can also be installed automatically in the coming days through the automatic update mechanism.
- Apple states that these versions include important security fixes, and the security notes show that they are related to the sophisticated Coruna exploit disclosed by Google last week.

## Results
- **4** update versions were released: **iOS 16.7.15, iPadOS 16.7.15, iOS 15.8.7, iPadOS 15.8.7**.
- Apple says these updates include "**important security fixes**" and bring issues previously fixed in **iOS 16** and **iOS 17** to older devices.
- A long-term support signal given in the article: Apple commits to providing security updates for iPhones for at least **5 years** after release; it also gives the example that the **iPhone 5s** still received an update earlier this year, **13 years** after launch.
- No quantitative metrics on patch effectiveness, test datasets, baseline comparisons, or performance figures are provided, so there are **no research-style quantitative results to report**.
- The strongest specific claim is that these patches address issues related to the disclosed **Coruna exploit** and cover users of older devices that cannot upgrade to iOS 17+.

## Link
- [https://www.macrumors.com/2026/03/11/apple-ios-16-7-15-release/](https://www.macrumors.com/2026/03/11/apple-ios-16-7-15-release/)
