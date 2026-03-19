---
source: hn
url: https://news.ycombinator.com/item?id=47282422
published_at: '2026-03-06T23:21:27'
authors:
- marstyl
topics:
- speech-to-text
- language-learning
- podcast-transcription
- consumer-tool
relevance_score: 0.16
run_id: materialize-outputs
language_code: en
---

# I built a tool to transcribe podcasts after struggling to learn languages

## Summary
This is a podcast transcription tool aimed at language learners, developed by the author after struggling to understand French/Russian podcasts. It automatically converts a single-episode link from Spotify or Apple Podcasts into text, helping users listen while reading to lower the comprehension barrier.

## Problem
- Language learners often cannot clearly understand podcast content because of connected speech, fast speaking pace, and words blending together, which can seriously undermine motivation to keep learning.
- Existing manual methods such as repeatedly pausing, replaying, and then using translation tools are cumbersome and inefficient.
- The lack of a reviewable transcript for podcast content makes “giving up when you can’t understand” a common outcome.

## Approach
- The author built a freemium tool called **PodcastsToText**. Users only need to paste a single-episode podcast link from Spotify or Apple Podcasts to trigger automatic transcription.
- The core mechanism is very straightforward: convert the audio program into a text transcript so users can look back, reread, and compare against the content when they cannot hear it clearly.
- The product design focuses on the language-learning scenario and does not emphasize complex features; instead, it addresses the core pain point of “not understanding and being unable to review.”
- The free tier supports automatic transcription of up to **30 minutes**, lowering the barrier to first use.

## Results
- The provided text includes **no paper-style experiments, benchmark data, or quantitative evaluation results**, so accuracy, WER, dataset comparisons, or relative baseline improvements cannot be reported.
- The most specific product capability confirmed in the text is support for automatic transcription after pasting a link from **Spotify** or **Apple Podcasts**.
- The free usage allowance is up to **30 minutes** per transcription or episode.
- The author’s core claim is that with a transcript, users can reduce the frustration of frequent pausing/replaying caused by not hearing clearly and shift their attention toward comprehension and language internalization; however, this claim is not accompanied by quantitative evidence.

## Link
- [https://news.ycombinator.com/item?id=47282422](https://news.ycombinator.com/item?id=47282422)
