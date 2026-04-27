# Genesis Garden — Decision Log

---

## Recent Decisions

### D-2026-04-27-01 — Workspace Location Selection
- **Date:** 2026-04-27
- **Context:** Original path /srv/hermes-lab/autonomous-sim was not writable.
- **Decision:** Use ~/autonomous-sim as workspace.
- **Alternatives:** /opt, /var (require sudo), ~/projects (less discoverable)
- **Rationale:** User-writable, semantically clear, immediately available.
- **Expected Outcome:** Fast bootstrapping without permission issues.
- **Actual Outcome:** Workspace created successfully. Git initialized. No permission errors.
- **Status:** Successful
