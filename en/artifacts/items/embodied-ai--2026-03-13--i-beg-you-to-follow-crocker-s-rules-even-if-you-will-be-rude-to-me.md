---
source: hn
url: https://lr0.org/blog/p/crocker/
published_at: '2026-03-13T23:14:37'
authors:
- ghd_
topics:
- communication
- crockers-rules
- engineering-culture
- technical-writing
relevance_score: 0.0
run_id: materialize-outputs
language_code: en
---

# I beg you to follow Crocker's Rules, even if you will be rude to me

## Summary
This is not a research paper, but an opinion piece about communication norms that argues for using more direct, lower-noise expression in technical collaboration. The core claim is that “Crocker’s Rules” can reduce social cushioning and communicate information faster and more clearly.

## Problem
- The article discusses the problem that excessive politeness, preemptive apologies, and lengthy preambles in technical teams can bury key information in noise.
- This matters because inefficient communication wastes time, reduces information readability, and weakens the efficiency of debugging, code review, and incident retrospectives.
- The author also points out that too much emotional management and self-justification can hinder direct discussion of the facts themselves.

## Approach
- The core mechanism is simple: adopt **Crocker’s Rules**, meaning that by default the other person permits you to be maximally direct and minimize social polishing, conveying only genuinely useful information.
- State facts via the shortest path, for example changing “there might maybe be a bit of a problem” to “the cache layer adds 400ms overhead on cold-start requests; here is the trace.”
- In incident reports or technical feedback, write only actionable facts, causes, and fix suggestions; if personal emotions, excuses, or background are not actionable, they should not take up space in the main body.
- Through a series of contrasting examples of “bad phrasing vs better phrasing,” the author shows how direct expression improves signal density.

## Results
- The text **does not provide experiments, datasets, or formal quantitative evaluation**, so there are no academic metrics, baselines, or statistically significant results to report.
- The most concrete numerical example is that the author uses “the cache layer causes **400ms overhead** on cold requests” to illustrate how direct expression should include key evidence, but this is only an example, not a research result.
- The article’s strongest claims are that more direct communication is “more useful, faster to read, and more respectful of time,” and that if a team cannot tolerate direct statements about reality, it will struggle to debug complex systems efficiently.
- From the perspective of research contribution, it offers normative claims and practical advice rather than a verifiable new algorithm, model, or empirical breakthrough.

## Link
- [https://lr0.org/blog/p/crocker/](https://lr0.org/blog/p/crocker/)
