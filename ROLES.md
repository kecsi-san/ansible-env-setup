# Roles

Status legend: ✅ Done | 🔧 Implemented (not wired) | 🚧 Incomplete | 📋 Planned

---

## Naming Standard

Role names follow the pattern: **`<verb>_<subject>`** or **`<verb>_<subject>-<qualifier>`**

### Verbs

| Verb | When to use |
|------|-------------|
| `configure_` | Modifying config files, adjusting settings, or wiring shell initialisation |
| `setup_` | Installing packages/services or performing multi-step environment setup |
| `install_` | Installing a single tool or package manager via a package manager |
| `upload_` | Copying or deploying static files to remote hosts |
| `disable_` | Disabling or masking a system feature or service |
| `debian_` | OS-specific upgrade or migration tasks (Debian only) |
| `upgrade_` | Upgrading packages managed by a specific package manager (brew, uv, etc.) |
| `report_` | Notifications or announcements triggered at playbook completion |

### Subject

- Use **lowercase** only
- Use a **hyphen** (`-`) to separate multiple words within the subject: e.g. `setup_network-tools`, `setup_cloud-aws`
- Use an **underscore** (`_`) only as the separator between verb and subject

### Examples

```
configure_ssh          ✅ correct
setup_cloud-aws        ✅ correct
install_linuxbrew      ✅ correct
upload_fav_bgimages    ✅ correct
setupNetworkTools      ❌ wrong — no camelCase
setup_network_tools    ❌ wrong — underscores in subject
networktools_setup     ❌ wrong — subject before verb
```

---

## Directory and File Structure

Every role must have `tasks/main.yml` and `README.md`. Add the others as needed.

```
roles/<role-name>/
├── tasks/
│   └── main.yml           # Required — task definitions
├── defaults/
│   └── main.yml           # User-overridable variables (lowest precedence)
├── vars/
│   ├── main.yml           # Role-internal constants (not meant to be overridden)
│   └── os/
│       └── Debian.yml     # OS-specific variable overrides
├── files/                 # Static files deployed with ansible.builtin.copy
├── templates/             # Jinja2 templates deployed with ansible.builtin.template
├── handlers/
│   └── main.yml           # Handlers triggered by notify:
└── README.md              # Required — purpose, variables, usage, notes
```

Use `roles/role_template/` as a starting point when creating a new role.

---

## ✅ Done — implemented and wired into a playbook

| Role | Purpose | Playbook(s) |
|------|---------|-------------|
| `configure_etc-hosts` | Manages `/etc/hosts` with cluster node entries | site.yml |
| `configure_fzf` | Adds fzf shell integration to `~/.bashrc` | site.yml |
| `configure_git` | Deploys `~/.gitconfig` | site.yml |
| `configure_oh-my-posh` | Installs Pluto OMP theme and shell init | site.yml |
| `configure_ssh` | Deploys SSH authorized key | site.yml, prerequisite.yml |
| `configure_sudo` | Configures passwordless sudo for `admin_user` | site.yml, local.yml, prerequisite.yml |
| `debian_upgrade` | `apt update && upgrade && autoremove` | site.yml, upgrade.yml |
| `disable_hibernation` | Disables suspend/hibernate via systemd | site.yml |
| `install_linuxbrew` | Installs Homebrew via `markosamuli.linuxbrew` galaxy role | local.yml |
| `install_nerd_fonts` | Installs Meslo LG + Fira Code Nerd Fonts via Homebrew | site.yml |
| `setup_legal_banner` | Deploys SSH/login banner; clears MOTD | site.yml |
| `setup_etckeeper` | Git-backs `/etc` via etckeeper | pre-k8s.yml |
| `setup_kube-extra` | Copies kubeconfig from cluster node; sets `KUBECONFIG` | post-k8s.yml |
| `setup_longhorn` | Installs Longhorn distributed block storage via Helm | post-k8s.yml |
| `setup_minimal` | Installs base APT packages; optional Homebrew base packages | site.yml, local.yml |
| `setup_network-tools` | Installs network diagnostic tools | site.yml, local.yml |
| `report_done` | Text-to-speech playbook completion notification | site.yml, local.yml |
| `upload_fav_bgimages` | Copies wallpapers to `/usr/share/backgrounds/`; generates GNOME XML descriptor | site.yml |
| `upload_profile_image` | Sets GNOME/GDM profile picture | site.yml |

---

## 🔧 Implemented — has tasks but not wired into any playbook yet

| Role | Purpose | Notes |
|------|---------|-------|
| `debian_dist_upgrade_12to13` | Full Debian 12→13 migration with disk space check and reboot | Needs its own playbook (e.g. `dist-upgrade.yml`) |

---

## 🚧 Incomplete — needs work before use

_(none currently)_

---

## 📋 Planned — empty placeholders

| Role | Intended Purpose |
|------|-----------------|
| `setup_apt_repos` | Manage custom APT repository sources |
| `setup_cloud-aws` | AWS CLI and tooling setup |
| `setup_cloud-azure` | Azure CLI and tooling setup |
| `setup_cloud-gcp` | GCP CLI and tooling setup |
| `setup_convinience` | General convenience/quality-of-life tools |
| `setup_email-server` | Email server setup |
| `setup_email-tools` | Email client tools |
| `setup_iac-extra` | Additional IaC tools (Terragrunt, Checkov, etc.) |
| `setup_iac-terraform` | Terraform installation and configuration |
| `setup_kubernetes` | Kubernetes node preparation (pre-Kubespray) |
| `setup_python-pyenv` | Python version management via pyenv |
| `setup_python-uv` | Python packaging via uv |
| `setup_security-tools` | Security scanning and hardening utilities |
| `setup_vscode` | VS Code installation and extension setup |
| `upgrade_brew` | Upgrade all Homebrew packages |
| `upgrade_python-uv` | Upgrade all uv-managed tools and packages |
