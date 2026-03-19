---
source: hn
url: https://arstechnica.com/gadgets/2026/03/amazon-appears-to-be-down-with-over-20000-reported-problems/
published_at: '2026-03-05T23:12:32'
authors:
- samizdis
topics:
- service-outage
- software-deployment
- incident-report
- site-reliability
relevance_score: 0.27
run_id: materialize-outputs
language_code: en
---

# Amazon Appears to Be Down

## Summary
This is not a research paper, but rather a news report about an Amazon service outage. The core information is: an issue related to a **software code deployment** caused a large-scale disruption to Amazon's website and app on March 5, 2026, and it was later resolved.

## Problem
- The article describes a visible large-scale outage affecting Amazon's e-commerce website and app, impacting users' ability to browse products, access the homepage, and complete checkout.
- This matters because Amazon is a critical large-scale online retail and cloud services platform, so outages directly affect transaction conversion, user experience, and perceptions of platform reliability.
- From an engineering perspective, the incident shows that a single software code deployment can trigger a widespread production incident, highlighting the importance of release safety and fault isolation.

## Approach
- This article **does not propose a research method**; it mainly describes the incident based on Downdetector reports, media verification, and Amazon's subsequent statement.
- The information closest to a "mechanism" is Amazon's post-incident explanation: the issue was related to a **software code deployment**, meaning a production code release triggered abnormalities in the website and app.
- The report organizes the incident's progression through a timeline: reports of problems began rising at 1:41 p.m. ET, peaked at 3:32 p.m. ET, started declining after 4:10 p.m. ET, and was largely recovered by the evening.
- The article also breaks down affected user scenarios by outage type, such as checkout, mobile, and product page issues, to help identify the scope of impact.

## Results
- Downdetector showed that reports of problems began increasing at **1:41 p.m. ET**, reaching **18,320** reports by **2:26 p.m. ET**.
- Reports peaked at **20,804** at **3:32 p.m. ET**, indicating a broad impact.
- In terms of outage distribution, about **50%** of reports were related to **checkout**, **21%** came from **mobile app** users, and **17%** pointed to **product page** issues.
- Ars Technica's own testing confirmed that some product pages failed to load properly, and the Amazon homepage also sometimes failed to load.
- By **4:10 p.m. ET**, Downdetector reports began to decline; by **5:55 p.m. ET**, they had dropped significantly.
- By **9:05 p.m. ET**, reports had fallen to **435**; Amazon subsequently stated that the issue had been resolved and explicitly identified the cause as a failure related to a **software code deployment**.

## Link
- [https://arstechnica.com/gadgets/2026/03/amazon-appears-to-be-down-with-over-20000-reported-problems/](https://arstechnica.com/gadgets/2026/03/amazon-appears-to-be-down-with-over-20000-reported-problems/)
