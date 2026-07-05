import json
from datetime import datetime
from pathlib import Path

from repository import MINIGIT_DIR


def read_index(repository_path="."):
    """Read staged filename-to-hash entries from .minigit/index."""
    root = Path(repository_path).resolve()
    index_path = root / MINIGIT_DIR / "index"
    entries = {}

    if not index_path.exists():
        return entries

    with open(index_path, "r", encoding="utf-8") as index:
        for line in index:
            line = line.strip()
            if not line:
                continue

            filename, digest = line.rsplit(" ", 1)
            entries[filename] = digest

    return entries


def next_commit_number(commits_path):
    """Find the next sequential commit number for .minigit/commits."""
    highest_number = 0

    for commit_file in commits_path.glob("*.json"):
        if commit_file.stem.isdigit():
            highest_number = max(highest_number, int(commit_file.stem))

    return highest_number + 1


def create_commit(message, repository_path="."):
    """Create a numbered JSON commit from the current staging index."""
    root = Path(repository_path).resolve()
    minigit_path = root / MINIGIT_DIR
    commits_path = minigit_path / "commits"

    if not minigit_path.is_dir():
        return False, "Error: MiniGit repository not found. Run 'python minigit.py init' first."

    staged_files = read_index(root)
    if not staged_files:
        return False, "Nothing to commit. The staging index is empty."

    commit_number = next_commit_number(commits_path)
    commit = {
        "commit_number": commit_number,
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "message": message,
        "files": staged_files,
    }

    commit_path = commits_path / f"{commit_number}.json"
    with open(commit_path, "w", encoding="utf-8") as commit_file:
        json.dump(commit, commit_file, indent=4)

    return True, f"Created commit {commit_number}: {message}"
