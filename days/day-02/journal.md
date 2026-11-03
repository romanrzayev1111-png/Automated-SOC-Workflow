# Day 02 implementation journal

Retrospective from original PNGs and the supplied execution handoff. Captures span October tests and 3 November NTP/Suricata work. Section order is the replay sequence, not an invented contemporaneous timeline. No VM was remotely operated during documentation.

## 01 · Timezone and clock sources

The handoff reports an initially synchronized server using America/New_York, followed by Baku timezone configuration. Captures show Asia/Baku and Azerbaijan Standard Time. Chrony initially showed stratum 0 / Not synchronised after restart despite UDP/123 listening; another capture shows stratum 3 / Normal. Recovery after upstream polling, without another manual fix, is reported by the handoff.

The Linux client selected .132 and Windows reports .132,0x8 / stratum 4. External Linux sources remain listed. Large frequency correction and Windows dispersion remain open. Full commands and eleven originals are at the beginning of [Day 01](../day-01/README.md#ntp-time-synchronization).

## 02 · LabShop decoder / static-field correction

The handoff records an initial field-name action error. The final captured rule uses `<action>LOGIN_FAILED</action>` and exact monitor exclusion. The decoder extracts action/dstuser/srcip using `\w+`; logtest confirms those fields. No missing initial error output is recreated.

## 03 · Duplicate custom IDs

Historical Day 01 Sysmon definitions use 100100–100103. The handoff reports relocating active definitions in local_rules.xml to 100200–100203 so LabShop can use 100100/100101. Original screenshots remain unchanged; a post-migration rule listing is not supplied. Inspect IDs before combined replay.

## 04 · Positive and negative test review

Single failures produce 100100/5, bulk same-source failures produce 100101/10. The monitor test ends at generic 1002/2: custom exclusion is supported, but no-rule-at-all is inaccurate.

The split-source crop includes 100101 without expanded source/history; that case stays unresolved. LOGIN_OK is visible in raw logs, while malformed input shows pre-decoding only. The handoff reports negative outcomes, but complete captured verdicts are missing. See the [six-case review](docs/test-matrix.md).

## 05 · Files and Registry

Linux realtime and Windows file create/modify/delete have 554/550/553 results. Linux detail explicitly shows realtime mode/path. Windows Environment modification is paired with value/key alerts. The exact shortened Windows interval is absent; Registry monitoring is not described as realtime.

## 06 · Scheduled FIM

Original Linux frequency is 43200 seconds; a later agent log records 60 seconds. /etc writes and dashboard rows follow. The timestamps are not a controlled latency study. Returning to 43200 is advised, not verified as complete.

## 07 · SCA hardening

The Ubuntu script records original modes, then changes crontab 644→600 and cron.hourly 755→700 with root ownership. Two checks pass and the summary moves 92→94 passed. Backups preserve modes only and are overwritten by a second run.

Windows exports PasswordHistorySize=0, applies 24 via an INF/secedit procedure and exports/verifies 24. Check 15500 passes; the summary moves 117→118 passed. No unrelated SCA or CVE remediation is claimed.

## 08 · Vulnerability review

Critical-filtered inventories show 103 Ubuntu and 71 Windows entries with package/build details. The handoff supplies kernel inspection context. No patch/reboot/rescan chain is provided; remediation and official-advisory mapping remain separate work.

## 09 · Suricata DNS / interface recovery

The handoff supplies temporary ens36 resolvectl repair and the exact nonexistent-eth0 error. The DOCX shows corrected ens33/HOME_NET, a running service and version 6.0.4, not the failed-service transcript. ens36 NAT is still present.

## 10 · Signature loading / packet path

The HTTP /admin rule uses SID 1000001 and passes config testing. The handoff reports one rule loaded, zero failures, ens33 MTU 1500 and AFP threads running; old no-rules lines predated the fix.

Windows curl enters ens33 and gets 404. tcpdump and an HTTP EVE record show the flow; fast.log records the signature. A local self-request is not used as the decisive NIC test.

## 11 · EVE delivery to Wazuh

After JSON collection/reload, a fresh request reaches Wazuh with eve.json location, event_type alert, SID 1000001, .133→.131 and built-in 86601/3. The user decided against Wazuh 100110. The updated source contains the correct EVE alert; the earlier Apache-only alert is not substituted.

The earlier local HTTP and later collected alert are different requests, not a delivery-latency measurement. Action allowed is IDS detection, not blocking.

## 12 · Outstanding proof

Retain controlled negatives, migrated IDs, restored FIM intervals, stable clocks, post-reboot services/data and actual NAT removal. Add patch/advisory/rescan evidence before claiming CVEs fixed. The [acceptance matrix](docs/acceptance.md) separates those gaps from the captured positives and completed documentation.
