# Charts

This folder contains all the helm charts for Phoenix. These can be used for the local development
or production deployments of phoenix.

## Open source Helm packages

The `phoenix_chart_main` (`./main/`) is the main helm chart for Phoenix . It is published to the
GitHub package registry and can be used by anyone. Using the command:
```bash
helm repo add phoenix_chart_main https://gitlab.com/api/v4/projects/54715878/packages/helm/stable
```

There is a CI set up so that the chart on the branch `main` is published to channel `stable`.
