from pathlib import Path

from click.testing import CliRunner

from pyrems.managers.records_manager import (
    build_fzf_input_from_records,
    extract_command_from_fzf_selection,
    increment_command_hits,
    read_commands,
)
from pyrems.cli.main import cli


def test_handle_install_creates_csv_file(runner: CliRunner, temp_csv_file: Path):
    csv_path = temp_csv_file.parent / 'new_file.csv'

    result = runner.invoke(cli, ['install', '--csv-path', str(csv_path)])
    assert result.exit_code == 0

    assert csv_path.exists()

    csv_path.unlink()


def test_handle_store_creates_new_command(runner: CliRunner, temp_csv_file: Path):
    result = runner.invoke(
        cli,
        ['store', '--csv-path', str(temp_csv_file), 'git status', '--note', 'Check repository status'],
    )
    assert result.exit_code == 0

    records = read_commands(temp_csv_file)

    assert len(records) == 1
    assert records[0].command == 'git status'
    assert records[0].note == 'Check repository status'
    assert records[0].hits == 1


def test_handle_store_updates_existing_command(runner: CliRunner, temp_csv_file: Path):
    runner.invoke(cli, ['store', '--csv-path', str(temp_csv_file), 'git status', '--note', 'First note'])
    result = runner.invoke(cli, ['store', '--csv-path', str(temp_csv_file), 'git status', '--note', 'Updated note'])
    assert result.exit_code == 0

    records = read_commands(temp_csv_file)

    assert len(records) == 1
    assert records[0].command == 'git status'
    assert records[0].note == 'Updated note'
    assert records[0].hits == 2


def test_handle_store_multiple_commands(runner: CliRunner, temp_csv_file: Path):
    runner.invoke(cli, ['store', '--csv-path', str(temp_csv_file), 'git status', '--note', 'First command'])
    runner.invoke(cli, ['store', '--csv-path', str(temp_csv_file), 'ls -la', '--note', 'Second command'])
    result = runner.invoke(cli, ['store', '--csv-path', str(temp_csv_file), 'pwd', '--note', 'Third command'])
    assert result.exit_code == 0

    records = read_commands(temp_csv_file)

    assert len(records) == 3


def test_handle_list_returns_all_commands(runner: CliRunner, temp_csv_file: Path):
    runner.invoke(cli, ['store', '--csv-path', str(temp_csv_file), 'git status', '--note', 'Command 1'])
    runner.invoke(cli, ['store', '--csv-path', str(temp_csv_file), 'ls -la', '--note', 'Command 2'])

    result = runner.invoke(cli, ['list', '--csv-path', str(temp_csv_file), '--limit', '20'])
    assert result.exit_code == 0


def test_handle_list_respects_limit(runner: CliRunner, temp_csv_file: Path):
    runner.invoke(cli, ['store', '--csv-path', str(temp_csv_file), 'command1', '--note', 'note1'])
    runner.invoke(cli, ['store', '--csv-path', str(temp_csv_file), 'command2', '--note', 'note2'])
    runner.invoke(cli, ['store', '--csv-path', str(temp_csv_file), 'command3', '--note', 'note3'])

    result = runner.invoke(cli, ['list', '--csv-path', str(temp_csv_file), '--limit', '2'])
    assert result.exit_code == 0


def test_build_fzf_input_from_records(runner: CliRunner, temp_csv_file: Path):
    runner.invoke(cli, ['store', '--csv-path', str(temp_csv_file), 'ls -la', '--note', 'List all files'])
    runner.invoke(cli, ['store', '--csv-path', str(temp_csv_file), 'git status'])

    records = read_commands(temp_csv_file)
    fzf_input = build_fzf_input_from_records(records)

    assert 'ls -la [List all files]' in fzf_input
    assert 'git status' in fzf_input


def test_extract_command_from_fzf_selection():
    selection_with_note = 'ls -la [List all files]'
    command = extract_command_from_fzf_selection(selection_with_note)
    assert command == 'ls -la'

    selection_without_note = 'git status'
    command = extract_command_from_fzf_selection(selection_without_note)
    assert command == 'git status'


def test_increment_command_hits(runner: CliRunner, temp_csv_file: Path):
    runner.invoke(cli, ['store', '--csv-path', str(temp_csv_file), 'git status', '--note', 'First note'])

    records_before = read_commands(temp_csv_file)
    assert records_before[0].hits == 1

    increment_command_hits(temp_csv_file, 'git status')

    records_after = read_commands(temp_csv_file)
    assert records_after[0].hits == 2
    assert records_after[0].note == 'First note'
