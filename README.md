# Automated Environment Setup Using Ansible

This repository helps automate the initial setup and configuration of Developer and DevOps environments using Ansible.

## LEGO Approach for Environment Setup: Small, Reusable Tasks

Identify small, self-contained components and create separate Ansible roles for each. Ensure these roles are configurable, so you can enable or disable them as needed in a playbook.

## Current set of Ansible roles

```bash
❯ tree -d -L1 roles/
roles/
├── base_setup
├── configure_fzf
├── configure_git
├── configure_oh-my-posh
├── configure_ssh
├── configure_sudo
├── debian_dist_upgrade
├── debian_dist_upgrade_12to13
├── debian_upgrade
├── disable_hibernation
├── install_linuxbrew
├── install_nerd_fonts
├── install_ssh_keys
├── markosamuli.linuxbrew
├── report_done
├── setup_apt_repos
├── setup_cloud-aws
├── setup_cloud-azure
├── setup_cloud-gcp
├── setup_convinience
├── setup_email-server
├── setup_email-tools
├── setup_etckeeper
├── setup_iac-extra
├── setup_iac-terraform
├── setup_kube-extra
├── setup_kubernetes
├── setup_legal_banner
├── setup_minimal
├── setup_network-tools
├── setup_python-pyenv
├── setup_python-uv
├── setup_security-tools
├── setup_vscode
├── upload_fav_bgimages
└── upload_profile_image
```

## Predefined example playbooks

Ideally you might able to use these playbooks without any changes but life is not that simple...

just a list of them for now, usage info going to follow

```bash
❯ tree playbooks/
playbooks/
├── kubespay.yml - kubernetes setup using kubespay ansible collection
├── local.yml - local env setup
├── prerequisite.yml - pre-requisite roles and collections install locally
├── reset-kubespay.yml - tear down kubernetes set up by kubespray
├── site.yml - prepare multiple hosts similarly as a local environment.
└── upgrade.yml - OS update for a set of hosts

```

## How to use content of this repository

This is basically a collection of ansible playbooks and scripts.
Scripts should be used to pre-configuration only, meaning before Ansible.

### Download pre-requisite Ansible collections or roles

```bash
ansible-galaxy collection install -r requirements.yml
```

### Edit invetory variables and configuration

### Run the playbook

```bash
ansible-playbook --ask-become-pass playbooks/local.yml
```
