#!/usr/bin/env python3
# Genesis Garden - Metrics Collector
# Incrementally updates METRICS.md after each cycle.

import re
import sys
from pathlib import Path

WORKSPACE = Path.home() / 'autonomous-sim'
METRICS_FILE = WORKSPACE / 'METRICS.md'

CORE_KPIS = [
    ('Cycles Completed',         r'\| Cycles Completed \| ([0-9N/A]+) \|'),
    ('Tasks Completed',          r'\| Tasks Completed \| ([0-9N/A]+) \|'),
    ('Tasks Failed',             r'\| Tasks Failed \| ([0-9N/A]+) \|'),
    ('Avg Cycle Duration (min)', r'\| Avg Cycle Duration \(min\) \| ([0-9N/A]+) \|'),
    ('Git Commits',              r'\| Git Commits \| ([0-9N/A]+) \|'),
    ('Experiments Run',          r'\| Experiments Run \| ([0-9N/A]+) \|'),
    ('Experiments Successful',   r'\| Experiments Successful \| ([0-9N/A]+) \|'),
    ('Decision Accuracy %',      r'\| Decision Accuracy % \| ([0-9N/A]+) \|'),
]

def parse_value(val):
    if val == 'N/A':
        return None
    try:
        return int(val)
    except ValueError:
        return float(val)

def format_value(val):
    if val is None:
        return 'N/A'
    return str(val)

def increment(metric_name, delta=1):
    content = METRICS_FILE.read_text()
    for name, pattern in CORE_KPIS:
        if name == metric_name:
            match = re.search(pattern, content)
            if not match:
                print(f"ERROR: Could not find metric row for '{name}'")
                sys.exit(1)
            current_val = parse_value(match.group(1))
            if current_val is None:
                print(f"ERROR: Metric '{name}' is N/A — cannot increment")
                sys.exit(1)
            new_val = current_val + delta
            old_cell = f'| {name} | {format_value(current_val)} |'
            new_cell = f'| {name} | {new_val} |'
            new_content = content.replace(old_cell, new_cell, 1)
            METRICS_FILE.write_text(new_content)
            print(f"  {name}: {current_val} -> {new_val}")
            return
    print(f"ERROR: Unknown metric '{metric_name}'")
    sys.exit(1)

def sync_git_commits():
    import subprocess
    result = subprocess.run(
        ['git', 'log', '--oneline'],
        cwd=WORKSPACE,
        capture_output=True,
        text=True
    )
    count = len([l for l in result.stdout.splitlines() if l.strip()])
    content = METRICS_FILE.read_text()
    new_content = re.sub(
        r'(\| Git Commits \| )[0-9N/A]+( \|)',
        f'\\g<1>{count}\\g<2>',
        content
    )
    METRICS_FILE.write_text(new_content)
    print(f"  Git Commits synchronized: {count}")

def main():
    if len(sys.argv) < 2:
        print("Usage: metrics.py increment <metric_name> [delta]")
        print("       metrics.py sync-git")
        sys.exit(1)
    
    action = sys.argv[1]
    if action == 'increment':
        if len(sys.argv) < 3:
            print("ERROR: metric name required")
            sys.exit(1)
        increment(sys.argv[2], int(sys.argv[3]) if len(sys.argv) > 3 else 1)
    elif action == 'sync-git':
        sync_git_commits()
    else:
        print(f"ERROR: Unknown action '{action}'")
        sys.exit(1)

if __name__ == '__main__':
    main()
