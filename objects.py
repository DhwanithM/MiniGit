import shutil
from pathlib import Path

from repository import MINIGIT_DIR
from utils import hash_file


def store_object(path, repository_path="."):
    """Store a file copy in .minigit/objects using its SHA-1 hash as the name."""
    root = Path(repository_path).resolve()
    minigit_path = root / MINIGIT_DIR
    objects_path = minigit_path / "objects"
    source_path = Path(path)

    if not minigit_path.is_dir():
        return False, "Error: MiniGit repository not found. Run 'python minigit.py init' first."

    if not source_path.is_file():
        return False, f"Error: file not found: {path}"

    digest = hash_file(source_path)
    object_path = objects_path / digest

    if object_path.exists():
        return False, f"Object already exists: {digest}"

    shutil.copyfile(source_path, object_path)
    return True, f"Stored object {digest} from {path}"
