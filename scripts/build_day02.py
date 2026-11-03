#!/usr/bin/env python3
"""Build the styled Day 02 landing page without altering original screenshots."""
from pathlib import Path
import re

from build_readmes import hero, scorecard, section_image
from screenshot_layout import DAY2_PRIMARY, prioritize, frame_screenshots

ROOT = Path(__file__).resolve().parents[1]
DAY = ROOT / 'days/day-02'


def architecture():
    target = DAY / 'architecture'
    target.mkdir(exist_ok=True)
    (target / 'architecture.svg').write_text('''<svg xmlns="http://www.w3.org/2000/svg" width="1280" height="640" viewBox="0 0 1280 640">
<title>Day 02: the recorded three-host monitoring topology</title>
<defs><marker id="arrow" markerWidth="9" markerHeight="9" refX="8" refY="4" orient="auto"><path d="M0 0 8 4 0 8" fill="#B28A3E"/></marker></defs>
<rect width="1280" height="640" rx="14" fill="#F4F3EF"/>
<g font-family="sans-serif" fill="#141A23">
<text x="35" y="49" font-size="24" font-weight="bold">DAY 02 / RECORDED TOPOLOGY</text>
<rect x="420" y="90" width="440" height="140" rx="10" fill="#141A23"/>
<g fill="#F8FAFC"><text x="445" y="126" font-size="24" font-weight="bold">siem-host · 192.168.38.132</text><text x="445" y="162" font-size="19">Wazuh 4.14.7 · Chrony NTP server</text><text x="445" y="196" font-size="17">Host-only network + upstream access via NAT</text></g>
<g stroke="#B28A3E" stroke-width="2" fill="none"><path d="M530 230V290H275V350"/><path d="M750 230V290H1005V350"/></g>
<text x="35" y="277" font-size="17">Agent events ↑ · NTP from .132 ↓</text><text x="882" y="277" font-size="17">Agent events ↑ · NTP from .132 ↓</text>
<rect x="35" y="350" width="510" height="205" rx="10" fill="white" stroke="#DDD8CD"/>
<text x="58" y="388" font-size="25" font-weight="bold">ubuntu-web · 192.168.38.131</text>
<text x="58" y="425" font-size="19">LabShop · Apache · Linux Wazuh agent</text>
<text x="58" y="460" font-size="19">Suricata 6.0.4 · AF_PACKET ens33</text>
<text x="58" y="495" font-size="18">eve.json → agent → manager → dashboard</text>
<text x="58" y="529" font-size="16" fill="#626A75">ens36 temporary NAT is still present in the capture</text>
<rect x="735" y="350" width="510" height="205" rx="10" fill="white" stroke="#DDD8CD"/>
<text x="758" y="388" font-size="25" font-weight="bold">win-client · 192.168.38.133</text>
<text x="758" y="425" font-size="19">Windows Wazuh agent · Sysmon</text>
<text x="758" y="460" font-size="19">File / Registry monitoring · local SCA</text>
<text x="758" y="495" font-size="18">curl.exe sends the /admin probe</text>
<text x="758" y="529" font-size="16" fill="#626A75">Windows Time uses .132,0x8</text>
<path d="M735 449H550" stroke="#B28A3E" stroke-width="2" fill="none" marker-end="url(#arrow)"/>
<text x="568" y="421" font-size="15">HTTP GET /admin</text>
<text x="35" y="600" font-size="18">VMnet1 / 192.168.38.0/24 · Addresses are recorded; final NAT removal and persistence need evidence.</text>
</g></svg>''')
    (target / 'README.md').write_text('''# Day 02 architecture

![Recorded topology](architecture.svg)

| System | Address | Recorded roles |
| :--- | :--- | :--- |
| siem-host | 192.168.38.132 | Wazuh 4.14.7 manager/indexer/dashboard, internal Chrony NTP server |
| ubuntu-web | 192.168.38.131 | LabShop, Apache, Linux agent, Suricata 6.0.4 on ens33 |
| win-client | 192.168.38.133 | Windows agent/Sysmon, files/Registry/SCA, HTTP test client |

W2-069 also shows ubuntu-web ens36 at 192.168.121.157/24. It was used for temporary installation access; final removal is not captured. HOME_NET is a rule variable, not capture-interface selection. The custom signature uses the literal .131 destination.

Time-service traffic uses UDP/123. Captured agents forward configured local logs; Suricata is a passive IDS in this setup, not a demonstrated inline firewall. [Day 01 NTP](../../day-01/README.md#ntp-time-synchronization) contains clock source and drift evidence.

[Back to walkthrough](../README.md)
''')


def build():
    hero('day-02-hero.svg', 'DAY 02 / IMPLEMENTATION NOTES', 'Detection & endpoint monitoring', 'LabShop logs, FIM, SCA, vulnerability inventory and Suricata EVE.', True, 'DAY 02')
    scorecard('day-02-metrics.svg', [('72', 'DAY 02 CAPTURES', 'Original embedded PNGs'), ('06', 'LABSHOP TEST CASES', 'Positive and qualified negatives'), ('02', 'SCA POLICIES', 'Before / after results'), ('01', 'EVE ALERT PIPELINE', 'Suricata SID → Wazuh rule')], 'Day 02 documentation coverage')
    phases = {
        1: ('day-02-application.svg', '01', 'Application detections', 'LabShop source → decoder → custom rules → six test cases'),
        4: ('day-02-integrity.svg', '02', 'File and Registry monitoring', 'Linux realtime · Windows files / Registry · scheduled scans'),
        8: ('day-02-assessment.svg', '03', 'Configuration and vulnerability review', 'SCA baselines → scoped hardening → inventory findings'),
        11: ('day-02-network.svg', '04', 'Suricata and SIEM integration', 'DNS / NIC recovery → HTTP signature → EVE JSON → Wazuh'),
    }
    body = (DAY / 'walkthrough.md').read_text()
    body = body[body.index('<a id="step-01">'):]
    for number, (filename, numeral, title, subtitle) in phases.items():
        section_image(filename, numeral, title, subtitle)
        marker = f'<a id="step-{number:02d}"></a>'
        body = body.replace(marker, f'![{title}](../../assets/{filename})\n\n' + marker, 1)
    intro = '''<p align="center"><img src="../../assets/day-02-hero.svg" alt="Day 02 — detection and endpoint monitoring" width="100%"></p>

<p align="center"><strong>Roman Rzayev</strong> · Wazuh 4.14.7 · Suricata 6.0.4 · Windows + Ubuntu</p>

# Day 02 · Detection and endpoint monitoring

This day adds application detections, file/Registry monitoring, SCA hardening and a Suricata HTTP rule to the existing deployment. Commands and key results are shown inline. Expand an arrow for command notes or supporting screenshots; click an image to open its original resolution.

![Day 02 coverage](../../assets/day-02-metrics.svg)

**Before generating fresh evidence:** complete [NTP and timezone synchronization at the beginning of Day 01](../day-01/README.md#ntp-time-synchronization).

| Application | Endpoint / assessment | Network detection |
| :--- | :--- | :--- |
| [01 · Source collection](#step-01) | [04 · Linux realtime FIM](#step-04) | [11 · Installation / DNS](#step-11) |
| [02 · Full decoder and rules](#step-02) | [05 · Windows files](#step-05) · [06 · Registry](#step-06) | [12 · ens33 / HOME_NET](#step-12) |
| [03 · Six tests](#step-03) | [07 · Scheduled FIM](#step-07) · [08 · SCA](#step-08) | [13 · HTTP signature](#step-13) |
| [Test verdict matrix](docs/test-matrix.md) | [09 · SCA remediation](#step-09) · [10 · Vulnerabilities](#step-10) | [14 · Packet/log validation](#step-14) |
| [Source notes](docs/source-notes.md) | [Acceptance gaps](docs/acceptance.md) | [15 · EVE collection](#step-15) · [16 · Wazuh 86601](#step-16) |

## Environment

![Three-host topology](architecture/architecture.svg)

| Host | Address | Main work |
| :--- | :--- | :--- |
| siem-host | 192.168.38.132 | Wazuh manager/container rules; Chrony server |
| ubuntu-web | 192.168.38.131 | LabShop, Apache, agent, FIM, SCA and Suricata ens33 |
| win-client | 192.168.38.133 | Windows agent, files/Registry/SCA and the HTTP probe |

## Results at a glance

| Supported by captures | Qualification / open check |
| :--- | :--- |
| LabShop 100100/5 and 100101/10 positives | Split-source negative contains a correlation alert; success/malformed verdicts need stronger proof |
| Linux/Windows file events and Registry changes | Scheduled interval restoration, exact Windows interval and formal latency comparison are not proved |
| Ubuntu SCA 92→94 passed; Windows 117→118 passed | Remaining policy failures and CVE remediation are separate work |
| Suricata SID 1000001 reaches Wazuh 86601/3 from eve.json | IDS action allowed; no blocking, reboot or final-isolation claim |

**Sources:** the execution handoff and the 25-page uploaded DOCX. All 83 media objects are preserved: 11 NTP images in Day 01 and 72 here. [Source notes](docs/source-notes.md) distinguish captured results, handoff reports and replay instructions. The VMs were not operated by this documentation work.

## Event paths

```mermaid
flowchart LR
  L[LabShop syslog] --> A[Ubuntu Wazuh agent]
  F[Files / Registry / SCA] --> W[Endpoint agents]
  C[Windows curl /admin] --> S[Suricata ens33]
  S --> E[eve.json alert]
  E --> A
  A --> M[Wazuh manager]
  W --> M
  M --> I[Indexer / dashboard]
  style S fill:#141A23,color:#ffffff,stroke:#E8BD62
  style M fill:#141A23,color:#ffffff,stroke:#E8BD62
```

For LabShop, custom manager rules use 100100/100101. For Suricata, custom network signature 1000001 is classified by built-in Wazuh 86601. These identifiers belong to different rule systems.

'''
    footer = '''
---

[All days](../../README.md) · [Day 01 and NTP](../day-01/README.md#ntp-time-synchronization) · [Evidence register](evidence/README.md) · [Configuration files](config/README.md) · [Journal](journal.md) · [Acceptance](docs/acceptance.md)

Prepared by Roman Rzayev.
'''
    page = prioritize(intro + body + footer, DAY2_PRIMARY)
    (DAY / 'README.md').write_text(frame_screenshots(page, DAY))
    architecture()
    print('Built Day 02: 16 stages, inline configuration and all 72 original captures.')


if __name__ == '__main__':
    build()
