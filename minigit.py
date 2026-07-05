import argparse
from pathlib import Path

from commits import create_commit, format_commit_log, read_commits
from index import update_index
from objects import store_object
from repository import init_repository
from utils import hash_file


def build_parser():
    parser = argparse.ArgumentParser(
        prog="minigit.py",
        description="A simplified Git clone in Python.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("init", help="Initialize a new MiniGit repository")

    hash_parser = subparsers.add_parser("hash", help="Compute a file's SHA-1 hash")
    hash_parser.add_argument("filename", help="File to hash")

    add_parser = subparsers.add_parser("add", help="Store a file as a MiniGit object")
    add_parser.add_argument("filename", help="File to store")

    commit_parser = subparsers.add_parser("commit", help="Create a commit from the staging index")
    commit_parser.add_argument("message", help="Commit message")

    subparsers.add_parser("log", help="Show commit history")

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "init":
        _, message = init_repository()
        print(message)
    elif args.command == "hash":
        file_path = Path(args.filename)

        if not file_path.is_file():
            print(f"Error: file not found: {args.filename}")
            return

        digest = hash_file(file_path)
        print(f"SHA-1 ({args.filename}): {digest}")
    elif args.command == "add":
        _, message, digest = store_object(args.filename)
        print(message)

        if digest is None:
            return

        update_index(args.filename, digest)
        print(f"Staged {args.filename} with hash {digest}")
    elif args.command == "commit":
        _, message = create_commit(args.message)
        print(message)
    elif args.command == "log":
        ok, message, commits = read_commits()

        if not ok:
            print(message)
            return

        print(format_commit_log(commits))


if __name__ == "__main__":
    main()
