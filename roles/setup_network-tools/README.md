# setup_network-tools

Installs a curated set of network diagnostic and monitoring tools via APT.

## What it does

- Loads OS-specific package list from `vars/os/{{ ansible_distribution }}.yml`
- Installs all packages in `network_packages` via APT

## Packages installed (Debian)

`dnsutils`, `ebtables`, `ethtool`, `iftop`, `iperf3`, `iproute2`, `iptables`,
`iputils-ping`, `mtr-tiny`, `net-tools`, `nmap`, `rsync`, `socat`, `tcpdump`,
`traceroute`, `whois`, `xfsprogs`

## Usage

```yaml
- name: Setup network tools
  ansible.builtin.import_role:
    name: setup_network-tools
  become: true
  tags:
    - network
```

## Notes

- Requires `become: true`
- OS-specific package lists are in `vars/os/Debian.yml` and `vars/os/Ubuntu.yml`
- Override `network_packages` in group_vars to customise per host group
