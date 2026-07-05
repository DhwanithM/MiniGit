import shutil

from repository import get_minigit_path, resolve_workspace_file
from utils import hash_file


def store_object(path, repository_path="."):
    """Store a workspace file copy in .minigit/objects using its SHA-1 hash."""
    minigit_path = get_minigit_path(repository_path)
    objects_path = minigit_path / "objects"
    source_path = resolve_workspace_file(path, repository_path)

    if not minigit_path.is_dir():
        return False, "Error: MiniGit repository not found. Run 'python src/minigit.py init' first.", None

    if source_path is None:
        return False, f"Error: file must be inside workspace: {path}", None

    if not source_path.is_file():
        return False, f"Error: file not found in workspace: {path}", None

    digest = hash_file(source_path)
    object_path = objects_path / digest

    if object_path.exists():
        return False, f"Object already exists: {digest}", digest

    shutil.copyfile(source_path, object_path)
    return True, f"Stored object {digest} from workspace/{path}", digest
