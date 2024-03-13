"""Test the user seed."""
import sqlalchemy.orm

from phiphi.seed import main as seed_main
from phiphi.users import crud


def test_user_seed(session: sqlalchemy.orm.Session, recreate_tables) -> None:
    """Test the user seed."""
    user_1 = crud.read_user(session, 1)
    user_2 = crud.read_user(session, 2)
    assert user_1 is None
    seed_main.init_first_admin_user(session)
    user_1 = crud.read_user(session, 1)
    user_2 = crud.read_user(session, 2)
    assert user_1
    assert user_2 is None
    assert user_1.id == 1

    # Check that a new user is not created
    seed_main.init_first_admin_user(session)
    user_1 = crud.read_user(session, 1)
    user_2 = crud.read_user(session, 2)
    assert user_1
    assert user_2 is None
