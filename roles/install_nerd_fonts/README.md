# install_nerd_fonts

Installs Nerd Font variants via Homebrew Cask for use with terminal themes like oh-my-posh.

## What it does

Installs two fonts via `community.general.homebrew_cask`:
- **Meslo LG Nerd Font** (`font-meslo-lg-nerd-font`)
- **Fira Code Nerd Font** (`font-fira-code-nerd-font`)

## Usage

```yaml
- name: Install nerd fonts
  ansible.builtin.import_role:
    name: install_nerd_fonts
  become: false
  tags:
    - fonts
    - desktop
```

## Notes

- Requires Linuxbrew to be installed (`install_linuxbrew` role)
- `become: false` — Homebrew Cask installs fonts into the user's font directory
- Fonts are primarily useful on desktop/developer machines, not headless servers
