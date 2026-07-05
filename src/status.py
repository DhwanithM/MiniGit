from repository import get_minigit_path, get_workspace_path
from utils import hash_file


IGNORED_DIRS = {"src", ".git", ".minigit", "__pycache__"}


def read_index(repository_path="."):
    """Read the staging index as workspace-relative filenames mapped to hashes."""
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


def read_workspace_files(repository_path="."):
    """Return current workspace files mapped to their SHA-1 hashes."""
    workspace_path = get_workspace_path(repository_path)
    files = {}

    if not workspace_path.exists():
        return files

    for path in workspace_path.rglob("*"):
        if not path.is_file():
            continue

        relative_parts = path.relative_to(workspace_path).parts
        if any(part in IGNORED_DIRS for part in relative_parts):
            continue

        filename = path.relative_to(workspace_path).as_posix()
        files[filename] = hash_file(path)

    return files


def get_status(repository_path="."):
    """Compare workspace files against the staging index."""
    minigit_path = get_minigit_path(repository_path)
    if not minigit_path.is_dir():
        return False, "Error: MiniGit repository not found. Run 'python src/minigit.py init' first.", None

    index_entries = read_index(repository_path)
    workspace_files = read_workspace_files(repository_path)

    modified = []
    new = []
    deleted = []
    unchanged = []

    for filename, current_hash in workspace_files.items():
        staged_hash = index_entries.get(filename)

        if staged_hash is None:
            new.append(filename)
        elif staged_hash != current_hash:
            modified.append(filename)
        else:
            unchanged.append(filename)

    for filename in index_entries:
        if filename not in workspace_files:
            deleted.append(filename)

    return True, "", {
        "modified": sorted(modified),
        "new": sorted(new),
        "deleted": sorted(deleted),
        "unchanged": sorted(unchanged),
    }


def format_status_report(status):
    """Format grouped status results for CLI output."""
    changed = status["modified"] or status["new"] or status["deleted"]
    if not changed:
        return "Working tree is clean."

    lines = []
    sections = [
        ("Modified", status["modified"]),
        ("New", status["new"]),
        ("Deleted", status["deleted"]),
        ("Unchanged", status["unchanged"]),
    ]

    for heading, files in sections:
        lines.append(f"{heading}:")
        if files:
            lines.extend(f"  {filename}" for filename in files)
        else:
            lines.append("  None")
        lines.append("")

    return "\n".join(lines).rstrip()
