# Day 02 · Implementation journal

Retrospective notes from the screenshots supplied in `WEEK2(1).docx`; not a live execution transcript.

## 01 — NTP / clock alignment
Initially all three VMs were configured for Baku time. A standalone timezone change alone did not guarantee NTP synchronization. `siem-host` Chrony initially reported `Stratum 0` and `Not synchronised` immediately after restart. After polling upstream pools, it reported `Stratum 3` and `Leap status: Normal`. Linux and Windows clients subsequently selected `192.168.38.132`. Persistent frequency corrections near 12755 ppm remain a virtualization timing investigation.

## 02 — LabShop parser and rules
An early expression used a generic `<field name="action">` for the static `action` field; corrected to `<action>LOGIN_FAILED</action>`. Overlapping Day 01 custom IDs were moved to `100200–100203`. Wazuh accepted the decoder and alerts were recorded at levels 5 and 10.

## 03 — False positive and correlation tests
The monitoring account `monitor`, successful login events and malformed data were tested for inappropriate custom alerts. Multiple failure sources were also exercised to assess `same_srcip` handling. Treat the six tests as separate windows when rerunning.

## 04 — FIM coverage
Realtime create/modify/delete was recorded for Linux `/var/www/html` and Windows `C:\LabShopData`. Windows Registry modification detection was recorded at `HKLM\SOFTWARE\LabShop`. For `/etc`, a temporary 60-second scheduled scan demonstrated scan-based detection. Final restoration to 43200 seconds is not independently captured.

## 05 — SCA remediation
Ubuntu cron file/directory permissions were tightened, changing baseline checks from 92 to 94 passing. On Windows, local password history was changed from 0 to 24, changing 117 to 118 passing. Findings outside those changes remained open.

## 06 — Vulnerability triage
Wazuh Dashboard recorded 103 critical Ubuntu and 71 critical Windows vulnerability findings. The captures do not prove that those findings were patched or disappeared; version-to-advisory and update availability must be verified before remediation claims.

## 07 — Suricata startup and capture
Initial service failed when configured for nonexistent `eth0`. Updating AF_PACKET to `ens33` enabled capture. The one-rule file loaded; `suricata -T` succeeded. `tcpdump` observed Windows-origin `GET /admin`.

## 08 — Suricata alert and SIEM delivery
`fast.log` recorded SID 1000001. Wazuh Agent collected `/var/log/suricata/eve.json`. Wazuh Dashboard displayed `LabShop Admin Page Probe` under built-in rule 86601, level 3, with matching source IP, destination IP and URI. An Apache access-log alert is *not* an acceptable substitute for the Suricata EVE-origin alert.

## 09 — Outstanding closure
Retain verified post-reboot service state, eventual NAT removal, `/etc` FIM interval restoration, exact realtime-vs-scheduled latency notes and three vulnerability/SCA rationales before declaring every Week 2 acceptance item closed.
