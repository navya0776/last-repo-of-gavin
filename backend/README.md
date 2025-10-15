## Managing Dependencies and Building Your Python Project

### Overall Workflow Overview

1. **Initial Build Using Existing Build Files**

- Start by building the project wheel/package from your current configuration files (e.g., `pyproject.toml`).
- This creates distributable files (`dist/*.whl`) on your local system that encapsulate the current dependencies and code.

***

### Development Phase

2. **Development Dependency Management**

- During active development, install dependencies via `requirements.txt`:

```bash
pip install -r requirements.txt
```

- This allows quick iteration with exact pinned versions.
- Add or update dependencies as development requires.
- After modifying dependencies, regenerate `requirements.txt` to reflect changes.

***

### Preparing the Package for Distribution

3. **Update `pyproject.toml`**

- Reflect the updated dependencies and metadata in `pyproject.toml` for future builds.
- This is the modern standard for packaging and dependency declaration.

Example snippet in `pyproject.toml`:

```toml
[project]
dependencies = [
  "SQLAlchemy>=2.0",
  "alembic>=1.17",
  "python-dotenv>=1.1",
  "fastapi>=0.118.3",
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
