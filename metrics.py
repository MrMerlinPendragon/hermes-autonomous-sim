#!/usr/bin/env python3
# Genesis Garden - Metrics Collector
# Incrementally updates METRICS.md after each cycle.
# Supports derived metrics recomputation.

import re
import subprocess
import sys
from pathlib import Path

WORKSPACE = Path.home() / "autonomous-sim"
METRICS_FILE = WORKSPACE / "METRICS.md"
DECISION_LOG_FILE = WORKSPACE / "DECISION_LOG.md"

CORE_KPIS = [
    ("Cycles Completed",         r"\| Cycles Completed \| ([0-9N/A]+) \|"),
    ("Tasks Completed",          r"\| Tasks Completed \| ([0-9N/A]+) \|"),
    ("Tasks Failed",             r"\| Tasks Failed \| ([0-9N/A]+) \|"),
    ("Avg Cycle Duration (min)", r"\| Avg Cycle Duration \(min\) \| ([0-9N/A]+) \|"),
    ("Git Commits",              r"\| Git Commits \| ([0-9N/A]+) \|"),
    ("Experiments Run",          r"\| Experiments Run \| ([0-9N/A]+) \|"),
    ("Experiments Successful",   r"\| Experiments Successful \| ([0-9N/A]+) \|"),
    ("Decision Accuracy %",      r"\| Decision Accuracy % \| ([0-9.]+%|N/A) \|"),
]

DERIVED_METRICS = [
    {
        "name": "Success Rate",
        "calc": lambda completed, failed: (completed / (completed + failed)) * 100 if (completed + failed) > 0 else None,
        "deps": ["Tasks Completed", "Tasks Failed"],
    },
]

def parse_value(val):
    if val == "N/A":
        return None
    try:
        return int(val)
    except ValueError:
        return float(val)

def format_value(val):
    if val is None:
        return "N/A"
    return str(int(val)) if isinstance(val, float) and val.is_integer() else str(val)

def increment(metric_name, delta=1):
    content = METRICS_FILE.read_text()
    for name, pattern in CORE_KPIS:
        if name == metric_name:
            match = re.search(pattern, content)
            if not match:
                print(f"ERROR: Could not find metric row for {name}")
                sys.exit(1)
            current_val = parse_value(match.group(1))
            if current_val is None:
                print(f"ERROR: Metric {name} is N/A — cannot increment")
                sys.exit(1)
            new_val = current_val + delta
            old_cell = f"| {name} | {format_value(current_val)} |"
            new_cell = f"| {name} | {new_val} |"
            new_content = content.replace(old_cell, new_cell, 1)
            METRICS_FILE.write_text(new_content)
            print(f"  {name}: {format_value(current_val)} -> {new_val}")
            return
    print(f"ERROR: Unknown metric {metric_name}")
    sys.exit(1)

def sync_git_commits():
    result = subprocess.run(
        ["git", "log", "--oneline"],
        cwd=WORKSPACE,
        capture_output=True,
        text=True,
    )
    count = len([l for l in result.stdout.splitlines() if l.strip()])
    content = METRICS_FILE.read_text()
    new_content = re.sub(
        r"(\| Git Commits \| )[0-9N/A]+( \|)",
        f"\\g<1>{count}\\g<2>",
        content,
    )
    METRICS_FILE.write_text(new_content)
    print(f"  Git Commits synchronized: {count}")

def recompute_derived():
    content = METRICS_FILE.read_text()
    derived_pat = re.compile(
        r"(## Derived Metrics\n\n\| Metric \| Value \| Calculation \|\n\|[- \|]+\n)"
        r"(?P<rows>(?:\| [^\|]+ \| [^\|]+ \| [^\|]+ \|\n?)*)"
    )
    m = derived_pat.search(content)
    if not m:
        print("ERROR: Could not find Derived Metrics table in METRICS.md")
        sys.exit(1)
    table_header = m.group(1)
    table_body   = m.group("rows") or ""
    table_rows   = [r for r in table_body.splitlines() if r.strip()]

    computed = {}
    for dm in DERIVED_METRICS:
        deps = {}
        for dep_name in dm["deps"]:
            pattern = next((p for n, p in CORE_KPIS if n == dep_name), None)
            match = re.search(pattern, content)
            if not match:
                print(f"ERROR: Could not find {dep_name} in METRICS.md")
                sys.exit(1)
            deps[dep_name] = parse_value(match.group(1))
        raw = dm["calc"](deps["Tasks Completed"], deps["Tasks Failed"])
        computed[dm["name"]] = f"{raw:.1f}%" if raw is not None else "N/A"

    new_rows = []
    for row in table_rows:
        cells = [c.strip() for c in row.strip("|").split("|")]
        if len(cells) >= 3 and cells[0] in computed:
            new_row = f"| {cells[0]} | {computed[cells[0]]} | {cells[2]} |"
            new_rows.append(new_row)
            print(f"  {cells[0]}: recomputed -> {computed[cells[0]]}")
        else:
            new_rows.append(row)

    new_table = table_header + "\n".join(new_rows)
    new_content = content[:m.start()] + new_table + content[m.end():]
    METRICS_FILE.write_text(new_content)

def compute_decision_accuracy():
    """Scan DECISION_LOG.md for decisions with SUCCESS/RESOLVED outcomes and update the metric."""
    if not DECISION_LOG_FILE.exists():
        print("ERROR: DECISION_LOG.md not found")
        sys.exit(1)

    log_content = DECISION_LOG_FILE.read_text()

    # Extract all decision sections by matching ### D-<date> headings
    # Each decision entry starts with heading and ends before next heading
    decision_blocks = re.findall(
        r"(### D-\d{4}-\d{2}-\d{2}-\d{2} .*?)(?=\n### |\Z)",
        log_content,
        re.DOTALL,
    )

    if not decision_blocks:
        print("WARNING: No decision entries found in DECISION_LOG.md")
        # Leave metric as-is
        return

    total = len(decision_blocks)
    positive = 0  # decisions with SUCCESS or RESOLVED outcome

    for block in decision_blocks:
        # Look for Outcome line
        outcome_match = re.search(r"^- \*\*Outcome:\*\* (.+)$", block, re.MULTILINE)
        if outcome_match:
            outcome = outcome_match.group(1).strip()
            if re.search(r"\bSUCCESS\b", outcome, re.IGNORECASE) or re.search(r"\bRESOLVED\b", outcome, re.IGNORECASE):
                positive += 1

    accuracy = (positive / total) * 100 if total > 0 else None
    accuracy_str = f"{accuracy:.1f}%" if accuracy is not None else "N/A"

    # Update METRICS.md
    content = METRICS_FILE.read_text()
    pattern = r"(\| Decision Accuracy % \| )[0-9N/A]+( \|)"
    replacement = f"\\g<1>{accuracy_str}\\g<2>"
    new_content = re.sub(pattern, replacement, content)
    if new_content == content:
        # No substitution happened — metric row missing?
        print("ERROR: Could not find Decision Accuracy % row in METRICS.md")
        sys.exit(1)
    METRICS_FILE.write_text(new_content)
    print(f"  Decision Accuracy %: {accuracy_str} ({positive}/{total} positive outcomes)")

def main():
    if len(sys.argv) < 2:
        print("Usage: metrics.py increment <metric_name> [delta]")
        print("       metrics.py sync-git")
        print("       metrics.py recompute-derived")
        print("       metrics.py compute-decision-accuracy")
        sys.exit(1)
    action = sys.argv[1]
    if action == "increment":
        if len(sys.argv) < 3:
            print("ERROR: metric name required")
            sys.exit(1)
        increment(sys.argv[2], int(sys.argv[3]) if len(sys.argv) > 3 else 1)
    elif action == "sync-git":
        sync_git_commits()
    elif action == "recompute-derived":
        recompute_derived()
    elif action == "compute-decision-accuracy":
        compute_decision_accuracy()
    else:
        print(f"ERROR: Unknown action {action}")
        sys.exit(1)

if __name__ == "__main__":
    main()
