# Phoenix Superset

This project contains the customization of the Apache Superset for Phoenix.

## Development

Use the development tools generic python development tools in [/python](../../).

### A note about typing

Both libraries `superset` and `flask_appbuilder` don't have stubs :( so we have to use ignore for
`no-untyped-def` and `import-untyped` errors.
