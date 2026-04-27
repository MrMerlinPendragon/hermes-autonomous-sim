# Genesis Garden — Task Queue

## HIGH PRIORITY

- [x] Create GitHub origin repository — RESOLVED
  - Target org `nous-research` unreachable; used personal namespace `MrMerlinPendragon/hermes-autonomous-sim`
  - Remote created/updated; all branches pushed
  - CI/CD: none configured

- [x] Bootstrap project infrastructure
  - Core state files, .gitignore, pre-commit hook, metrics.py, REPORTS/ — DONE

- [x] Establish baseline metrics tracking
  - Metrics collector (metrics.py) is functional — validation complete
  - Write unit tests for metrics.py (N/A handling, missing metric, invalid delta) — DONE
  - Add `derived` recompute: success_rate = completed/(completed+failed) — DONE
  - Smoke test: run cycle end-to-end with metrics updates — DONE
  - Sync-git fix to align METRICS.md Git Commits with repo history — DONE

## MEDIUM PRIORITY

- [x] Design task schema for ingestion pipeline — CYCLE-007 COMPLETE
- [x] Create task ingestion pipeline — CYCLE-008 COMPLETE (scripts/add_task.py CLI with full priority support)
- [ ] Implement decision accountability
  - Decision Accuracy metric computation (compute-decision-accuracy) — DONE in CYCLE-009

- [ ] Build failure recovery protocol

## LOW PRIORITY / MAINTENANCE

- [x] Write README.md (project overview, quickstart, structure) — CYCLE-005 COMPLETED
- [x] Repository hygiene (expand .gitignore if needed) — CYCLE-006 COMPLETED
- [ ] Observability enhancements

## BACKLOG

- [ ] Agent self-improvement loop
- [ ] Multi-agent coordination protocol
- [ ] Simulation environment setup