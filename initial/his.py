import subprocess
import os


def get_last_bash_command():
    try:
        # history is a bash built-in, so we need to run it through bash
        result = subprocess.run(
            ["bash", "-i", "-c", "history 10"],
            capture_output=True,
            text=True,
            timeout=2,
            # Use the user's home directory to access .bash_history
            env=os.environ.copy(),
        )

        # Extract the last command (remove the history number)
        output = result.stdout.strip()
        if output:
            lines = output.split("\n")
            if lines:
                # Get the last line and remove the history number
                last_line = lines[-1].strip()
                parts = last_line.split(None, 1)
                if len(parts) > 1:
                    return parts[1]
        return "No command found"
    except Exception as e:
        return f"Error: {e}"


if __name__ == "__main__":
    print(f"Last command: {get_last_bash_command()}")
