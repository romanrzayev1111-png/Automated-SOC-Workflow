<p align="center"><img src="assets/project-hero.svg" alt="Automated SOC Workflow — Roman Rzayev" width="100%"></p>

<p align="center"><strong>BUILD → COLLECT → DETECT → VALIDATE → DOCUMENT</strong></p>

# Automated SOC Workflow

A personal security engineering journal by **Roman Rzayev**. Follow a monitoring environment from its initial network and Wazuh deployment into endpoint telemetry and custom detection rules. Each day combines the actual command sequence, configuration, explanation and retained evidence.

<p align="center"><a href="days/day-01#step-01"><strong>Open Day 01 walkthrough →</strong></a> &nbsp; · &nbsp; <a href="days/day-01#step-12">Read the custom rules</a> &nbsp; · &nbsp; <a href="days/day-01/evidence">Inspect the evidence</a></p>

![Recorded Day 01 metrics](assets/day-01-metrics.svg)

## The journey

| Day | Build focus | Read it here | Evidence status |
| :--- | :--- | :--- | :--- |
| **01** | Monitoring foundation · Wazuh · Sysmon · Windows/Linux | **[Commands, full configurations & explanations](days/day-01/README.md)** | Platform and selected alerts recorded; acceptance checks tracked |

Future days will be added as their work is supplied. Each receives its own walkthrough, configuration and evidence set.

## Day 01 · From infrastructure to detection

![Day 01 topology](days/day-01/architecture/architecture.svg)

| Foundation | Platform | Endpoints | Detection |
| :--- | :--- | :--- | :--- |
| Host-only topology | Wazuh **4.14.7** | `ubuntu-web` + `win-client` | Sysmon process creation |
| Persistent-IP examples | Three-container single-node stack | Linux and Windows agent procedures | Four full custom XML rules |
| Bidirectional peer tests | Certificate generation and recovery | Apache, SSH and Sysmon | Rule-level result attribution |
| [Network commands →](days/day-01#step-02) | [Deployment commands →](days/day-01#step-06) | [Endpoint commands →](days/day-01#step-08) | [Rules and explanations →](days/day-01#step-12) |

### A command is only the start

For example, from the **existing single-node deployment directory on siem-host**:

```bash
sudo docker compose up -d
sudo docker compose ps
sudo docker compose logs --tail=100 wazuh.indexer wazuh.manager wazuh.dashboard
```

`up -d` starts the services in the background; `ps` inspects their current state; `logs` checks what they did during initialization. [The Day 01 page](days/day-01/README.md) shows the preceding installation and configuration steps, the remaining commands and the evidence that limits each claim.

<details>
<summary><strong>See the recorded endpoint coverage</strong></summary>

![Two Active agents](days/day-01/evidence/screenshots/image26.png)

The captured inventory lists win-client and ubuntu-web Active on 4.14.7. Full acceptance also requires retained test events, recovery checks and hardening evidence.

</details>

## Project notebook

- **[Complete Day 01 walkthrough](days/day-01/README.md):** commands and configuration are visible inline, with purpose tables and checks.
- **[Detection results](days/day-01/docs/event-validation.md):** recorded rule IDs, levels, descriptions and gaps.
- **[Evidence register](days/day-01/evidence/README.md):** forty original captures and a source/hash manifest.
- **[Implementation journal](days/day-01/journal.md):** genuine observed failures, corrections and open actions.
- **[Acceptance matrix](days/day-01/docs/acceptance.md):** the deployment’s remaining validation work.

## Documentation checks

```bash
python3 scripts/build_readmes.py
python3 scripts/verify_artifacts.py
```

The check verifies evidence hashes/dimensions, local links, inline configuration fidelity, rule expressions and shell syntax. Live VM replay and PowerShell execution require the original environment. Professional report files remain separate from the main personal walkthrough.

**Roman Rzayev** · [GitHub](https://github.com/romanrzayev1111-png)
