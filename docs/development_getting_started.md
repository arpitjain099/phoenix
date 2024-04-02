# Development Getting Started

Welcome to the development guide for contributors! This document outlines the steps necessary to
set up your development environment for working on the project. Our project leverages a local
Kubernetes (k8s) cluster for the development of the full system, while sub-projects may have
smaller-scale set-ups for more focused development.

This approach allows you to test changes in a controlled environment that closely mimics
production. For sub-projects, smaller-scale set-ups are available and can be used for more specific
development tasks. See sub folders for more information on this.

Thank you for contributing to our project, and happy coding!

## Using `asdf` for Version Management

We use `asdf` as our tool of choice for managing multiple runtime versions for different languages
and tools. `asdf` allows you to easily switch between different versions of tools like Node.js,
helm, Python, and more, ensuring consistency across our development environments.

You can also use a different version management system and see
[.tool-versions](./../.tool-versions) for the configuration of versions.

Install `asdf`: Follow the instructions on the `asdf`, see
[docs](https://asdf-vm.com/guide/getting-started.html)

To setup `asdf` with the correct plugins and  versions of the tools, run the following command:

```bash
make setup_asdf
```

This will also install `kubectl` that is needed for working with the local cluster.

## Set up a local cluster

We recommend that you use [mircok8s](https://microk8s.io/) but you can use any as documented by
tilt, see below. To get up and running follow the steps:

1. [Install mircok8s](https://microk8s.io/docs/install-alternatives)
3. Check that you don't have anything else running on port 80 of your local machine
4. Run `source setup_microk8s.sh` to set up the cluster and `kubectl`
5. The command will output instructions on setting up your `/etc/hosts` file

### Using another local cluster

If is possible to use a different cluster
that tilt works with, see [tilt docs on clusters](https://docs.tilt.dev/choosing_clusters).

If you do this the set up of the ingress/host name and the `kubctl` setup might be different. For
instance when using `k3s` you will need to add `<traefik-serivce-ip> phoenix.local` to your
`/etc/hosts` and [follow cluster access](https://docs.k3s.io/cluster-access)

## Setting secrets for local cluster

To allow for the secrets to not be in the charts you can add the secrets as a Kubernetes SECRET.

```bash
cp clusters/local/.example_secrets.yaml clusters/local/secret.yaml
```

The secrets will be applied when the command `make up` is run.


## Running the Development Environment with tilt up

Our development environment leverages [`tilt`](https://tilt.dev/) to streamline the process of
running services in the local Kubernetes cluster.

Once you have you local cluster up and running you can do:

```bash
make up
```

In the browser you will be able to see the `tilt` UI via the URL that `tilt up` prints.

You can also use the `tilt` cli if needs be. Such as `tilt down` to bring down the resources in the
cluster.

## Hello world

Once your set up is complete you should be able to see an hello world at:

* [http://localhost/](http://localhost/)
* [http://phoenix.local/](http://phoenix.local/)
