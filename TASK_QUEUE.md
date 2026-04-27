# Genesis Garden — Task Queue

## HIGH PRIORITY

- [ ] Bootstrap project infrastructure
  - Create core state files (CURRENT_STATE, DECISION_LOG, EXPERIMENT_LOG, METRICS, REPORTS dir)
  - Initialize git repo with proper .gitignore
  - Set up cycle report naming convention (cycle-YYYY-MM-DD-HHMMSS.md)
  - Validate SSH connectivity and workspace permissions
  
- [ ] Establish baseline metrics tracking
  - Define core KPIs: tasks completed per cycle, success rate, experiment velocity
  - Create simple metrics collector script (incremental updates to METRICS.md)
  - Add metrics validation (checks that values are numeric and monotonic where expected)
  
- [ ] Design first micro-experiment
  - Pick a simple, self-contained agent behavior to test
  - Define success criteria and measurement method
  - Create experiment scaffold with configurable parameters
  - Document in EXPERIMENT_LOG.md upon completion

## MEDIUM PRIORITY

- [ ] Create task ingestion pipeline
- [ ] Implement decision accountability
- [ ] Build failure recovery protocol

## LOW PRIORITY / MAINTENANCE

- [ ] Improve reporting format
- [ ] Repository hygiene
- [ ] Observability

## BACKLOG

- [ ] Agent self-improvement loop
- [ ] Multi-agent coordination protocol
- [ ] Simulation environment setup
