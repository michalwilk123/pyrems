import subprocess
import sys


def run_command(command: list[str], description: str) -> bool:
    print(f"\n{'='*60}")
    print(f"Running: {description}")
    print(f"{'='*60}\n")

    result = subprocess.run(command)

    if result.returncode != 0:
        print(f"\n❌ {description} failed with exit code {result.returncode}")
        return False

    print(f"\n✓ {description} completed successfully")
    return True


def main() -> int:
    print("Starting code linting...")

    commands = [
        (["ruff", "check", "--fix", "pyrems/", "tests/"], "Ruff fix"),
        (["vulture", "pyrems/", "tests/", "whitelist.py"], "Vulture dead code check"),
    ]

    all_passed = True
    for command, description in commands:
        if not run_command(command, description):
            all_passed = False

    print(f"\n{'='*60}")
    if all_passed:
        print("✓ All linting checks passed")
        print(f"{'='*60}\n")
        return 0
    else:
        print("❌ Some linting checks failed")
        print(f"{'='*60}\n")
        return 1


if __name__ == "__main__":
    sys.exit(main())
