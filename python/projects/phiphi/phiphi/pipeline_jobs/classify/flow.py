"""Module containing the Prefect flow for classify."""
from typing import Coroutine

import prefect

from phiphi import constants
from phiphi.api.projects.classifiers import schemas
from phiphi.pipeline_jobs.classify import keyword_match_classifier


@prefect.flow(name="classify_flow")
def classify_flow(
    classifier_dict: dict,  # dict of schemas.ClassifierResponse
    job_run_id: int,
    project_namespace: str,
) -> None:
    """Flow which runs classifier on all (as yet unclassified by this classifier) messages."""
    classifier = schemas.ClassifierResponse(**classifier_dict)

    if classifier.type == schemas.ClassifierType.keyword_match:
        # Run keyword_match classifier
        classifier = schemas.ClassifierKeywordMatchResponse(**classifier_dict)
        keyword_match_classifier.classify(
            classifier=classifier, bigquery_dataset=project_namespace, job_run_id=job_run_id
        )
    else:
        raise ValueError(f"{classifier.type=} not implemented.")


def create_deployments(
    override_work_pool_name: str | None = None,
    deployment_name_prefix: str = "",
    image: str = constants.DEFAULT_IMAGE,
    tags: list[str] = [],
    build: bool = False,
    push: bool = False,
) -> list[Coroutine]:
    """Create deployments for flow.

    Args:
        override_work_pool_name (str | None): The name of the work pool to use to override the
        default work pool.
        deployment_name_prefix (str, optional): The prefix of the deployment name. Defaults to "".
        image (str, optional): The image to use for the deployments. Defaults to
        constants.DEFAULT_IMAGE.
        tags (list[str], optional): The tags to use for the deployments. Defaults to [].
        build (bool, optional): If True, build the image. Defaults to False.
        push (bool, optional): If True, push the image. Defaults to False.

    Returns:
        list[Coroutine]: List of coroutines that create deployments.
    """
    work_pool_name = str(constants.WorkPool.main)
    if override_work_pool_name:
        work_pool_name = override_work_pool_name
    task = classify_flow.deploy(
        name=deployment_name_prefix + classify_flow.name,
        work_pool_name=work_pool_name,
        image=image,
        build=build,
        push=push,
        tags=tags,
    )

    return [task]
