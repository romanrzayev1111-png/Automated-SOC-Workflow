# Time synchronization evidence

Original PNGs extracted byte-for-byte from the supplied `WEEK2.docx`. File names are descriptive; `source_member` in the manifest retains the original Word image number. No image was resized or reconstructed.

| Evidence | Capture | What it proves and its limits |
| :--- | :--- | :--- |
| NTP-001 | [001-ubuntu-timezone.png](screenshots/001-ubuntu-timezone.png) | Asia/Baku is configured on ubuntu-web; timedatectl reports synchronized=yes and NTP active. This does not identify the selected NTP peer. |
| NTP-002 | [002-siem-timezone.png](screenshots/002-siem-timezone.png) | siem-host uses Asia/Baku and reports a synchronized system clock with NTP active. |
| NTP-003 | [003-windows-timezone.png](screenshots/003-windows-timezone.png) | Windows selects Azerbaijan Standard Time and displays the Baku timezone and local date. |
| NTP-004 | [004-chrony-upstream-tracking.png](screenshots/004-chrony-upstream-tracking.png) | siem-host Chrony is active, stratum 3, Leap status Normal; frequency correction is 12730.671 ppm slow. |
| NTP-005 | [005-chrony-upstream-sources.png](screenshots/005-chrony-upstream-sources.png) | The server source list selects 91.234.235.13 with ^*; it also lists Ubuntu pools and other NTP sources. |
| NTP-006 | [006-chrony-server-subnet-acl.png](screenshots/006-chrony-server-subnet-acl.png) | The server chrony.conf includes allow 192.168.38.0/24. Only the relevant tail of the file is shown. |
| NTP-007 | [007-chrony-restart-unsynchronized.png](screenshots/007-chrony-restart-unsynchronized.png) | After a Chrony restart, ss shows UDP/123 listening; tracking reports stratum 0 and Not synchronised. This is not the final successful tracking capture. |
| NTP-008 | [008-chrony-client-peer-config.png](screenshots/008-chrony-client-peer-config.png) | ubuntu-web chrony.conf contains server 192.168.38.132 iburst prefer. |
| NTP-009 | [009-chrony-client-selected-source.png](screenshots/009-chrony-client-selected-source.png) | ubuntu-web selects ^* 192.168.38.132; additional external sources remain listed. Internal-only source configuration is not established. |
| NTP-010 | [010-windows-ntp-configuration.png](screenshots/010-windows-ntp-configuration.png) | w32tm applies peer 192.168.38.132,0x8; W32Time becomes Automatic, restarts and reports a successful resync. |
| NTP-011 | [011-windows-ntp-source-status.png](screenshots/011-windows-ntp-source-status.png) | Windows reports source 192.168.38.132,0x8, stratum 4, no leap warning and a last successful sync time. Root dispersion is about 8.12 seconds. |

[Integrity manifest](manifest.json)
