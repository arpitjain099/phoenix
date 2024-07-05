# Phoenix Superset

This project contains the customization of the Apache Superset for Phoenix.

## Superset Version

It is important that the version of the superset is the same in both:
- Dockerfile
- requirements.in

## Development

Use the development tools generic python development tools in [/python](../../).

There are however some cases where developing in the Local cluster is needed. If you hit problems
with developing in a virtual machine then use the local cluster.

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

## Testing in the local cluster

If you are testing authentication it is recommended to use the local cluster. There are some very
strange behaviours with the use of the phiphi-user-email cookie in the virtual machine and docker
environment.

## Adding drivers

To add drivers to the superset image you can add the driver to the `docker.requirements.in` file and follow the below steps:

- Check the list of available drivers for superset,
  [here](https://superset.apache.org/docs/databases/installing-database-drivers).
- Update the `docker.requirements.in` file with the new driver package. Include the version, see below.
- Build the image using `make build`
- You can check that the driver is working by following the steps in the testing section. And
  creating a new database connection.

A note about pinning the version of the driver. It is important to pin the version of the driver to
avoid breaking changes. The version should be pinned to the latest version that is compatible with
the superset version. However, we are not using a compiled requirements.txt as this causes problems
with the build and local install.
