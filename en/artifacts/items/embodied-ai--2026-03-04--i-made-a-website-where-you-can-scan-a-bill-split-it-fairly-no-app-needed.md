---
source: hn
url: https://snapfair.pages.dev/
published_at: '2026-03-04T23:17:12'
authors:
- Herliken
topics:
- bill-splitting
- receipt-scanning
- ocr
- consumer-web-app
relevance_score: 0.0
run_id: materialize-outputs
language_code: en
---

# I made a website where you can: Scan a bill. Split it fairly. No app needed

## Summary
This is not a research paper, but a web product description for scanning bills and splitting expenses fairly. It describes the basic flow from scanning a receipt, correcting line items, assigning purchases to multiple people, and initiating payment requests.

## Problem
- It addresses the problem that **manually splitting a bill after group dining is troublesome, error-prone, and inefficient**.
- Its importance lies in the fact that bill splitting is a high-frequency real-life need; without a tool, people often have to manually calculate how much each person owes.
- It offers a web-based approach with **no app installation required**, lowering the barrier to use.

## Approach
- Users **scan a bill/receipt** through the web interface by aligning the receipt within the frame for capture.
- The system appears to automatically extract items and prices first, then allows users to **edit names or prices and remove recognition errors**, indicating a basic OCR/structured entry workflow, though no technical details are provided.
- Users can **add everyone at the table**, then assign each purchased item to the corresponding person by tapping on people.
- Finally, it generates **a shared bill-splitting result** and supports follow-up settlement flows such as “someone shared a bill split with you” or “someone is requesting payment.”

## Results
- The text **does not provide any quantitative experimental results**: no dataset, accuracy, recall, latency, baseline comparison, or user study figures.
- The strongest concrete product claim is: **"No app needed"**, meaning it can be used without installing an app.
- It also states **"This may take a few seconds"**, implying the scanning/processing time is a few seconds, but no precise value or test conditions are given.
- Another explicit claim is **"It's free forever"**, indicating the product is free permanently, but this is not a research performance metric.

## Link
- [https://snapfair.pages.dev/](https://snapfair.pages.dev/)
