# setup_apt_repos

Manages custom APT repositories and installs packages from them.

Local-only role — not included in `site.yml`.

## What it does

### Docker CE

Installs Docker CE from the official Docker apt repository:

1. Adds Docker's GPG key to `/etc/apt/keyrings/docker.asc`
2. Adds the Docker stable apt repository
3. Installs Docker CE packages
4. Adds the current user to the `docker` group (passwordless Docker access)

## Packages installed

| Package | Purpose |
|---------|---------|
| `docker-ce` | Docker Community Edition engine |
| `docker-ce-cli` | Docker CLI |
| `containerd.io` | Container runtime |
| `docker-buildx-plugin` | Extended build capabilities |
| `docker-compose-plugin` | Docker Compose v2 (`docker compose`) |

## Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `docker_arch` | auto-detected | CPU architecture for apt repo (`amd64`, `arm64`, `armhf`) |
| `docker_packages` | see `defaults/main.yml` | Docker packages to install |

## Usage

```yaml
- name: Setup apt repositories
  ansible.builtin.import_role:
    name: setup_apt_repos
  become: true
  tags:
    - apt-repos
    - docker
```

## Notes

- `become: true` — all tasks require root (APT + user group management)
- After first run, log out and back in (or `newgrp docker`) for group membership to take effect
- `docker compose` (v2) is available as a plugin — no separate `docker-compose` binary needed
