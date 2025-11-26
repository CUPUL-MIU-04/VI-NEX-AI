# VI-NEX-AI

## Contributing to VI-NEX-AI

The VI-NEX-AI project welcomes any constructive contribution from the community and the team is more than willing to work on problems you have encountered to make it a better project.

## Development Environment Setup

To contribute to VI-NEX-AI, we would like to first guide you to set up a proper development environment so that you can better implement your code. You can install this library from source with the editable flag (-e, for development mode) so that your change to the source code will be reflected in runtime without re-installation.

You can refer to the Installation Section and replace pip install -v . with pip install -v -e ..

## Prerequisites

```bash
# Clone the repository
git clone https://github.com/Cupul-miu-04/VI-NEX-AI.git
cd VI-NEX-AI

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -v -e .

# Install development dependencies
pip install -r requirements-dev.txt
```

## Code Style

We have some static checks when you commit your code change, please make sure you can pass all the tests and make sure the coding style meets our requirements. We use pre-commit hook to make sure the code is aligned with the writing standard. To set up the code style checking, you need to follow the steps below.

```shell
# these commands are executed under the VI-NEX-AI directory
pip install pre-commit
pre-commit install
```

Code format checking will be automatically executed when you commit your changes.

## Contribution Guide

You need to follow these steps below to make contribution to the main repository via pull request. You can learn about the details of pull request here.

## 1. Fork the Repository

Firstly, you need to visit the VI-NEX-AI repository and fork into your own account. The fork button is at the right top corner of the web page alongside with buttons such as watch and star.

Now, you can clone your own forked repository into your local environment.

```shell
git clone https://github.com/Cupul-miu-04/VI-NEX-AI.git
```

## 2. Configure Git

You need to set the official repository as your upstream so that you can synchronize with the latest update in the official repository. You can learn about upstream here.

Then add the original repository as upstream

```shell
cd VI-NEX-AI
git remote add upstream https://github.com/Cupul-miu-04/VI-NEX-AI.git
```

you can use the following command to verify that the remote is set. You should see both origin and upstream in the output.

```shell
git remote -v
```

## 3. Synchronize with Official Repository

Before you make changes to the codebase, it is always good to fetch the latest updates in the official repository. In order to do so, you can use the commands below.

```shell
git fetch upstream
git checkout main
git merge upstream/main
git push origin main
```

## 4. Create a New Branch

You should not make changes to the main branch of your forked repository as this might make upstream synchronization difficult. You can create a new branch with the appropriate name. General branch name format should start with hotfix/ and feature/. hotfix is for bug fix and feature is for addition of a new feature.

```shell
git checkout -b <NEW-BRANCH-NAME>
```

Branch Naming Convention:

· feature/: New features (e.g., feature/vi-nex-video-enhancement)
· hotfix/: Bug fixes (e.g., hotfix/fix-memory-leak)
· docs/: Documentation updates (e.g., docs/update-api-docs)
· test/: Test-related changes (e.g., test/add-inference-tests)

## 5. Implementation and Code Commit

Now you can implement your code change in the source code. Remember that you installed the system in development, thus you do not need to uninstall and install to make the code take effect. The code change will be reflected in every new Python execution.

You can commit and push the changes to your local repository. The changes should be kept logical, modular and atomic.

```shell
git add -A
git commit -m "<COMMIT-MESSAGE>"
git push -u origin <NEW-BRANCH-NAME>
```

Commit Message Guidelines:

```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

## Types:

· feat: New feature
· fix: Bug fix
· docs: Documentation changes
· style: Code style changes (formatting, etc.)
· refactor: Code refactoring
· test: Test-related changes
· chore: Maintenance tasks

## Example:

```
feat(video_generation): add support for 4K resolution generation

- Implement new scaling mechanism for high-resolution videos
- Add configuration options for resolution scaling
- Update inference pipeline to handle larger tensors

Closes #123
```

## 6. Open a Pull Request

You can now create a pull request on the GitHub webpage of your repository. The source branch is <NEW-BRANCH-NAME> of your repository and the target branch should be main of VI-NEX-AI/VI-NEX-AI.

Pull Request Template:

```markdown
## Description
Brief description of the changes and the problem it solves.

## Related Issues
Fixes # (issue number)

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Performance improvement
- [ ] Code refactoring

## Testing
- [ ] Added tests
- [ ] Manual testing
- [ ] All tests pass

## Checklist
- [ ] My code follows the code style of this project
- [ ] I have updated the documentation accordingly
- [ ] I have added tests to cover my changes
- [ ] All new and existing tests passed
```

## Areas for Contribution

High Priority Areas

1. Video Generation Models: New diffusion architectures or improvements
2. Training Pipelines: Optimizations for faster training and better convergence
3. Inference Optimization: Memory usage, speed improvements, and quantization
4. New Features: Additional conditioning mechanisms, style controls, prompt engineering
5. Documentation: Tutorials, API documentation, and usage examples

For Beginners

· Documentation improvements
· Test cases addition
· Bug reports with reproduction steps
· Example notebooks and demos

Code Standards

Python Standards

· Follow PEP 8 guidelines
· Use type hints for function signatures
· Write comprehensive docstrings
· Keep functions focused and modular
· Use meaningful variable names

## VI-NEX-AI Specific Standards

· Maintain backward compatibility when possible
· Add configuration files for new features
· Update relevant documentation
· Include performance benchmarks when applicable

Testing

Before submitting your pull request, please ensure:

```bash
# Run linting and code style checks
pre-commit run --all-files

# Run tests (if available)
pytest tests/

# Test basic functionality
python -c "import opensora; print('Import successful')"

# Test inference (if models are available)
python scripts/diffusion/inference.py --config configs/diffusion/inference/vi_nex_256px.py --test
```
## Getting Help

· GitHub Issues: For bug reports and feature requests
· GitHub Discussions: For questions and community support
· Documentation: Check our docs for detailed guides

Recognition

## Contributors will be recognized in:

· CONTRIBUTORS.md file
· Release notes
· Project documentation

FAQ

1. How do I start contributing?
   Look for issues labeled good-first-issue or help-wanted in the issue tracker.
2. What if I'm new to AI/ML?
   We welcome contributions in documentation, testing, UI improvements, and more!
3. How long does review take?
   We aim to provide initial feedback within 2-3 business days.
4. pylint cannot recognize some members:

Add this into your settings.json in VSCode:

```json
{
    "python.linting.pylintArgs": [
        "--generated-members=numpy.*,torch.*,cv2.*,PIL.*,matplotlib.*,tensorflow.*",
        "--extension-pkg-whitelist=cv2,PIL,tensorflow"
    ]
}
```

1. Pre-commit hooks are failing:

```bash
# Run pre-commit on all files
pre-commit run --all-files

# Skip pre-commit for a specific commit (use sparingly)
git commit --no-verify -m "Emergency fix"
```

---

Thank you for contributing to VI-NEX-AI! Together we're building the future of video generation. 🚀
