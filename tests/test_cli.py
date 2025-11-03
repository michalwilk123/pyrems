from pathlib import Path

from click.testing import CliRunner

from pyrems.cli.main import cli
from pyrems.managers.records_manager import read_commands


def test_cli_store_creates_record(temp_csv_file: Path):
    runner = CliRunner()
    result = runner.invoke(
        cli,
        ['store', '--csv-path', str(temp_csv_file), 'git status', '--note', 'Check repository status'],
    )
    assert result.exit_code == 0

    records = read_commands(temp_csv_file)
    assert len(records) == 1
    assert records[0].command == 'git status'


def test_cli_list_runs(temp_csv_file: Path):
    runner = CliRunner()
    # Pre-populate two commands using the CLI
    runner.invoke(cli, ['store', '--csv-path', str(temp_csv_file), 'ls -la'])
    runner.invoke(cli, ['store', '--csv-path', str(temp_csv_file), 'pwd'])

    result = runner.invoke(cli, ['list', '--csv-path', str(temp_csv_file), '--limit', '2'])
    assert result.exit_code == 0


def test_cli_install_creates_file():
    runner = CliRunner()
    with runner.isolated_filesystem():
        csv_path = Path('install_created.csv')
        assert not csv_path.exists()

        result = runner.invoke(cli, ['install', '--csv-path', str(csv_path)])
        assert result.exit_code == 0
        assert csv_path.exists()


