# Maintainer actions

Last verified: 2026-07-27

This file contains the small set of account and approval actions that cannot be
completed safely from the repository. Code, release copy, checks, and routine
channel preparation remain agent-owned.

Never paste a password, recovery code, session cookie, API token, or app
password into a GitHub issue, pull request, or chat. Enter secrets directly in
the named service or a local secret store. Recoleta's PyPI release path uses
short-lived OpenID Connect credentials and does not need a stored PyPI token.

## Required before the package release

Maintainer status: both publisher-configuration tasks below were confirmed
complete on 2026-07-27. The instructions remain as a reproducible account
record. Huldra `0.4.2` and Recoleta `0.7.0` are now published through the
configured workflows.

### 1. Enable Huldra's protected PyPI publisher

GitHub:

1. Open <https://github.com/NeapolitanIcecream/huldra/settings/environments>.
2. Select **New environment**.
3. Name it exactly `pypi`, then select **Configure environment**.
4. If another trusted maintainer is available, add them under **Required
   reviewers**. Do not enable **Prevent self-review** when there is no second
   reviewer, because that would block the release.
5. Under deployment branches and tags, allow protected tags or a `v*` tag
   pattern.

PyPI:

1. Sign in to <https://pypi.org/>.
2. Open **Your projects**, select `huldra-arxiv`, then **Manage** and
   **Publishing**.
3. Add a GitHub Actions trusted publisher with these exact values:

   | Field | Value |
   | --- | --- |
   | Owner | `NeapolitanIcecream` |
   | Repository | `huldra` |
   | Workflow | `publish.yml` |
   | Environment | `pypi` |

4. Confirm that the publisher appears on the project.
5. Tell the release operator only: `Huldra publisher ready`. No credential is
   needed.

PyPI requires the repository owner, repository, workflow filename, and optional
environment to match the workflow identity. The environment is strongly
recommended because it can add a human approval gate:
<https://docs.pypi.org/trusted-publishers/adding-a-publisher/>.

### 2. Reserve Recoleta's first publication path

`recoleta` did not exist on PyPI at the 2026-07-25 API check. Configure this
close to the release because a pending publisher does not reserve the name.

GitHub:

1. Open
   <https://github.com/NeapolitanIcecream/recoleta/settings/environments>.
2. Create the exact environment `pypi`.
3. Apply the same reviewer and `v*` tag policy used for Huldra.

PyPI:

1. Sign in and open the account-level **Publishing** page.
2. Under pending publishers, add a GitHub Actions publisher with:

   | Field | Value |
   | --- | --- |
   | PyPI project name | `recoleta` |
   | Owner | `NeapolitanIcecream` |
   | Repository | `recoleta` |
   | Workflow | `publish.yml` |
   | Environment | `pypi` |

3. Confirm that the pending publisher appears.
4. Tell the release operator only: `Recoleta pending publisher ready`.

The first successful workflow run creates the project and converts the pending
publisher into a normal publisher:
<https://docs.pypi.org/trusted-publishers/creating-a-project-through-oidc/>.

## Required after the first Recoleta release

### 3. Make the container image public

Status: complete without an additional account action. On 2026-07-27,
anonymous registry requests returned HTTP 200 for `0.7.0`, `0.7`, and `latest`;
all three tags resolved to the same verified OCI digest.

The steps below remain as a recovery checklist if a later package is not
public:

1. Open the `recoleta` package under the `NeapolitanIcecream` account's
   **Packages** tab.
2. Select **Package settings**.
3. Confirm that the package is linked to
   `NeapolitanIcecream/recoleta`.
4. Under **Danger Zone**, choose **Change visibility**, then **Public**.
5. Type the package name to confirm.
6. Verify that this works without authentication:

   ```bash
   docker pull ghcr.io/neapolitanicecream/recoleta:latest
   ```

This visibility change is irreversible: GitHub does not allow a public package
to become private again. Public container images can be pulled anonymously:
<https://docs.github.com/en/packages/learn-github-packages/configuring-a-packages-access-control-and-visibility>.

### 4. Enable private vulnerability reports

Status: complete. On 2026-07-27, the repository API enabled private
vulnerability reporting for both Recoleta and Huldra and a separate read
confirmed both settings.

The manual recovery steps are:

1. Open **Settings**.
2. Under **Security**, open **Advanced Security**.
3. Enable **Private vulnerability reporting**.
4. Watch **Security alerts** or confirm that the responsible maintainer receives
   its notifications.

This activates the private route already named in each repository's
`SECURITY.md`:
<https://docs.github.com/en/code-security/how-tos/report-and-fix-vulnerabilities/configure-vulnerability-reporting/configuring-private-vulnerability-reporting-for-a-repository>.

## Visual approval

Review history:

- local candidate `visuals/banner-candidate-a-light.png`;
- local candidate `visuals/banner-candidate-b-dark.png`.

The maintainer preferred Candidate B to Candidate A but raised a concern about
its artistic complexity. “Dark blue” was only the identifier for Candidate B,
not a requested palette.

The maintainer approved the simplified structure on 2026-07-27.

Final visual review covered:

- `visuals/review-round-2/recoleta-banner.png`;
- `visuals/review-round-2/recoleta-social-card.png`;
- `visuals/review-round-2/fleet-proof-board.png`.

These assets use the current live-fleet site tokens. The blue value comes from
the running site, not from an inferred background preference. The maintainer
approved the revised set, including its simplified social-card and proof-board
copy, on 2026-07-27. PR 79 published the stable copies, and the approved
1200 by 630 PNG is now the repository social preview.

Any later visual revision returns to maintainer review before publication.

## Show HN human-authorship gate

Hacker News currently requires every title, submission text, and comment to be
written without AI generation or editing. This is a platform rule, so the agent
cannot perform the writing task that would otherwise be delegated.

The minimum maintainer action is:

1. Use a personal Hacker News account that is eligible to submit Show HN.
2. Read [`show-hn-handoff.md`](./show-hn-handoff.md).
3. Write the title and context by hand from personal experience and verified
   facts.
4. Submit the repository URL and remain available for the discussion.
5. Send the public thread URL to the operator for the launch log and outcome
   checks.

Do not paste text from the handoff into Hacker News. The agent can check facts
and public links but cannot edit the maintainer's Hacker News wording.

## Optional later: Bluesky project account

Bluesky is a public microblogging network built on the open AT Protocol. It had
more than 44 million users as of May 2026, and sign-up requires no invitation:
<https://bsky.social/about/faq>. It is a plausible low-cost place to syndicate a
release and selected public fleet briefs, but it is not required for the first
release and has not yet proved that it can produce Recoleta activations.

If the 28-day pilot is approved:

1. Create a dedicated project account at <https://bsky.app/> rather than using
   a personal account.
2. Choose an available project handle, such as `recoleta.bsky.social`.
3. Use display name `Recoleta` and this profile:

   > Continuously operated research radars for traceable trends, ideas, and
   > living research sites. Automated project updates; replies only when
   > tagged.

4. Link <https://neapolitanicecream.github.io/recoleta/>.
5. Verify the account email and retain recovery access.
6. Do not share the main password. If automation is approved, create an app
   password under **Settings → Advanced → App Passwords** and enter it directly
   into the agreed secret store.
7. Tell the operator that the account and secret location are ready; do not send
   the secret itself.

The automation will self-label the profile as a bot, post only approved project
or fleet material, and like, repost, or reply only when the account is tagged.
Those are Bluesky's documented bot practices:
<https://docs.bsky.app/docs/starter-templates/bots>. Bluesky profiles and posts
are public, and complete deletion across the decentralized network is not
guaranteed:
<https://bsky.social/about/support/tos>.
