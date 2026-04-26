# CI/CD

## Overview

A single GitHub Actions workflow (`lint.yml`) runs on every push and pull request to `main`.
It validates YAML formatting and Ansible best practices. No deployment automation — all
cluster and workstation changes are applied manually via `ansible-playbook`.

---

## Workflow: lint.yml

### Triggers

| Event | Branch |
|-------|--------|
| `push` | `main` |
| `pull_request` | `main` |

### Concurrency

A `concurrency` group is set to `${{ github.workflow }}-${{ github.ref }}` with
`cancel-in-progress: true`. Pushing multiple commits quickly cancels the previous run
rather than queuing redundant jobs.

### Runner

`ubuntu-24.04` — pinned to a specific Ubuntu version so the environment does not change
silently when GitHub updates `ubuntu-latest`.

### Timeout

`timeout-minutes: 10` — prevents a hung step (e.g. a stalled `ansible-galaxy` download)
from blocking the shared runner indefinitely.

---

## Steps

```
Checkout
  └─ Set up Python 3.12 (pip cache keyed on requirements-lint.txt)
       └─ Install linting tools (ansible-lint, yamllint)
            └─ Restore Ansible collections cache (keyed on requirements.yml)
                 └─ Install collections [skipped on cache hit]
                      └─ Create vault password file
                           ├─ Run yamllint
                           └─ Run ansible-lint  ← always runs, even if yamllint fails
```

### Caching

| Cache | Key | Path |
|-------|-----|------|
| pip packages | `pip-<hash of requirements-lint.txt>` | `~/.cache/pip` (managed by `actions/setup-python`) |
| Ansible collections | `ansible-collections-<hash of requirements.yml>` | `~/.ansible/collections` |

The collections install step is skipped entirely on a cache hit, saving ~45 seconds per run.
The cache invalidates automatically when `requirements.yml` changes.

### Vault password

The Ansible Vault password is stored as a GitHub Actions secret named `ANSIBLE_VAULT_PASSWORD`.
It is written to `~/.vault_pass.txt` using `printf` (not `echo`) to correctly handle passwords
containing special characters or no trailing newline. The path matches `vault_password_file`
in `ansible.cfg`.

### Linter behaviour

Both linters always report results even if the other fails:

- `yamllint` runs first with `--strict` (configured in `.pre-commit-config.yaml`)
- `ansible-lint` runs with `if: success() || failure()` — never skipped due to yamllint failure

---

## Linting tools

### yamllint

Configured via `.yamllint` (project root). Runs in strict mode. The same configuration is
used by the pre-commit hook for local feedback before push.

### ansible-lint

Configured via `.ansible-lint` (project root):

| Setting | Value | Reason |
|---------|-------|--------|
| `profile` | `moderate` | Balanced — catches real issues without noise |
| `offline` | `true` | Skips galaxy role downloads; roles are mocked |
| `mock_roles` | `markosamuli.linuxbrew` | Vendored galaxy role — prevents "role not found" error |
| `exclude_paths` | `.venv/`, `collections/`, `roles/markosamuli.linuxbrew/`, `playbooks/k8s.yml`, `playbooks/reset-k8s.yml` | Kubespray collection not installed in lint environment |
| `skip_list` | `yaml[line-length]`, `var-naming[no-role-prefix]`, `role-name` | Intentional deviations — see ROLES.md for naming conventions |

Ansible collections required by the playbooks (`community.general`, `ansible.posix`,
`kubernetes.core`) are installed at lint time. The Kubespray collection is excluded
because it is a full git repo (~200 MB) that is unnecessary for linting.

---

## Local pre-commit hooks

Pre-commit is configured in `.pre-commit-config.yaml` and uses system-installed tools
(installed via the `setup_python-uv` role) to avoid version conflicts.

| Hook | Runs on | Notes |
|------|---------|-------|
| `yamllint` | every commit | Fast (~1s); catches YAML errors before push |
| `ansible-lint` | CI only | ~70s locally — too slow for pre-commit; runs in GitHub Actions instead |

Install hooks once after cloning:

```bash
pre-commit install
```

---

## Version pinning

Linting tool versions are pinned in `requirements-lint.txt`:

```
ansible-lint>=25.1,<26
yamllint>=1.35,<2
```

Update these deliberately after testing new versions locally:

```bash
uv tool list          # see current local versions
# update requirements-lint.txt, push, confirm CI passes
```

---

## Dependabot

`.github/dependabot.yml` opens weekly pull requests to bump GitHub Actions versions
(`actions/checkout`, `actions/setup-python`, `actions/cache`). Commit message prefix: `chore`.

---

## Adding a new playbook

When a new playbook is added, check whether it uses modules from a collection not yet
installed in the CI workflow. If so, add the collection to the `Install Ansible collections`
step in `lint.yml`. If it delegates to an external tool like Kubespray, add it to
`exclude_paths` in `.ansible-lint` instead.
