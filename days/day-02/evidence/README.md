# Day 02 evidence register

Original PNGs extracted byte-for-byte from the supplied `WEEK2.docx`. File names are descriptive; `source_member` in the manifest retains the original Word image number. No image was resized or reconstructed.

| Evidence | Capture | What it proves and its limits |
| :--- | :--- | :--- |
| W2-012 | [012-labshop-log-format.png](screenshots/012-labshop-log-format.png) | tail shows syslog-style LabShop LOGIN_FAILED records with user and src fields in /var/log/labshop/app.log. |
| W2-013 | [013-labshop-agent-localfile.png](screenshots/013-labshop-agent-localfile.png) | The endpoint localfile fragment collects /var/log/labshop/app.log as syslog. |
| W2-014 | [014-labshop-decoder-definitions.png](screenshots/014-labshop-decoder-definitions.png) | The captured parent/child decoders match program labshop and extract action,dstuser,srcip using a leading \w+ action capture. |
| W2-015 | [015-labshop-decoder-logtest.png](screenshots/015-labshop-decoder-logtest.png) | Wazuh-logtest 4.14.7 decodes LOGIN_FAILED, admin and 192.168.38.133. The capture establishes Phase 2 fields. |
| W2-016 | [016-labshop-rule-definitions.png](screenshots/016-labshop-rule-definitions.png) | Rules 100100/5 and 100101/10 use action, monitor exclusion, frequency=5, timeframe=60, same_srcip and MITRE T1110. |
| W2-017 | [017-test1-single-failure-command.png](screenshots/017-test1-single-failure-command.png) | The generator is invoked three times with fail admin 192.168.38.133 1. |
| W2-018 | [018-test1-single-failure-dashboard.png](screenshots/018-test1-single-failure-dashboard.png) | Three ubuntu-web dashboard rows show failed-login rule 100100 at level 5. |
| W2-019 | [019-test2-brute-force-command.png](screenshots/019-test2-brute-force-command.png) | The generator is invoked three times with fail admin 192.168.38.133 6. Exact per-event timing is not shown. |
| W2-020 | [020-test2-brute-force-dashboard.png](screenshots/020-test2-brute-force-dashboard.png) | The dashboard shows three 100101 level-10 correlation alerts; the description says five failures in 60 seconds. |
| W2-021 | [021-test3-monitor-account-command.png](screenshots/021-test3-monitor-account-command.png) | Three generator invocations use fail monitor 10.10.10.1 1. |
| W2-022 | [022-test3-monitor-logtest-fallback.png](screenshots/022-test3-monitor-logtest-fallback.png) | monitor decodes correctly and does not match the custom failure rule in the displayed test; generic rule 1002, level 2, does match. This is not a zero-rule result. |
| W2-023 | [023-test4-split-source-command.png](screenshots/023-test4-split-source-command.png) | Two generator invocations request three failures from 10.10.10.50 and three from 10.10.10.60. |
| W2-024 | [024-test4-split-source-dashboard.png](screenshots/024-test4-split-source-dashboard.png) | The associated dashboard crop includes 100101/10 and two 100100/5 rows. Source-IP fields and full test context are absent; a clean negative result is not demonstrated. |
| W2-025 | [025-test5-successful-login-command.png](screenshots/025-test5-successful-login-command.png) | The generator is invoked twice with ok alice 10.10.10.50 2. |
| W2-026 | [026-test5-successful-login-log.png](screenshots/026-test5-successful-login-log.png) | The raw log contains LOGIN_OK records for alice. This does not independently verify the absence of a custom dashboard alert. |
| W2-027 | [027-test6-malformed-log-command.png](screenshots/027-test6-malformed-log-command.png) | An INVALID_DATA test=hello message is appended with a syslog-style prefix; tail shows the resulting raw line. |
| W2-028 | [028-test6-malformed-logtest.png](screenshots/028-test6-malformed-logtest.png) | The malformed line reaches Phase 1 pre-decoding, with hostname and program_name. Structured field extraction and the final rule verdict are not shown. |
| W2-029 | [029-linux-realtime-fim-config.png](screenshots/029-linux-realtime-fim-config.png) | The Linux syscheck configuration adds realtime/check_all/report_changes monitoring for /var/www/html. |
| W2-030 | [030-linux-fim-create-command.png](screenshots/030-linux-fim-create-command.png) | touch creates /var/www/html/fim-test. |
| W2-031 | [031-linux-fim-create-dashboard.png](screenshots/031-linux-fim-create-dashboard.png) | ubuntu-web rows show file-added rule 554/5 and integrity-changed rule 550/7. |
| W2-032 | [032-linux-fim-realtime-detail.png](screenshots/032-linux-fim-realtime-detail.png) | The expanded record identifies syscheck.mode=realtime and path /var/www/html/fim-test, with timestamps and hash fields. |
| W2-033 | [033-linux-fim-modify-command.png](screenshots/033-linux-fim-modify-command.png) | echo overwrites the monitored test file with Modified Content. |
| W2-034 | [034-linux-fim-modify-dashboard.png](screenshots/034-linux-fim-modify-dashboard.png) | The dashboard lists integrity-changed rule 550 at level 7 for ubuntu-web. |
| W2-035 | [035-linux-fim-delete-command.png](screenshots/035-linux-fim-delete-command.png) | The terminal deletes the single test path with rm -rf. The guide uses rm -- for a known regular file as an explicitly safer replay. |
| W2-036 | [036-linux-fim-delete-dashboard.png](screenshots/036-linux-fim-delete-dashboard.png) | The dashboard includes File deleted rule 553 at level 7. |
| W2-037 | [037-windows-fim-registry-config.png](screenshots/037-windows-fim-registry-config.png) | Select-String shows realtime file monitoring for C:\LabShopData and arch=both registry monitoring for HKLM\SOFTWARE\LabShop. |
| W2-038 | [038-windows-fim-create-command.png](screenshots/038-windows-fim-create-command.png) | Set-Content writes Original LabShop Data to C:\LabShopData\test.txt. |
| W2-039 | [039-windows-fim-create-dashboard.png](screenshots/039-windows-fim-create-dashboard.png) | win-client inventory rows show file-added 554/5 and integrity-changed 550/7. |
| W2-040 | [040-windows-fim-modify-command.png](screenshots/040-windows-fim-modify-command.png) | Add-Content appends Modified LabShop Data to the monitored file. |
| W2-041 | [041-windows-fim-modify-dashboard.png](screenshots/041-windows-fim-modify-dashboard.png) | win-client rows include integrity-changed rule 550/7. Raw diff details are not expanded in this crop. |
| W2-042 | [042-windows-fim-delete-command.png](screenshots/042-windows-fim-delete-command.png) | Remove-Item deletes C:\LabShopData\test.txt. |
| W2-043 | [043-windows-fim-delete-dashboard.png](screenshots/043-windows-fim-delete-dashboard.png) | win-client dashboard includes file-deleted rule 553/7. |
| W2-044 | [044-registry-modification-command.png](screenshots/044-registry-modification-command.png) | Set-ItemProperty changes the Environment value under HKLM:\SOFTWARE\LabShop to Development. |
| W2-045 | [045-registry-modification-dashboard.png](screenshots/045-registry-modification-dashboard.png) | Expanded columns identify HKLM\SOFTWARE\LabShop with modified entries: registry-value rule 750/5 and registry-key rule 594/5. |
| W2-046 | [046-scheduled-fim-original-config.png](screenshots/046-scheduled-fim-original-config.png) | The original syscheck block sets frequency 43200, scan_on_start=yes, scheduled system directories and realtime web-directory monitoring. |
| W2-047 | [047-scheduled-fim-test-frequency.png](screenshots/047-scheduled-fim-test-frequency.png) | The agent log states File integrity monitoring scan frequency: 60 seconds. This supports a temporary test setting, not a restored 12-hour interval. |
| W2-048 | [048-scheduled-fim-create-command.png](screenshots/048-scheduled-fim-create-command.png) | tee creates /etc/labshop-fim-test.txt with Original FIM Content. |
| W2-049 | [049-scheduled-fim-create-dashboard.png](screenshots/049-scheduled-fim-create-dashboard.png) | The dashboard shows a file-added 554/5 row. The path/mode fields are not expanded here. |
| W2-050 | [050-scheduled-fim-modify-command.png](screenshots/050-scheduled-fim-modify-command.png) | date displays 2026-10-30 14:17:52 before the test file is modified. This is the command timestamp, not an end-to-end latency measurement. |
| W2-051 | [051-scheduled-fim-modify-dashboard.png](screenshots/051-scheduled-fim-modify-dashboard.png) | Integrity-changed rule 550/7 appears alongside a session event. The crop alone is insufficient for precise realtime-versus-scheduled timing. |
| W2-052 | [052-ubuntu-sca-baseline.png](screenshots/052-ubuntu-sca-baseline.png) | Ubuntu CIS 22.04 v2.0.0 baseline: 92 passed, 104 failed, 11 not applicable; score 46%. |
| W2-053 | [053-windows-sca-baseline.png](screenshots/053-windows-sca-baseline.png) | Windows 10 Enterprise CIS v4.0.0 baseline: 117 passed, 302 failed, 5 not applicable; score 27%. |
| W2-054 | [054-ubuntu-sca-check-definitions.png](screenshots/054-ubuntu-sca-check-definitions.png) | The policy excerpt identifies checks 28626 (/etc/crontab) and 28627 (/etc/cron.hourly), with neighboring checks. |
| W2-055 | [055-ubuntu-sca-remediation-script.png](screenshots/055-ubuntu-sca-remediation-script.png) | The captured script saves permission modes, changes root ownership and sets crontab 600 / cron.hourly 700. Before/after output is present. |
| W2-056 | [056-ubuntu-sca-passed-events.png](screenshots/056-ubuntu-sca-passed-events.png) | SCA event rows report the two permission checks as passed. |
| W2-057 | [057-ubuntu-sca-after-remediation.png](screenshots/057-ubuntu-sca-after-remediation.png) | Ubuntu SCA summary changes to 94 passed, 102 failed, 11 not applicable; score 47%. |
| W2-058 | [058-windows-sca-before-policy.png](screenshots/058-windows-sca-before-policy.png) | secedit exports the initial local policy; PasswordHistorySize is 0. |
| W2-059 | [059-windows-sca-remediation-script.png](screenshots/059-windows-sca-remediation-script.png) | An INF template sets PasswordHistorySize=24; secedit configures/exports it, and after.inf reports 24. Successful commands are visible. |
| W2-060 | [060-windows-sca-passed-event.png](screenshots/060-windows-sca-passed-event.png) | SCA event row reports check 15500, Ensure Enforce password history is set to 24 or more passwords, as passed. |
| W2-061 | [061-windows-sca-after-remediation.png](screenshots/061-windows-sca-after-remediation.png) | Windows SCA summary changes to 118 passed, 301 failed, 5 not applicable; score 28%. |
| W2-062 | [062-windows-sca-effective-policy.png](screenshots/062-windows-sca-effective-policy.png) | A separate verification export shows PasswordHistorySize=24 in verify.inf. |
| W2-063 | [063-windows-vulnerability-dashboard.png](screenshots/063-windows-vulnerability-dashboard.png) | The filtered Windows dashboard displays 71 Critical findings. Other severity counts in this filtered view are not a whole-host vulnerability assessment. |
| W2-064 | [064-ubuntu-vulnerability-dashboard.png](screenshots/064-ubuntu-vulnerability-dashboard.png) | The filtered Ubuntu dashboard displays 103 Critical findings. |
| W2-065 | [065-ubuntu-vulnerability-inventory.png](screenshots/065-ubuntu-vulnerability-inventory.png) | Ubuntu critical inventory rows identify linux-image-6.8.0-138-generic and associated CVE entries. No patch/reboot/re-scan is shown. |
| W2-066 | [066-windows-vulnerability-inventory.png](screenshots/066-windows-vulnerability-inventory.png) | Windows critical inventory lists Windows 10 Enterprise 10.0.19045.6456 and CVE entries; successful remediation is not established. |
| W2-067 | [067-suricata-package-install.png](screenshots/067-suricata-package-install.png) | APT installs Suricata and dependencies. PPA execution or a latest-release installation is not proved by this capture. |
| W2-068 | [068-suricata-active-service.png](screenshots/068-suricata-active-service.png) | systemctl shows Suricata active (running) and enabled, with the AF_PACKET launch command. An earlier eth0 failure is not displayed here. |
| W2-069 | [069-suricata-interface-addresses.png](screenshots/069-suricata-interface-addresses.png) | ubuntu-web has ens33 192.168.38.131/24 and a dynamic NAT-side ens36 address 192.168.121.157/24. Final endpoint isolation is not yet shown. |
| W2-070 | [070-suricata-af-packet-config.png](screenshots/070-suricata-af-packet-config.png) | The AF_PACKET block selects ens33, cluster-id 99 and cluster-type cluster_flow. |
| W2-071 | [071-suricata-home-net-config.png](screenshots/071-suricata-home-net-config.png) | HOME_NET is [192.168.38.0/24]. This controls rule variables, not NIC selection. |
| W2-072 | [072-suricata-update-version.png](screenshots/072-suricata-update-version.png) | suricata-update detects version 6.0.4 and reads the configuration. Completion of the ET Open fetch is outside this crop. |
| W2-073 | [073-suricata-admin-signature.png](screenshots/073-suricata-admin-signature.png) | The custom HTTP rule targets 192.168.38.131, uses http.uri content /admin, and SID 1000001 rev 1. |
| W2-074 | [074-suricata-config-test.png](screenshots/074-suricata-config-test.png) | Suricata 6.0.4 reports configuration successfully loaded in -T test mode. Runtime delivery is checked separately. |
| W2-075 | [075-suricata-windows-http-request.png](screenshots/075-suricata-windows-http-request.png) | Windows curl.exe requests /admin on ubuntu-web and receives an Apache 404 response. |
| W2-076 | [076-suricata-tcpdump-http-flow.png](screenshots/076-suricata-tcpdump-http-flow.png) | tcpdump on ens33 observes Windows .133 to Ubuntu .131 TCP/80, GET /admin and the 404 response. |
| W2-077 | [077-suricata-eve-http-record.png](screenshots/077-suricata-eve-http-record.png) | The local EVE JSON query selects event_type=http, showing URL /admin and status 404. This is an HTTP record, not the alert-type proof. |
| W2-078 | [078-suricata-fast-log-alert.png](screenshots/078-suricata-fast-log-alert.png) | fast.log records [1:1000001:1] LabShop Admin Page Probe from .133 to .131:80. |
| W2-079 | [079-suricata-agent-eve-localfile.png](screenshots/079-suricata-agent-eve-localfile.png) | The Wazuh agent localfile fragment reads /var/log/suricata/eve.json as json. |
| W2-080 | [080-suricata-wazuh-eve-alert.png](screenshots/080-suricata-wazuh-eve-alert.png) | The expanded Wazuh source contains event_type=alert, signature_id=1000001, LabShop Admin Page Probe, action=allowed, ens33, source .133 and destination .131. |
| W2-081 | [081-suricata-wazuh-signature-fields.png](screenshots/081-suricata-wazuh-signature-fields.png) | Wazuh event detail identifies ubuntu-web, alert signature 1000001, app_proto=http and destination .131. |
| W2-082 | [082-suricata-wazuh-http-fields.png](screenshots/082-suricata-wazuh-http-fields.png) | The event detail retains event_type=alert, GET and HTTP URL /admin, with flow fields. |
| W2-083 | [083-suricata-wazuh-rule-86601.png](screenshots/083-suricata-wazuh-rule-86601.png) | Wazuh detail shows decoder=json, location=/var/log/suricata/eve.json, groups ids/suricata, rule 86601 and level 3. This is the EVE-origin proof, not an Apache access-log alert. |

[Integrity manifest](manifest.json)

The eleven NTP captures are retained in [Day 01](../../day-01/evidence/ntp/README.md). The terminal capture W2-077 shows an HTTP EVE record. W2-080–W2-083 establish the alert-type EVE event and built-in Wazuh rule 86601.
