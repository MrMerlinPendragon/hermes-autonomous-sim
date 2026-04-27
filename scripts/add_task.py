#!/usr/bin/env python3
"""
Task Ingestion CLI — Genesis Garden
Adds tasks to TASK_QUEUE.md programmatically with proper priority handling.

Usage:
  python3 scripts/add_task.py --priority MEDIUM "Describe the task here"
  python3 scripts/add_task.py -p HIGH "Fix the critical bug"
  python3 scripts/add_task.py -p LOW "Update documentation"

The script inserts the task under the appropriate priority section,
preserving existing content and formatting conventions.
"""

import re
import sys
from pathlib import Path

WORKSPACE = Path.home() / 'autonomous-sim'
TASK_QUEUE_FILE = WORKSPACE / 'TASK_QUEUE.md'

PRIORITY_HEADERS = {
    'HIGH': '## HIGH PRIORITY',
    'MEDIUM': '## MEDIUM PRIORITY',
    'LOW': '## LOW PRIORITY / MAINTENANCE',
}

SECTION_ORDER = ['HIGH', 'MEDIUM', 'LOW']


def find_section_position(content, priority):
    """Find the line number where to insert a new task under the given priority section."""
    lines = content.split('\n')
    header = PRIORITY_HEADERS[priority]
    
    # Find the header line
    header_line = None
    for i, line in enumerate(lines):
        if line.strip() == header:
            header_line = i
            break
    
    if header_line is None:
        return None
    
    # Find the next section header (or end of file)
    next_section_line = len(lines)
    for i in range(header_line + 1, len(lines)):
        if lines[i].startswith('## '):
            next_section_line = i
            break
    
    # Return position just after the header
    insert_line = header_line + 1
    # Skip blank lines after header
    while insert_line < next_section_line and lines[insert_line].strip() == '':
        insert_line += 1
    
    return insert_line


def add_task(priority, description):
    """Add a task to TASK_QUEUE.md under the specified priority section."""
    if priority not in PRIORITY_HEADERS:
        print(f"ERROR: Unknown priority '{priority}'. Use one of: {', '.join(PRIORITY_HEADERS.keys())}")
        sys.exit(1)
    
    content = TASK_QUEUE_FILE.read_text()
    
    insert_pos = find_section_position(content, priority)
    if insert_pos is None:
        print(f"ERROR: Could not find '{PRIORITY_HEADERS[priority]}' section in TASK_QUEUE.md")
        sys.exit(1)
    
    lines = content.split('\n')
    
    # Prepare the new task line
    new_task_line = f"- [ ] {description}"
    
    lines.insert(insert_pos, new_task_line)
    
    new_content = '\n'.join(lines)
    TASK_QUEUE_FILE.write_text(new_content)
    
    print(f"  Task added to {priority} priority: {description}")
    return True


def main():
    if len(sys.argv) < 3:
        print("Usage: python3 scripts/add_task.py --priority LEVEL \"task description\"")
        print("   or: python3 scripts/add_task.py -p LEVEL \"task description\"")
        print("\nPriority levels: HIGH, MEDIUM, LOW")
        sys.exit(1)
    
    # Parse arguments
    priority = None
    description = None
    
    args = sys.argv[1:]
    i = 0
    while i < len(args):
        if args[i] in ('--priority', '-p'):
            if i + 1 >= len(args):
                print("ERROR: Priority level required after --priority/-p")
                sys.exit(1)
            priority = args[i + 1].upper()
            i += 2
        else:
            description = ' '.join(args[i:])
            break
    
    if priority is None:
        print("ERROR: Priority not specified (use --priority or -p)")
        sys.exit(1)
    
    if description is None or description.strip() == '':
        print("ERROR: Task description required")
        sys.exit(1)
    
    add_task(priority, description)
    print("TASK_QUEUE.md updated successfully.")


if __name__ == '__main__':
    main()
