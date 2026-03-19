---
source: hn
url: https://arstechnica.com/gadgets/2026/03/amazon-appears-to-be-down-with-over-20000-reported-problems/
published_at: '2026-03-05T23:12:32'
authors:
- samizdis
topics:
- service-outage
- amazon
- incident-report
- web-reliability
relevance_score: 0.0
run_id: materialize-outputs
language_code: en
---

# Amazon Appears to Be Down

## Summary
This article reports on a large-scale Amazon service outage in March 2026, which mainly affected the website checkout flow, product pages, and mobile access. Based on Downdetector data and Amazon’s official response, it outlines the occurrence, spread, and recovery of the incident.

## Problem
- The question the article addresses is: **whether Amazon was experiencing a widespread service outage at the time, which functions were affected, and when service recovered**.
- This matters because Amazon is a hyperscale e-commerce and cloud services platform, and an outage directly affects shopping, checkout, and platform availability.
- For outside observers and users, promptly confirming the scope, timeline, and cause of the incident helps determine whether it is an individual network problem or a platform-level outage.

## Approach
- The article’s core method is very simple: **aggregate user-submitted data from the third-party outage reporting platform Downdetector, combine it with the reporter’s direct verification through site access, and then supplement it with Amazon’s official social account updates and later statement**.
- It first uses time-series data to determine when the outage began, when it peaked, and when it subsided.
- It then uses the share of issue categories to show which functional modules were most severely affected, such as checkout, the mobile app, and product pages.
- Finally, Amazon’s official statement provides the cause of the incident: it was related to a **software code deployment**, and confirms that the issue has been resolved.

## Results
- Downdetector showed that reports of problems began rising at **1:41 p.m. ET**, reaching **18,320** reports by **2:26 p.m. ET**.
- The outage reports peaked at **20,804** at **3:32 p.m. ET**, indicating a widespread, short-duration, high-intensity service disruption.
- By issue type, about **50%** of reports were related to **checkout**, **21%** came from **mobile app** users, and **17%** pointed to **product page** problems.
- Ars Technica’s testing confirmed that some product pages **failed to load properly or did not load at all**, and the Amazon homepage also intermittently failed to load.
- After **4:10 p.m. ET**, outage reports began to decline, falling significantly by **5:55 p.m. ET**; by **9:05 p.m. ET** that evening, the number of Downdetector reports had dropped to **435**.
- Amazon later stated that the issue had been resolved and explicitly identified the cause as a **software code deployment-related failure**; the article does not provide deeper technical remediation details or system-level performance metrics.

## Link
- [https://arstechnica.com/gadgets/2026/03/amazon-appears-to-be-down-with-over-20000-reported-problems/](https://arstechnica.com/gadgets/2026/03/amazon-appears-to-be-down-with-over-20000-reported-problems/)
