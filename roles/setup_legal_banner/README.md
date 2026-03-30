# setup_legal_banner

Deploys a legal/compliance login banner and clears the MOTD.

## What it does

1. Copies `files/banner.txt` to `/etc/issue` and `/etc/issue.net`
2. Sets `Banner /etc/issue.net` in `/etc/ssh/sshd_config`
3. Empties `/etc/motd`
4. Reloads `sshd` to apply the banner immediately

## Usage

```yaml
- name: Setup legal banner
  ansible.builtin.import_role:
    name: setup_legal_banner
  become: true
  tags:
    - banner
    - security
```

## Notes

- Requires `become: true`
- Edit `roles/setup_legal_banner/files/banner.txt` to customise the banner text
- `sshd_config` is validated before writing via `sshd -t -f`
