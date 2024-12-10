import argparse
from . import core


def main():
    parser = argparse.ArgumentParser(description="A Distributed Version Control System")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Initialize repository
    subparsers.add_parser("init", help="Initialize a new repository")

    # Add files to staging
    parser_add = subparsers.add_parser("add", help="Stage files for commit")
    parser_add.add_argument("files", nargs='+', help="Files to stage")

    # Commit changes
    parser_commit = subparsers.add_parser("commit", help="Commit staged changes")
    parser_commit.add_argument("-m", "--message", required=True, help="Commit message")

    # View commit history
    subparsers.add_parser("log", help="View commit history")

    # Branch management
    parser_branch = subparsers.add_parser("branch", help="Manage branches")
    parser_branch.add_argument("action", choices=["create", "list", "switch"], help="Branch action")
    parser_branch.add_argument("branch_name", nargs="?", help="Branch name (if applicable)")

    # Merge branches
    parser_merge = subparsers.add_parser("merge", help="Merge a branch into the current branch")
    parser_merge.add_argument("branch_name", help="Branch to merge")

    # Diff between commits
    parser_diff = subparsers.add_parser("diff", help="Show differences between commits")
    parser_diff.add_argument("commit1", help="First commit hash")
    parser_diff.add_argument("commit2", help="Second commit hash")

    # Clone repository
    parser_clone = subparsers.add_parser("clone", help="Clone a repository")
    parser_clone.add_argument("source", help="Source directory")
    parser_clone.add_argument("destination", help="Destination directory")

    # Parse arguments and call respective functions
    args = parser.parse_args()
    handle_command(args)

def handle_command(args):
    if args.command == "init":
        init_repo()
    elif args.command == "add":
        for file in args.files:
            stage_file(file)
    elif args.command == "commit":
        commit(args.message)
    elif args.command == "log":
        log()
    elif args.command == "branch":
        if args.action == "create":
            create_branch(args.branch_name)
        elif args.action == "list":
            list_branches()
        elif args.action == "switch":
            switch_branch(args.branch_name)
    elif args.command == "merge":
        merge(args.branch_name)
    elif args.command == "diff":
        diff(args.commit1, args.commit2)
    elif args.command == "clone":
        clone_repo(args.source, args.destination)
