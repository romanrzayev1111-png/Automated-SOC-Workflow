# Day 02 · Acceptance matrix

This matrix reflects only the supplied 25-page Week 2 screenshot document and chat-confirmed test results; no VM was remotely replayed by this documentation step.

| Area | Status | Basis / remaining requirement |
| :--- | :--- | :--- |
| LabShop log decoder | Recorded | `labshop` syslog-style parsing and manager `wazuh-logtest` evidence |
| Single failed login | Recorded | Custom Wazuh `100100`, level 5 |
| Same-source brute-force | Recorded | Custom Wazuh `100101`, level 10 |
| Six LabShop test cases | Recorded | Normal, repeated, monitor, distributed, success and malformed input |
| Linux web FIM | Recorded | File added, modified, deleted under `/var/www/html` |
| Windows file FIM | Recorded | File added, modified, deleted under `C:\LabShopData` |
| Registry FIM | Recorded | `HKLM\SOFTWARE\LabShop` changes |
| Scheduled Linux FIM | Partial | `/etc` test done at 60 seconds; formal latency comparison / 43200-second restore proof open |
| Ubuntu SCA | Recorded | 92→94 passing after two permissions fixes |
| Windows SCA | Recorded | 117→118 passing after PasswordHistorySize=24 |
| Third failed SCA rationale | Open | Record a named unremediated finding and risk justification |
| Vulnerability inventory | Recorded | 103 critical Linux, 71 critical Windows findings |
| CVE remediation | Open | Neither confirmed patches nor updated inventory clearing findings |
| Suricata custom rule | Recorded | SID `1000001`; HTTP `/admin`; `suricata -T` success |
| Suricata → Wazuh | Recorded | EVE JSON location, Wazuh `86601` level 3, signature 1000001 in dashboard |
| NTP synchronization | Recorded | `siem-host` upstream Normal; endpoints point to server |
| Long-term clock drift | Open | Correct abnormal frequency adjustment / test sustained synchronization |
| Reboot persistence | Open | `systemctl is-enabled` is not a real post-reboot validation |
| Final NAT isolation | Open | Endpoint NAT still observed in the Suricata `ip addr` capture |
| GitHub evidence binaries | Open | Screenshots packaged separately from markdown until upload is confirmed |

**Overall:** implementation evidence is strong, but unresolved checks are explicitly retained rather than described as PASS.
