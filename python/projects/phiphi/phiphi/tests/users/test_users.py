"""Test Users."""
import sqlalchemy

from phiphi.users import models


def test_user(session: sqlalchemy.orm.Session) -> None:
    """Test that there are no users."""
    response = session.execute(sqlalchemy.select(sqlalchemy.func.count()).select_from(models.User))
    count = response.one()
    assert count
    assert count[0] == 0
