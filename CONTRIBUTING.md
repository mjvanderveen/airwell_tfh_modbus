# Contribution guidelines

Contributing to this project should be as easy and transparent as possible, whether it's:

- Reporting a bug
- Discussing the current state of the code
- Submitting a fix
- Proposing new features

## Github is used for everything

Github is used to host code, to track issues and feature requests, as well as accept pull requests.

Pull requests are the best way to propose changes to the codebase.

1. Fork the repo and create your branch from `main`.
2. If you've changed something, update the documentation.
3. Make sure your code lints (using `scripts/lint`).
4. Test your contribution against a real (or mocked) Airwell TFH controller.
5. Issue that pull request!

## Any contributions you make will be under the MIT Software License

In short, when you submit code changes, your submissions are understood to be under the same
[MIT License](http://choosealicense.com/licenses/mit/) that covers the project.

## Report bugs using Github's [issues](../../issues)

GitHub issues are used to track public bugs. Report a bug by
[opening a new issue](../../issues/new/choose); it's that easy!

## Write bug reports with detail, background, and sample code

**Great Bug Reports** tend to have:

- A quick summary and/or background
- Steps to reproduce
  - Be specific!
  - Include the diagnostic download for the config entry if possible.
- What you expected would happen
- What actually happens
- Notes (possibly including why you think this might be happening, or stuff you tried that
  didn't work)

## Register-map corrections

If you find that your TFHW/TFHX/TFHZ unit reports a different register map than the one vendored
in `custom_components/airwell_tfh/airwell_tfh_modbus/`, please open an issue or PR with a captured
raw register snapshot rather than guessing.

## License

By contributing, you agree that your contributions will be licensed under its MIT License.
