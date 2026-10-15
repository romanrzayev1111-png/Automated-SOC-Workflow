# Day 01 — Command and rule index

The [ordered guide](../step-by-step.md) is the complete command sequence. This index identifies **where** each command belongs and distinguishes evidence-backed outcomes from procedures that still need execution.

| Step | Machine | Commands / configuration | Evidence or status |
| :--- | :--- | :--- | :--- |
| 1 | VMware host | Create VMs, host-only VMnet1, server NAT, starting snapshots | Resource and network captures E01–E04; snapshots open |
| 2 | Linux VMs / Windows | `hostnamectl`, Netplan examples, Windows IPv4 settings, clock/route checks | Dynamic addresses E05–E07; naming E38–E40; static/clock proof open |
| 3 | All VMs | `ping -c 3` / `ping -n 4` against the other two peers | E08–E10 |
| 4 | siem-host | Official Docker APT key/repository, Engine and Compose plugin, `hello-world`, version checks | Official procedure; original install provenance/version outputs missing |
| 5 | siem-host | Persistent `vm.max_map_count=262144`, `sysctl --system` | Procedure; reboot persistence evidence open |
| 6 | siem-host | Clone v4.14.7, generate certificates, `docker compose up -d`, `ps`, `logs` | E15–E20 |
| 7 | siem-host | Private password/hash updates and indexer security administration | Procedure; successful rotation evidence open |
| 8 | ubuntu-web | Signed Wazuh APT repository, agent 4.14.7-1, manager .132, systemd | E25–E26 verify Running/Active |
| 9 | ubuntu-web | Install/enable Apache and SSH; verify workstation HTTP access | E12–E14 show Apache and localhost page; physical-workstation proof open |
| 10 | win-client | Signed MSI check/install, manager .132, `WazuhSvc` | E22–E23, E26 |
| 11 | win-client | Signed Sysmon download, community configuration, eventchannel localfile, restart agent | E11; event context strengthened by E33–E35 |
| 12.1 | siem-host | Load custom rule XML, check duplicate IDs, `wazuh-analysisd -t`, `wazuh-logtest`, restart manager | All four definitions E35; three matching custom alert IDs E34 |
| 12.1 | win-client | `whoami.exe`, `ipconfig.exe /all`, `hostname.exe`, encoded benign whoami | E33–E34 |
| 12.2 | Both endpoints / server | Failed SSH, successful sudo, new user, Windows process, failed logon | [Event register](event-validation.md) |
| 13 | siem-host | `docker stats --no-stream`, stack down/up **without -v**, server reboot | Measurement/recovery evidence open |
| 14 | All VMs / host | Remove endpoint NAT; routes, clocks, `slmgr.vbs /xpr`, final snapshots | Procedure; final artifacts open |

## Every custom rule in the supplied source

| ID | Level | Parent | Purpose | Implementation |
| :--- | :--- | :--- | :--- | :--- |
| 100100 | 10 | 61603 | whoami process command line | [XML](../config/windows-discovery-rules.xml) |
| 100101 | 9 | 61603 | ipconfig process command line | [XML](../config/windows-discovery-rules.xml) |
| 100102 | 8 | 61603 | hostname process command line | [XML](../config/windows-discovery-rules.xml) |
| 100103 | 12 | 61603 | Encoded PowerShell command line | [XML](../config/windows-discovery-rules.xml) |

## Built-in rules visible in result captures

| ID | Level | Recorded description | Figure |
| :--- | :--- | :--- | :--- |
| 60122 | 5 | Logon Failure - Unknown user or bad password | E32 |
| 61102 | 5 | Windows System error event | E32; not attributed to the controlled test |
| 60642 | 3 | Software protection service scheduled successfully. | E32; background result |
| 92057 | 12 | Powershell.exe spawned a powershell process which executed a base64 encoded command | E34 |
| 92213 | 15 | Executable file dropped in folder commonly used by malware | E34; causal relationship not established |
| 5710 | 5 | sshd: Attempt to login using a non-existent user | E37 |
| 2502 | 10 | syslog: User missed the password more than one time | E37 |
| 5501 | 3 | PAM: Login session opened. | E37; background result |

These built-in rules are listed for interpretation, **not redefined** in custom XML. The expected parent 61603 is verified in the [Wazuh 4.14.7 Sysmon ruleset](https://github.com/wazuh/wazuh/blob/v4.14.7/ruleset/rules/0595-win-sysmon_rules.xml).

## Initial commands that did not establish success

- `ssh salam@192.168.99.130`: unreachable wrong subnet (E29). Use the intended .131 endpoint and prove an authentication failure (E36).
- `sudo ls` and `sudo useradd testuser`: failed sudo authentication (E30–E31). They do not prove successful sudo execution or user creation.
- Intermediate Windows/Linux wizards use wrong server addresses/names; the final command uses manager .132 and the correct agent names.

The conversation references `too_many_nested_clauses`, but it supplies no final setting or actual fix. No undocumented configuration change is included as a working repair.
