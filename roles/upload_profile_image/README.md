# upload_profile_image

Sets the user's GNOME/GDM profile picture on remote hosts.

## What it does

1. Copies `files/.face` to `~/.face` (used by GNOME and X11 applications)
2. Copies the same image to `/var/lib/AccountsService/icons/{{ gdm_user }}`
3. Ensures the AccountsService user config file exists
4. Writes the user info block (`[User]`, `Language`, `XSession`, `Icon`) into the AccountsService config

## Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `upload_profile_image` | `true` | Set to `false` to skip this role |
| `profile_image_file` | `.face` | Image filename in `files/` |
| `home` | `{{ ansible_env.HOME }}` | User home directory |
| `gdm_user` | `{{ ansible_env.USER }}` | Username for AccountsService config |

## Usage

```yaml
- name: Upload profile image
  ansible.builtin.import_role:
    name: upload_profile_image
  become: false
  tags:
    - face
    - desktop
```

## Notes

- Replace `roles/upload_profile_image/files/.face` with your own image (PNG or JPEG, square recommended)
- The AccountsService tasks require `become: true` (applied per-task inside the role)
- Set `upload_profile_image: false` in group_vars to disable on specific host groups
