#!/usr/bin/env python3
"""Compose the GitHub landing pages with commands/configuration visible inline."""
from pathlib import Path
from html import escape
import re

ROOT = Path(__file__).resolve().parents[1]
DAY = ROOT / 'days/day-01'
ASSETS = ROOT / 'assets'


def hero(filename, eyebrow, title, subtitle, day=False):
    side = '''<g transform="translate(1120 96)"><rect width="305" height="232" rx="14" fill="#1B222C" stroke="#38404B"/><text x="24" y="39" fill="#E8BD62" font-size="15" font-weight="bold" letter-spacing="3">DAY 01</text><path d="M53 99H250M150 99V175" stroke="#E8BD62" stroke-width="2"/><g fill="#11161E" stroke="#59616B"><rect x="25" y="73" width="78" height="52" rx="7"/><rect x="199" y="73" width="78" height="52" rx="7"/><rect x="111" y="154" width="78" height="52" rx="7"/></g><g fill="white" font-size="12" text-anchor="middle"><text x="64" y="104">LINUX</text><text x="238" y="104">WINDOWS</text><text x="150" y="185">WAZUH</text></g></g>'''
    ASSETS.mkdir(exist_ok=True)
    (ASSETS / filename).write_text(f'''<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="430" viewBox="0 0 1600 430"><title>{escape(title)}</title><defs><linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%"><stop stop-color="#0B1018"/><stop offset="1" stop-color="#202732"/></linearGradient><pattern id="grid" width="38" height="38" patternUnits="userSpaceOnUse"><path d="M38 0H0V38" fill="none" stroke="#ffffff" stroke-opacity=".035"/></pattern></defs><rect width="1600" height="430" rx="16" fill="url(#bg)"/><rect width="1600" height="430" rx="16" fill="url(#grid)"/><path d="M0 55H350L374 79H1510L1550 119V430M38 0V315L80 357H1600" fill="none" stroke="#E8BD62" stroke-width="2"/><g font-family="sans-serif"><text x="88" y="135" fill="#E8BD62" font-size="19" letter-spacing="4" font-weight="bold">{escape(eyebrow)}</text><text x="84" y="220" fill="#F8FAFC" font-size="{48 if day else 49}" font-weight="bold">{escape(title)}</text><text x="88" y="272" fill="#BAC2CC" font-size="22">{escape(subtitle)}</text><text x="88" y="380" fill="#CDD2D9" font-size="16" letter-spacing="2">ROMAN RZAYEV  /  SECURITY ENGINEERING JOURNAL</text>{side}</g></svg>''')


def section_image(filename, number, title, sub):
    (ASSETS / filename).write_text(f'''<svg xmlns="http://www.w3.org/2000/svg" width="1440" height="128" viewBox="0 0 1440 128"><title>{escape(title)}</title><rect width="1440" height="128" rx="10" fill="#141A23"/><rect width="6" height="128" rx="3" fill="#E8BD62"/><g font-family="sans-serif"><text x="35" y="80" fill="#E8BD62" font-size="47" font-weight="bold">{number}</text><text x="133" y="58" fill="#F8FAFC" font-size="26" font-weight="bold">{escape(title)}</text><text x="134" y="92" fill="#AEB8C6" font-size="17">{escape(sub)}</text></g><path d="M1180 32H1360V96H1270" stroke="#E8BD62" stroke-opacity=".4" fill="none"/><circle cx="1270" cy="96" r="4" fill="#E8BD62"/></svg>''')


def scorecard():
    cells = [('03', 'SYSTEMS', 'One platform, two endpoints'), ('02', 'ACTIVE AGENTS', 'Recorded dashboard inventory'), ('04', 'CUSTOM RULES', 'Three matching IDs observed'), ('40', 'SOURCE CAPTURES', 'Original pixels retained')]
    cards = []
    for n, (count, title, sub) in enumerate(cells):
        x = n * 365
        cards.append(f'<g transform="translate({x} 0)"><rect x="1" y="1" width="344" height="159" rx="10" fill="#F4F3EF" stroke="#DDD8CD"/><text x="22" y="65" font-size="42" font-weight="bold" fill="#141A23">{count}</text><text x="23" y="103" font-size="14" letter-spacing="1.2" fill="#8B671F" font-weight="bold">{title}</text><text x="23" y="133" font-size="12" fill="#535D6B">{sub}</text></g>')
    (ASSETS / 'day-01-metrics.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg" width="1440" height="162" viewBox="0 0 1440 162"><title>Day 01 recorded implementation metrics</title><g font-family="sans-serif">' + ''.join(cards) + '</g></svg>')


def explanation(rows, label='Command / setting'):
    return '\n\n**What each part does**\n\n| ' + label + ' | Explanation |\n| :--- | :--- |\n' + '\n'.join('| ' + a + ' | ' + b + ' |' for a, b in rows) + '\n'


EXPLAIN = {
1: [('Host-only / VMnet1', 'Places all three systems on the same private virtual network; external routing is not supplied by this mode.'), ('Server NAT adapter', 'Allows the monitoring server to download packages/images. Endpoints use temporary NAT only during installation.'), ('Starting and final snapshots', 'Provide identifiable recovery points. Their names must reflect when they were actually taken.')],
2: [('`hostnamectl set-hostname` / `--static`', 'Changes the persistent Linux machine name, then reads it back so the target can be identified in later evidence.'), ('`netplan generate`', 'Validates the merged Netplan configuration and generates backend files before the network is changed.'), ('`netplan try`', 'Applies a temporary trial with rollback; confirm it at the VM console after checking connectivity.'), ('`ip -br address` / `ip route`', 'Shows interface addresses and the routes that determine whether traffic can leave the isolated network.'), ('`hostname` / `Get-NetIPConfiguration`', 'Reads the Windows computer name, addresses, gateway and adapter details.'), ('`Get-NetRoute ... 0.0.0.0/0`', 'Looks for an IPv4 default route; a final host-only endpoint should not retain an internet gateway.'), ('`Get-Date`, `w32tm`, `timedatectl status`', 'Checks local clock/time-service state so event timestamps can be correlated.')],
3: [('Linux `ping -c 3`', 'Sends three ICMP requests to the named peer; retain the replies and packet-loss summary.'), ('Windows `ping -n 4`', 'Sends four requests. Windows uses `-n` for the count; the Linux command uses `-c`.'), ('All six directed paths', 'Tests server→Linux, server→Windows, Linux→server, Linux→Windows, Windows→Linux and Windows→server.')],
4: [('`apt-get update` / prerequisite install', 'Refreshes repository metadata and installs HTTPS certificates, curl and Git.'), ('`install -d` / `curl -fsSL .../gpg` / `chmod a+r`', 'Creates the keyring directory, retrieves Docker’s official repository key over verified HTTPS and makes it readable to APT.'), ('`tee ...docker.sources`', 'Writes the Docker APT source with the local Ubuntu codename and CPU architecture; `Signed-By` scopes trust to the Docker key.'), ('`docker-ce`, `docker-ce-cli`, `containerd.io`', 'Installs the engine, command-line client and container runtime.'), ('`docker-buildx-plugin`, `docker-compose-plugin`', 'Adds the build extension and the `docker compose` multi-service command.'), ('`systemctl enable --now docker`', 'Starts the daemon now and enables it at boot.'), ('`docker run --rm hello-world`', 'Exercises image retrieval and container execution; removes the test container after exit.'), ('`docker --version` / `docker compose version`', 'Records the actual installed tooling; these are separate from the Wazuh application version.')],
5: [('`vm.max_map_count`', 'Limits memory mappings per process. The indexer needs at least 262144; this is not a RAM allocation.'), ('`sudoedit ...99-wazuh-max-map-count.conf`', 'Edits a persistent sysctl drop-in. Preserve a higher existing setting.'), ('`sysctl --system`', 'Reloads the configured sysctl files; a reboot check establishes that the setting persists.')],
6: [('`git clone --depth 1 --branch v4.14.7`', 'Fetches the selected release without unrelated history. A release-tag checkout is expected to have a detached HEAD.'), ('`git rev-parse HEAD`', 'Checks the source against the recorded full commit instead of trusting a folder name.'), ('`cd single-node`', 'Selects the Compose model for the one-server deployment.'), ('`-f generate-indexer-certs.yml run --rm generator`', 'Runs the release certificate generator once during initial provisioning and removes its temporary container.'), ('`docker compose up -d`', 'Creates/starts the stack in the background using the private deployment configuration.'), ('`docker compose ps`', 'Shows the service containers and current states.'), ('`docker compose logs --tail=100 ...`', 'Reads recent indexer, manager and dashboard output to diagnose initialization problems.')],
7: [('`INDEXER_PASSWORD` / `internal_users.yml`', 'The dependent services and indexer user hash must agree on the new credential. These are private runtime files.'), ('`docker compose down`', 'Stops/removes service containers and network while retaining named volumes when `-v` is absent.'), ('Indexer `hash.sh`', 'Prompts interactively and derives the password hash; avoids placing the plaintext credential in the command line.'), ('`compose exec wazuh.indexer bash`', 'Enters the running indexer container so its local certificate and security tools can be used.'), ('`JAVA_HOME`', 'Selects the Java runtime bundled with the indexer.'), ('`securityadmin.sh -f ... -t internalusers`', 'Applies the specified internal-user configuration rather than overwriting unrelated security configuration.'), ('`-h wazuh.indexer -p 9200 -icl`', 'Targets the certificate-matching node name/HTTPS port; `-icl` ignores the cluster-name check, not TLS verification.'), ('`-cacert`, `-cert`, `-key`', 'Uses the trusted CA and administrative client certificate/key to authenticate the security configuration update.')],
8: [('Official key / `gpg --dearmor` / `signed-by`', 'Builds an APT keyring and ties the Wazuh package source to it; package signature verification stays enabled.'), ('`apt-cache policy wazuh-agent`', 'Checks which versions the configured repository offers before selecting one.'), ('`WAZUH_MANAGER=192.168.38.132`', 'Points enrollment and event delivery at the monitoring server, not at the endpoint itself.'), ('`WAZUH_AGENT_NAME=ubuntu-web`', 'Sets the intended Linux endpoint identity.'), ('`wazuh-agent=4.14.7-1`', 'Pins the package to the manager’s release line instead of silently selecting a newer agent.'), ('`daemon-reload` / `enable --now`', 'Refreshes systemd’s unit view, enables boot startup and starts the installed agent.'), ('`apt-mark hold`', 'Prevents an unrelated package upgrade from moving this agent beyond the chosen manager version.'), ('`systemctl is-active`', 'Returns service state; verify the additional Active inventory state in the dashboard.')],
9: [('`apt-get install apache2 openssh-server`', 'Adds the web workload and inbound SSH service needed for the controlled authentication test.'), ('`systemctl enable --now apache2 ssh`', 'Starts both services and enables them at boot.'), ('`systemctl is-active ...`', 'Checks Apache, SSH and the Wazuh agent together.'), ('Workstation request to `http://192.168.38.131/`', 'Tests the actual client-to-server HTTP path; localhost tests only the browser’s own machine.')],
10: [('`Join-Path $env:TEMP ...` / `Invoke-WebRequest`', 'Chooses a local installer path and downloads the version-matched official MSI.'), ('`Get-AuthenticodeSignature` + `throw`', 'Stops installation if the Windows publisher signature is not valid.'), ('`Start-Process msiexec.exe -Wait -PassThru`', 'Runs the installer to completion and captures its exit code instead of racing the service start.'), ('`/i`, `/qn`', 'Install the MSI without an interactive wizard; manager/name properties are passed explicitly.'), ('Exit code `0` / `3010`', 'Means success / success with reboot required. Other codes are treated as a failure.'), ('`Start-Service` / `Get-Service WazuhSvc`', 'Starts and then verifies the correct Windows Wazuh service.')],
11: [('Sysinternals ZIP + `Expand-Archive`', 'Downloads and unpacks the vendor Sysmon distribution outside the repository.'), ('Sysmon Authenticode check', 'Verifies the executable’s Windows signature before it is run.'), ('Pinned community configuration URL', 'Makes the guide’s configuration reference reproducible; it is separate from the changing vendor binary download.'), ('`Sysmon64.exe -accepteula -i`', 'Installs Sysmon with the reviewed event configuration. An existing installation uses supported update mode instead.'), ('`location` / `log_format=eventchannel`', 'Instructs Wazuh to read the exact Sysmon Windows event channel; it does not install Sysmon.'), ('`Restart-Service WazuhSvc`', 'Reloads the agent after its channel configuration is edited.'), ('`Start-Process notepad.exe` / `Get-WinEvent`', 'Creates a benign process and looks for recent local Sysmon process-creation events. Dashboard delivery is checked separately.')],
12: [('`group`', 'Places the definitions in local/Sysmon/custom-detection groups for organization.'), ('`rule id` / `level`', 'Provides the unique custom identifier and configured alert severity. A high level is a rule setting, not proof of compromise.'), ('`if_sid=61603`', 'Requires the built-in Wazuh 4.14.7 Sysmon Event 1 process-creation parent to match first.'), ('`field ...commandLine` / `type=pcre2`', 'Tests the decoded process command line with a PCRE2 regular expression.'), ('`(?i)` / `\\.exe` / `\\\\hostname`', 'Makes the match case-insensitive; escapes the dot in .exe; requires a Windows path separator before hostname.'), ('`description` / `$(win.system.computer)`', 'Builds the alert’s readable text and inserts the decoded computer name.'), ('`mitre/id`', 'Labels the detection with the supplied ATT&CK technique; it does not establish malicious intent.'), ('Duplicate-ID search / `compose cp`', 'Checks for existing definitions before copying one reviewed file into the manager’s persistent rules directory.'), ('`chown` / `chmod 640`', 'Sets the manager-readable owner/group and limits file access.'), ('`wazuh-analysisd -t` / `wazuh-logtest`', 'Validates manager configuration, then tests decoding/rule selection against an actual raw event.'), ('`compose restart wazuh.manager`', 'Reloads the changed rules. Check logs and agent recovery afterwards.'), ('Windows discovery commands', 'Generate controlled process events: user identity, network configuration, machine name and a benign encoded whoami.'), ('Dashboard agent/rule filters', 'Narrow the event view; retain rule IDs, levels, descriptions, timestamps and agent identity before marking a case complete.')],
13: [('`docker stats --no-stream`', 'Captures one container resource snapshot; use an idle observation period and retain the measurement context.'), ('Stack down/up without `-v`', 'Exercises container recreation while keeping the persistent data volumes.'), ('Recheck the same old alert after reboot', 'Shows retained data; a new empty dashboard or only newly arriving events would not prove persistence.'), ('Routine `docker compose stop`', 'Stops service containers without deleting them. Resume using the existing deployment.')],
14: [('Final adapter / route checks', 'Establishes that temporary endpoint NAT and default routes were actually removed.'), ('`slmgr.vbs /xpr`', 'Displays Windows activation/evaluation expiry state; record the displayed value rather than estimating it.'), ('Final snapshots / journal', 'Captures the state after validation and records the real commands, failures and corrections.')],
15: [('Recorded', 'A screenshot/output supports the specific stated observation.'), ('Configured', 'The definition exists, but its own alert ID is not necessarily shown firing.'), ('Open', 'Required evidence remains absent; the implementation is not represented as fully accepted.')],
}


def inline_netplan():
    chunks = ['\n### Persistent network configurations — shown in full\n']
    for file, title in [('netplan-siem-host.example.yaml', 'siem-host / NAT plus host-only'), ('netplan-ubuntu-web.example.yaml', 'ubuntu-web / host-only endpoint')]:
        chunks += [f'\n**{title}** — merge into the existing Netplan configuration after checking local interface names.\n', '```yaml\n' + (DAY / 'config' / file).read_text().strip() + '\n```\n']
    chunks += [explanation([('`version: 2`', 'Uses the Netplan configuration schema.'), ('Server `ens33: dhcp4: true`', 'Retains DHCP on the observed NAT-side server interface.'), ('Server `ens36` / endpoint `ens33`', 'Uses the host-only interface names from the supplied captures; verify them locally before applying.'), ('`dhcp4: false` + `addresses`', 'Requests the specified persistent IPv4 address on the host-only interface.'), ('No host-only gateway', 'Does not intentionally create an IPv4 internet default route on either endpoint. Verify final routes and IPv6 separately.')], 'YAML field')]
    return '\n'.join(chunks)


def make_day():
    guide = (DAY / 'step-by-step.md').read_text()
    body = guide[guide.index('## 1. Prepare'):]
    parts = re.split(r'(?=^## \d+\.)', body, flags=re.M)
    rendered = []
    banners = {1: ('design-network.svg', 'Foundation & network'), 4: ('platform.svg', 'Platform deployment'), 8: ('endpoints.svg', 'Endpoint onboarding'), 12: ('detections.svg', 'Detection engineering')}
    for part in parts:
        match = re.match(r'## (\d+)\.', part)
        if not match:
            rendered.append(part)
            continue
        n = int(match[1])
        if n == 2:
            part = part.replace('From the VM console, validate and trial the edited configuration:', inline_netplan() + '\nFrom the VM console, validate and trial the edited configuration:')
        if n == 12:
            xml = (DAY / 'config/windows-discovery-rules.xml').read_text().strip()
            spot = 'On **siem-host**, keep a local copy of this repository'
            part = part.replace(spot, '### Full custom rule configuration\n\n```xml\n' + xml + '\n```\n\n' + spot)
        # Keep command explanations inside their chapter, ahead of the next heading.
        if '## Source references' in part:
            a, b = part.split('## Source references', 1)
            part = a + explanation(EXPLAIN[n]) + '\n## Source references' + b
        else:
            part += explanation(EXPLAIN[n])
        if n == 6:
            part += '\n<details>\n<summary><strong>Recorded result · three Wazuh containers</strong></summary>\n\n![Wazuh container inventory](evidence/screenshots/image18.png)\n\nE18 records 4.14.7 containers Up at capture time.\n\n</details>\n'
        if n == 12:
            part += '\n**Recorded detection output**\n\n![Windows discovery rule results](evidence/screenshots/image34.png)\n\nE34 shows 100100, 100101 and 100102; encoded PowerShell is reported by built-in 92057.\n'
        prefix = f'\n<a id="step-{n:02d}"></a>\n\n'
        if n in banners:
            filename, label = banners[n]
            prefix = f'\n![{label}](../../assets/{filename})\n\n' + prefix
        rendered.append(prefix + part)
    intro = '''<p align="center"><img src="../../assets/day-01-hero.svg" alt="Day 01 — Security Monitoring Foundation" width="100%"></p>

<p align="center"><strong>Roman Rzayev</strong> · Wazuh 4.14.7 · VMware · Windows + Linux · Sysmon</p>

# Day 01 · Security Monitoring Foundation

Build the monitoring server, onboard two endpoints and follow selected process/authentication events into Wazuh. The commands, network configuration, event-channel configuration and four custom rules are shown **directly on this page**, followed by explanations and checks.

![Recorded project metrics](../../assets/day-01-metrics.svg)

| Start here | Continue here | Inspect the results |
| :--- | :--- | :--- |
| [01 · Network](#step-01) | [04 · Docker](#step-04) · [06 · Wazuh](#step-06) | [Evidence register](evidence/README.md) |
| [02 · Full Netplan YAML](#step-02) | [08 · Linux agent](#step-08) · [10 · Windows agent](#step-10) | [Event results](docs/event-validation.md) |
| [03 · Peer connectivity](#step-03) | [11 · Sysmon](#step-11) · [12 · Full custom XML](#step-12) | [Acceptance matrix](docs/acceptance.md) |
| [07 · Credential rotation](#step-07) | [13 · Recovery](#step-13) · [14 · Handover](#step-14) | [Implementation journal](journal.md) |

## Recorded architecture

![Three-system topology](architecture/architecture.svg)

| Machine | Address | Responsibility | Run commands as |
| :--- | :--- | :--- | :--- |
| **siem-host** | `192.168.38.132` | Docker, Wazuh manager/indexer/dashboard | Linux administration user with sudo |
| **ubuntu-web** | `192.168.38.131` | Linux agent, Apache, SSH | Linux administration user with sudo |
| **win-client** | `192.168.38.133` | Windows agent, Sysmon, test processes | Elevated PowerShell where stated |

## What the deployment demonstrates

| Recorded | Still needs acceptance evidence |
| :--- | :--- |
| Three running Wazuh containers and two Active agents | Persistent addressing, final isolation and credential rotation |
| Windows logon failure and three custom discovery IDs | Successful sudo, Linux user creation and full raw-event context |
| Corrected SSH failure plus an alert listing | Restart/reboot persistence, idle memory and snapshot inventory |

<details>
<summary><strong>Open the recorded two-agent dashboard</strong></summary>

![Two Active endpoint agents](evidence/screenshots/image26.png)

E26 records both agents Active on 4.14.7. This is a point-in-time inventory, not a continuous uptime measurement.

</details>

> **Execution context:** The original VMware systems are not running in this documentation workspace. Source/release checks and command syntax were validated here; the guide does not label unexecuted VM steps as live-tested. Captured results and remaining checks are identified separately.

The source release is `v4.14.7`, commit `adcc5b57d2f7edfcbe6c399272dc76fbdf12b623`. Network examples must be merged into each VM’s existing configuration after its interface names and address availability are checked.

## Follow the event

```mermaid
flowchart LR
    A[Windows / Linux event] --> B[Wazuh agent]
    B --> C[Manager: decode + rules]
    C --> D[Filebeat: forward alert]
    D --> E[Indexer: store + search]
    E --> F[Dashboard: investigate]
    style C fill:#141A23,color:#ffffff,stroke:#E8BD62
    style F fill:#F4F3EF,color:#141A23,stroke:#C6A15A
```

The flow is the expected single-node design. The captures establish selected results rather than a full trace of every source event.

'''
    footer = '''
---

**Continue the project:** [All days](../../README.md) · [Command/rule index](docs/command-and-rule-index.md) · [Original screenshots](evidence/README.md) · [Operations handover](docs/operations.md)

The professional report is delivered separately. This is Roman Rzayev’s personal implementation record.
'''
    (DAY / 'README.md').write_text(intro + '\n'.join(rendered) + footer)


def make_root():
    (ROOT / 'README.md').write_text('''<p align="center"><img src="assets/project-hero.svg" alt="Automated SOC Workflow — Roman Rzayev" width="100%"></p>

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
''')


if __name__ == '__main__':
    hero('project-hero.svg', 'PERSONAL SECURITY ENGINEERING PORTFOLIO', 'Automated SOC Workflow', 'Build the platform. Follow the telemetry. Explain the detection.')
    hero('day-01-hero.svg', 'IMPLEMENTATION WALKTHROUGH / DAY 01', 'Security Monitoring Foundation', 'Commands, configuration, detection rules and the evidence behind them.', True)
    scorecard()
    for filename, number, title, subtitle in [
        ('design-network.svg', '01', 'Foundation & network', 'Provision → name → address → verify connectivity'),
        ('platform.svg', '02', 'Monitoring platform', 'Docker → kernel prerequisites → Wazuh → credential lifecycle'),
        ('endpoints.svg', '03', 'Endpoint telemetry', 'Linux agent → Apache / SSH → Windows agent → Sysmon'),
        ('detections.svg', '04', 'Detection engineering', 'Read the full XML → validate → generate events → attribute results'),
    ]:
        section_image(filename, number, title, subtitle)
    make_day()
    make_root()
    print('Built personal project and Day 01 pages with commands/configurations inline.')
