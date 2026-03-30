# setup_kube-extra

Post-cluster setup: copies the kubeconfig from a control plane node to the local machine and configures the `KUBECONFIG` environment variable.

## What it does

1. Copies `.kube/config` from `{{ kube_control_plane_host }}` via SCP to `~/.kube/k8s-<domain>.yaml`
2. Renames the context to `admin@k8s` using `yq`
3. Sets `current-context` to `admin@k8s`
4. Adds `KUBECONFIG` export to `~/.profile`

Runs once on `localhost` (`delegate_to: localhost`, `run_once: true`).

## Variables

| Variable | Source | Description |
|----------|--------|-------------|
| `kube_control_plane_host` | `secrets.yml` | Short SSH hostname of a control plane node |
| `domain_name` | `secrets.yml` | Used to name the kubeconfig file (e.g. `k8s-kinet-local.yaml`) |

## Usage

```yaml
- name: Setup kube-extra
  ansible.builtin.import_role:
    name: setup_kube-extra
  become: false
  tags:
    - kubeconfig
    - kubernetes
```

## Notes

- Requires `yq` and `scp` on the control node (`yq` is installed via `setup_minimal` brew packages)
- Not yet wired into `post-k8s.yml` — add it after `setup_longhorn`
- The task file is currently incomplete (the `lineinfile` task for `.profile` has no arguments)
