"""All models of the application.

This module is used to import all models of the application to be used in the
Alembic migrations and testing.
"""
from phiphi import platform_db
from phiphi.api.projects import models as project_models  # noqa: F401
from phiphi.api.projects import user_project_associations  # noqa: F401
from phiphi.api.projects.classifiers import models as classifier_models  # noqa: F401
from phiphi.api.projects.classifiers.keyword_match import (
    models as keyword_match_models,  # noqa: F401
)
from phiphi.api.projects.classifiers.manual_post_authors import (
    models as manual_post_authors_models,  # noqa: F401
)
from phiphi.api.projects.gathers import models as gather_models  # noqa: F401
from phiphi.api.projects.gathers.apify_facebook_comments import (
    models as apify_facebook_comments_models,  # noqa: F401,
)
from phiphi.api.projects.gathers.apify_facebook_posts import (
    models as apify_facebook_posts_models,  # noqa: F401,
)
from phiphi.api.projects.gathers.apify_facebook_search_posts import (
    models as apify_facebook_search_posts_models,  # noqa: F401,
)
from phiphi.api.projects.gathers.apify_tiktok_accounts_posts import (
    models as apify_tiktok_accounts_posts_models,  # noqa: F401,
)
from phiphi.api.projects.gathers.apify_tiktok_comments import (
    models as apify_tiktok_comments_models,  # noqa: F401,
)
from phiphi.api.projects.gathers.apify_tiktok_hashtags_posts import (
    models as apify_tiktok_hashtags_posts_models,  # noqa: F401,
)
from phiphi.api.projects.gathers.apify_tiktok_searches_posts import (
    models as apify_tiktok_searches_posts_models,  # noqa: F401,
)
from phiphi.api.projects.job_runs import models as job_runs_models  # noqa: F401
from phiphi.api.users import models as user_models  # noqa: F401
from phiphi.api.workspaces import models as workspace_models  # noqa: F401

Base = platform_db.Base
base_metadata = Base.metadata
