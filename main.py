"""Loading Screen Gold entry.

A tiny program for make.fun's one-line loading-screen-tip bounty. It writes
one tip — a single line for stressed developers and AI coding agents — to
/output/entry.txt, where the house judge picks it up. Standard library only:
no network, no randomness, and the output is byte-identical on every run.
"""

import os
from pathlib import Path

TIP = "Tip: Nobody knows why it works now. The agent won't ask. You won't ask. Just ship it quietly."

# The gate allows 1-200 characters, a single line, more than whitespace.
if not 1 <= len(TIP) <= 200:
    raise SystemExit(f"tip is {len(TIP)} characters, must be 1-200")
if not TIP.strip():
    raise SystemExit("tip must not be only whitespace")
if "\n" in TIP:
    raise SystemExit("tip must be a single line")


def resolve_out_dir() -> Path:
    """Where the entry goes: $MAKEFUN_OUTPUT_DIR, else the harness /output."""
    configured = os.environ.get("MAKEFUN_OUTPUT_DIR")
    return Path(configured) if configured else Path("/output")


def write_entry() -> Path:
    """Write the tip and pin the file readable (0644) whatever the umask."""
    out_dir = resolve_out_dir()
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / "entry.txt"
    target.write_text(TIP, encoding="utf-8", newline="\n")
    target.chmod(0o644)
    return target


def verify(target: Path) -> None:
    """Fail loudly unless the file on disk is exactly the approved tip."""
    with open(target, encoding="utf-8", newline="\n") as f:
        written = f.read()
    if written != TIP:
        raise SystemExit("entry.txt does not match the approved tip")


if __name__ == "__main__":
    verify(write_entry())
