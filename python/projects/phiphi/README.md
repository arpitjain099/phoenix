# PhiPhi

This project is the main API and backend processing for phoenix.

## Development

For simplicity `phiphi` uses a docker compose environment rather then a local virtual environment.
This is so as the project gets more complex the CI and development environment are the same and we
are not maintaining two different environments. It is still recommend to set up an virtual
environment using the instructions in the [`/python/README.md`](/python/README.md) so that your IDE
can provide better support.

To start the development environment run the following command:
```bash
make up
```

Visit the API at [`http://localhost:8080/`](http://localhost:8080/) and the docs at
[`http://localhost:8080/docs/`](http://localhost:8080/docs/). By default you should be able to
change the user by setting the cookie `phiphi-user-email` to the email of the user you want to use.

See the [`Makefile`](Makefile) for more commands.

### Testing and Linting

Make commands to run testing and linting:
```bash
make all
make test
make format
```

Be aware that these commands use the `make` in the parent directory, but inside the container. This
is to ensure that the commands are run in the same environment as the API and to simplify the setup
of the development environment.

## Problems with files created in the container

If a file is created in the container, for instance using `make alembic_revision`, it could have a
different owner then your default shell user. To fix the local permissions if a file is created in
the container, run. This command will ask for you password:
```bash
make fix_local_permissions
```

It is also possible to run the commands in the container as the current user. For Unix systems
you can you can run the following before running a `make` or `docker compose` command:
```bash
source set_host_uid_unix.sh
```

### Database migrations

If you have created a new file with a new model, you will need to add this to
`phiphi/all_platform_models.py` so that alembic has it in the table metadata.

Use make commands to create a revision. Be aware that by default the revision will be created with
the user `root`. See "Problems with files created in the container" for more information.
```bash
message="<revision description>" make alembic_revision
```

This will create a new migration file in the `phiphi/migrations/versions/platform` directory. The
file will be `r_$datetime_$revision_slug_$description`.

Check and edit the migration file as needed and fixing any linting issues.

The migrations will be applied when you do `make up` and the `api` service is started. However, if
you want to explicitly run migrations you can do:
```bash
make alembic_upgrade
```

Note: When we have the use case to add another alembic branch this should be done making an
addition to `version_locations` in `alembic.ini` separating new additions with the
`version_path_separator`.

See the `Makefile` for more commands.
