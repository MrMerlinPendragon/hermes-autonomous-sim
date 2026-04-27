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

- [ ] Create task ingestion pipeline
- [ ] Implement decision accountability
- [ ] Build failure recovery protocol

## LOW PRIORITY / MAINTENANCE

- [ ] Write README.md (project overview, quickstart, structure)
- [ ] Repository hygiene (expand .gitignore if needed)
- [ ] Observability enhancements

## BACKLOG

- [ ] Agent self-improvement loop
- [ ] Multi-agent coordination protocol
- [ ] Simulation environment setup
