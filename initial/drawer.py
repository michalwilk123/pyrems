#!/usr/bin/env python3
import sys
import os

# Storage file for commands
STORAGE_FILE = "bash_drawer.txt"


def load_commands():
    """Load commands from storage file"""
    if not os.path.exists(STORAGE_FILE):
        return []
    with open(STORAGE_FILE, "r") as f:
        return [line.strip() for line in f if line.strip()]


def save_command(command):
    """Save a new command"""
    with open(STORAGE_FILE, "a") as f:
        f.write(command + "\n")


def list_commands():
    """List all stored commands"""
    commands = load_commands()
    if not commands:
        print("No commands stored yet.")
        return
    for i, cmd in enumerate(commands, 1):
        print(f"{i}: {cmd}")


def get_command(index):
    """Get command by index and output it for readline"""
    commands = load_commands()
    if index < 1 or index > len(commands):
        print(f"Error: Invalid index. Valid range: 1-{len(commands)}", file=sys.stderr)
        sys.exit(1)

    # This prints the command to stdout so bash can use it
    print(commands[index - 1])


def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  drawer list           - List all commands")
        print("  drawer add <command>  - Add a command")
        print("  drawer <number>       - Get command by number")
        sys.exit(1)

    action = sys.argv[1]

    if action == "list":
        list_commands()
    elif action == "add":
        if len(sys.argv) < 3:
            print("Error: Please provide a command to add")
            sys.exit(1)
        command = " ".join(sys.argv[2:])
        save_command(command)
        print(f"Added: {command}")
    else:
        # Assume it's a number
        try:
            index = int(action)
            get_command(index)
        except ValueError:
            print(f"Error: Unknown action '{action}'")
            sys.exit(1)


if __name__ == "__main__":
    main()
