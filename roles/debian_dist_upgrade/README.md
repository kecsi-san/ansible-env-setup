# debian_dist_upgrade

> **Note:** This role is likely superseded by `debian_dist_upgrade_12to13`. Consider using that role for a more robust Debian major version upgrade with pre-flight checks.

Performs an in-place Debian major version upgrade by replacing `bookworm` with `trixie` in APT sources, running a dist-upgrade, and modernising sources.

## What it does

1. Replaces `bookworm` → `trixie` in `/etc/apt/sources.list`
2. `apt update`
3. Removes `apt-listchanges` to avoid interactive prompts
4. `apt upgrade --without-new-pkgs`
5. `apt dist-upgrade` + autoclean
6. Reboots if packages were upgraded
7. Runs `apt modernize-sources` once on Trixie
8. Final `apt dist-upgrade`

## Usage

```bash
# Not currently wired into any playbook — run directly:
ansible-playbook --ask-become-pass -e "target=kube" -m import_role -a name=debian_dist_upgrade playbooks/site.yml
```

## Notes

- Only runs when `ansible_os_family == 'Debian'` and release is `bookworm`
- No disk space pre-check — use `debian_dist_upgrade_12to13` for a safer upgrade path
