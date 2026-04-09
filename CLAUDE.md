# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Repo Does

Ansible automation for setting up and maintaining developer and DevOps environments. Uses a modular "LEGO" approach: each Ansible role is self-contained and independently runnable. Supports both local workstation setup and a distributed Kubernetes cluster (via Kubespray).

## Common Commands

```bash
# Install dependencies
pip install -r requirements.txt
ansible-galaxy install -r requirements.yml

# Run local workstation setup (uses localhost)
ansible-playbook playbooks/local.yml

# Run setup across kube group hosts
ansible-playbook playbooks/k8s-nodes.yml

# Run prerequisite SSH/sudo setup before k8s-nodes.yml (--ask-become-pass required here only — passwordless sudo not yet configured)
ansible-playbook --ask-become-pass playbooks/prerequisite.yml

# Pre-Kubernetes node preparation (etckeeper etc.)
ansible-playbook playbooks/pre-kubespray.yml

# Install Kubernetes cluster
ansible-playbook -b playbooks/kubespray.yml

# Reset/tear down Kubernetes cluster
ansible-playbook playbooks/reset-kubespray.yml

# Post-Kubernetes setup (Longhorn storage etc.)
ansible-playbook playbooks/post-kubespray.yml

# OS upgrades on all kube group hosts
ansible-playbook playbooks/upgrade.yml

# Run only specific roles using tags
ansible-playbook --ask-become-pass -t ssh,sudo playbooks/prerequisite.yml
ansible-playbook -t minimal,brew playbooks/local.yml

# Dry run (check mode)
ansible-playbook --check playbooks/local.yml

# Syntax check
ansible-playbook --syntax-check playbooks/local.yml
```

## Architecture

### Playbooks vs Roles

**Playbooks** (`playbooks/`) orchestrate roles for specific scenarios:
- `local.yml` — localhost only; used for testing and local workstation setup
- `k8s-nodes.yml` — mirrors local.yml but targets `kube` group (remote hosts)
- `prerequisite.yml` — must run before `k8s-nodes.yml`; sets up SSH keys and passwordless sudo
- `kubespray.yml` / `reset-kubespray.yml` — delegate entirely to the Kubespray collection
- `pre-kubespray.yml` — runs after `prerequisite.yml` and before `kubespray.yml`; prepares nodes (etckeeper)
- `post-kubespray.yml` — runs after Kubernetes cluster is up; installs cluster-level tools (Longhorn, kube-extra)
- `upgrade.yml` — OS package upgrades across all kube hosts

**Playbook naming convention:**
- Lowercase, hyphens only (no underscores), `.yml` extension
- Categories and patterns:
  - Environment setup → `<target>.yml` (e.g. `local.yml`, `k8s-nodes.yml`)
  - Kubernetes cluster ops → `[<phase>-]<tool>.yml` (e.g. `kubespray.yml`, `pre-kubespray.yml`, `post-kubespray.yml`, `reset-kubespray.yml`)
  - Maintenance → `<operation>.yml` (e.g. `upgrade.yml`, `prerequisite.yml`)
  - One-off operations → `<specific-action>.yml` (e.g. `dist-upgrade.yml`)

**Roles** (`roles/`) are the building blocks. The LEGO principle means roles should have no dependencies on each other. Add new functionality by writing a new role and including it in the appropriate playbook.

### Roles Reference

#### Active / Implemented

| Role | Purpose |
|------|---------|
| `configure_etc-hosts` | Manages `/etc/hosts` with kube group IPs and domain names |
| `configure_fzf` | Adds fzf initialization to `~/.bashrc` (idempotent) |
| `configure_git` | Copies `~/.gitconfig` from static file |
| `configure_oh-my-posh` | Installs Pluto OMP theme; adds init block to `~/.bashrc` |
| `configure_ssh` | Hardens `/etc/ssh/sshd_config` |
| `configure_sudo` | Creates `/etc/sudoers.d/{user}` with NOPASSWD (visudo-validated) |
| `debian_upgrade` | `apt update && upgrade && autoremove --purge` |
| `debian_dist_upgrade_12to13` | Full Debian 12→13 migration; verifies 5GB free space; reboots |
| `disable_hibernation` | Creates `/etc/systemd/sleep.conf.d/nosuspend.conf`; masks sleep targets |
| `install_linuxbrew` | Installs Homebrew via `markosamuli.linuxbrew` (galaxy role, not vendored) |
| `install_nerd_fonts` | Installs Meslo LG + Fira Code Nerd Fonts via `homebrew_cask` |
| `setup_etckeeper` | Installs etckeeper; initialises git-backed `/etc` tracking |
| `setup_legal_banner` | Copies `banner.txt` to `/etc/issue*`; clears MOTD; reloads sshd |
| `setup_longhorn` | Installs iSCSI deps, longhornctl, and Longhorn via Helm |
| `setup_minimal` | Installs base + compression APT packages; optional brew base packages |
| `setup_network-tools` | Installs network diagnostic APT packages |
| `setup_python-uv` | Installs uv CLI tools (checkov, ansible, black, etc.) and Python library packages into `~/.venv/devops` |
| `setup_kube-extra` | Copies kubeconfig from cluster; adjusts context via yq; sets `KUBECONFIG` |
| `upload_fav_bgimages` | Copies wallpapers to `/usr/share/backgrounds/`; generates GNOME background picker XML |
| `upload_profile_image` | Copies `~/.face` and AccountsService profile image (GNOME/GDM) |

#### Placeholder Roles (empty `tasks/main.yml`)

`setup_cloud-aws`, `setup_cloud-azure`, `setup_cloud-gcp`, `setup_convinience`, `setup_email-server`, `setup_email-tools`, `setup_iac-terraform`, `setup_iac-extra`, `setup_security-tools`, `setup_vscode`, `setup_apt_repos`, `setup_kubernetes`

### Inventory Structure

`inventory/hosts` (gitignored — copy from `inventory/hosts.example`) defines:
- `local` group → `127.0.0.1` (localhost)
- `kube` group → physical servers (defined in `inventory/hosts`, gitignored)
- Kubernetes sub-groups under `k8s_cluster`: `kube_control_plane` (3 nodes), `kube_node` (4 nodes), `etcd` (3 nodes)
- `api.k8s` → `kube_vip_address` (Kubernetes API load balancer VIP via kube-vip, defined in `secrets.yml`)

Group variables in `inventory/group_vars/`:
- `all/all.yml` — Kubernetes cluster-wide settings (API server domain, load balancer)
- `all/secrets.yml` — **gitignored**; holds `domain_name`, `upstream_dns_servers`, `kube_vip_address`, `kube_vip_interface`. Copy from `secrets.yml.example`.
- `k8s_cluster/` — Network plugin (Calico) and addons config
- `kube.yml` — SSH user, Python interpreter, feature flags for the kube group
- `local.yml` — Same variables scoped to localhost

Key variables that control what gets installed: `linuxbrew: true/false`, `etckeeper: true/false`, `domain_name`, `admin_user`.

Variables `ansible_ssh_user` and `admin_user` are defined in `secrets.yml` (gitignored). `remote_user` in playbooks references `{{ ansible_ssh_user }}`.

Sensitive values (`admin_email`, `admin_full_name`, `git_user_signkey`, `git_user_email`) are Ansible-vaulted in `group_vars/local.yml`.

The `setup_kube-extra` role requires `kube_control_plane_host` to be set (short SSH hostname of a control plane node) — add it to `secrets.yml`.

### Role Conventions

Standard role layout:
```
roles/<role-name>/
├── tasks/main.yml
├── vars/main.yml          # Role-specific variables
├── vars/os/Debian.yml     # OS-specific overrides
├── files/                 # Static files
├── templates/             # Jinja2 templates
└── defaults/main.yml      # Overridable defaults
```

- Target OS: Debian/Ubuntu only; OS-specific vars go in `vars/os/Debian.yml`
- Use `become: true` for system-level tasks; omit or use `become: false` for user-level tasks
- SSH user is defined via `admin_user` / `ansible_ssh_user` in `secrets.yml`; uses Ed25519 key (`~/.ssh/id_ed25519`)
- Prefer Linuxbrew for tools that update frequently; use APT for system packages

### Tagging

Tags enable selective role execution without running the full playbook:
- `local.yml` tags: `sudo`, `brew`, `minimal`, `network`
- `k8s-nodes.yml` tags: `update`, `ssh`, `hosts`, `banner`, `fonts`, `omp`, `fzf`, `gitconfig`, `hibernation`

Always tag new roles consistently so users can run them individually.

### Kubernetes Setup

Two strategies, two different targets:

**Kubespray — bare-metal multi-node cluster (`kube` group)**
- Uses `kubernetes-sigs/kubespray` collection (release-2.29 branch, installed via `requirements.yml`)
- HA control plane with kube-vip at `api.k8s.<domain_name>:6443`, Calico CNI, 3-node etcd
- Kubespray group vars live in `inventory/group_vars/` alongside custom role vars — same inventory serves both
- Post-cluster setup (`post-kubespray.yml`) installs Longhorn distributed block storage via `setup_longhorn`

**k3s — single-node local dev cluster (localhost)**
- Linux (WSL2): native k3s via official installer script (`get.k3s.io`)
- macOS: k3s via k3d (k3s in Docker) installed through Homebrew — requires Docker Desktop or OrbStack
- Kubeconfig written to `~/.kube/k3s.yaml` and appended to `KUBECONFIG` in `~/.bashrc`
- Managed by `setup_k3s` role; playbooks: `k3s.yml` (install), `reset-k3s.yml` (uninstall)
