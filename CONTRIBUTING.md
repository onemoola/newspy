# Contributing to Newspy

Thanks for taking the time to contribute! We appreciate all contributions, from reporting bugs to implementing new
features.
If you're unclear on how to proceed after reading this guide, please create an issue and tag it with the `question`
label.

## Table of Contents

- [Reporting Bugs or Suggesting Enhancements](#reporting-bugs-or-suggesting-enhancements)
- [Contributing to the codebase](#contributing-to-the-codebase)
    - [Forking the repository](#forking-the-repository)
    - [Picking an issue](#picking-an-issue)
    - [Setting up your local environment](#setting-up-your-local-environment)
    - [Install the right versions of Python (3.10+) and Poetry (1.4.2+)](#install-the-right-versions-of-python-310-and-poetry-142)
    - [Install the requirements](#install-the-requirements)
    - [Install the git hook scripts](#install-the-git-hook-scripts)
    - [Yarn install semantic-release dependencies](#yarn-install-semantic-release-dependencies)
    - [Set up husky pre-commit hook](#set-up-husky-pre-commit-hook)

## Reporting Bugs or Suggesting Enhancements

Before creating a bug report, please check that your bug has not already been reported, and that your bug exists on the
latest version of Newspy.
If you find a closed issue that seems to report the same bug you're experiencing, open a new issue and include a link to
the original issue in your issue description.

Please include as many details as possible in your bug report. The information helps the maintainers resolve the issue
faster.

We use [GitHub issues](https://github.com/onemoola/newspy/issues) to track bugs and suggested enhancements.
You can report a bug by opening a [new issue](https://github.com/onemoola/newspy/issues/new/choose).

## Contributing to the codebase

### Forking the repository

Start by [forking](https://docs.github.com/en/get-started/quickstart/fork-a-repo) the Newspy repository, then clone your
forked repository using `git`:

```bash
git clone git@github.com:<username>/newspy.git

cd newspy/
```

### Setup Git Hooks

We use git hooks to enforce commit message standards (Conventional Commits). Run the setup script immediately after
cloning:

```bash
chmod +x setup-hooks.sh
./setup-hooks.sh
```

### Picking an issue

Pick an issue by going through the [issue tracker](https://github.com/onemoola/newspy/issues) and finding an issue you
would like to work on.
Feel free to pick any issue that is not already assigned.
We use the [help wanted](https://github.com/onemoola/newspy/issues?q=is%3Aopen+is%3Aissue+label%3A%22help+wanted%22)
label to indicate issues that are high on our wishlist.

If you are a first time contributor, you might want to look for issues
labeled [good first issue](https://github.com/onemoola/newspy/issues?q=is%3Aopen+is%3Aissue+label%3A%22good+first+issue%22).
The Newspy code base is quite complex, so starting with a small issue will help you find your way around!

If you would like to take on an issue, please comment on the issue to let others know.
You may use the issue to discuss possible solutions.

### Setting up your local environment

### Install the right versions of Python (3.10+) and Poetry (1.4.2+)

```bash
python --version
> Python 3.10.11 # or 3.11.5

poetry --version
> Poetry (version 1.4.2) # or higher
```

### Install the requirements

```bash
poetry install
```

### Install the git hook scripts

```bash
pre-commit install
```

## License

Any contributions you make to this project will fall under the [MIT License](LICENSE) that covers the Newspy project.