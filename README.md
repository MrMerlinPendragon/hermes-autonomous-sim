# Genesis Garden

> Autonomous AI Life Simulation — Hermes Prime Orchestration

**Status:** Active (Cycle 4 complete — remote operational)
**Workspace:** `~/autonomous-sim`
**Orchestrator:** Hermes Prime (Hermes Agent)

---

## Overview

Genesis Garden is an autonomous AI life simulation project where Hermes Prime orchestrates self-improving cycles of task execution, metrics tracking, and decision logging. The system runs as a tick-based autonomous loop — each cycle selects a task, executes it, validates the outcome, updates state, and commits progress.

This is a **phase-gated** project following an evidence-first workflow. Every cycle produces durable artifacts: updated metrics, decision logs, cycle reports, and git commits.

---

## Quickstart

### Run the metrics collector

```bash
cd ~/autonomous-sim

# Increment a core metric
python3 metrics.py increment "Cycles Completed"

# Sync Git Commits counter with actual repo history
python3 metrics.py sync-git

# Recompute derived metrics (Success Rate, etc.)
python3 metrics.py recompute-derived
```

### Run tests

```bash
cd ~/autonomous-sim
python3 -m pytest test_metrics.py -v
# or directly:
python3 test_metrics.py
```

All tests must pass before committing (pre-commit hook enforced).

### View recent cycle reports

```bash
ls -lt ~/autonomous-sim/REPORTS/
cat ~/autonomous-sim/REPORTS/cycle-*.md
```

---

## Project Structure

```
autonomous-sim/
├── CURRENT_STATE.md       # Snapshot of system status, cycle history, blockers
├── TASK_QUEUE.md          # Prioritized backlog (HIGH / MEDIUM / LOW)
├── DECISION_LOG.md        # Rationale for key decisions (D-YYYY-MM-DD-NNN format)
├── EXPERIMENT_LOG.md      # Log of experiments run and outcomes
├── METRICS.md             # Live KPI dashboard (auto-updated by metrics.py)
├── metrics.py             # Metrics collector CLI: increment / sync-git / recompute-derived
├── test_metrics.py        # Unit tests for metrics.py (8 tests, all passing)
├── .gitignore             # Python/OS/project-specific ignores
├── .git/hooks/pre-commit  # Validates state file integrity before commits
├── REPORTS/               # Cycle reports: cycle-YYYY-MM-DD-HHMMSS.md
└── README.md              # This file
```

---

## Core Metrics

| Metric | Description |
|--------|-------------|
| **Cycles Completed** | Number of autonomous cycles finished |
| **Tasks Completed** | Tasks successfully executed |
| **Tasks Failed** | Tasks that failed (blocks Success Rate) |
| **Git Commits** | Total commits on the current branch (auto-synced) |
| **Experiments Run** | Number of experiments executed |
| **Experiments Successful** | Experiments that succeeded |
| **Decision Accuracy %** | Assessment of decision quality (future) |
| **Success Rate** (derived) | Tasks Completed / (Completed + Failed) |
| **Cycle Velocity** (derived) | Tasks per cycle (future) |

Metrics are updated programmatically via `metrics.py` to ensure consistency.

---

## How a Cycle Works

1. **SSH** to the server and `cd ~/autonomous-sim`
2. **Read state** files (CURRENT_STATE, TASK_QUEUE, DECISION_LOG, EXPERIMENT_LOG, METRICS, latest REPORTS)
3. **Select task** — pick one small, concrete, completable-in-one-tick item
4. **Execute** using terminal/file/execute_code tools, staying inside the workspace
5. **Validate** — run an import test, unit test, or smoke test to confirm it works
6. **Update state** — amend CURRENT_STATE.md, TASK_QUEUE.md, DECISION_LOG.md as needed
7. **Git commit** — `git add`, `git commit` with clear message, `git push origin`
8. **Write cycle report** — 2-5 sentence summary to `REPORTS/cycle-<date>.md`
9. **Signal completion** — response delivered to the configured destination

---

## Task Triage

### HIGH PRIORITY
- Unblockers (infrastructure, integrations, remote access)
- Critical bugs affecting the cycle loop itself
- Foundational pieces without which medium/low tasks cannot proceed

### MEDIUM PRIORITY
- Feature implementations that extend automation capacity
- Decision accountability infrastructure
- Failure recovery protocols
- Task ingestion pipeline

### LOW PRIORITY / MAINTENANCE
- Documentation (README, inline docs)
- Repository hygiene (.gitignore, branch cleanup)
- Observability enhancements

---

## Git Workflow

- **Branch:** `main` (primary integration branch)
- **Remote:** `origin` → `git@github.com:MrMerlinPendragon/hermes-autonomous-sim.git`
- **Pre-commit hook:** Enforces required files present, valid task markers `[ ]`/`[x]`, numeric metrics
- **Commit message format:** `<type>(<scope>): <subject>` — e.g. `feat(metrics): add sync-git`
- Conventional Commits used throughout for automated changelog generation

---

## Development Constraints

- Working directory: strictly within `~/autonomous-sim`
- No `sudo` usage
- No exposure of public services
- No spending money
- No contacting real people
- No committing secrets (SSH keys, tokens)
- After 3 consecutive task failures, record blocker in CURRENT_STATE & TASK_QUEUE, pick fallback

---

## Governance

- **Orchestrator:** Hermes Prime (Hermes Agent running as cron job)
- **Human-in-the-loop:** Phase-gated review only; day-to-day fully autonomous
- **Source of truth:** Files in workspace; GitHub mirror is secondary
- **Phase transitions:** Require evidence accumulation (completed cycles, stable metrics, validated artifacts)

---

## Getting Help

- Read `CURRENT_STATE.md` for latest status and active blockers
- Check `DECISION_LOG.md` for past decision rationales
- Review `REPORTS/` for detailed cycle-by-cycle accounts
- Inspect `metrics.py` for metric definitions and update logic
- Run `test_metrics.py` to validate metrics system integrity

---

*Last updated: 2026-04-27 — baseline established, remote operational, 4 cycles complete*
