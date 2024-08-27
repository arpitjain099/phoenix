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
