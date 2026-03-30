# Automated Environment Setup Using Ansible

Ansible automation for setting up and maintaining developer and DevOps environments. Uses a modular **LEGO approach**: each role is self-contained and independently runnable via tags.

Supports two scenarios:
- **Local workstation** setup (localhost)
- **Distributed Kubernetes cluster** on bare-metal hosts (via Kubespray)

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

```bash
# Local workstation setup
ansible-playbook --ask-become-pass playbooks/local.yml

# Remote hosts: run prerequisites first, then full setup
ansible-playbook --ask-become-pass playbooks/prerequisite.yml
ansible-playbook --ask-become-pass playbooks/site.yml

# Install Kubernetes cluster (via Kubespray)
ansible-playbook -i inventory/hosts playbooks/kubespray.yml

# Post-Kubernetes setup (Longhorn distributed storage)
ansible-playbook --ask-become-pass playbooks/post-k8s.yml

# OS upgrades across all hosts
ansible-playbook --ask-become-pass playbooks/upgrade.yml
```

### Run specific roles with tags

```bash
ansible-playbook --ask-become-pass -t ssh,sudo playbooks/prerequisite.yml
ansible-playbook --ask-become-pass -t minimal,brew playbooks/local.yml
ansible-playbook --ask-become-pass -t fonts,omp,fzf playbooks/site.yml
```

## Playbooks

| Playbook | Target | Purpose |
|----------|--------|---------|
| `local.yml` | localhost | Local workstation setup and testing |
| `site.yml` | `kube` group | Full setup across remote hosts |
| `prerequisite.yml` | `kube` group | SSH hardening + passwordless sudo (run before site.yml) |
| `kubespray.yml` | `kube` group | Install Kubernetes cluster via Kubespray |
| `reset-kubespray.yml` | `kube` group | Tear down Kubernetes cluster |
| `post-k8s.yml` | `kube` group | Post-cluster setup (Longhorn storage) |
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
| `upload_fav_bgimages` | Uploads wallpaper images to remote hosts |
| `upload_profile_image` | Sets GNOME/GDM profile picture |
| `report_done` | Text-to-speech playbook completion notification |

### Placeholder (not yet implemented)

`setup_cloud-aws`, `setup_cloud-azure`, `setup_cloud-gcp`, `setup_convinience`,
`setup_email-server`, `setup_email-tools`, `setup_iac-terraform`, `setup_iac-extra`,
`setup_python-pyenv`, `setup_python-uv`, `setup_security-tools`, `setup_vscode`,
`setup_apt_repos`, `setup_kubernetes`

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
