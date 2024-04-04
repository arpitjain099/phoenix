# Phoenix Superset

This project contains the customization of the Apache Superset for Phoenix.

## Superset Version

It is important that the version of the superset is the same in both:
- Dockerfile
- requirements.in

## Development

Use the development tools generic python development tools in [/python](../../).

### A note about typing

Both libraries `superset` and `flask_appbuilder` don't have stubs :( so we have to use ignore for
`no-untyped-def` and `import-untyped` errors.

## Testing

In general when developing python tests should be made however to manually test can be done by
running the following command:

```bash
make up
# In a different terminal
make init
```

You can then visit [`localhost:8089`](http://localhost:8089), open the browser console and set the cookie as instructed in
the output of `make init`: `document.cookie = "phiphi-user-email=admin@admin.com";` and refresh .
You should then be able to see the superset welcome page.
