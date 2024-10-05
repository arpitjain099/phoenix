# Phoenix

An open-source social media analysis platform for peacebuilders.

## Where to start

Phoenix has a number of different levels of interface and components to fit the different needs of
its users.

### Platform

The platform is a full stack web application that provides a user-friendly interface for managing
configuration, collecting and processing data, and analyzing and visualizing the results. It is
designed to be used by non technical peacebuilders and analysts who want to monitor and analyze
social media data.

It has the most complex set up process of the levels of interface and components, but is the most
the most feature rich and complete. See the [Platform Quick start](#platform-quick-start) section
below to get started.

Build Up provides a hosted version of the platform find out more at
[https://howtobuildup.org/programs/digital-conflict/phoenix/](https://howtobuildup.org/programs/digital-conflict/phoenix/).

### PhiPhi API

The PhiPhi API is a RESTful API that provides an interface for managing configuration, collecting
and processing data. It is has an auto-generated Swagger web interface (documentation) and is
designed to be used by developers who may want to integrate Phoenix with other (visualisation)
systems or want to manage a large number of projects and users but don't need a fancy web
interface.

This has a simpler set up process than the platform, but would probably need to be deployed in to a
cloud environment to be useful. See the [PhiPhi Readme](python/projects/phiphi/README.md) for more
information.

### PhiPhi Pipeline Jobs

The PhiPhi Pipeline Jobs are a set of prefect flows (python functions) that can be used to collect
and process social media data. They are designed to be used by developers who want to do their own
social media data collection and processing. This is best for developers that are working on just
a couple of projects and they want to process these data locally.

This has the simplest set up process of the levels of interface and components, but is requires the
developer to manage the configuration themselves. See the [PhiPhi Pipeline Jobs
Readme](python/projects/phiphi/docs/getting_started_with_pipeline_jobs.md) for more information.

## Platform Quick start

### Requirements

- [asdf](https://asdf-vm.com/guide/getting-started.html)
- [microk8s](https://microk8s.io/docs/install-alternatives)

```bash
make setup_asdf
source setup_microk8s.sh
make up
```

Visit in your browser:
- [http://console.phoenix.local](http://console.phoenix.local)
- [http://api.phoenix.local/docs](http://api.phoenix.local/docs)

More detailed documentation at [docs/development_getting_started.md](docs/development_getting_started.md).

## Organizations

<a href="https://howtobuildup.org">
    <img
      src="https://howtobuildup.org/wp-content/uploads/2021/04/build-up-logo.png"
      height="100"
      alt="build-up-logo"
    >
</a>
<a href="http://datavaluepeople.com">
    <img
      src="https://howtobuildup.org/wp-content/uploads/2022/03/dvp.png"
      height="100"
      alt="datavaluepeople_logo"
    >
</a>

## License

[GNU AGPLv3](/COPYING)

## v1

If you are looking for the old version it is [here](https://gitlab.com/howtobuildup/phoenix_v1). 
