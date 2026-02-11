#!/usr/bin/env python3
"""
Detect and report LaTeX beamer frame overflows from pdflatex .log files.

Parses overfull vbox/hbox warnings, maps them to frame titles in .tex files,
and produces a severity-rated report.
"""

import argparse
import re
from pathlib import Path
from dataclasses import dataclass
from typing import List, Tuple, Optional
from collections import defaultdict


@dataclass
class Overflow:
    """Represents a single overflow warning."""
    overflow_type: str  # 'vbox' or 'hbox'
    amount_pt: float
    line_number: int
    line_range: Optional[Tuple[int, int]] = None  # For hbox only

    @property
    def severity(self) -> str:
        """Return severity level based on overflow amount."""
        if self.amount_pt > 50:
            return "CRITICAL"
        elif self.amount_pt >= 30:
            return "HIGH"
        elif self.amount_pt >= 15:
            return "MEDIUM"
        else:
            return "LOW"


@dataclass
class Frame:
    """Represents a LaTeX beamer frame."""
    title: str
    start_line: int
    end_line: int
    overflows: List[Overflow]

    def contains_line(self, line_num: int) -> bool:
        """Check if line number falls within this frame."""
        return self.start_line <= line_num <= self.end_line


def parse_log_file(log_path: Path) -> List[Overflow]:
    """Parse a pdflatex .log file for overflow warnings."""
    overflows = []

    # Regex patterns
    vbox_pattern = re.compile(r'Overfull \\vbox \(([\d.]+)pt too high\) detected at line (\d+)')
    hbox_pattern = re.compile(r'Overfull \\hbox \(([\d.]+)pt too wide\) in paragraph at lines (\d+)--(\d+)')

    try:
        with open(log_path, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                # Check for vbox overflow
                vbox_match = vbox_pattern.search(line)
                if vbox_match:
                    amount = float(vbox_match.group(1))
                    line_num = int(vbox_match.group(2))
                    overflows.append(Overflow('vbox', amount, line_num))
                    continue

                # Check for hbox overflow
                hbox_match = hbox_pattern.search(line)
                if hbox_match:
                    amount = float(hbox_match.group(1))
                    start_line = int(hbox_match.group(2))
                    end_line = int(hbox_match.group(3))
                    overflows.append(Overflow('hbox', amount, start_line, (start_line, end_line)))

    except Exception as e:
        print(f"Warning: Could not parse {log_path}: {e}")

    return overflows


def parse_tex_frames(tex_path: Path) -> List[Frame]:
    """Parse a .tex file to extract frame boundaries and titles."""
    frames = []

    # Regex for \begin{frame}[options]{Title} or \begin{frame}{Title}
    frame_begin_pattern = re.compile(r'\\begin\{frame\}(?:\[([^\]]*)\])?\{([^}]*)\}')
    frame_end_pattern = re.compile(r'\\end\{frame\}')

    try:
        with open(tex_path, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()

        current_frame_start = None
        current_frame_title = None

        for line_num, line in enumerate(lines, start=1):
            # Check for \begin{frame}
            begin_match = frame_begin_pattern.search(line)
            if begin_match:
                current_frame_start = line_num
                current_frame_title = begin_match.group(2).strip()
                if not current_frame_title:
                    current_frame_title = "(untitled)"
                continue

            # Check for \end{frame}
            if frame_end_pattern.search(line) and current_frame_start is not None:
                frames.append(Frame(
                    title=current_frame_title,
                    start_line=current_frame_start,
                    end_line=line_num,
                    overflows=[]
                ))
                current_frame_start = None
                current_frame_title = None

    except Exception as e:
        print(f"Warning: Could not parse {tex_path}: {e}")

    return frames


def assign_overflows_to_frames(overflows: List[Overflow], frames: List[Frame]) -> None:
    """Assign each overflow to the frame that contains it."""
    for overflow in overflows:
        # Use the start of line range for hbox, or line_number for vbox
        line_to_check = overflow.line_range[0] if overflow.line_range else overflow.line_number

        for frame in frames:
            if frame.contains_line(line_to_check):
                frame.overflows.append(overflow)
                break


def generate_report(directory: Path) -> None:
    """Generate overflow report for all .log files in directory."""
    log_files = list(directory.glob("*.log"))

    if not log_files:
        print(f"No .log files found in {directory}")
        return

    try:
        display_dir = directory.relative_to(Path.cwd())
    except ValueError:
        display_dir = directory
    print(f"=== Overflow Report for {display_dir} ===\n")

    all_stats = defaultdict(int)
    file_summaries = []

    for log_file in sorted(log_files):
        tex_file = log_file.with_suffix('.tex')

        if not tex_file.exists():
            print(f"Warning: No corresponding .tex file for {log_file.name}\n")
            continue

        # Parse log and tex files
        overflows = parse_log_file(log_file)
        frames = parse_tex_frames(tex_file)

        if not overflows:
            continue

        # Assign overflows to frames
        assign_overflows_to_frames(overflows, frames)

        # Count stats
        file_stats = defaultdict(int)
        vbox_count = sum(1 for o in overflows if o.overflow_type == 'vbox')
        hbox_count = sum(1 for o in overflows if o.overflow_type == 'hbox')

        print(f"FILE: {tex_file.name} ({len(overflows)} overflows: {vbox_count} vbox, {hbox_count} hbox)\n")

        # Sort frames by worst overflow first
        frames_with_overflows = [f for f in frames if f.overflows]
        frames_with_overflows.sort(key=lambda f: max(o.amount_pt for o in f.overflows), reverse=True)

        for frame in frames_with_overflows:
            # Get worst overflow for this frame
            worst_overflow = max(frame.overflows, key=lambda o: o.amount_pt)
            severity = worst_overflow.severity
            file_stats[severity] += 1
            all_stats[severity] += 1

            print(f"  [{severity}] Frame \"{frame.title}\" (lines {frame.start_line}-{frame.end_line})")

            # List all overflows in this frame
            for overflow in sorted(frame.overflows, key=lambda o: o.amount_pt, reverse=True):
                if overflow.overflow_type == 'vbox':
                    print(f"    {overflow.overflow_type} overflow: {overflow.amount_pt:.2f}pt too high")
                else:
                    print(f"    {overflow.overflow_type} overflow: {overflow.amount_pt:.2f}pt too wide (lines {overflow.line_range[0]}-{overflow.line_range[1]})")
            print()

        # File summary
        file_summaries.append({
            'name': tex_file.name,
            'total': len(overflows),
            'vbox': vbox_count,
            'hbox': hbox_count,
            'critical': file_stats['CRITICAL'],
            'high': file_stats['HIGH'],
            'medium': file_stats['MEDIUM'],
            'low': file_stats['LOW']
        })

        print()

    # Overall summary
    total_overflows = sum(s['total'] for s in file_summaries)

    if total_overflows > 0:
        print("=" * 70)
        print("SUMMARY:")
        print(f"  CRITICAL (>50pt): {all_stats['CRITICAL']}")
        print(f"  HIGH (30-50pt): {all_stats['HIGH']}")
        print(f"  MEDIUM (15-30pt): {all_stats['MEDIUM']}")
        print(f"  LOW (<15pt): {all_stats['LOW']}")

        total_vbox = sum(s['vbox'] for s in file_summaries)
        total_hbox = sum(s['hbox'] for s in file_summaries)
        print(f"  Total: {total_vbox} vbox, {total_hbox} hbox = {total_overflows}")
        print()

        # Per-file summary table
        if len(file_summaries) > 1:
            print("\nPER-FILE SUMMARY:")
            print(f"{'File':<40} {'Total':>6} {'CRIT':>5} {'HIGH':>5} {'MED':>5} {'LOW':>5}")
            print("-" * 70)
            for summary in file_summaries:
                print(f"{summary['name']:<40} {summary['total']:>6} "
                      f"{summary['critical']:>5} {summary['high']:>5} "
                      f"{summary['medium']:>5} {summary['low']:>5}")
    else:
        print("No overflows detected!")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Detect and report LaTeX beamer frame overflows from pdflatex .log files."
    )
    parser.add_argument(
        'directory',
        type=Path,
        nargs='?',
        default=Path.cwd(),
        help='Directory containing .log and .tex files (default: current directory)'
    )

    args = parser.parse_args()

    if not args.directory.exists():
        print(f"Error: Directory {args.directory} does not exist")
        return 1

    if not args.directory.is_dir():
        print(f"Error: {args.directory} is not a directory")
        return 1

    generate_report(args.directory)
    return 0


if __name__ == '__main__':
    exit(main())
