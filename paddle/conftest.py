import sys
import os

import pytest

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))


@pytest.fixture(scope="session", autouse=True)
def _abort_if_pytest_uses_dev_db(django_db_setup, django_db_blocker):
    """Safety net: refuse running tests against dev SQLite."""
    from django.db import connection

    with django_db_blocker.unblock():
        db_name = str(connection.settings_dict.get("NAME", ""))

    normalized = db_name.replace("\\", "/").lower()
    if normalized.endswith("/db.sqlite3") or normalized == "db.sqlite3":
        raise RuntimeError(
            "Unsafe test configuration: pytest is targeting development db.sqlite3. "
            "Use config.test_settings so tests run on an isolated test database."
        )
