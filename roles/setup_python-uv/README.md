# setup_python-uv

Installs Python-based DevOps tools and libraries using [uv](https://github.com/astral-sh/uv).

Covers **Tier 3** of the tool management strategy (Python-only packages). See [Tool Management Philosophy](../../README.md#tool-management-philosophy).

## What it does

Packages are split into two categories based on how they are used:

### CLI tools — `uv tool install`

Each tool gets its own isolated virtual environment (like pipx). Tools are available on `PATH` via `~/.local/bin`.

| Tool | Purpose |
|------|---------|
| `ansible` | Infrastructure automation CLI |
| `black` | Python code formatter |
| `checkov` | IaC security scanner |
| `flake8` | Python linter |
| `git-changelog` | Changelog generator from git history |
| `git-semver` | Semantic version bumper from git tags |
| `gitstats` | Git repository statistics |
| `mkdocs-material` | Documentation site builder (includes `mkdocstrings-python` plugin) |
| `pdoc3` | API documentation generator |
| `pip-audit` | Python dependency vulnerability scanner |
| `pip-tools` | `pip-compile` / `pip-sync` workflow |
| `pipreqs` | Generate `requirements.txt` from imports |
| `pylint` | Python static analysis |

### Library packages — `uv pip install`

Installed into a shared virtualenv at `~/.venv/devops`. These are primarily used as imported libraries in scripts and notebooks.

`aspose-diagram`, `aspose-diagram-python`, `atlassian-python-api`, `aws-lambda-powertools`, `aws-xray-sdk`, `datadog-api-client`, `diagraform`, `diagrams`, `dot2mmd`, `graphviz`, `hvac`, `jira`, `jsonpath-ng`, `lxml`, `markdown2`, `matplotlib`, `mkdocstrings-python`, `nc-py-api`, `openai`, `parliament`, `pyhcl`, `PyJWT`, `pyOpenSSL`, `pytest-asyncio`, `pytest-cov`, `pytest-mock`, `python-jenkins`, `requests-mock`, `setuptools-scm`, `tfparse`, `tinycss2`

## Prerequisites

- `uv` must be installed before running this role (via Homebrew: `install_linuxbrew` + `uv` in `setup_minimal` brew packages)

## Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `uv_bin` | `/home/linuxbrew/.linuxbrew/bin/uv` | Path to the uv binary |
| `uv_venv_path` | `~/.venv/devops` | Path for the shared library venv |
| `uv_tools` | see `defaults/main.yml` | List of tools for `uv tool install` |
| `uv_pip_packages` | see `defaults/main.yml` | List of packages for `uv pip install` |

## Usage

```yaml
- name: Setup Python uv packages
  ansible.builtin.import_role:
    name: setup_python-uv
  become: false
  tags:
    - python
    - uv
```

## Activating the devops venv

To use the library packages in scripts or interactively:

```bash
source ~/.venv/devops/bin/activate
```

## Notes

- `become: false` — all packages are installed in user space
- `changed_when: false` on install tasks — uv is idempotent but doesn't produce reliable change output; use `upgrade_python-uv` to actually upgrade packages
- Adding or removing packages from the lists reruns the install on next playbook run (new packages get installed; removed packages are not uninstalled automatically)
