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

### Integration tests

There are integration tests allow for quicker development iteration. To run some of the integration
tests you need to have your local environment authenticated with gcloud. You can do this by
running:
```bash
gcloud auth application-default login
```

And, in the same terminal session as you run the next `make` command, you need to set the
`GOOGLE_CLOUD_PROJECT` environment variable to the project you want to use. You can do this by`:
```bash
export GOOGLE_CLOUD_PROJECT=<project_id>
```

Then you can run the integration tests with:
```bash
make integration_test
```

Be aware that the integration tests will create and delete resources in the Gcloud project. Make
sure that you are using the correct project. Also be aware that if the integration test fails, the
resources might not be deleted and will need to be deleted manually. See documentation in the test
file for more information.

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

## Databases

In phiphi there are two types of database:
- platform: This is the main database for the user platform. It contains contains
configurations for users, workspaces, and projects. There is a single test and single
production Postgres database.
- project: There is a separate database for every project. This contains the scraped
and processed data for the project. There are as many project DBs as there are
projects, plus more testing and development. Bigquery is used for project databases in
production, and a mixture of sqlite and bigquery is used for testing and development.

Both databases are managed by alembic and use SQLAlchemy to define the tables/ORM models.

### Platform database migration

If you have created a new file with a new model, you will need to add this to
`phiphi/all_platform_models.py` so that alembic has it in the table metadata.

Use make commands to create a revision. Be aware that by default the revision will be created with
the user `root`. See "Problems with files created in the container" for more information.
WARNING: The revision description must not contain spaces. (The commands get messed up, so use _.)
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

### Project database migration

For project data migrations an sqlite database is used for testing. For production the migrations
are applied to a bigquery dataset that is specific to a project. See the file
[`project_db.alembic.ini`](./project_db.alembic.ini) `sqlalchemy.url` for more information about
test migration db.

To create and test new tables and their migrations:

A `sqlalchemy.Table` should be create and not an `ORM` model. See docstring in
[phiphi/project_db.py](phiphi/project_db.py) for more information for gottchas and best practices.

Create new tables in a new file and add it as an import to `phiphi/all_project_tables.py`.

Upgrade the test migration db: `make project_alembic_upgrade`.

Use make commands to create a revision/file with migration. Be aware that by default the revision
will be created with the user `root`. See "Problems with files created in the container" for more
information.
WARNING: The revision description must not contain spaces. (The commands get messed up, so use _.)
```bash
message="<revision description>" make project_alembic_revision
```

This will create a new migration file in the `phiphi/project_db_migrations/versions/project`
directory. The file will be `r_$datetime_$revision_slug_$description`.

Check and edit the migration file as needed and fixing any linting issues.

Apply the migration to the test database: `make project_alembic_upgrade` to see if it works.

If you want to manually test this in a real cloud dataset:
* Set up you gcloud credentials: `gcloud auth application-default login`
* Create a dataset in BigQuery
* In the file project_db.alembic.ini set sqlalchemy.url to the dataset:
  `bigquery://<project_id>/<dataset_id>`
* Run `make project_alembic_upgrade`. The google credentials should be automagically set up in the
  container.
* Check the dataset in BigQuery to see if the tables were created
* Delete the dataset in BigQuery
* Change the sqlalchemy.url back to the test sqlite database

## Running deployments locally for testing full flow runs

If you are developing flows and want to test the full flow run, you can run the flow locally.

This is done by:

- Start the local cluster, see the `phoenix` root README for more information.
- Set up and log in to prefect cloud: `prefect cloud login_with_browser`.
- Run: `group_name=<dev_id> make create_prefect_grouped_deployments`. `dev_id` the something
  to indicate that you create the flows. This could be the branch name.
- You should see a number of `prefect deployment run` commands that you can use to run the flows.
- You should be able to see the logs in the cluster and in the prefect cloud/server.

Be aware that if more then one developer use the same `dev_id` the flows and images will overwrite
each other.

## Adding a new gather

See the [Adding Gathers](./docs/adding_gathers.md) document for more information.
