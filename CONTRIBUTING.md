# CONTRIBUTING.md

## Welcome

Thank you for considering contributing to the `phoenix` project! We welcome contributions from
everyone, and are grateful for any help, big or small. This document is a guide to help you
understand how you can contribute.

## How to Contribute

Contributions to `phoenix` can come in various forms. Here are some ways you can help:

* **Bug Reports**: If you find a bug, please open an issue in our GitLab repository. Include a
  detailed description of the bug, steps to reproduce it, and, if possible, a suggestion for how it
  could be fixed.
* **Feature Requests**: Have an idea for a new feature or an improvement to an existing one? Submit
  an issue, describing your idea and how it would benefit the project.
* **Code Contributions**: Ready to start coding? Great! Look through our issues for tasks to
  tackle, or suggest your own ideas as a new issue. Once you're ready, submit a Merge Request (MR)
  with your changes.
* **Other ways**: See [phoenix landing
  page](https://howtobuildup.org/programs/digital-conflict/phoenix/)

## Principles

These principles give guidelines and direction for collaborating and developing the repository.

### General Principles

* We prioritise the understandability and usability of everything do
* We support and respect one another: we can be tough on ideas but are always gentle on people
* We are not violent or derogatory
* We resolve conflict through peaceful and pragmatic ways
* We tend towards combining already existing tools and ideas rather than coming up with our own
* We work asynchronous and are aware of the requirements for this, [more info in a blog from
  gitlab](https://about.gitlab.com/company/culture/all-remote/asynchronous/#how-does-asynchronous-communication-work)
* We aim to be concise and considerate in our communication
* There is no right and wrong, there are advantages and disadvantages

### Coding Principles

* We prioritise the understandability and usability of everything do
* We aim to write documentation first, have that reviewed and then implement the feature
* We try to make small understandable changes: with commits that are atomic and MRs (PRs) that are
  like short stories for the reviewer, see below for resources
* We attempt to make software tools that follow the Unix philosophy of “Doing one thing well”,
  [more info here](http://www.catb.org/~esr/writings/taoup/html/ch01s06.htm)

#### Further reading and resources

* [On MRs (PRs)](https://wiki.crdb.io/wiki/spaces/CRDB/pages/1411744698/Organizing+PRs+and+Commits)

## Getting Started

1. Fork the repository on GitLab. This creates your own copy of the project, where you can make
changes without affecting the original.
2. Clone your fork to your local machine, so you can start working on the changes.
3. Create a new branch for your changes. This keeps your modifications organized and separate from
the main branch.
4. Make your changes. Be sure to follow the coding standards and guidelines of the project.
5. Test your changes. Ensure that your code does not break any existing functionality and meets the
project's quality standards.
6. Submit a Merge Request. Go to the original Phoenix repository on GitLab and click on "Merge
Requests". Click "New Merge Request", and select your fork and branch as the source. Fill in the
details, explaining your changes and why they should be included. Generally MRs should be made on
to `dev` and not `main`.

## Release Process

The release process is managed by the maintainers of the project. If you have a feature or bug fix
that you would like to see included in the next release, please submit a Merge Request with `dev` as
the target branch. The maintainers will review your changes and decide whether to include them in
the next release.

To make a release, the maintainers will follow these steps:
- Merge all approved changes in to `dev`
- Update the version number in:
  - [./charts/main/Chart.yaml](./charts/main/Chart.yaml), `version` and `appVersion`
- Commit these changes and tag the commit with the version number
- Create a MR from `dev` to `main` with the changes and commit with the version change. This will
  publish the release ready for deployment.
- Create a MR in `phoenix-infra` to update the version of the chart for dev and prod
- Apply the tofu environment `dev` and manually test if needed
- Merge the MRs both in `phoenix` and `phoenix-infra` and apply the tofu environment `prod`

### Helpful

* [Development Getting Started](/docs/development_getting_started.md)

## Communication

Use GitLab issues to ensure that everyone can participate and the conversation is recorded. Or see
[phoenix landing page](https://howtobuildup.org/programs/digital-conflict/phoenix/)

## Thank You

Every contribution is valuable to the project. Thank you for your hard work and dedication.
