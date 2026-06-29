---
source: hn
url: https://footbeen.com/blog/i-built-a-production-app-with-ai-no-developers
published_at: '2026-05-10T22:24:17'
authors:
- dmgmyza
topics:
- ai-coding
- automated-software-production
- human-ai-interaction
- code-intelligence
- software-teams
relevance_score: 0.82
run_id: materialize-outputs
language_code: en
---

# I run a company with 30 engineers. Built this app with AI and none of them

## Summary
A software company founder reports building Footbeen, a production football match-tracking app, in 8 weeks using Claude without engineers, designers, or QA staff. The piece matters for automated software production because it gives concrete delivery claims, failure modes, and workflow changes from one real app build.

## Problem
- The author wanted to test whether AI coding tools can replace a small product team for a real shipped app, since clients are asking why they need five-person teams.
- The product problem was personal: football fans who track attended matches and stadium visits often use notes or spreadsheets, while existing apps are paid, dated, or have poor data quality.
- The business question is staffing: whether one domain-aware senior person with AI can ship more effectively than a larger team with weaker product context.

## Approach
- The author used Claude as the main coding assistant and gave feature requests in plain English, similar to a brief for a senior developer.
- The app stack was React Native with Expo, Supabase for Postgres and Auth, Mapbox, React Query, Vercel, and EAS.
- The human handled product judgment: flow design, error states, performance checks, feature selection, and repeated review of generated code.
- Prompting improved after early failures: the author made requests more specific, set constraints, read generated code before accepting it, and re-prompted when behavior felt wrong.
- The workflow still needed manual diagnosis for production crashes, bad React state patterns, slow database queries, and features that worked technically but gave poor user experience.

## Results
- Week 1 produced a running app with Google and Apple sign-in, a Supabase schema, leagues, clubs, stadiums, matches, a searchable match catalogue, a visited-stadium map, and basic stats.
- A Travel Planner feature was shipped in 1 day, compared with the author’s estimate of a 2-week sprint at his company; it included city and date search, 100 km match discovery, geolocation queries, match cards, and responsive design.
- After 8 weeks, the app claimed 25,000+ stadiums, 1,300+ leagues, 200+ countries, and 1,000,000+ fixtures back to 2010.
- The app shipped on iOS, Android, and web from one codebase, with 650+ SEO pages and 7 language versions of the landing page.
- The author reports 600+ automated tests in CI, Sentry monitoring, and a crash-free rate above 99%.
- The build used $0 spent on developers, designers, or QA, but the evidence is a single founder report with no independent benchmark or controlled comparison.

## Link
- [https://footbeen.com/blog/i-built-a-production-app-with-ai-no-developers](https://footbeen.com/blog/i-built-a-production-app-with-ai-no-developers)
