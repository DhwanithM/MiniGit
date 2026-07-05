from repository import get_minigit_path


def update_index(filename, digest, repository_path="."):
    """Add or replace a workspace-relative filename-to-hash entry."""
    index_path = get_minigit_path(repository_path) / "index"
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
