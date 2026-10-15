# Implementation journal

Prepared on 15 October 2026 as a **retrospective from supplied evidence**, not as a claim of live execution or a contemporaneous diary. Original activity dates are not independently established. Each entry separates an observation, an issue and a demonstrated or pending resolution.

## 01 — Provisioning and capacity

**Attempt / observation:** VMware resource settings exist for Windows, the Linux endpoint and the monitoring server (E01–E03).

**Issue:** The resource allocations differ from the baseline: 24 GB assigned RAM in total, 4 Windows vCPUs and a 60 GB Windows disk, plus larger Linux disks.

**Resolution status:** No corrective resize is recorded. Documented as a variance for capacity review; no successful correction is claimed.

## 02 — Network reachability

**Attempt / observation:** VMnet1 is host-only; address captures show .131, .132 and .133. The three ping captures cover all six directed peer checks with 0% packet loss (E04–E10).

**Issue:** Linux addresses are flagged dynamic, and DHCP is enabled. The source notes mention temporary NAT on endpoints, but final adapter removal is not captured.

**Resolution status:** Peer reachability is demonstrated. Persistent addressing and final isolation remain open; no undocumented network fix is asserted.

## 03 — Endpoint service preparation

**Attempt / observation:** Sysmon 15.22 loads a SwiftOnSecurity configuration and reports Running (E11). Apache is installed, enabled and Running; its default page opens (E12–E14).

**Issue:** Apache reports a ServerName warning. The corrected source adds custom Sysmon-process definitions and discovery alerts (E33–E35); a full raw channel event is still useful.

**Resolution status:** Apache serves its page despite the warning; no warning removal is recorded. Sysmon dashboard ingestion remains to be tested.

## 04 — Wazuh stack startup

**Attempt / observation:** The v4.14.7 release is cloned, certificates are generated and three containers show Up. Dashboard login and an authenticated overview are visible (E15–E20).

**Issue:** The source checkout is detached at the release tag, which is expected and not an installation failure. Password rotation, persistent kernel settings and reboot behavior are not captured.

**Resolution status:** Startup and dashboard access are demonstrated. No persistence or credential-hardening result is invented.

## 05 — Windows agent service start

**Attempt / observation:** The enrollment command names win-client. An initial service-start attempt produces NET HELPMSG 2185 (E22).

**Issue:** The first service-start command does not find the expected service at that point. The capture alone does not establish whether installation timing or another cause explains it.

**Demonstrated resolution:** A subsequent `NET START WazuhSvc` succeeds, and E23 lists win-client Active. No undocumented reinstall or configuration change is credited as the fix.

## 06 — Linux agent and endpoint inventory

**Attempt / observation:** Linux systemctl output shows wazuh-agent enabled and Running; E26 lists both win-client and ubuntu-web Active on agent 4.14.7. Hostname-setting commands follow in E38–E40.

**Issue:** The corrected source adds Windows logon/discovery results and a Linux SSH result; successful sudo and user creation are still absent. Restart/reboot persistence, snapshots and idle memory are absent.

**Resolution status:** Enrollment is recorded. Add genuine dated test entries as the outstanding acceptance tasks are executed; do not treat this retrospective as five independently recorded troubleshooting sessions.

## 07 — Corrected authentication tests

**Attempt / observation:** E29 targets the wrong 192.168.99.130 subnet and receives Network is unreachable. E36 reaches the intended .131 endpoint and records genuine authentication failure; E37 lists non-existent-user rule 5710 / level 5.

**Issue:** E30/E31 fail sudo authentication, so neither the successful-sudo requirement nor local-user creation is demonstrated. E37 omits agent/time columns.

**Demonstrated resolution:** The SSH destination is corrected. Successful sudo, new-user creation and full SSH alert context remain open; no unrecorded fix is claimed.

## 08 — Windows discovery rules and result attribution

**Attempt / observation:** E33 runs whoami, ipconfig, hostname and encoded benign whoami. E35 contains four custom definitions inheriting Sysmon Event 1 parent 61603; E34 lists 100100/10, 100101/9 and 100102/8.

**Issue:** The encoded-PowerShell result is built-in 92057/12, not proof that custom 100103 fired. The extra 92213 row cannot be causally attributed from the crop.

**Demonstrated resolution:** All four definitions are transcribed and documented, with observed and configured-only results separated. The parent definition was checked against the release ruleset; no unknown if_sid or search-limit repair is invented.
