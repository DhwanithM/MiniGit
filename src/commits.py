import json
from datetime import datetime

from repository import get_minigit_path


def read_index(repository_path="."):
    """Read staged workspace-relative filename-to-hash entries."""
    index_path = get_minigit_path(repository_path) / "index"
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
    minigit_path = get_minigit_path(repository_path)
    commits_path = minigit_path / "commits"

    if not minigit_path.is_dir():
        return False, "Error: MiniGit repository not found. Run 'python src/minigit.py init' first."

    staged_files = read_index(repository_path)
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


def read_commits(repository_path="."):
    """Return all numbered commit JSON objects from newest to oldest."""
    minigit_path = get_minigit_path(repository_path)
    commits_path = minigit_path / "commits"

    if not minigit_path.is_dir():
        return False, "Error: MiniGit repository not found. Run 'python src/minigit.py init' first.", []

    commits = []
    for commit_file in commits_path.glob("*.json"):
        if not commit_file.stem.isdigit():
            continue

        with open(commit_file, "r", encoding="utf-8") as file:
            commits.append(json.load(file))

    commits.sort(key=lambda commit: commit["commit_number"], reverse=True)
    return True, "", commits


def format_commit_log(commits):
    """Format commit metadata for display in the MiniGit log command."""
    if not commits:
        return "No commits yet. Stage files and run 'python src/minigit.py commit \"message\"' first."

    lines = []
    separator = "-" * 40

    for commit in commits:
        tracked_files = len(commit.get("files", {}))
        lines.extend(
            [
                separator,
                f"Commit: {commit['commit_number']}",
                f"Timestamp: {commit['timestamp']}",
                f"Message: {commit['message']}",
                f"Tracked files: {tracked_files}",
            ]
        )

    lines.append(separator)
    return "\n".join(lines)
