---
source: hn
url: https://syndicode.com/blog/csp-failure-rails/
published_at: '2026-03-12T23:58:21'
authors:
- lglazyeva
topics:
- content-security-policy
- rails
- activeadmin
- web-security
- csp-nonce
relevance_score: 0.01
run_id: materialize-outputs
language_code: en
---

# How a subtle CSP misconfiguration broke our admin panel and how we fixed it

## Summary
This article analyzes an issue in a Rails + ActiveAdmin admin backend where an overly strict CSP configuration without nonce enabled caused inline scripts to be silently blocked by the browser, breaking form interactions. The author presents a CSP nonce-based fix that restores functionality without weakening the security policy.

## Problem
- The problem addressed is that a strict `Content-Security-Policy: script-src 'self'` without configured nonce/hash prevents the inline JavaScript relied on by ActiveAdmin from executing, causing key admin workflows such as dynamic forms, validation, and button enabling to fail.
- This matters because there is **no obvious UI breakage on the surface**; only a CSP refusal message appears in the console, making it easy to slip past routine QA and automated checks while directly affecting production admin operations.
- Fundamentally, this is a functional failure caused by a case where the “security policy is correct, but the implementation is incomplete”: the CSP meant to prevent XSS instead blocks trusted server-generated scripts.

## Approach
- The core method is simple: **generate a random nonce for each request, and include it both in the CSP response header and in the allowed inline `<script>` tags**; the browser will only execute scripts whose nonce matches.
- The author first identified the issue by checking the browser console for CSP refusal messages, inspecting response headers to confirm `script-src 'self'`, and then reviewing the page source to verify that ActiveAdmin was still outputting inline scripts.
- They then evaluated four options: moving all JS out to external files, adding `unsafe-inline`, using a hash for each script, and using nonce; they ultimately chose nonce because it offered the best balance among security, maintainability, and implementation cost.
- The Rails implementation included configuring `content_security_policy_nonce_generator = ->(_request) { SecureRandom.base64(16) }`, applying the nonce to `script-src`, exposing `content_security_policy_nonce` to the view through the controller, and adding `nonce: csp_nonce` to ActiveAdmin `script` blocks.
- Beyond the fix itself, the team also added end-to-end tests for CSP silent failures, a security checklist, and implementation documentation to reduce future regressions.

## Results
- The article **does not provide formal benchmarks or experimental data**, nor does it include quantitative metrics such as dataset details, error-rate reduction percentages, or latency changes.
- The most specific technical result described is that the CSP response header changed from only `script-src 'self'` to one including `script-src 'self' 'nonce-xyz…'`, while the page’s inline scripts received a matching `nonce="xyz…"` attribute.
- After the fix, the author says ActiveAdmin’s dynamic form behavior was “fully restored,” including dynamic field show/hide behavior, form validation triggering, and button state recovery.
- Compared with the alternatives, the nonce approach avoided the security weakening introduced by `unsafe-inline` and also avoided the high development cost of refactoring “dozens” of small inline scripts into external files.
- An additional outcome was process-related: the team introduced lightweight E2E checks for CSP regressions and documented the nonce-based implementation as a standard Rails/ActiveAdmin practice.

## Link
- [https://syndicode.com/blog/csp-failure-rails/](https://syndicode.com/blog/csp-failure-rails/)
