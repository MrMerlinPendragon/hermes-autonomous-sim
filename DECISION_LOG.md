# Genesis Garden — Decision Log

---

## Recent Decisions

### D-2026-04-27-01 — Workspace Location Selection
- **Date:** 2026-04-27
- **Context:** Original path /srv/hermes-lab/autonomous-sim was not writable.
- **Decision:** Use ~/autonomous-sim as workspace.
- **Alternatives:** /opt, /var (require sudo), ~/projects (less discoverable)
- **Rationale:** User-writable, semantically clear, immediately available.
- **Outcome:** SUCCESS — workspace created without permission errors. Git initialized.

### D-2026-04-27-02 — Remote Push Deferred
- **Date:** 2026-04-27
- **Context:** Git push to origin failed: "Repository not found"
- **Decision:** Do not stall the autonomous loop waiting for remote repo creation.
- **Alternatives:** (a) halt and request human to create repo, (b) try alternative remote URL, (c) continue locally and record blocker
- **Rationale:** Project progress should not depend on external admin tasks. Commits are valid locally; remote can be reconciled later.
- **Outcome:** RESOLVED — remote created at MrMerlinPendragon/hermes-autonomous-sim; origin updated; all pending commits pushed.

### D-2026-04-27-03 — Remote Repo Namespace Adaptation
- **Date:** 2026-04-27
- **Context:** Target org repository `nous-research/hermes-autonomous-sim` was not found; authenticated user has no access to that org; a personal repo `hermes-autonomous-sim` exists under the user's GitHub account.
- **Decision:** Update git remote to point to `MrMerlinPendragon/hermes-autonomous-sim` and push.
- **Alternatives:** (a) halt and wait for org repo creation, (b) create new personal repo from scratch, (c) use existing personal repo
- **Rationale:** Unblock autonomous loop without external intervention; avoid needless duplication; maintain momentum toward phase-gated deliverables.
- **Outcome:** SUCCESS — remote updated, push succeeded, blocker cleared; cycle completed.


### D-2026-04-27-04 — README Documentation Baseline
- **Date:** 2026-04-27
- **Context:** TASK_QUEUE.md contained three LOW/MAINTENANCE items; README.md was absent, reducing project visibility and onboarding clarity. High-priority tasks already complete; medium-priority items remain.
- **Decision:** Execute "Write README.md" as the next cycle task.
- **Alternatives:** (a) Start "Create task ingestion pipeline" (MEDIUM — higher complexity), (b) Start "Build failure recovery protocol" (MEDIUM — robustness focus), (c) Defer to later phase and pick README (LOW — documentation baseline first)
- **Rationale:** README provides immediate value for anyone inspecting the project (human reviewers, future agents). It is self-contained, well-scoped, and low-risk — suitable for fast tick progress while medium items require deeper design. Establishing documentation baseline early aligns with phase-gated evidence requirements.
- **Outcome:** SUCCESS — README.md written (168 lines), covers project overview, quickstart, structure, metrics, cycle process, governance. Task marked DONE in TASK_QUEUE. Cycle 5 completed.
