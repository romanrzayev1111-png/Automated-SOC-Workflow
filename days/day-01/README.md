# Day 01 — Security Monitoring Foundation

A personal security monitoring implementation by **Roman Rzayev**: Wazuh 4.14.7, Windows and Linux endpoint enrollment, Sysmon installation and an Apache web service. This repository presents the recorded implementation, the operating procedure and the checks still needed for acceptance.

**[Step-by-step guide](step-by-step.md)** · **[Architecture](architecture/README.md)** · **[Acceptance matrix](docs/acceptance.md)**

The professional PDF is delivered separately. This directory is the Day 01 technical record; the [guide](step-by-step.md) contains the command sequence. Later days receive their own directories.

## Implementation at a glance

| Component | Recorded state | Evidence |
| :--- | :--- | :--- |
| Wazuh manager, indexer and dashboard | Version **4.14.7**; three containers Up | [E18](evidence/screenshots/image18.png) |
| Windows endpoint | `win-client` · `192.168.38.133` · agent 4.14.7 Active | [E23](evidence/screenshots/image23.png) |
| Linux endpoint | `ubuntu-web` · `192.168.38.131` · agent 4.14.7 Active | [E26](evidence/screenshots/image26.png) |
| Windows process telemetry | Sysmon 15.22 installed; service Running | [E11](evidence/screenshots/image11.png) |
| Linux web service | Apache Running; default page opens | [E13](evidence/screenshots/image13.png), [E14](evidence/screenshots/image14.png) |
| Internal connectivity | All six directed peer tests show replies | [E08–E10](evidence/README.md) |

![Recorded architecture](architecture/architecture.svg)

The diagram represents the supplied deployment evidence. The monitoring server also has NAT access. Final endpoint routing, persistent static addressing and the recovery controls require additional evidence. **Active agents do not by themselves prove delivery of all required security events.**

## Repository guide

```text
architecture/   Recorded diagram, addresses and resource variances
docs/           Operating procedure, acceptance matrix and event register
evidence/       40 original screenshots, captions and SHA-256 manifest
journal.md      Retrospective implementation record grounded in evidence
```

## Start and stop the environment

The original implementation runs in VMware VMs, **not in this repository's cloud container**. This repository contains documentation and report-generation tooling; it does not contain a deployable copy of the original VMs or the local credential-bearing Wazuh configuration.

1. Start `siem-host`. Confirm the internal address and the indexer kernel prerequisite.
2. In the existing Wazuh deployment directory (recorded as `/root/wazuh-docker/single-node`), run `docker compose up -d`, inspect `docker compose ps`, and troubleshoot startup using service logs.
3. Open the configured HTTPS dashboard from the operator workstation. Verify login and index availability.
4. Start `ubuntu-web` and `win-client`. Check Apache, Wazuh agent services and Sysmon64; verify both agents Active and search for a fresh test event.
5. To shut down, stop endpoint workloads and shut down the endpoints first. Run `docker compose stop` on `siem-host`, then shut down that VM. Preserve the data volumes.

The [operations guide](docs/operations.md) includes readiness checks, safe lifecycle commands and the outstanding restart/reboot acceptance test. These are documented procedures, not claims of newly executed VM tests.

## Event path

1. An endpoint produces a configured operating-system or application event.
2. The Wazuh agent reads that source and forwards the event to the manager.
3. The manager decodes the event and evaluates rules; matching events produce alerts.
4. Filebeat forwards alert records to the Wazuh indexer.
5. The dashboard queries indexed data for analyst investigation.

SIEM centralizes event analysis. EDR focuses on endpoint detection and response. XDR correlates across multiple security domains. Wazuh supplies endpoint monitoring and centralized analysis; the actual visibility depends on the sources and rules configured. This deployment's recorded coverage is narrower than a fully validated response workflow.

## Controlled-event acceptance

The revised document adds Windows logon/discovery results, four custom rule definitions and a corrected SSH test. Successful sudo and new-user creation are still absent. The [capture register](docs/event-validation.md) records each result and its limits.

| Event | Rule description | Level | Screenshot |
| :--- | :--- | :--- | :--- |
| Failed SSH login | sshd: Attempt to login using a non-existent user (5710) | 5 | [E36–E37](evidence/README.md); agent/time crop incomplete |
| Command run with sudo | Not recorded | Not recorded | Not supplied |
| Linux local-user creation | Not recorded | Not recorded | Not supplied |
| Windows process launch through Sysmon | User discovery (100100); network discovery (100101); system discovery (100102) | 10 / 9 / 8 | [E33–E35](evidence/README.md) |
| Failed Windows logon | Logon Failure - Unknown user or bad password (60122) | 5 | [E32](evidence/screenshots/image32.png) |

## Resource and recovery records

| Wazuh container | Idle memory |
| :--- | :--- |
| `wazuh.manager` | Not measured in supplied evidence |
| `wazuh.indexer` | Not measured in supplied evidence |
| `wazuh.dashboard` | Not measured in supplied evidence |

Run `docker stats --no-stream` at idle and retain the output. Stack restart/reboot persistence, default-password rotation, snapshot names `w1-clean-install` / `w1-done`, and the Windows evaluation expiry date are also **not documented**. The complete [acceptance matrix](docs/acceptance.md) maps every baseline requirement to evidence or a specific remaining action.

## Commands and rules

The [step-by-step guide](step-by-step.md) identifies the machine, command sequence, expected checks and source limitations for each step. The [custom rule XML](config/windows-discovery-rules.xml) contains all four captured rules, and the [command/rule index](docs/command-and-rule-index.md) links each operation to the guide.

The professional report is delivered separately. This directory is the personal GitHub implementation record.

## Repository hygiene

No credentials, private keys, certificate files, live Compose secrets or VM disk images are included. [.gitignore](../../.gitignore) excludes common sensitive and generated files; it is a safeguard, not proof that every future commit is safe. The current artifact check validates screenshot hashes/dimensions, local links, XML rules, representative rule expressions and Bash syntax. Review new evidence for visible secrets before publishing.

## References

- [Wazuh single-node Docker deployment](https://documentation.wazuh.com/current/deployment-options/docker/wazuh-container.html)
- [Docker Engine on Ubuntu](https://docs.docker.com/engine/install/ubuntu/)
- [Microsoft Sysmon](https://learn.microsoft.com/en-us/sysinternals/downloads/sysmon)
- [SwiftOnSecurity Sysmon configuration](https://github.com/SwiftOnSecurity/sysmon-config)

Prepared by **Roman Rzayev**.
