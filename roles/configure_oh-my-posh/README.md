# configure_oh-my-posh

Installs an oh-my-posh prompt theme and wires it into `~/.bashrc`.

## What it does

1. Creates the themes directory (`~/.poshthemes/` by default)
2. Copies the selected theme file from `files/` to the themes directory
3. Checks if oh-my-posh is already initialised in `~/.bashrc`
4. If not, appends a managed block: `eval "$(oh-my-posh init bash --config <theme>)"`

## Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `omp_themes_dir` | `~/.poshthemes/` | Directory where theme files are stored |
| `default_omp_theme` | `debian.omp.yaml` | Theme filename to deploy and activate |
| `home` | `{{ ansible_env.HOME }}` | User home directory |

## Available themes

Theme files are in `roles/configure_oh-my-posh/files/`:
- `debian.omp.yaml` (default)
- `pluto.omp.yaml` / `pluto.omp.json`
- `pluto-deb-red.omp.yaml`
- `pluto-nocache.omp.yaml`
- `pluto-ubu-orange.omp.yaml`
- `epam.omp.yaml` / `epam-deb-red.omp.yaml`

## Usage

```yaml
- name: Configure oh-my-posh
  ansible.builtin.import_role:
    name: configure_oh-my-posh
  become: false
  tags:
    - omp
    - fancy
    - developer
```

## Notes

- Requires `oh-my-posh` to already be installed (via `setup_minimal` brew packages)
- Uses `blockinfile` with a named marker — safe to re-run
- Override `default_omp_theme` in group_vars to use a different theme per host group
