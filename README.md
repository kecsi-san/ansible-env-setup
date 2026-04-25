# Automated Environment Setup Using Ansible

Ansible automation for setting up and maintaining developer and DevOps environments. Uses a modular **LEGO approach**: each role is self-contained and independently runnable via tags.

Supports two scenarios:
- **Local workstation** setup (localhost) — tested on **Debian 13 under WSL2** (Windows) and **macOS**
- **Distributed Kubernetes cluster** on bare-metal hosts (via Kubespray) — tested on **Debian 13 nodes**

## Tool Management Philosophy

Tools are managed using three strategies depending on how the tool is distributed and how frequently it is updated:

| # | Method | When to use | Roles |
|---|--------|-------------|-------|
| 1 | **APT** (system package manager) | Rarely changing tools; well-maintained in Debian repos; system-level dependencies | `setup_minimal`, `setup_network-tools`, `debian_upgrade` |
| 2 | **Homebrew** (Linuxbrew) | Frequently updated tools; tools not in APT or lagging behind upstream | `install_linuxbrew`, `install_nerd_fonts`, `setup_minimal` (brew packages), `upgrade_brew` |
| 3 | **uv** (Python package manager) | Tools only available as Python packages; security scanners; linters; IaC helpers | `setup_python-uv`, `upgrade_python-uv` |

> **Rule of thumb:** APT for system stability, Homebrew for freshness, uv for the Python ecosystem.

## Prerequisites

- Python 3 + pip
- Ansible

```bash
pip install -r requirements.txt
ansible-galaxy install -r requirements.yml
```

## Quick Start

### 1. Configure inventory and secrets

```bash
# Copy and fill in your host definitions
cp inventory/hosts.example inventory/hosts

# Copy and fill in infrastructure-specific values
cp inventory/group_vars/all/secrets.yml.example inventory/group_vars/all/secrets.yml
```

Edit `inventory/hosts` with your host IPs and `secrets.yml` with your domain name, DNS servers, SSH user, and kube-vip settings.

### 2. Run a playbook

> **Note:** `--ask-become-pass` is intentionally omitted from all commands below. This project
> configures passwordless sudo via the `configure_sudo` role (run as part of `prerequisite.yml`).
> If you prefer to keep sudo password-protected, add `--ask-become-pass` to each command.
> `prerequisite.yml` itself always requires `--ask-become-pass` since passwordless sudo is not yet
> set up at that point.

```bash
# Local workstation — core system (brew, apt repos, minimal, network, python-uv)
ansible-playbook playbooks/local.yml

# Local workstation — security (sudo, duosecurity repo, fail2ban, rkhunter, lynis, trivy)
ansible-playbook playbooks/local-security.yml

# Local workstation — developer tooling (vscode, go, nodejs, rust)
ansible-playbook playbooks/local-dev.yml

# Local workstation — Cloud and DevOps tooling (terraform, aws, azure, gcp, kube)
ansible-playbook playbooks/local-cloud.yml

# Upgrade local workstation packages (apt, brew, uv)
ansible-playbook playbooks/upgrade-local.yml

# Remote hosts: run prerequisites first (requires password), then full setup
ansible-playbook --ask-become-pass playbooks/prerequisite.yml
ansible-playbook playbooks/k8s-nodes.yml

# Pre-Kubernetes node preparation
ansible-playbook playbooks/pre-k8s.yml

# Install Kubernetes cluster (via Kubespray)
ansible-playbook -b playbooks/k8s.yml

# Post-Kubernetes setup (Longhorn distributed storage)
ansible-playbook playbooks/post-k8s.yml

# OS upgrades across all hosts
ansible-playbook playbooks/upgrade.yml

# Local k3s dev cluster (single-node, localhost)
ansible-playbook playbooks/k3s.yml
ansible-playbook playbooks/reset-k3s.yml   # to uninstall
```

### Run specific roles with tags

```bash
ansible-playbook --ask-become-pass -t ssh,sudo playbooks/prerequisite.yml
ansible-playbook -t minimal,brew playbooks/local.yml
ansible-playbook -t fonts,omp,fzf playbooks/k8s-nodes.yml
```

## Playbooks

### Naming convention

- **Syntax:** lowercase, words separated by hyphens, `.yml` extension — no underscores
- **Pattern:** name reflects what the playbook does and/or where it runs

| Category | Pattern | Examples |
|----------|---------|---------|
| Environment setup | `<target>.yml` | `local.yml`, `k8s-nodes.yml` |
| Kubernetes cluster ops | `[<phase>-]<tool>.yml` | `k8s.yml`, `pre-k8s.yml`, `post-k8s.yml`, `reset-k8s.yml`, `k3s.yml`, `reset-k3s.yml` |
| Maintenance | `<operation>.yml` | `upgrade.yml`, `prerequisite.yml` |
| One-off operations | `<specific-action>.yml` | `dist-upgrade.yml` |

### Inventory

| Playbook | Target | Purpose |
|----------|--------|---------|
| `local.yml` | localhost | Core system setup (brew, apt repos, minimal, network, python-uv) |
| `local-security.yml` | localhost | Security hardening (sudo, duosecurity repo, fail2ban, rkhunter, lynis, trivy) |
| `local-dev.yml` | localhost | Developer tooling (vscode, go, nodejs, rust) — optional, run after local.yml |
| `local-cloud.yml` | localhost | Cloud and DevOps tooling (terraform, iac-extra, aws, azure, gcp, kube) — optional |
| `upgrade-local.yml` | localhost | Upgrade local apt, brew, and uv packages |
| `k8s-nodes.yml` | `kube` group | Full setup across remote hosts |
| `prerequisite.yml` | `kube` group | SSH hardening + passwordless sudo (run before k8s-nodes.yml) |
| `upgrade.yml` | `kube` group | OS package upgrades |
| `pre-k8s.yml` | `kube` group | Node prep before Kubespray (etckeeper) — **bare-metal cluster** |
| `k8s.yml` | `kube` group | Install Kubernetes cluster via Kubespray — **bare-metal cluster** |
| `reset-k8s.yml` | `kube` group | Tear down Kubespray cluster — **bare-metal cluster** |
| `post-k8s.yml` | `kube` group | Post-cluster setup (Longhorn storage) — **bare-metal cluster** |
| `k3s.yml` | localhost | Install single-node k3s cluster — **local dev** (Linux native / macOS via k3d) |
| `reset-k3s.yml` | localhost | Uninstall k3s local dev cluster |
| `personalise.yml` | localhost | Taste-driven setup — fonts, shell prompt, wallpapers, profile image |

## Roles

### Active

| Role | Purpose |
|------|---------|
| `configure_etc-hosts` | Manages `/etc/hosts` with cluster node entries |
| `configure_fzf` | Adds fzf shell integration to `~/.bashrc` |
| `configure_git` | Deploys `~/.gitconfig` |
| `configure_oh-my-posh` | Installs Pluto OMP theme and shell init |
| `configure_ssh` | Hardens `sshd_config` |
| `configure_sudo` | Configures passwordless sudo for `admin_user` |
| `debian_upgrade` | `apt update && upgrade && autoremove` |
| `disable_hibernation` | Disables suspend/hibernate via systemd |
| `install_linuxbrew` | Installs Homebrew (via `markosamuli.linuxbrew` galaxy role, not vendored) |
| `install_nerd_fonts` | Installs Meslo LG + Fira Code Nerd Fonts via Homebrew |
| `setup_etckeeper` | Git-backs `/etc` via etckeeper |
| `setup_kube-extra` | Copies kubeconfig from cluster node; sets `KUBECONFIG` |
| `setup_legal_banner` | Deploys SSH/login banner; clears MOTD |
| `setup_longhorn` | Installs Longhorn distributed block storage via Helm |
| `setup_minimal` | Installs base APT packages; optional Homebrew base packages |
| `setup_network-tools` | Installs network diagnostic tools (APT on Linux, Homebrew on macOS) |
| `setup_k3s` | Single-node local dev cluster — Linux native k3s / macOS via k3d |
| `setup_go-dev-tools` | go, gopls, golangci-lint; optional: delve, goreleaser, ko, air |
| `setup_nodejs-dev-tools` | node, pnpm; optional brew tools + npm global packages |
| `setup_rust-dev-tools` | rustup + stable toolchain (rustc, cargo, rustfmt, clippy); optional cargo tools |
| `setup_vscode` | VS Code via apt (Linux) or Homebrew Cask (macOS); installs configured extensions |
| `upgrade_brew` | `brew update && upgrade && cleanup` — cross-platform (Linux/macOS) |
| `upgrade_python-uv` | `uv tool upgrade --all` + `uv pip install --upgrade` in devops venv |
| `upload_fav_bgimages` | Copies wallpapers to `/usr/share/backgrounds/`; generates GNOME background picker XML |
| `upload_profile_image` | Sets GNOME/GDM profile picture; source path set via `profile_image_src` variable |

### Placeholder (not yet implemented)

`setup_email-server`, `setup_email-tools`,
`setup_mlops-tools`, `setup_aiops-tools`, `setup_mle-tools`

## Inventory Structure

```
inventory/
├── hosts                          # gitignored — copy from hosts.example
├── hosts.example                  # template
└── group_vars/
    ├── all/
    │   ├── all.yml                # Kubespray cluster-wide settings
    │   ├── secrets.yml            # gitignored — copy from secrets.yml.example
    │   └── secrets.yml.example    # template: domain, DNS, SSH user, kube-vip
    ├── kube.yml                   # Feature flags for remote hosts
    ├── local.yml                  # Feature flags for localhost (vaulted values)
    └── k8s_cluster/               # Kubespray network and addons config
```

Key variables in `secrets.yml`: `domain_name`, `admin_user`, `ansible_ssh_user`, `upstream_dns_servers`, `kube_vip_address`, `kube_vip_interface`, `kube_control_plane_host`.

## Kubernetes

Two Kubernetes strategies are supported — each targets a different environment:

| | Kubespray | k3s |
|-|-----------|-----|
| **Target** | Bare-metal remote hosts (`kube` group) | localhost only |
| **Use case** | Production-grade HA cluster | Local development cluster |
| **Nodes** | Multi-node (3 control plane + workers) | Single-node |
| **macOS support** | No | Yes (via k3d) |
| **Playbooks** | `pre-k8s.yml` → `k8s.yml` → `post-k8s.yml` | `k3s.yml` |

### Kubespray (bare-metal cluster)

Uses [kubespray](https://github.com/kubernetes-sigs/kubespray) (release-2.29) configured for:

- HA control plane with kube-vip at `api.k8s.<domain_name>:6443`
- Calico CNI
- 3-node etcd cluster

Kubespray group vars live alongside custom role vars in `inventory/group_vars/` — the same inventory serves both.

Run playbooks in this sequence for a full cluster deployment:

```bash
# 1. SSH keys + passwordless sudo (password required — sudo not yet configured)
ansible-playbook --ask-become-pass playbooks/prerequisite.yml

# 2. Node preparation (etckeeper, future pre-cluster tooling)
ansible-playbook playbooks/pre-k8s.yml

# 3. Install Kubernetes cluster via Kubespray
ansible-playbook -b playbooks/k8s.yml

# 4. Post-cluster setup (Longhorn storage, kubeconfig)
ansible-playbook playbooks/post-k8s.yml
```

### k3s (local dev cluster)

Single-node cluster on localhost — no inventory or SSH required.

- **Linux (WSL2):** native k3s via the official installer script
- **macOS:** k3s via k3d (k3s in Docker) — requires Docker Desktop or OrbStack

```bash
# Install
ansible-playbook playbooks/k3s.yml

# Uninstall
ansible-playbook playbooks/reset-k3s.yml
```
