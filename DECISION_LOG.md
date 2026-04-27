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
- **Outcome:** IN PROGRESS — blocker recorded in CURRENT_STATE; TASK_QUEUE amended with explicit remote-creation task. Cycle completed successfully without remote.
