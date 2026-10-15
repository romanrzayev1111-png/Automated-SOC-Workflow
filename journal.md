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

**Issue:** Apache reports a ServerName warning. No Sysmon event is shown in Wazuh.

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

**Attempt / observation:** Linux systemctl output shows wazuh-agent enabled and Running; E26 lists both win-client and ubuntu-web Active on agent 4.14.7. Hostname-setting commands follow in E27–E29.

**Issue:** Agent status does not establish delivery of the five required controlled events. Restart/reboot persistence, snapshots and idle memory are absent.

**Resolution status:** Enrollment is recorded. Add genuine dated test entries as the outstanding acceptance tasks are executed; do not treat this retrospective as five independently recorded troubleshooting sessions.
