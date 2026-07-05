from pathlib import Path

from repository import MINIGIT_DIR


def update_index(filename, digest, repository_path="."):
    """Add or replace a filename-to-hash entry in the MiniGit index."""
    root = Path(repository_path).resolve()
    index_path = root / MINIGIT_DIR / "index"
    entries = {}

    if index_path.exists():
        with open(index_path, "r", encoding="utf-8") as index:
            for line in index:
                line = line.strip()
                if not line:
                    continue

                staged_filename, staged_hash = line.rsplit(" ", 1)
                entries[staged_filename] = staged_hash

    entries[filename] = digest

    with open(index_path, "w", encoding="utf-8") as index:
        for staged_filename, staged_hash in entries.items():
            index.write(f"{staged_filename} {staged_hash}\n")
