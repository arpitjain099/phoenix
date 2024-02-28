# Development Getting Started

Welcome to the development guide for contributors! This document outlines the steps necessary to
set up your development environment for working on the project. Our project leverages a local
Kubernetes (k8s) cluster for the development of the full system, while sub-projects may have
smaller-scale set-ups for more focused development.

This approach allows you to test changes in a controlled environment that closely mimics
production. For sub-projects, smaller-scale set-ups are available and can be used for more specific
development tasks. See sub folders for more information on this.

Thank you for contributing to our project, and happy coding!

## Set up a local cluster

We recommend that you use [mircok8s](https://microk8s.io/) but you can use any as documented by
tilt, see below. To get up and running follow the steps:

1. [Install mircok8s](https://microk8s.io/docs/install-alternatives)
2. Make `kubectl` command to use the mircok8s see bellow
3. `microk8s enable ingress`. First check that you don't have anything else running on port 80 of
  your local machine
4. If you want superset and oauth to work you also have to add these to `/etc/hosts`
```
127.0.0.1       superset.phoenix.local
127.0.0.1       oauth.phoenix.local
```

### `kubectl` setup

For `tilt` to work you need to have `kubectl` access to the `mircok8s` cluster. There are a number
of ways to do this but here is the one we found to be the best:

* `sudo microk8s config > ~/.kube/microk8s-config`
* `export KUBECONFIG=~/.kube/microk8s-config:~/.kube/config` You can also add this to you
  `.bashrc/.bash_profile`
  so the config is always included. Or run you will need to run it before you set the context.
* `kubectl config use-context microk8s`. Do this command before `tilt` commands are run to setup
  the correct cluster.

If you recreate your cluster you can recreate the config: `sudo microk8s config >
~/.kube/microk8s-config` to set up `kubectl` again.

### Using another local cluster

If is possible to use a different cluster
that tilt works with, see [tilt docs on clusters](https://docs.tilt.dev/choosing_clusters).

If you do this the set up of the ingress/host name and the `kubctl` setup might be different. For
instance when using `k3s` you will need to add `<traefik-serivce-ip> phoenix.local` to your
`/etc/hosts` and [follow cluster access](https://docs.k3s.io/cluster-access)

## Using `asdf` for Version Management

We use `asdf` as our tool of choice for managing multiple runtime versions for different languages
and tools. `asdf` allows you to easily switch between different versions of tools like Node.js,
helm, Python, and more, ensuring consistency across our development environments.

You can also use a different version management system and see
[.tool-versions](./../.tool-versions) for the configuration of versions.

Install `asdf`: Follow the instructions on the `asdf`, see
[docs](https://asdf-vm.com/guide/getting-started.html)

### `asdf` install tools

To install correct tool versions run this command in the root directory:

```bash
asdf install
```

You may need to add Plugins to `asdf` to install all the tools, see
[docs](https://asdf-vm.com/manage/plugins.html)

### `asdf` usage

Run a shim/command:

```bash
asdf reshim
# Check the helm version
helm version
```

## Setting secretes

To allow for the secrets to not be in the charts you can add the secrets as a Kubernetes SECRET.

```bash
cp clusters/local/.example_secrets.yaml clusters/local/secret.yaml
```

Fill in the required values of clusters/local/secret.yaml

```bash
kubectl apply -f clusters/local/secret.yaml
```

This needs to be done before `tilt up` is run otherwise passwords and secrets will be created in
correctly.

## Running the Development Environment with tilt up

Our development environment leverages [`tilt`](https://tilt.dev/) to streamline the process of
running services in the local Kubernetes cluster.

Once you have you local cluster up and running you can do:

```bash
tilt up
```

In the browser you will be able to see the `tilt` UI via the URL that `tilt up` prints.

## Hello world

Once your set up is complete you should be able to see an hello world at:

* [http://localhost/](http://localhost/)
* [http://phoenix.local/](http://phoenix.local/)
