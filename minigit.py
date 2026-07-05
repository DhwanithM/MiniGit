import argparse

from repository import init_repository


def build_parser():
    parser = argparse.ArgumentParser(
        prog="minigit.py",
        description="A simplified Git clone in Python.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("init", help="Initialize a new MiniGit repository")
    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "init":
        _, message = init_repository()
        print(message)


if __name__ == "__main__":
    main()
