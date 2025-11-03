from pathlib import Path
from tempfile import NamedTemporaryFile

import pytest
from click.testing import CliRunner

from pyrems.managers.records_manager import create_empty_csv


@pytest.fixture
def temp_csv_file():
    with NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as tmp_file:
        csv_path = Path(tmp_file.name)

    create_empty_csv(csv_path)

    yield csv_path

    if csv_path.exists():
        csv_path.unlink()


@pytest.fixture
def runner():
    return CliRunner()
