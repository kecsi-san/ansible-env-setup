# setup_iac-terraform

Installs Terraform and core IaC security/quality tooling via Homebrew.

## What it does

Installs the following via Homebrew (Tier 2 — frequently updated):

| Tool | Purpose |
|------|---------|
| `terraform` | Infrastructure as Code provisioning |
| `terraform-docs` | Auto-generates documentation from Terraform modules |
| `tflint` | Terraform linter and static analysis |
| `trivy` | Vulnerability and misconfiguration scanner (replaces tfsec) |

> `checkov` (IaC security scanner) is handled by `setup_python-uv` as a `uv tool install` — no need to install it here.

## Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `iac_brew_packages` | see `defaults/main.yml` | List of Homebrew packages to install |

## Usage

```yaml
- name: Setup IaC Terraform tooling
  ansible.builtin.import_role:
    name: setup_iac-terraform
  become: false
  tags:
    - iac
    - terraform
```

## Notes

- `become: false` — Homebrew runs in user space
- Requires Homebrew (`install_linuxbrew` role)
- See [Tool Management Philosophy](../../README.md#tool-management-philosophy)
