# Day 02 acceptance matrix

Reviewed against the 25-page DOCX, execution handoff and prior draft. **Captured** is direct image evidence; **reported** is handoff context; **partial/open** needs more proof. There is no blanket all-tests-passed verdict.

| Area | Status | Evidence and remaining work |
| :--- | :--- | :--- |
| LabShop source / collection | Captured | W2-012/013 show syslog records and localfile. Original generator implementation is absent. |
| Decoder fields | Captured | W2-014/015 show definitions and action/dstuser/srcip. Earlier static-action correction is handoff-reported. |
| Rule definitions / positives | Captured | W2-016/018/020 show 100100/5 and 100101/10. Exact isolated threshold is not measured. |
| Sysmon ID migration | Reported | Handoff reports active IDs 100200–100203 in local_rules.xml. Post-migration capture/live duplicate-ID listing is absent. |
| Monitor exclusion | Qualified capture | W2-022 matches generic 1002/2, not the custom detector. |
| Split-source negative | Open | W2-024 includes 100101. Need expanded source/time context and isolated retest. |
| Success / malformed negatives | Partial | Source LOGIN_OK and malformed pre-decoding captured; final negative verdicts are not. See test-matrix.md. |
| Linux realtime FIM | Captured | W2-029–036: config, create/modify/delete, explicit realtime path detail. |
| Windows file FIM | Captured | W2-037–043: config, commands and 554/550/553 results. |
| Registry modification | Captured / interval gap | W2-044/045: Environment change and 750/594 results. Exact temporary Windows interval is absent. |
| Scheduled Linux FIM | Partial | Original 43200, active test 60 and events in W2-046–051. Restoration and exact latency comparison open. |
| Ubuntu SCA | Captured | W2-054–057: checks 28626/28627; modes 644→600, 755→700; passed 92→94, failed 104→102. |
| Windows SCA | Captured | W2-058–062: password history 0→24, check 15500 passed; summary passed 117→118. |
| Additional deferred SCA finding | Open if required | Separate named failed check and accepted risk rationale not supplied. |
| Vulnerability inventory | Captured | W2-063–066: Critical-filtered 103 Linux / 71 Windows entries and package versions; not whole-host lower-severity totals. |
| CVE remediation | Open | No verified patch, reboot, advisory mapping or cleared rescan. SCA hardening is separate. |
| Suricata install / recovery | Captured + reported | W2-067/068 show install/active service. DNS repair and eth0 failure are handoff-reported, not recreated screenshots. |
| Interface / HOME_NET | Captured | W2-069–072: ens33, 192.168.38.0/24, version 6.0.4. Full ET Open download and effective rule-files list not shown. |
| Network signature | Captured | W2-073/074/078: SID 1000001, successful config test and fast.log alert. |
| HTTP flow / metadata | Captured | W2-075–077: Windows request, ens33 flow and 404. W2-077 is HTTP JSON, not alert JSON. |
| Suricata EVE → Wazuh | Captured | W2-079–083: JSON localfile, signature 1000001, eve.json location, 86601/3. No Wazuh 100110 deployment; allowed means IDS-only. |
| NTP source selection | Captured + reported | Eleven Day 01 images show upstream, internal Linux peer and Windows source. Extra activity/tracking details are handoff-only. |
| Long-term clock stability | Open | Large frequency corrections and Windows root dispersion; no sustained-drift repair/test. |
| Reboot persistence | Open | Enabled/active is not post-reboot evidence for Chrony, agents, Suricata or the Docker stack. |
| Final endpoint isolation | Open | NAT ens36 remains in W2-069; public NTP sources remain in NTP-009. Retain final routes/adapters/sources. |
| Documentation / source images | Complete locally; publication verified at delivery | All 83 media objects: 11 Day 01 NTP + 72 Day 02, with hashes and inline evidence. Commit/push status is reported separately. |

## Close-out on the actual VMs

Complete controlled negatives, retain migrated IDs, restore intended FIM intervals, test stable clocks/reboot recovery and record NAT removal. Any patch/remediation claim needs its own before/after evidence.

The documentation check validates assets, links, configuration structure and command syntax; it does not perform these VM operations.
