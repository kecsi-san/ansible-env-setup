# install_linuxbrew

Installs Homebrew (Linuxbrew) by delegating to the `markosamuli.linuxbrew` Galaxy role.

## What it does

- Includes `markosamuli.linuxbrew` via `include_role`
- Handles OS-specific dependencies, the Homebrew installer, and shell integration

## Dependencies

Requires the Galaxy role to be installed first:

```bash
ansible-galaxy install -r requirements.yml
```

The role is declared in `requirements.yml` at version `v2.0.2`.

## Variables

All variables are inherited from `markosamuli.linuxbrew`. Key ones set in group_vars:

| Variable | Value | Description |
|----------|-------|-------------|
| `linuxbrew` | `true` | Enable/disable Linuxbrew installation |
| `linuxbrew_use_installer` | `true` | Use the official Homebrew install script |

## Usage

```yaml
- name: Install linuxbrew
  ansible.builtin.import_role:
    name: install_linuxbrew
  tags:
    - brew
```

## Notes

- Set `linuxbrew: false` in group_vars to skip installation on a host group
- Required before `install_nerd_fonts`, `configure_oh-my-posh`, `configure_fzf`, and brew packages in `setup_minimal`
