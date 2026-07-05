from pathlib import Path


MINIGIT_DIR = ".minigit"


def init_repository(path="."):
    root = Path(path).resolve()
    minigit_path = root / MINIGIT_DIR

    if minigit_path.exists():
        return False, f"MiniGit repository already exists at {minigit_path}"

    (minigit_path / "objects").mkdir(parents=True)
    (minigit_path / "commits").mkdir()
    (minigit_path / "HEAD").write_text("", encoding="utf-8")
    (minigit_path / "index").write_text("", encoding="utf-8")

    return True, f"Initialized empty MiniGit repository in {minigit_path}"
