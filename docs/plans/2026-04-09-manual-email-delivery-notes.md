# Manual Email Delivery Notes

Date: 2026-04-09

Status: implemented for v1 manual trend email delivery

## Purpose

Record the current design direction for adding an email delivery surface to
Recoleta without leaving the discussion only in chat context.

This note captures the conclusions reached so far, the constraints that shaped
them, and the implementation gates that were resolved while landing `v1`.

## Implementation Snapshot

The current repository implementation matches the narrow `v1` plan:

- `run email preview|send` and `fleet run email preview|send` exist.
- `v1` only supports trend email, not ideas or subscribe flows.
- transport is fixed to Resend via the official Python SDK.
- site build writes a private email link-map companion artifact.
- send is blocked unless the primary public trend URL is reachable.
- delivery persistence remains dedupe-oriented on top of `TrendDelivery`;
  `v1` does not preserve multi-version send history for updated trends.
- batch semantics are recipient-batch oriented: mixed partially-sent state
  requires `--force-batch`.

## Scope of the Current Proposal

The current direction is intentionally narrow.

- Do not build a subscription system yet.
- Do not add site-side email capture forms yet.
- Do not introduce a permanently running email backend yet.
- Treat email as a manually triggered delivery surface, closer to `deploy` than
  to a user-facing newsletter product.

That means the first design target is:

- operator-configured sender identity
- operator-configured recipient list
- manual preview/send command
- idempotent behavior so the same content is not sent twice by accident

## Constraints From the Existing Architecture

Recoleta already has a strong output contract:

- canonical human-readable output is markdown
- richer surfaces are derived from markdown and adjacent presentation sidecars
- the public site is a derived static export
- Telegram delivery already models a delivery channel with persisted send state

Relevant current code paths and documents include:

- `recoleta/presentation.py`
- `recoleta/site.py`
- `recoleta/site_pages.py`
- `recoleta/site_presentation.py`
- `recoleta/pipeline/publish_runtime.py`
- `recoleta/pipeline/trends_stage.py`
- `recoleta/models.py`
- `recoleta/storage/deliveries.py`
- `docs/design/outputs.md`

Two architectural implications matter most:

1. Email should not invent a new primary content source.

The email renderer should consume the same derived projection contract already
used by site and other reader-facing outputs. In practice that means trend and
idea `*.presentation.json` sidecars are the most stable content contract to
reuse.

2. Email should not depend on live site rendering or browser-only HTML.

The current site and PDF layers share some rendering helpers, but those HTML
structures are optimized for browsers or PDF generation, not for email
clients. Email needs its own renderer with a stricter, more compatible layout.

## Main Design Conclusions

### 1. Email is not `subscribe` in v1

The current proposal is not a newsletter product.

It is an operator-triggered delivery workflow with fixed recipients configured
in runtime settings.

This avoids a large amount of unrelated complexity:

- subscriber storage
- double opt-in
- unsubscribe handling
- bounce/complaint processing
- site-side POST handling on a static deployment

Those may become relevant later, but they should not block a first useful
email surface.

### 2. Email should be site-first, not source-first

The preferred link target for email is the public site.

This means:

- the main CTA should open the trend detail page on the public site
- secondary navigation should link to public site indexes or topic pages
- evidence links should prefer public site item/detail pages when those exist
- evidence links may fall back to the original source URL when no public item
  page exists

This keeps the email aligned with the intended reader-facing surface instead of
dropping readers into raw markdown files or upstream source material too early.

For v1, this also implies a hard dependency on site output:

- `run email send` should refuse to run unless the selected trend page can be
  resolved to a public site URL
- primary and secondary CTA links should be treated as send blockers if they
  are missing or not yet deployed
- evidence link fallback is acceptable, but only for supporting links, not for
  the main trend destination

### 3. Email should reuse the site design language, not the site HTML

The current static site has an established design language:

- deep blue hero surface
- cool light background and card stack
- serif display headings
- pill/meta panel chrome
- dense but calm research-oriented hierarchy

The email should visually align with that language, but it should not try to
send the existing site page HTML directly.

Reasons:

- email clients strip or break large parts of normal web CSS
- sticky headers, navigation chrome, and richer page layout do not belong in
  email
- email needs a single-column layout and much stricter HTML

The right approach is:

- preserve the same visual tone
- preserve the same content hierarchy
- re-render that hierarchy through an email-safe template

### 4. The content contract should come from presentation sidecars

For trends, the current sidecar contract is already close to what email needs:

- `title`
- `overview`
- `clusters[]`
- cluster `evidence[]`

For ideas, the analogous structure is:

- `title`
- `summary`
- `ideas[]`
- idea `evidence[]`

This is preferable to rendering from arbitrary markdown or from site HTML
because it is already normalized for downstream reading surfaces.

### 5. Start with one trend per email

The first email surface should most likely be:

- one selected trend document
- one rendered email batch
- one send attempt across the configured recipient set

This is simpler than a multi-document digest and matches the existing delivery
model better.

The current repository already has useful delivery primitives, but they are not
yet a perfect match for email semantics. In particular, the existing
`TrendDelivery` schema is good enough for dedupe-oriented current-state
tracking, but not for preserving a full history of repeated sends for updated
versions of the same trend.

A later digest surface can still be added, but it should be treated as a
distinct design with its own selection rules and content hash semantics.

## Proposed Email Shape

The current preferred shape is a short research brief, not a full site page.

Suggested layout:

1. Preheader
   A short excerpt derived from the overview.

2. Hero block
   Include instance, granularity, period, and the trend title.

3. Meta row
   Include a few compact fields such as window, topics, language, and
   instance.

4. Overview card
   The main summary prose.

5. Cluster cards
   Usually 2 to 4 clusters.

6. Evidence links
   Keep only the strongest few evidence entries per cluster.

7. Footer CTA row
   Link back to the public site.

The desired tone is:

- editorial, not transactional
- visually aligned with the public site
- compact enough to scan in an inbox
- still useful when viewed as plain HTML in restrictive mail clients

## Link Strategy

The link policy should be explicit rather than ad hoc.

### Primary links

- trend title -> trend detail page on the public site
- hero CTA -> trend detail page on the public site
- footer main CTA -> trend detail page on the public site

### Secondary links

- `Open all trends` -> trends index on the public site
- topic pills or topic CTA -> topic page on the public site

### Evidence links

For each evidence entry:

- prefer the public site item/detail page if one exists
- otherwise fall back to the underlying canonical/source URL

### Language behavior

When multilingual site output exists, email should link directly to the
resolved language-specific page rather than relying on the site root redirect.

That avoids ambiguous routing and makes email links stable even when the root
redirect behavior changes.

## Public Link Contract In v1

Public link resolution is explicit in the landed implementation.

The site build now writes a private companion artifact beside the site root:

- `.<site_output_dir.name>-email-links.json`
- with the default site output path `MARKDOWN_OUTPUT_DIR/site`, that becomes
  `MARKDOWN_OUTPUT_DIR/.site-email-links.json`

That artifact records:

- absolute source markdown path -> public relative detail page path
- topic slug -> public relative topic page path
- per-language topic page mappings when multilingual output exists

`run email preview` requires that artifact to exist.

`run email send` adds two more hard checks:

1. `email.public_site_url` must be configured
2. the selected primary trend page under that base URL must be publicly
   reachable before send is allowed

This keeps the main trend CTA site-first without guessing URLs from markdown
paths or silently downgrading to source links.

## Required Configuration Direction

The landed implementation uses a dedicated email config section rather than
folding email into `publish_targets`.

Implemented shape:

```yaml
email:
  public_site_url: "https://example.github.io/recoleta"
  from_email: "recoleta@example.com"
  from_name: "Recoleta"
  to:
    - "operator@example.com"
  granularity: "week"
  language_code: "en"
  max_clusters: 3
  max_evidence_per_cluster: 2
  subject_prefix: "[Recoleta]"
```

Related secret:

- `RECOLETA_RESEND_API_KEY` is env-only and rejected if it appears in a config
  file

Important observations that still hold:

- `public_site_url` should be explicit configuration
- email should not guess public URLs from local export paths
- instance-level overrides may make sense in the current instance-first runtime
- v1 should use a single transport choice rather than an abstract provider
  plugin system
- provider API keys should be treated as secrets and loaded from environment
  variables rather than committed config files

## Transport and Provider Direction

The recommended v1 transport is the Resend HTTP API.

Reasons:

- it is a modern API-first email product rather than a lowest-common-
  denominator SMTP surface
- it has an official Python SDK and a straightforward API-key authentication
  model
- it supports batch sending directly, which fits the current batch-oriented send
  semantics
- it supports request idempotency keys, which can complement Recoleta's own
  dedupe logic
- it does not require a production-approval or sandbox escape workflow before
  first real sends

The recommended v1 transport boundary is:

- `transport = resend` only
- authenticate with a single env-only API key
- use the provider's batch API for normal send operations
- pass an explicit provider idempotency key on each batch request
- treat SMTP and alternate HTTP providers as out of scope for the first
  implementation

Retry behavior should be modest and explicit:

- retry only transient network or 5xx-class provider failures
- do not retry content or recipient validation errors
- keep the retry policy narrower than the Telegram sender until real failure
  data justifies expansion
- map provider request failures into a small normalized error surface instead of
  mirroring the entire upstream response model

Error handling should also be conservative:

- never store API keys
- never log full provider request bodies with recipient lists by default
- sanitize recipient addresses and auth material in persisted error text
- persist only the minimum message/delivery metadata needed for operator audit

### Why Resend first

As of 2026-04-10, Resend is the best fit for the current project goals.

Reference pages reviewed for this comparison:

- [Resend pricing](https://resend.com/pricing)
- [Resend Python sending guide](https://resend.com/docs/send-with-python)
- [Resend batch send API](https://resend.com/docs/api-reference/emails/send-batch-emails)
- [Resend domain verification overview](https://resend.com/docs/dashboard/domains/introduction)
- [Resend production approval note](https://resend.com/docs/knowledge-base/does-resend-require-production-approval)

- Free plan: `$0/mo`, `3,000 emails/mo`, `100 emails/day`
- Setup: API key plus domain verification
- Batch support: up to `100` emails in one API call
- Production access: available immediately, including on free accounts

This combination fits the current goals well:

- modern API-first integration
- low setup friction
- enough free capacity for early manual batches
- native batch and idempotency support

### Why not SMTP first

SMTP remains useful as a compatibility transport, but it is not the preferred
modern default here.

Compared with an API-first provider, SMTP has weaker ergonomics for:

- request-level idempotency
- normalized delivery metadata
- structured failure handling
- explicit batch send semantics

### Why Postmark is the main fallback candidate

Postmark remains a strong fallback if Resend proves limiting.

As of 2026-04-10, its main tradeoff is not integration complexity but free-tier
headroom:

Reference pages reviewed for this comparison:

- [Postmark pricing](https://postmarkapp.com/pricing/)
- [Postmark send-email API guide](https://postmarkapp.com/developer/user-guide/send-email-with-api)

- Free plan: `$0/mo`, `100 emails/month`
- Paid entry: `$15/mo` for `10,000 emails/month`
- Setup: server token plus sender signature or domain verification

Postmark is operationally simple and mature, but its free tier is much tighter
than Resend's for exploratory internal use.

### Why not SES or SendGrid for v1

SES and SendGrid are both credible products, but they are not the best fit for
this first slice.

Reference pages reviewed for this comparison:

- [Amazon SES pricing](https://aws.amazon.com/ses/pricing/)
- [Amazon SES verified identities](https://docs.aws.amazon.com/ses/latest/dg/verify-addresses-and-domains.html)
- [Amazon SES production access](https://docs.aws.amazon.com/ses/latest/dg/request-production-access.html)
- [SendGrid pricing](https://sendgrid.com/en-us/pricing)
- [SendGrid sender verification](https://www.twilio.com/docs/sendgrid/ui/sending-email/sender-verification)

- SES is powerful and inexpensive at scale, but configuration is heavier and
  operationally more infrastructure-shaped than product-shaped.
- SendGrid is widely used, but the free experience is trial-oriented rather
  than a long-lived low-volume developer tier.

They can be revisited later if scale, compliance, or vendor constraints change.

## CLI and Workflow Direction

The current design leans toward a manual run command rather than automatic
publish-time delivery.

Suggested command shape:

- `recoleta run email preview`
- `recoleta run email send`

The preview command should generate email artifacts without sending. The send
command should independently re-render, check send preconditions, send the
configured batch, and persist delivery state.

This keeps email conceptually aligned with `run deploy`:

- explicit operator action
- deliberate output generation
- no automatic fan-out during ordinary publish flows

For v1, `run email send` should have hard preconditions:

- a selected trend was resolved from config or explicit CLI arguments
- site-link mapping for that selected trend is available
- `public_site_url` is configured
- the trend detail page and other required public CTA destinations are
  reachable
- the batch is in a clean state rather than a mixed partial-success state

If those preconditions are not met, send should refuse rather than silently
downgrade to a weaker link strategy.

## Idempotency Direction

Idempotency is a core requirement for this feature.

The desired behavior is:

- do not send the same rendered content to the same recipient twice
- preserve enough state to retry a fully failed batch cleanly
- explicitly treat “trend updated and re-sent later” history as out of scope
  for v1

The existing delivery model suggests the right baseline:

- `channel = email`
- `destination = recipient-specific identity` for persisted delivery rows
- `content_hash = email payload identity for the chosen trend/surface`

For trend-level email, the closest precedent is the existing trend delivery
record, but the current schema shape is only sufficient for dedupe-oriented
current-state tracking. It is not sufficient for preserving multiple sent
versions of the same trend over time because the uniqueness boundary today is
`doc_id + channel + destination` and later sends overwrite stored
`content_hash` and `message_id`.

That leads to an explicit v1 narrowing:

- v1 supports dedupe-only semantics
- v1 does not promise multi-version send history for updated trends
- if future product needs require repeated sends of updated trend content, that
  should be treated as a schema change rather than assumed to “already fit”

## Preview Artifacts

Even for a manual workflow, preview artifacts are worth treating as first-class
outputs.

Suggested preview bundle contents:

- `body.html`
- `body.txt`
- `manifest.json`
- optional small screenshot or browser preview later

This gives the operator a chance to inspect:

- visual structure
- resolved links
- selected trend metadata
- content hash used for idempotency

Preview is advisory, not a security boundary.

For v1:

- `run email preview` does not become a required input to `run email send`
- `run email send` re-renders from the current canonical inputs at send time
- send should emit its own manifest and computed content hash for operator audit
- a future `send --from-preview` mode can be considered later if a stricter
  approval chain becomes necessary

## What Should Not Be Done in v1

The current design explicitly avoids these choices:

- sending the public site HTML directly as email
- embedding the full site navigation in email
- building a subscriber database
- using a static-site form workflow as a prerequisite
- mixing public site links and raw markdown links inconsistently
- starting with a many-trend digest before single-trend delivery semantics are
  clear
- pretending the current site manifest already provides stable email link
  mapping when it does not
- pretending the current trend delivery schema already preserves multi-version
  email send history when it does not
- implementing a transport plugin matrix before one concrete provider works
- silently retrying a partially successful batch on a per-recipient basis

## Questions Resolved In v1

The initial design discussion left a handful of open questions. The current
repository implementation resolves them like this:

### 1. Selection semantics

- default to the latest eligible trend for the configured `granularity`
- respect `email.language_code` when set; otherwise use the settings' default
  site language
- allow explicit period selection through `--date`
- treat the selected trend as one batch candidate for the configured recipient
  set

### 2. Config placement

- keep one shared `email:` schema in settings
- allow instance-first workflows to override it through child configs
- keep fleet email commands targeted at exactly one child instance per run

### 3. Ideas support

- still out of scope for `v1`
- trend email is the only shipped manual email surface

### 4. Recipient tracking granularity

- persist trend delivery rows per recipient for auditability
- keep selection and resend semantics batch-oriented
- reject mixed partially sent batches unless the operator passes
  `--force-batch`

### 5. Public site page resolution

- use the private site email link-map artifact as the only path resolver
- compose public absolute URLs from `email.public_site_url` plus resolved
  relative page paths
- require the primary trend page to be reachable before send is allowed
- allow evidence links to fall back to source URLs when no public item page
  exists

### 6. Transport/provider choice

- support Resend only in `v1`
- use the official Python SDK batch path
- authenticate with one env-only API key
- keep alternate providers out of scope

### 7. Preview-to-send contract

- treat preview as advisory only
- `run email send` re-renders from current canonical inputs
- preview and send each write their own manifest and content hash

## Delivered v1 Slice

The repository now ships this narrow slice:

1. Explicit `email:` configuration including `public_site_url`.
2. One env-only `RECOLETA_RESEND_API_KEY` secret.
3. A dedicated email-safe renderer for one selected trend document.
4. Manual `run email preview` and `fleet run email preview`.
5. Site-backed email link-map artifacts for single-instance and fleet site
   builds.
6. Manual `run email send` and `fleet run email send` with public-site
   reachability checks.
7. Dedupe-only send state on top of `TrendDelivery`.
8. Batch-oriented resend rules with explicit mixed-state refusal.
9. Site-first CTA and evidence link resolution.
10. `fleet run email preview|send` support `--site-output-dir` when the
    aggregate fleet site was built into a custom location.

This is still intentionally narrow, but it is no longer only a proposal. It is
the current `v1` manual trend email surface in the repository.
