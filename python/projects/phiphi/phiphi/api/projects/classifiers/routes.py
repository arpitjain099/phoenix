"""Classifier routes."""
import fastapi

from phiphi.api.projects.classifiers.keyword_match import routes as keyword_match_routes

router = fastapi.APIRouter()
router.include_router(keyword_match_routes.router)
