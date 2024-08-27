# Adding Gathers to Phiphi

This document outlines the steps to add a new gather type to Phiphi.

When adding a new gather it is recommended to follow the steps outlined here while using one of the
other gathers, such as
[`apify_facebook_posts`](python/projects/phiphi/phiphi/api/projects/gathers/apify_facebook_posts/),
as a example for the changes and conventions.

Currently there are only Apify gathers, but in the future there might be other gather types. These
steps are then specific to Apify gathers.

## Steps - Stage 1

### Decided which Apify actor

Look at the possible actors here: https://apify.com/actors

### Decided on a `child_type_name`

This name should follow the conventions of the other child names. However, since there are lots of
different types of actors please feel free to come up with a name that seems to make sense but can
be out of the conversion of the other gathers.

Make the additions:
- Add the `child_type_name` to `ChildTypeName` in `phiphi/api/projects/gathers/schemas.py`.
- Add a folder `phiphi/api/projects/gathers/<child_type_name>/` with an `__init__.py` file.

### Make base schemas

Make schemas in `phiphi/api/projects/gathers/<child_type_name>/schemas.py for the
`<child_type_name>Base` and <child_type_name>Response`. For class names use `CamelCase` and
for the fields use `snake_case`.

These schemas should use attribute names that are clear to a technical peace builder. They can be
different from the names that are used in the Apify actor. If they are then use the Pydantic Field
parameter `serialization_alias` to map the Apify attribute name.

Add test for the serialization of the Response schema in
`phiphi/tests/api/projects/gathers/test_<child_type_name>_schemas.py`.

See other examples for more information.

### Make an MR

At this point it is recommended to make a merge request to the `phiphi` repository. This will allow
for feedback and discussion on the `child_type_name` and what is being proposed to be added.

## Steps - Stage 2

### Add schemas to child_types.py`

Add the `Base` and `Response` schemas and `child_type_name` to the config maps in
`phiphi/api/projects/gathers/child_type.py`. This includes making the correct additions to
the variable `CHILD_TYPES_MAP_PROJECT_DB_DEFAULTS`.

### Make an example gather

Add an example gather in `phiphi/tests/pipeline_jobs/gathers/example_gathers.py`. Do not use PI
data in the definition but it is recommended to use attributes that actually return results from
Apify as this will be used to make a real request to Apify.

### Make a real request to Apify

Using the example gather you made in the previous step, make a real request to the gather service to
get real output data for the example gather. This can be done by running the integration tests with
`phiphi/tests/pipeline_jobs/gathers/test_apify_scrape.py::manual_test_apify_scrape_and_batch_download`.
Using this test will mean that you will also test the batch download functionality for the gather
you are adding.

### Create sample data

Add the real output data that was gotten from the request as the json sample data:
`phiphi/pipeline_jobs/gathers/<child_type_name>.json`.

It is important to remove PI data. List of things that should be removed:
- Ids
- Ids or usernames of accounts
- Names of user names people (that are not well known) also in the text of a post or comment.
- URLs

One option is to replace this with the attribute name and an index. See
`tiktok_hashtags_posts.json` for examples.

### Add normalizer

Add normaliser to `phiphi/pipeline_jobs/gathers/normalisers.py` including test and fixtures to
`phiphi/tests/pipeline_jobs/gathers/conftest.py`

Also add the normaliser to the variable `gather_normalisation_map` in
`phiphi/pipeline_jobs/gathers/normalise.py`.

### Make an MR

At this point the gather should work through the pipeline. For instance you could add an
integration test that would run the gather and output the data into Big Query. It is not needed to
add this integration test as if `manual_test_apify_scrape_and_download` runs and normaliser test
pass things should work.

It is however a good idea to make a MR so others can see the changes and give feedback.
