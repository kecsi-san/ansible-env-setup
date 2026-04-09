# setup_nodejs-dev-tools

Installs Node.js development tooling via Homebrew and npm.

## What it does

| Tool | Source | Default | Purpose |
|------|--------|---------|---------|
| `node` | brew | always | Node.js runtime (latest LTS) + npm |
| `pnpm` | brew | always | Fast, disk-efficient package manager |
| `yarn` | brew | optional | Alternative package manager |
| `typescript` | brew | optional | TypeScript compiler (`tsc`) + type checker |
| `tsx` | brew | optional | Run TypeScript files directly (ts-node alternative) |
| `eslint` | brew | optional | JavaScript/TypeScript linter |
| `prettier` | brew | optional | Opinionated code formatter |
| npm global packages | npm -g | optional | Any packages listed in `nodejs_npm_global_packages` |

## Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `nodejs_dev_enabled` | `true` | Set to `false` to skip the role entirely |
| `nodejs_brew_packages` | `[node, pnpm]` | Core packages — always installed |
| `nodejs_optional_brew_packages` | all `false` | Optional tools — flip to `true` to install |
| `nodejs_npm_global_packages` | `[]` | Extra packages to install globally via npm |

## Usage

```yaml
- name: Setup Node.js development tooling
  ansible.builtin.import_role:
    name: setup_nodejs-dev-tools
  when: nodejs_dev_enabled
  vars:
    nodejs_dev_enabled: true
    nodejs_optional_brew_packages:
      yarn: false
      typescript: false
      tsx: false
      eslint: false
      prettier: false
    nodejs_npm_global_packages: []
  tags:
    - nodejs
    - dev
```

## Notes

- `become: false` — all installs are user-space
- Installs the latest LTS via Homebrew; for multi-version management consider `nvm` or `volta` (not included here)
- `pnpm` is preferred over npm for workspace projects — faster installs, content-addressable store
- `eslint` and `prettier` are usually installed per-project via devDependencies; use global install only for standalone linting scripts
