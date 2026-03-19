---
source: hn
url: https://mxmap.ch/
published_at: '2026-03-10T23:08:13'
authors:
- notmine1337
topics:
- dns-analysis
- digital-sovereignty
- email-infrastructure
- public-sector-tech
relevance_score: 0.18
run_id: materialize-outputs
language_code: en
---

# Classifying email providers of 2000 Swiss municipalities via DNS

## Summary
This project classifies and visualizes the official email service providers of approximately 2,100 Swiss municipalities using public DNS records, in order to increase transparency around public-sector email infrastructure. Its core value lies in supporting public discussion around digital sovereignty and data-jurisdiction risks.

## Problem
- It is often not transparent which kinds of email providers municipalities use, making it difficult for the public to understand the actual dependencies of public communication infrastructure.
- This matters because US providers may be subject to the **US CLOUD Act**, raising concerns about cross-border data access and digital sovereignty.
- It is difficult to systematically identify the nationwide distribution of municipal email providers through casual inspection alone, so a scalable and reviewable method is needed.

## Approach
- The project collects public **DNS** information for each Swiss municipality’s official domain, focusing on **MX** and **SPF** records.
- It infers who routes the email and which senders are authorized based on these records, and uses that to classify municipalities into different provider types.
- The results are displayed on a map covering municipalities across the country, grouped by jurisdiction, making it easier to observe the provider landscape.
- The method relies as much as possible on public, verifiable data sources; at the same time, it explicitly states that DNS can only reflect mail routing and authorized senders, and **cannot directly prove where data is actually stored**.
- The code and data are open-sourced on GitHub, supporting external review and error reporting.

## Results
- Coverage: it presents a map classifying the official email providers of approximately **2,100** Swiss municipalities.
- Data source: classification is performed after checking the public **MX + SPF** records of each municipality’s official domain.
- The excerpt **does not provide** quantitative evaluation results such as accuracy, recall, F1, comparisons against manual labels, or baseline methods.
- The strongest concrete claim is that the system makes the landscape of Swiss municipal email providers visible, thereby providing an actionable evidentiary basis for discussions of digital sovereignty.
- Another explicit claim is that the classification is based on public DNS signals and is therefore reviewable, but its conclusions are limited by the fact that DNS cannot directly reveal where data is stored.

## Link
- [https://mxmap.ch/](https://mxmap.ch/)
