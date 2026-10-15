# Recorded architecture

[Vector diagram](architecture.svg) · [High-resolution diagram](architecture.png) · [PDF diagram](architecture.pdf)

![Day 01 system architecture](architecture.svg)

| System | Internal IP | OS / role | RAM | vCPU | Virtual disk | Recorded adapters |
| :--- | :--- | :--- | ---: | ---: | ---: | :--- |
| siem-host | 192.168.38.132/24 | Ubuntu monitoring server; Wazuh 4.14.7 | 16 GB | 6 | 500 GB | NAT + Custom VMnet1 |
| ubuntu-web | 192.168.38.131/24 | Ubuntu 22.04; Apache; Wazuh agent | 4 GB | 2 | 500 GB | Custom VMnet1 in resource capture |
| win-client | 192.168.38.133/24 | Windows 10 Enterprise Evaluation; Sysmon; Wazuh agent | 4 GB | 4 | 60 GB | Custom VMnet1 in resource capture |

The server's NAT-side interface shows `192.168.121.156/24` on `ens33`; the host-only interface is `ens36`. VMnet1 is `192.168.38.0/24`, Host-only, with DHCP enabled. Both Linux captures show the `dynamic` address flag. Stable static addressing or reservations must be verified rather than assumed.

VMware resource screenshots E01–E03 establish the allocations above. The total assigned RAM is **24 GB**, compared with the 22 GB baseline. The Linux endpoint is assigned 4 GB instead of 2 GB; Windows has 4 vCPUs instead of 2 and a 60 GB disk instead of the required 80 GB. Both Linux disks show 500 GB rather than 40 GB / 250 GB. Virtual disk capacity does not establish physical host usage.

The source notes state that endpoint NAT adapters were temporarily added for software downloads. No final route table or post-installation adapter inventory proves removal. Do not infer permanent internet isolation from the initial resource screenshots alone.

This drawing shows observed roles and addressing, not a measured packet capture or a complete firewall policy. Enrollment commonly uses TCP 1515 and event forwarding TCP 1514; validate the actual local configuration before documenting port-specific rules. The dashboard's configured HTTPS port must also be confirmed locally.
