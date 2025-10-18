## Managing Dependencies and Building Your Python Project

### Overall Workflow Overview

1. **Initial Build Using Existing Build Files**

- Start by building the project wheel/package from your current configuration files (e.g., `pyproject.toml`).
- This creates distributable files (`dist/*.whl`) on your local system that encapsulate the current dependencies and code.

***

### Development Phase

2. **Development Dependency Management**

- During active development, install dependencies via `pyproject.toml`:

```bash
pip install -e ".[test]"
```

- This allows quick iteration with exact pinned versions.
- Add or update dependencies as development requires.
- After modifying dependencies, regenerate `pyproject.toml` to reflect changes.

***

### Preparing the Package for Distribution

3. **Update `pyproject.toml`**

- Reflect the updated dependencies and metadata in `pyproject.toml` for future builds.
- This is the modern standard for packaging and dependency declaration.

Example snippet in `pyproject.toml`:

```toml
[project]
dependencies = [
  "python-dotenv>=1.1",
  "fastapi>=0.118.3",
  "motor>=3.7.1",
  "uvicorn>=0.37.0",`
]
```

***

### Rebuild and Install

4. **Build the Project Wheel**

- Run the following commands to update the build with the latest `pyproject.toml`:

```bash
python -m pip install --upgrade pip build
python -m build
```

- This generates new distribution files (`*.whl`) in the `dist/` directory.

5. **Install Dependencies and Your Package**

- Install the build artifacts along with dependencies:

```bash
python -m pip install --upgrade pip setuptools wheel
pip install dist/*.whl
```

- To include optional dependencies (e.g., test tools), use:

```bash
pip install "ims-backend[test]"
```

6. During Deployment on main server, install deployment dependencies using:

```bash
pip install ".[deploy]"
```

This will install `gunicorn` which is used as a load balancer and a worker

### Using `pre-commits`

Pre-commits is a useful tool that will allow us to now mess this project up and is a replacement of `act`

- Setup
To setup the hooks of `pre-commits` we need to install the `test` dependencies. That can be done using

```bash
  pip install -e ".[test]"
```

There is also using `wheels/`

```bash
python -m pip install --upgrade pip build
python -m build
python -m pip install --upgrade pip setuptools wheel
pip install dist/*.whl
pip install "ims-backend[test]"
```

- Installing hooks
To install the hooks, simply do:

```bash
pre-commit install
```

> [!NOTE]
> This will only work where a `.pre-commit-config,yaml` file is present

To run `pre-commit` every time you push your changes, run:

```bash
pre-commit run --all-files
```

Congratulations, we are now 1 step further from messing up this repo :)
