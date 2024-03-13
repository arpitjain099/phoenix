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
[`http://localhost:8080/docs/`](http://localhost:8080/docs/).

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
