# Acceptance matrix

This matrix maps the supplied Week 1 brief to the implementation evidence. The professional report uses Tetrion branding; requirement IDs are retained here for traceability. A screenshot is point-in-time evidence, not a new live test.

**Recorded** = directly supported for the stated scope. **Partial** = only part demonstrated. **Open** = not established. No overall compliance percentage is assigned.

| ID | Status | Evidence and remaining action |
| :--- | :--- | :--- |
| L1 | Partial | E01–E03 show all three VMs; endpoint RAM, CPUs and disk sizes differ from the baseline. Resolve/document approved resource changes. |
| L2 | Partial | E04–E07 show the host-only subnet and server NAT. DHCP/dynamic flags contradict a claim of demonstrated static addressing. Retain persistent address configuration and final endpoint adapters. |
| L3 | Partial | E08–E10 show all directed peer pings; E19–E20 show a dashboard browser. Record workstation origin and clock synchronization on all systems. |
| L4 | Open | Compose commands run, but official-repository Docker installation, plugin versions and persistent vm.max_map_count are not recorded. |
| L5 | Open | Retain each VM's snapshot inventory showing w1-clean-install and w1-done. |
| W1 | Recorded | E15 and E18 show v4.14.7 source/images and three Up containers. README records the exact version. This is a startup observation. |
| W2 | Partial | E19–E20 show browser access. Record the configured HTTPS URL and explain the actual certificate issuer/trust warning from the operator workstation. |
| W3 | Open | Login is visible; administrator password rotation is not. Complete the documented Docker-specific password procedure and retain a secret-free confirmation. |
| W4 | Open | Capture identical agent inventory and a known pre-existing alert after stack stop/start and after server reboot. |
| W5 | Open | Retain dated idle docker stats output and populate the three-container memory table. |
| A1 | Recorded | E25 shows Linux agent Running; E26 lists ubuntu-web Active at 192.168.38.131. |
| A2 | Recorded | E23 and E26 list win-client Active at 192.168.38.133. |
| A3 | Partial | E11 shows Sysmon64 Running with SwiftOnSecurity configuration. No Sysmon event in the dashboard is supplied. |
| A4 | Partial | E13 shows Apache Running; E14 shows the default page. Confirm the request originated on the operator workstation. |
| V1 | Open | Five deliberate event captures with rule descriptions and levels are absent. Complete docs/event-validation.md. |
| V2 | Recorded (documentation) | README and the report explain the expected agent -> manager -> Filebeat -> indexer -> dashboard path. A traced real event is still recommended. |
| S1 | Partial | .gitignore and artifact checks are included; current supplied images contain no visually identified credentials. Complete a repository/history secret review before treating this as a comprehensive check. |
| S2 | Partial | VMnet1 is host-only and server NAT is visible. Source notes mention temporary endpoint NAT; final routes and adapter removal are unverified. |
| D1 | Recorded (this delivery) | README, architecture/, evidence/ and journal.md are present. Publication status is reported separately. |
| D2 | Partial | Start/stop order and readiness procedure are documented in README and docs/operations.md. Replay against the original VMs remains outstanding. |
| D3 | Partial | The journal contains six evidence-based retrospective entries. It does not invent five contemporaneous troubleshooting attempts or undocumented fixes. Add genuine dated operational entries. |

## Suggested completion order

1. Resolve resource variance, addressing, endpoint isolation and credential rotation.
2. Verify Docker provenance, persistent kernel settings, VM clocks and snapshots.
3. Capture Sysmon ingestion and the five deliberate event cases.
4. Test restart/reboot persistence and measure idle container memory.
5. Record Windows evaluation expiry and replay the operating procedure.

All validation activity must be authorized and limited to systems you own or administer. No attack execution or changes to the original VMs were performed in preparing these documents.
