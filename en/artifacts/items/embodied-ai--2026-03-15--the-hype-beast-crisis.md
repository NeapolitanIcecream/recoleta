---
source: hn
url: https://excipio.tech/blog/the-hype-beast-crisis/
published_at: '2026-03-15T22:57:03'
authors:
- lvales
topics:
- ai-security-reports
- xss-analysis
- static-code-review
- mattermost
- llm-hype
relevance_score: 0.02
run_id: materialize-outputs
language_code: en
---

# The Hype-Beast Crisis

## Summary
This article is not an academic paper, but a piece of technical commentary and social criticism. By tracing the code, the author argues that a Mattermost XSS report labeled by AI as a “critical vulnerability” is actually not triggerable, and further criticizes the hype culture around AI-generated security reports.

## Problem
- The article addresses the question of whether a Mattermost email-template XSS vulnerability claimed to be **CRITICAL** actually exists, and why incorrect AI security reports can cause real harm.
- This matters because false high-severity vulnerability reports waste maintainers’ time, pollute the vulnerability disclosure process, and can even undermine bug bounty mechanisms, as in the cURL case mentioned in the article.
- More broadly, the author is concerned with the misconceptions caused by AI hype: packaging unverified model output as evidence of “security findings” or “AI outperforming humans.”

## Approach
- The author starts from the Mattermost function `prepareTextForEmail`, pointing out that the seemingly dangerous branch returns unescaped text when Markdown-to-HTML conversion fails.
- Then the author traces the call chain layer by layer: `prepareTextForEmail -> MarkdownToHTML -> goldmark.Convert -> renderer.Render`, examining whether an error can actually occur.
- The core mechanism is very simple: if the underlying `md.Convert()` never returns an error on this path, then the upper-layer “return unescaped text” branch is dead code, and the vulnerability is not exploitable.
- The author analyzes the implementation of `goldmark`’s `Render()` and argues that when `strings.Builder` is wrapped as a `bufio.Writer`, the only possible source of errors would be node rendering functions, and in the current scenario those functions do not return errors.
- The conclusion is therefore that this is a “theoretical issue that might appear if library behavior changes in the future,” but not a currently triggerable real-world vulnerability; while the correct fix should indeed return `escapedText`, the current state does not constitute an actual XSS.

## Results
- The most central technical conclusion in the article is qualitative: the author claims that the error-handling branch in `prepareTextForEmail()` is **“always nil”**, meaning that under the current code path `err` is in practice always `nil`, so the alleged XSS cannot be triggered.
- The layer-by-layer conclusion chain is: `Render()` **never returns an error** → `Convert()` does not error → `MarkdownToHTML()` does not error → the dangerous fallback in `prepareTextForEmail()` is dead code.
- No experimental data, benchmark tests, or standard security metrics are provided; **the article contains no quantitative results**, nor any CVSS, PoC success rate, dataset, or comparative experiments.
- The strongest concrete claim is that this report is not a “critical vulnerability,” and not even a real current vulnerability; at most it is a potential defect that could be exposed only if dependency behavior changes in the future.
- The social-level outcome claim includes that crude AI-generated vulnerability reports have already polluted the security disclosure ecosystem; the author cites cURL shutting down its bug bounty program as a related case, but provides no further numerical evidence.

## Link
- [https://excipio.tech/blog/the-hype-beast-crisis/](https://excipio.tech/blog/the-hype-beast-crisis/)
