#!/usr/bin/env python3
"""Check Day 01 evidence fidelity, local links, XML rules and shell syntax."""
from pathlib import Path
import hashlib
import json
import re
import struct
import subprocess
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
DAY = ROOT / 'days/day-01'
records = json.loads((DAY / 'evidence/manifest.json').read_text())
assert len(records) == 40, 'Expected all 40 unique screenshots'
assert len({r['sha256'] for r in records}) == 40, 'Duplicate evidence assets'
for item in records:
    path = DAY / 'evidence/screenshots' / item['file']
    data = path.read_bytes()
    assert hashlib.sha256(data).hexdigest() == item['sha256'], path
    assert data[:8] == b'\x89PNG\r\n\x1a\n', path
    assert struct.unpack('>II', data[16:24]) == (item['width'], item['height']), path
    assert item['source_document'] in ['windows.docx', 'faridexiyetimbrat.docx'], path

for path in ROOT.rglob('*.md'):
    if '.venv' in path.parts:
        continue
    for link in re.findall(r'\]\(([^)]+)\)', path.read_text()):
        if '://' in link or link.startswith('#'):
            continue
        assert (path.parent / link.split('#')[0]).exists(), f'Broken link: {path.relative_to(ROOT)} -> {link}'
    for link in re.findall(r'src="([^"]+)"', path.read_text()):
        if '://' not in link:
            assert (path.parent / link).exists(), f'Broken image: {link}'

rules = ET.parse(DAY / 'config/windows-discovery-rules.xml').getroot()
expected = {'100100': '10', '100101': '9', '100102': '8', '100103': '12'}
assert {x.attrib['id']: x.attrib['level'] for x in rules.findall('rule')} == expected
samples = {
    '100100': r'C:\Windows\System32\whoami.exe',
    '100101': r'C:\Windows\System32\ipconfig.exe /all',
    '100102': r'C:\Windows\System32\hostname.exe',
    '100103': r'powershell.exe -EncodedCommand dwBoAG8AYQBtAGkA',
}
for rule in rules.findall('rule'):
    assert rule.findtext('if_sid') == '61603'
    field = rule.find('field')
    assert field.attrib == {'name': 'win.eventdata.commandLine', 'type': 'pcre2'}
    pattern = re.compile(field.text)
    assert pattern.search(samples[rule.attrib['id']]), f'Rule positive sample: {rule.attrib["id"]}'
    assert not pattern.search(r'C:\Windows\System32\notepad.exe'), f'Rule negative sample: {rule.attrib["id"]}'
assert ET.parse(DAY / 'config/sysmon-eventchannel.xml').getroot().findtext('location') == 'Microsoft-Windows-Sysmon/Operational'

guide_text = (DAY / 'step-by-step.md').read_text()
inline_text = (DAY / 'README.md').read_text()
for language, block in re.findall(r'```([^\n]+)\n(.*?)\n```', guide_text, re.S):
    assert f'```{language}\n{block}\n```' in inline_text, f'Guide block missing from visible Day 01 page: {language}'
for filename, language in [('netplan-siem-host.example.yaml', 'yaml'), ('netplan-ubuntu-web.example.yaml', 'yaml'), ('windows-discovery-rules.xml', 'xml')]:
    source = (DAY / 'config' / filename).read_text().strip()
    assert f'```{language}\n{source}\n```' in inline_text, f'Inline configuration differs: {filename}'
for step in range(1, 16):
    assert f'id="step-{step:02d}"' in inline_text, f'Missing navigation anchor: {step}'
blocks = re.findall(r'```bash\n(.*?)\n```', inline_text, re.S)
assert len(blocks) >= 15, 'Missing guide command blocks'
for n, block in enumerate(blocks, 1):
    result = subprocess.run(['bash', '-n'], input=block, text=True, capture_output=True)
    assert result.returncode == 0, f'Bash syntax block {n}: {result.stderr}'

# Inspect the current working tree, avoiding staged deletions from a restructure.
for path in ROOT.rglob('*'):
    if not path.is_file() or '.git' in path.parts or '.venv' in path.parts:
        continue
    name = str(path.relative_to(ROOT))
    assert not re.search(r'(^|/)(\.env(?:\..*)?|id_rsa|id_ed25519)$|\.(key|pem|p12|pfx|crt|cer|vmdk|vdi|qcow2|iso)$', name, re.I), f'Sensitive-file pattern: {name}'
print(f'PASS: 40 source hashes/dimensions; local links; full inline command/config fidelity; 15 chapter anchors; 4 XML rules; 8 regex cases; event-channel XML; {len(blocks)} Bash syntax blocks; sensitive-file patterns.')
print('Not performed here: live VMware/Wazuh replay, PowerShell execution, comprehensive secret/history scan.')
