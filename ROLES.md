# Roles

Status legend: ✅ Done | 🔧 Implemented (not wired) | 🚧 Incomplete | 📋 Planned

---

## ✅ Done — implemented and wired into a playbook

| Role | Purpose | Playbook(s) |
|------|---------|-------------|
| `configure_etc-hosts` | Manages `/etc/hosts` with cluster node entries | site.yml |
| `configure_fzf` | Adds fzf shell integration to `~/.bashrc` | site.yml |
| `configure_git` | Deploys `~/.gitconfig` | site.yml |
| `configure_oh-my-posh` | Installs Pluto OMP theme and shell init | site.yml |
| `configure_ssh` | Hardens `sshd_config` | site.yml, prerequisite.yml |
| `configure_sudo` | Configures passwordless sudo for `admin_user` | site.yml, local.yml, prerequisite.yml |
| `debian_upgrade` | `apt update && upgrade && autoremove` | site.yml, upgrade.yml |
| `disable_hibernation` | Disables suspend/hibernate via systemd | site.yml |
| `install_linuxbrew` | Installs Homebrew via `markosamuli.linuxbrew` (installed via `ansible-galaxy install -r requirements.yml`) | local.yml |
| `install_nerd_fonts` | Installs Meslo LG + Fira Code Nerd Fonts via Homebrew | site.yml |
| `setup_legal_banner` | Deploys SSH/login banner; clears MOTD | site.yml |
| `setup_longhorn` | Installs Longhorn distributed block storage via Helm | post-k8s.yml |
| `setup_minimal` | Installs base APT packages; optional Homebrew base packages | site.yml, local.yml |
| `setup_network-tools` | Installs network diagnostic tools | site.yml, local.yml |
| `upload_fav_bgimages` | Copies wallpapers to `/usr/share/backgrounds/`; generates GNOME XML descriptor | site.yml |
| `upload_profile_image` | Sets GNOME/GDM profile picture | site.yml |

---

## 🔧 Implemented — has tasks but not wired into any playbook yet

| Role | Purpose | Notes |
|------|---------|-------|
| `debian_dist_upgrade` | Debian major version in-place upgrade | Older/simpler version — likely superseded by `debian_dist_upgrade_12to13`; consider removing |
| `debian_dist_upgrade_12to13` | Full Debian 12→13 migration with disk space check and reboot | Needs its own playbook (e.g. `dist-upgrade.yml`) |
| `report_done` | Text-to-speech playbook completion notification | Could be appended to `site.yml` and `local.yml` |
| `setup_etckeeper` | Git-backs `/etc` via etckeeper | `etckeeper: true` is set in group_vars but role is not in any playbook |
| `setup_kube-extra` | Copies kubeconfig from cluster node; sets `KUBECONFIG` | Needs wiring into `post-k8s.yml` |

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
