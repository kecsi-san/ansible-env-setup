# configure_ssh

Deploys the SSH public key to the remote user's `authorized_keys`.

## What it does

- Reads the Ed25519 public key from `~/.ssh/{{ ansible_ssh_pub_key_file }}` on the control node
- Adds it to the remote user's `authorized_keys` via `ansible.posix.authorized_key`

## Variables

| Variable | Source | Description |
|----------|--------|-------------|
| `ansible_ssh_user` | `secrets.yml` | Remote user whose `authorized_keys` is updated |
| `ansible_ssh_pub_key_file` | `kube.yml` | Public key filename (e.g. `id_ed25519.pub`) |

## Usage

```yaml
- name: Configure SSH
  ansible.builtin.import_role:
    name: configure_ssh
  become: true
  tags:
    - ssh
    - prerequisites
    - developer
```

## Notes

- Run this role via `prerequisite.yml` before `site.yml` so key-based auth is in place
- `manage_dir: yes` ensures `~/.ssh/` is created with correct permissions if missing
