---
source: hn
url: https://baweaver.com/writing/2026/06/05/rails-sharp-parts-lock-is-not-a-mutex/
published_at: '2026-06-13T22:31:22'
authors:
- mooreds
topics:
- rails
- database-locking
- transactions
- concurrency-control
- data-integrity
relevance_score: 0.71
run_id: materialize-outputs
language_code: en
---

# Rails: The Sharp Parts. Lock Is Not a Mutex

## Summary
This article explains why Rails locks are easy to misuse and how that leads to lost updates, deadlocks, stale reads, and other production races. Its main point is that the invariant should drive the design, and the database should enforce it when possible.

## Problem
- Rails `lock`, `lock!`, and `with_lock` look simple, but they depend on transaction scope, adapter behavior, isolation level, and query shape.
- Many app invariants are larger than one row, so a row lock alone cannot protect them.
- Hidden writes, background jobs, admin scripts, and console changes can bypass application-level locking rules.

## Approach
- Start from the invariant, then choose the smallest mechanism that enforces it: row lock, unique index, `CHECK`, `SERIALIZABLE`, advisory lock, or ordered locking.
- Use `with_lock` or an explicit transaction when you need pessimistic row locking, and keep the locked section short.
- Prefer database constraints for single-source-of-truth rules, such as a unique reservation row instead of a mutable flag.
- For sets and counters, lock a parent row, switch to `SERIALIZABLE`, or encode the rule as a constraint.
- Make write paths go through one controlled ingress so callers cannot bypass the rule.

## Results
- No new benchmark numbers are reported in the excerpt.
- It shows that `Seat.lock.find(id)` without a surrounding transaction releases the lock immediately and protects nothing.
- It shows that locking all matching rows can create an unintended queue, while `FOR UPDATE SKIP LOCKED` lets workers claim available rows from a pool.
- It shows that long transactions hold locks across external calls and increase contention; the fix is to move non-database work outside the transaction.
- It shows that deadlocks can appear when rows are locked in different orders, and that sorting IDs before locking reduces that risk.
- It shows that write skew and phantom reads can break invariants like “at least one admin on call” or “no more than 100 reservations per event,” and that `SERIALIZABLE`, a locked parent row, or a constraint can fix them.

## Link
- [https://baweaver.com/writing/2026/06/05/rails-sharp-parts-lock-is-not-a-mutex/](https://baweaver.com/writing/2026/06/05/rails-sharp-parts-lock-is-not-a-mutex/)
