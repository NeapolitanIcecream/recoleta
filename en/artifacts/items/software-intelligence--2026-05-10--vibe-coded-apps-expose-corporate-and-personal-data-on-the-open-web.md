---
source: hn
url: https://www.wired.com/story/thousands-of-vibe-coded-apps-expose-corporate-and-personal-data-on-the-open-web/
published_at: '2026-05-10T22:05:48'
authors:
- abdelhousni
topics:
- ai-code-generation
- vibe-coding
- software-security
- data-exposure
- web-app-security
- human-ai-interaction
relevance_score: 0.86
run_id: materialize-outputs
language_code: en
---

# Vibe-Coded Apps Expose Corporate and Personal Data on the Open Web

## Summary
RedAccess found more than 5,000 AI-generated web apps on Lovable, Replit, Base44, and Netlify domains that were publicly reachable with no real access control. The finding matters because employees can publish tools with corporate or personal data outside normal security review.

## Problem
- AI coding platforms let users create and host web apps quickly, often without security training.
- Missing authentication or weak sign-in rules can expose private data to anyone who has or finds the URL.
- Security teams may not know these apps exist, so data can leave approved software development and review processes.

## Approach
- RedAccess searched Google and Bing for Lovable, Replit, Base44, and Netlify-hosted domains with terms likely to reveal AI-built apps.
- The team manually inspected exposed apps to check whether they had authentication, access controls, or private-looking data.
- WIRED reviewed screenshots and verified that several exposed apps were still online.
- RedAccess contacted some apparent app owners; several users confirmed exposure and then secured or removed apps.

## Results
- RedAccess claims it found more than 5,000 publicly accessible AI-coded apps with little or no security.
- About 40% of those apps, close to 2,000, appeared to expose sensitive data.
- Reported exposed data included hospital work assignments with doctor identifiers, ad purchasing records, go-to-market slides, chatbot logs with customer names and contact details, shipping cargo records, sales records, and financial records.
- In some cases, RedAccess says the exposed apps could have allowed administrative access or removal of other administrators.
- RedAccess also reported phishing sites on Lovable that impersonated Bank of America, Costco, FedEx, Trader Joe’s, and McDonald’s.
- The companies disputed parts of the report and pointed to user-controlled visibility settings, but the excerpt says they did not deny that some public apps were accessible on the open web.

## Link
- [https://www.wired.com/story/thousands-of-vibe-coded-apps-expose-corporate-and-personal-data-on-the-open-web/](https://www.wired.com/story/thousands-of-vibe-coded-apps-expose-corporate-and-personal-data-on-the-open-web/)
