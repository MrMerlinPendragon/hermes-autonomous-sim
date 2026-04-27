# Genesis Garden — Task Queue

## HIGH PRIORITY

- [ ] Create GitHub origin repository (BLOCKED — push failed without remote)
  - Create repo `nous-research/hermes-autonomous-sim` (GitHub)
  - Or update origin to an existing repo URL
  - Push master branch
  - Verify CI/CD if any

- [x] Bootstrap project infrastructure
  - Core state files, .gitignore, pre-commit hook, metrics.py, REPORTS/ — DONE

- [ ] Establish baseline metrics tracking
  - Metrics collector (metrics.py) is functional — remaining: edge-case validation
  - Write unit tests for metrics.py (N/A handling, missing metric, invalid delta)
  - Add `derived` recompute: success_rate = completed/(completed+failed)
  - Smoke test: run cycle end-to-end with metrics updates

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
