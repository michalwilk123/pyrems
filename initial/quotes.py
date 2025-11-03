import os
import sys
import subprocess
import textwrap
import shutil


def get_quotes_file():
    """Get the path to quotes file."""
    quotes_file = "quotes.txt"
    if not os.path.isfile(quotes_file):
        print(f"Error: quotes.txt not found at {quotes_file}")
        print("Set QUOTES_FILE environment variable or create ~/quotes.txt")
        sys.exit(1)
    return quotes_file


def check_fzf():
    """Check if fzf is installed."""
    try:
        subprocess.run(
            ["fzf", "--version"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
        )
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("Error: fzf is not installed")
        print("Install it with: brew install fzf (macOS) or apt install fzf (Ubuntu)")
        sys.exit(1)


def select_quote(quotes_file):
    """Use fzf to select a quote."""
    try:
        with open(quotes_file, "r", encoding="utf-8") as f:
            quotes = f.read()

        result = subprocess.run(
            [
                "fzf",
                "--prompt=Search quotes: ",
                "--height=40%",
                "--reverse",
                "--border",
            ],
            input=quotes,
            text=True,
            capture_output=True,
        )

        if result.returncode == 0:
            return result.stdout.strip()
        return None
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


def display_quote(line):
    """Display the selected quote nicely formatted."""
    if not line:
        return

    if "," in line:
        # Split quote and author (split from the right to handle commas in quotes)
        quote, author = line.rsplit(",", 1)
        quote = quote.strip().strip('"').strip("'")
        author = author.strip()

        # Get terminal width
        try:
            width = shutil.get_terminal_size().columns
            max_width = min(width - 4, 80)
        except:
            max_width = 76

        # Print the quote nicely formatted
        print()
        wrapped = textwrap.fill(quote, width=max_width)
        print(f'  "{wrapped}"')
        print()

        # Right-align the author name
        author_text = f"— {author}"
        padding = max(0, max_width - len(author) + 2)
        print(f"{' ' * padding}{author_text}")
        print()
    else:
        print(line)


def main():
    quotes_file = get_quotes_file()
    check_fzf()
    selected = select_quote(quotes_file)
    display_quote(selected)


if __name__ == "__main__":
    main()
