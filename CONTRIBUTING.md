# Contributing

## Advice for new contributors
Small tasks get merged easier as the scope of changes won't require wider review. We recommend starting with these.

Always create an `Issue` before doing a `Pull Request`. This helps us track our progress easier. We don't accept `Pull Requests` on their own.

Search through already labeled Issues such as `area:contracts` and `kind:feature`. You will get those merged easier as they are examined and identified already by one of our core committers.

If you want to start solving the `Issue`, please comment in it with something like: "I would like to take a stab at this". This will help us coordinate and distribute the workload.

See below for more guidelines on [Pull Requests](#pull-requests).

## Developer setup
We support the current version generally in the docker ecosystem.

In order to build the image you need [Docker](https://www.docker.com/) installed on your computer.

Run these commands in order to get going:
```
git clone https://github.com/hCaptcha/prometheus2honeycomb
cd prometheus2honeycomb
bin/test
```

The final "OK" after the tests should be an indication that everything works.

## Making Changes
When you are preparing to make your pull request, do the following things.

### Tests

If your task is labeled with anything that adds new functionality like `kind:feature` or `kind:improvement` please write the supporting tests as well.

The easiest way run all the tests is by running `bin/test`. Our current testsuite can be found in that file, so if you need to add more, please add it there (or a separate python unit test file).

Before doing a pull request, remember also to run `bin/lint` so your code complies with our style.

### Pull requests
Before your pull request, keep in mind the following things:

* Rebase your changes on the latest development branch, resolving any conflicts. This ensures that your changes will merge cleanly when you open your PR.
* Add tests and run your tests before the PR.
* Make sure the diff between our master and your branch contains the minimal amount of changes needed to implement the feature or bugfix. This speeds up the process of approving your PR and getting it to our codebase.
* Don't submit a PR with commented out code or unfinished features. We encourage however "PR early approach". The PR's that start with `WIP: <PR description>` can be opened even before you have a single line of code written. It also lets our core dev's give important input down the way.
* Provide well written commit messages. We use the imperative form in our PRs: "Update README", "Add solhint to lint solidity code", "Add helper methods to tests to reduce repetitive code".
* Provide a well written Pull Request message. Include in your summary
    * What you changed
    * Why this change was made ([Use keywords](https://help.github.com/articles/closing-issues-using-keywords/) to close the issue e.g. Fixes #117)
    * Any relevant technical details or motivation for your implementation choices. Longer explanation is better than a shorter one when in doubt.

