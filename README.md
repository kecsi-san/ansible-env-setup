# Automated Environment Setup Using Ansible

Ansible automation for setting up and maintaining developer and DevOps environments. Uses a modular **LEGO approach**: each role is self-contained and independently runnable via tags.

Supports two scenarios:
- **Local workstation** setup (localhost) — primarily tested on **Debian 13 under WSL2** on Windows
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
# Local workstation setup
ansible-playbook playbooks/local.yml

# Remote hosts: run prerequisites first (requires password), then full setup
ansible-playbook --ask-become-pass playbooks/prerequisite.yml
ansible-playbook playbooks/k8s-nodes.yml

# Pre-Kubernetes node preparation
ansible-playbook playbooks/pre-kubespray.yml

# Install Kubernetes cluster (via Kubespray)
ansible-playbook -b playbooks/kubespray.yml

# Post-Kubernetes setup (Longhorn distributed storage)
ansible-playbook playbooks/post-kubespray.yml

# OS upgrades across all hosts
ansible-playbook playbooks/upgrade.yml
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
| Kubernetes cluster ops | `[<phase>-]<tool>.yml` | `kubespray.yml`, `pre-kubespray.yml`, `post-kubespray.yml`, `reset-kubespray.yml` |
| Maintenance | `<operation>.yml` | `upgrade.yml`, `prerequisite.yml` |
| One-off operations | `<specific-action>.yml` | `dist-upgrade.yml` |

### Inventory

| Playbook | Target | Purpose |
|----------|--------|---------|
| `local.yml` | localhost | Local workstation setup |
| `k8s-nodes.yml` | `kube` group | Full setup across remote hosts |
| `prerequisite.yml` | `kube` group | SSH hardening + passwordless sudo (run before k8s-nodes.yml) |
| `pre-kubespray.yml` | `kube` group | Node preparation before Kubespray (etckeeper) |
| `kubespray.yml` | `kube` group | Install Kubernetes cluster via Kubespray |
| `reset-kubespray.yml` | `kube` group | Tear down Kubernetes cluster |
| `post-kubespray.yml` | `kube` group | Post-cluster setup (Longhorn storage) |
| `upgrade.yml` | `kube` group | OS package upgrades |

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
| `debian_dist_upgrade_12to13` | Full Debian 12→13 in-place upgrade |
| `disable_hibernation` | Disables suspend/hibernate via systemd |
| `install_linuxbrew` | Installs Homebrew (via `markosamuli.linuxbrew` galaxy role, not vendored) |
| `install_nerd_fonts` | Installs Meslo LG + Fira Code Nerd Fonts via Homebrew |
| `setup_etckeeper` | Git-backs `/etc` via etckeeper |
| `setup_kube-extra` | Copies kubeconfig from cluster node; sets `KUBECONFIG` |
| `setup_legal_banner` | Deploys SSH/login banner; clears MOTD |
| `setup_longhorn` | Installs Longhorn distributed block storage via Helm |
| `setup_minimal` | Installs base APT packages; optional Homebrew base packages |
| `setup_network-tools` | Installs network diagnostic tools |
| `setup_go-dev-tools` | go, gopls, golangci-lint; optional: delve, goreleaser, ko, air |
| `setup_nodejs-dev-tools` | node, pnpm; optional brew tools + npm global packages |
| `setup_rust-dev-tools` | rustup + stable toolchain (rustc, cargo, rustfmt, clippy); optional cargo tools |
| `upload_fav_bgimages` | Copies wallpapers to `/usr/share/backgrounds/`; generates GNOME background picker XML |
| `upload_profile_image` | Sets GNOME/GDM profile picture |

### Placeholder (not yet implemented)

`setup_convinience`, `setup_email-server`, `setup_email-tools`,
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

Uses [kubespray](https://github.com/kubernetes-sigs/kubespray) (release-2.29) configured for:

- HA control plane with kube-vip at `api.k8s.<domain_name>:6443`
- Calico CNI
- 3-node etcd cluster

Kubespray group vars live alongside custom role vars in `inventory/group_vars/` — the same inventory serves both.

### Kubernetes cluster setup order

Run playbooks in this sequence for a full cluster deployment:

```bash
# 1. SSH keys + passwordless sudo (password required — sudo not yet configured)
ansible-playbook --ask-become-pass playbooks/prerequisite.yml

# 2. Node preparation (etckeeper, future pre-cluster tooling)
ansible-playbook playbooks/pre-kubespray.yml

# 3. Install Kubernetes cluster via Kubespray
ansible-playbook -b playbooks/kubespray.yml

# 4. Post-cluster setup (Longhorn storage, kubeconfig)
ansible-playbook playbooks/post-kubespray.yml
```
