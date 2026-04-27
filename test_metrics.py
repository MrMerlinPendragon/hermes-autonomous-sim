#!/usr/bin/env python3
"""metrics.py unit tests — edge cases and smoke tests"""
import sys, os, re
from pathlib import Path

WORKSPACE = Path.home() / "autonomous-sim"
METRICS_FILE = WORKSPACE / "METRICS.md"

CORE_KPIS = [
    ("Cycles Completed",        r"\| Cycles Completed \| ([0-9N/A]+) \|"),
    ("Tasks Completed",         r"\| Tasks Completed \| ([0-9N/A]+) \|"),
    ("Tasks Failed",            r"\| Tasks Failed \| ([0-9N/A]+) \|"),
    ("Avg Cycle Duration (min)",r"\| Avg Cycle Duration \(min\) \| ([0-9N/A]+) \|"),
    ("Git Commits",             r"\| Git Commits \| ([0-9N/A]+) \|"),
    ("Experiments Run",         r"\| Experiments Run \| ([0-9N/A]+) \|"),
    ("Experiments Successful",  r"\| Experiments Successful \| ([0-9N/A]+) \|"),
    ("Decision Accuracy %",     r"\| Decision Accuracy % \| ([0-9N/A]+) \|"),
]

def parse_value(val):
    return None if val == "N/A" else (int(val) if val.isdigit() else float(val))

def format_value(val):
    return "N/A" if val is None else str(val)

def replace_metric(content, name, new_val):
    for label, pattern in CORE_KPIS:
        if label == name:
            m = re.search(pattern, content)
            if not m: raise ValueError(f"Metric row not found: {label}")
            old_val = parse_value(m.group(1))
            old_cell = f"| {label} | {format_value(old_val)} |"
            new_cell = f"| {label} | {new_val} |"
            return content.replace(old_cell, new_cell, 1)
    raise ValueError(f"Unknown metric: {name}")

# Escaped label for inline regex construction
def escaped_label(s):
    return re.escape(s)

# ------- tests -------
PASS, FAIL = 0, 0
def t(name, fn):
    global PASS, FAIL
    try: fn(); print(f"[PASS] {name}"); PASS += 1
    except AssertionError as e: print(f"[FAIL] {name}: {e}"); FAIL += 1
    except Exception as e: print(f"[ERR ] {name}: {e}"); FAIL += 1

def test_regex_matches_template():
    content = METRICS_FILE.read_text()
    for label, _ in CORE_KPIS:
        pat = rf"\| {escaped_label(label)} \| [0-9N/A]+ \|"
        assert re.search(pat, content), f"no match: {label}"

t("Regex patterns match METRICS.md rows", test_regex_matches_template)

def test_increment_cycles():
    content = METRICS_FILE.read_text()
    before = re.search(r"\| Cycles Completed \| ([0-9N/A]+) \|", content).group(1)
    new = replace_metric(content, "Cycles Completed", 999)
    assert "| Cycles Completed | 999 |" in new
    assert f"| Cycles Completed | {before} |" not in new

t("Increment replaces value correctly", test_increment_cycles)

def test_na_handling():
    assert parse_value("N/A") is None
    assert format_value(None) == "N/A"

t("N/A round-trip", test_na_handling)

def test_unknown_metric():
    content = METRICS_FILE.read_text()
    try:
        replace_metric(content, "Totally Fake", 1)
        raise AssertionError("should fail")
    except ValueError as e:
        assert "Unknown metric" in str(e)

t("Unknown metric raises", test_unknown_metric)

def test_sync_git_commits():
    import subprocess
    result = subprocess.run(["git","log","--oneline"], cwd=WORKSPACE, capture_output=True, text=True)
    expected = len([l for l in result.stdout.splitlines() if l.strip()])
    content = METRICS_FILE.read_text()
    m = re.search(r"\| Git Commits \| ([0-9N/A]+) \|", content)
    actual = parse_value(m.group(1))
    assert isinstance(actual, int) and actual >= 0, f"Git Commits not numeric: {actual}"
    assert actual == expected, f"Mismatch: file={actual} vs git={expected}"

t("Git Commits sync matches repo history", test_sync_git_commits)

print(f"\n{'='*40}")
print(f"RESULTS: {PASS} passed, {FAIL} failed")
sys.exit(0 if FAIL == 0 else 1)
