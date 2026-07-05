from pathlib import Path


MINIGIT_DIR = ".minigit"
WORKSPACE_DIR = "workspace"


def get_repository_root(path="."):
    """Return the MiniGit project root."""
    return Path(path).resolve()


def get_minigit_path(repository_path="."):
    """Return the .minigit directory at the project root."""
    return get_repository_root(repository_path) / MINIGIT_DIR


def get_workspace_path(repository_path="."):
    """Return the workspace directory where user files live."""
    return get_repository_root(repository_path) / WORKSPACE_DIR


def resolve_workspace_file(filename, repository_path="."):
    """Resolve a user filename safely inside workspace/."""
    workspace_path = get_workspace_path(repository_path)
    file_path = (workspace_path / filename).resolve()

    if file_path != workspace_path and workspace_path not in file_path.parents:
        return None

    return file_path


def init_repository(path="."):
    root = get_repository_root(path)
    minigit_path = get_minigit_path(root)
    workspace_path = get_workspace_path(root)

    workspace_path.mkdir(exist_ok=True)

    if minigit_path.exists():
        return False, f"MiniGit repository already exists at {minigit_path}"

    (minigit_path / "objects").mkdir(parents=True)
    (minigit_path / "commits").mkdir()
    (minigit_path / "HEAD").write_text("", encoding="utf-8")
    (minigit_path / "index").write_text("", encoding="utf-8")

    return True, f"Initialized empty MiniGit repository in {minigit_path}"
