import json
import shutil

from repository import get_minigit_path, resolve_workspace_file


def read_commit(commit_number, repository_path="."):
    """Read a numbered commit JSON file from .minigit/commits."""
    minigit_path = get_minigit_path(repository_path)
    commit_path = minigit_path / "commits" / f"{commit_number}.json"

    if not minigit_path.is_dir():
        return False, "Error: MiniGit repository not found. Run 'python src/minigit.py init' first.", None

    if not commit_path.is_file():
        return False, f"Error: commit {commit_number} does not exist.", None

    with open(commit_path, "r", encoding="utf-8") as commit_file:
        return True, "", json.load(commit_file)


def restore_commit(commit_number, repository_path="."):
    """Restore tracked files from objects back into workspace/."""
    objects_path = get_minigit_path(repository_path) / "objects"
    ok, message, commit = read_commit(commit_number, repository_path)

    if not ok:
        return False, message

    for filename, digest in commit.get("files", {}).items():
        object_path = objects_path / digest
        target_path = resolve_workspace_file(filename, repository_path)

        if target_path is None:
            return False, f"Error: commit contains invalid workspace path: {filename}."

        if not object_path.is_file():
            return False, f"Error: missing object {digest} for file {filename}."

        target_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(object_path, target_path)

    return True, f"Restored commit {commit_number} into workspace."
