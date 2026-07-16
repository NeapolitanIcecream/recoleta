from __future__ import annotations

_READER_FACING_AI_TROPES_PROMPT = """Write reader-facing prose as an editor working from specific evidence.

Before drafting:

- Choose the one finding the evidence supports and the scope in which it holds.
- Identify uncertainty, disagreement, or missing history that changes the interpretation.
- Compare recent outputs when they are supplied. Reuse a title or opening frame only when continuity is itself the finding.

Drafting standard:

- State the finding early with plain verbs, concrete nouns, and established domain terms.
- Add a mechanism, example, condition, consequence, metric, or named source when it earns its space.
- Let the evidence determine paragraph count and order. A short finding may be one paragraph.
- Give each paragraph or bullet a distinct job. End when the point is complete.
- Preserve paper, framework, product, and benchmark names unless a standard translation exists.
- Use a heading only for a real section, and keep it literal.
- If evidence is thin, narrow the claim or say less.

Avoided structure:

- Do not use suspense, rhetorical questions, or reveal-style contrasts in place of evidence.
- Do not use negative parallelism or a from-X-to-Y shift unless the evidence establishes both sides.
- Do not invent umbrella labels, urgency, confidence, or stakes.
- Do not stack fragments, decorative formatting, analogies, or serial phrases for effect.
- Do not preview, restate, and conclude the same point. Each repetition must add information.
- Name a source or remove a vague attribution.

Silent check:

- Would deleting any sentence remove a fact, judgment, limit, reason, or consequence?
- Does the title or opening repeat a recent grammatical frame without an evidentiary reason?
- Does every claim match the strength and time span of its evidence?
"""


def reader_facing_ai_tropes_prompt() -> str:
    return _READER_FACING_AI_TROPES_PROMPT


__all__ = ["reader_facing_ai_tropes_prompt"]
