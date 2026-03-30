# report_done

Announces playbook completion with a text-to-speech message on the Ansible control node.

## What it does

- Uses `community.general.say` to speak a completion message via the `Zarvox` voice
- Delegates to `localhost` — always runs on the control node regardless of target hosts

## Usage

Append to any playbook as a final role:

```yaml
- name: Report done
  ansible.builtin.import_role:
    name: report_done
  tags:
    - always
```

## Notes

- Requires the `say` command to be available on the control node (macOS built-in; Linux needs `espeak` or `festival`)
- Not currently wired into any playbook — add to `site.yml` or `local.yml` as desired
