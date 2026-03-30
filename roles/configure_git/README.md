# configure_git

Deploys a static `~/.gitconfig` to the remote user's home directory.

## What it does

- Copies `files/gitconfig` to `{{ ansible_env.HOME }}/.gitconfig`
- Sets owner and group to the current user

## Variables

The `gitconfig` file itself references these variables (resolved at template time if using vault):

| Variable | Source | Description |
|----------|--------|-------------|
| `admin_full_name` | vaulted in `local.yml` | Git user name |
| `admin_email` | vaulted in `local.yml` | Git user email |
| `git_signing_key` | vaulted in `local.yml` | GPG signing key ID |

## Usage

```yaml
- name: Configure git
  ansible.builtin.import_role:
    name: configure_git
  become: false
  tags:
    - gitconfig
    - git
    - developer
```

## Notes

- The `gitconfig` file is static — edit `files/gitconfig` directly to change git settings
- GPG commit signing is enabled by default (`gpgsign = true`)
