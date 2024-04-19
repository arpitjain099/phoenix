"""All models of the application.

This module is used to import all models of the application to be used in the
Alembic migrations and testing.
"""
from phiphi import platform_db
from phiphi.api.environments import models as environment_models  # noqa: F401
from phiphi.api.instances import models as instance_models  # noqa: F401
from phiphi.api.instances.gathers import models as gather_models  # noqa: F401
from phiphi.api.instances.instance_runs import models as instane_runs_models  # noqa: F401
from phiphi.api.users import models as user_models  # noqa: F401

Base = platform_db.Base
base_metadata = Base.metadata
