# setup_python-uv

Installs Python-based DevOps tools and libraries using [uv](https://github.com/astral-sh/uv).

Covers **Tier 3** of the tool management strategy (Python-only packages). See [Tool Management Philosophy](../../README.md#tool-management-philosophy).

## Summary

**13 CLI tools** via `uv tool install` (isolated envs, available on `~/.local/bin`):
- Security / audit: `checkov`, `pip-audit`
- Code quality: `black`, `flake8`, `pylint`
- Docs: `mkdocs` (with `mkdocs-material` theme + `mkdocstrings-python` plugin), `pdoc3`
- Package management: `pip-tools`, `pipreqs`
- Git utilities: `git-changelog`, `git-semver`, `gitstats`
- Infrastructure: `ansible`

**31 library packages** via `uv pip install` into `~/.venv/devops`:
- Cloud / API clients: `atlassian-python-api`, `aws-lambda-powertools`, `aws-xray-sdk`, `datadog-api-client`, `hvac`, `jira`, `nc-py-api`, `openai`, `python-jenkins`
- IaC / security: `parliament`, `pyhcl`, `tfparse`
- Diagramming: `diagrams`, `graphviz`
- Docs / formatting: `markdown2`, `matplotlib`, `mkdocstrings-python`, `tinycss2`
- Testing: `pytest-asyncio`, `pytest-cov`, `pytest-mock`, `requests-mock`
- Python utilities: `jsonpath-ng`, `lxml`, `PyJWT`, `pyOpenSSL`, `setuptools-scm`

---

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
| `mkdocs` | Documentation site builder (with `mkdocs-material` theme + `mkdocstrings-python` plugin) |
| `pdoc3` | API documentation generator |
| `pip-audit` | Python dependency vulnerability scanner |
| `pip-tools` | `pip-compile` / `pip-sync` workflow |
| `pipreqs` | Generate `requirements.txt` from imports |
| `pylint` | Python static analysis |

### Library packages — `uv pip install`

Installed into a shared virtualenv at `~/.venv/devops`. These are primarily used as imported libraries in scripts and notebooks.

| Package | Purpose |
|---------|---------|
| `atlassian-python-api` | Jira / Confluence / Bitbucket REST client |
| `aws-lambda-powertools` | AWS Lambda utilities (tracing, logging, metrics) |
| `aws-xray-sdk` | AWS X-Ray distributed tracing |
| `datadog-api-client` | Datadog API client |
| `diagrams` | Diagrams-as-code (cloud architecture) |
| `graphviz` | Graphviz Python bindings |
| `hvac` | HashiCorp Vault API client |
| `jira` | Jira REST API client |
| `jsonpath-ng` | JSONPath expressions for Python |
| `lxml` | XML/HTML processing |
| `markdown2` | Markdown to HTML converter |
| `matplotlib` | Data visualisation / plotting |
| `mkdocstrings-python` | Python API autodoc plugin for MkDocs |
| `nc-py-api` | Nextcloud API client |
| `openai` | OpenAI API client |
| `parliament` | AWS IAM policy linter |
| `pyhcl` | HashiCorp Configuration Language (HCL) parser |
| `PyJWT` | JSON Web Token encode/decode |
| `pyOpenSSL` | OpenSSL bindings |
| `pytest-asyncio` | pytest plugin for async tests |
| `pytest-cov` | pytest coverage reporting |
| `pytest-mock` | pytest mock fixtures |
| `python-jenkins` | Jenkins REST API client |
| `requests-mock` | Mock HTTP requests in tests |
| `setuptools-scm` | Version management from git tags |
| `tfparse` | Terraform HCL parser |
| `tinycss2` | CSS parser |

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

## Platform limitations

**Currently Linux-only.** Two hardcoded assumptions prevent this role from running on macOS as-is:

- `uv_bin` defaults to `/home/linuxbrew/.linuxbrew/bin/uv` — the Linuxbrew path
- `uv_venv_path` is derived from `ansible_env.HOME` which resolves correctly on Linux but the binary path above won't exist on macOS

To add Mac support, `uv_bin` would need to resolve dynamically (e.g. `/opt/homebrew/bin/uv` on Apple Silicon, `/usr/local/bin/uv` on Intel).
