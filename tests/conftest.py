from pathlib import Path

import pytest


@pytest.fixture
def base_dir():
    base_dir = Path(__file__).parent.parent
    assert (base_dir / "pyproject.toml").exists()
    return base_dir


@pytest.fixture
def dist_dir(base_dir):
    dist_dir = base_dir / "dist"
    dist_dir.mkdir(exist_ok=True)
    return dist_dir
