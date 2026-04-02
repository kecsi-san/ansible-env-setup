# setup_kube-extra

Installs kubectl and helm, sets up system-wide bash completions, and adds a `k=kubectl` alias.

## What it does

1. Installs `kubectl` via Homebrew (Tier 2 — follows k8s release cadence)
2. Installs `helm` via Homebrew (Tier 2 — frequently updated)
3. Generates and installs bash completion for `kubectl` to `/etc/bash_completion.d/kubectl`
4. Generates and installs bash completion for `helm` to `/etc/bash_completion.d/helm`
5. Creates `/etc/profile.d/kubectl-alias.sh` with `k=kubectl` alias and tab completion for `k`

## Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `kubectl_bin` | `/home/linuxbrew/.linuxbrew/bin/kubectl` | Path to kubectl binary |
| `helm_bin` | `/home/linuxbrew/.linuxbrew/bin/helm` | Path to helm binary |

## Usage

```yaml
- name: Setup kube extra tooling
  ansible.builtin.import_role:
    name: setup_kube-extra
  tags:
    - kube
    - kubernetes
```

## Notes

- Requires Homebrew (`install_linuxbrew` role)
- Completions are system-wide (`/etc/bash_completion.d/`) — requires `become: true` internally
- The `k` alias completion relies on `__start_kubectl` being loaded from the kubectl completion script
- Open new shell (or `source /etc/profile.d/kubectl-alias.sh`) after first run for alias to take effect
