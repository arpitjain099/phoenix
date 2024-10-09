"""Test Keyword match."""
import pytest

from phiphi.api.projects.classifiers import base_schemas, child_crud, response_schemas
from phiphi.api.projects.classifiers.keyword_match import schemas as keyword_match_schemas

CREATED_TIME = "2024-04-01T12:00:01"


@pytest.mark.freeze_time(CREATED_TIME)
def test_create_keyword_match_classifier_crud(reseed_tables) -> None:
    """Test create keyword match classifier."""
    keyword_match_create = keyword_match_schemas.KeywordMatchVersionCreate(
        classes_dict={"class1": "class1 description", "class2": "class2"},
        params=keyword_match_schemas.KeywordMatchParams(
            class_to_keyword_configs=[
                keyword_match_schemas.ClassToKeywordConfig(
                    class_name="class1",
                    musts="keyword1",
                )
            ]
        ),
    )
    classifer_response = child_crud.create_classifier(
        session=reseed_tables,
        project_id=1,
        classifier_type=base_schemas.ClassifierType.keyword_match,
        classifier_create=keyword_match_schemas.KeywordMatchClassifierCreate(
            name="First apify gather",
            version=keyword_match_create,
        ),
    )
    assert isinstance(classifer_response, keyword_match_schemas.KeywordMatchClassifierResponse)
    assert classifer_response.name == "First apify gather"
