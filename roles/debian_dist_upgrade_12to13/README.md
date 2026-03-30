# debian_dist_upgrade_12to13

Performs a safe, fully automated in-place upgrade from Debian 12 (Bookworm) to Debian 13 (Trixie).

## What it does

1. Skips the host if not running Debian 12
2. Verifies at least 5 GiB free disk space on `/`
3. Brings Debian 12 fully up to date (`apt dist-upgrade`)
4. Reboots if required before the major upgrade
5. Replaces `bookworm` → `trixie` in `/etc/apt/sources.list` and all files under `/etc/apt/sources.list.d/`
6. Runs `apt dist-upgrade` to move to Debian 13
7. Verifies the system is now on Debian 13 (fails fast if not)
8. `apt autoremove` + `apt clean`
9. Reboots into Trixie
10. Runs `apt modernize-sources`
11. Pauses 5 minutes (stagger upgrades across multiple hosts)

## Usage

This role is not yet wired into a playbook. Create a dedicated playbook or run ad-hoc:

```bash
ansible-playbook --ask-become-pass playbooks/site.yml --tags dist-upgrade
```

## Notes

- Requires `become: true`
- Safe to run on multiple hosts — the 5-minute pause staggers reboots
- Third-party APT repos in `/etc/apt/sources.list.d/` are also migrated from bookworm to trixie
- Role aborts cleanly if the host is not Debian 12 or if disk space is insufficient
