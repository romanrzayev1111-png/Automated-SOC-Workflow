#!/usr/bin/env python3
"""Check both days, original evidence, local navigation and configuration syntax."""
from pathlib import Path
import hashlib
import json
import re
import struct
import subprocess
import xml.etree.ElementTree as ET
from urllib.parse import unquote

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

DAY2 = ROOT / 'days/day-02'
source_members = []
new_image_count = 0
for folder, expected_count in [(DAY / 'evidence/ntp', 11), (DAY2 / 'evidence', 72)]:
    items = json.loads((folder / 'manifest.json').read_text())
    assert len(items) == expected_count, folder
    assert {p.name for p in (folder / 'screenshots').glob('*.png')} == {v['file'] for v in items}
    assert len({v['sha256'] for v in items}) == expected_count
    landing = (DAY / 'README.md' if expected_count == 11 else DAY2 / 'README.md').read_text()
    for item in items:
        data = (folder / 'screenshots' / item['file']).read_bytes()
        assert hashlib.sha256(data).hexdigest() == item['sha256'], item['file']
        assert struct.unpack('>II', data[16:24]) == (item['width'], item['height'])
        assert item['source_document'] == 'WEEK2.docx'
        assert item['source_document_sha256'] == 'e81724f790bd3a058298a3557b823e228bb11b0a7aae46e41c27c8e2441500a5'
        assert item['file'] in landing, f'Image absent from walkthrough: {item["file"]}'
        source_members.append(item['source_member'])
        new_image_count += 1
assert set(source_members) == {f'word/media/image{i}.png' for i in range(1, 84)}


def anchors(path):
    content = re.sub(r'```.*?```', '', path.read_text(), flags=re.S)
    result = set(re.findall(r'\bid="([^"]+)"', content))
    counts = {}
    for heading in re.findall(r'^#{1,6}\s+(.+)$', content, re.M):
        heading = re.sub(r'<[^>]+>', '', heading).lower().strip()
        slug = ''.join(c for c in heading if c.isalnum() or c in ' _-').replace(' ', '-')
        count = counts.get(slug, 0);counts[slug] = count + 1
        result.add(slug if count == 0 else f'{slug}-{count}')
    return result


link_count = 0
for path in ROOT.rglob('*.md'):
    if '.venv' in path.parts or '.git' in path.parts:
        continue
    content = path.read_text()
    links = re.findall(r'\]\(([^)]+)\)', content) + re.findall(r'(?:src|href)="([^"]+)"', content)
    for link in links:
        if '://' in link or link.startswith(('data:', 'mailto:')):
            continue
        target, _, fragment = unquote(link).partition('#')
        resolved = (path.parent / target).resolve() if target else path
        assert resolved.exists(), f'Broken link: {path.relative_to(ROOT)} -> {link}'
        if resolved.is_dir():resolved = resolved / 'README.md'
        if fragment and resolved.suffix == '.md':
            assert fragment in anchors(resolved), f'Broken anchor: {path.relative_to(ROOT)} -> {link}'
        link_count += 1

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

ntp_text = (DAY / 'docs/time-synchronization.md').read_text()
assert inline_text.count('id="ntp-time-synchronization"') == 1, 'NTP duplicated'
assert inline_text.index('## 0. NTP and timezone synchronization') < inline_text.index('## 1. VMs and network')
assert inline_text.index('## 0. NTP and timezone synchronization') < inline_text.index('## 4. Docker installation')
for language, block in re.findall(r'```([^\n]+)\n(.*?)\n```', ntp_text, re.S):
    assert f'```{language}\n{block}\n```' in inline_text, 'NTP block missing from Day 01'

day2_text = (DAY2 / 'README.md').read_text()
walkthrough = (DAY2 / 'walkthrough.md').read_text()
for language, block in re.findall(r'```([^\n]+)\n(.*?)\n```', walkthrough, re.S):
    assert f'```{language}\n{block}\n```' in day2_text, f'Day 02 inline block missing: {language}'
for step in range(1, 17):assert f'id="step-{step:02d}"' in day2_text
for text in [inline_text, day2_text]:
    assert len(re.findall(r'<details(?:\s[^>]*)?>', text)) == text.count('</details>')
    assert not re.search(r'<details\b[^>]*\bopen\b', text), 'Panels should be collapsed by default'

# XML fragments may contain multiple top-level Wazuh elements.
for path in list(DAY2.glob('config/*.xml')):
    ET.fromstring('<document>' + path.read_text() + '</document>')
decoder = ET.fromstring('<document>' + (DAY2 / 'config/labshop_decoders.xml').read_text() + '</document>')
assert decoder.find("decoder[@name='labshop']/program_name").text == '^labshop$'
child = decoder.find("decoder[@name='labshop-login']")
assert child.findtext('regex') == r'^(\w+) user=(\S+) src=(\S+)'
assert child.findtext('order') == 'action,dstuser,srcip'
parsed = re.match(child.findtext('regex'), 'LOGIN_FAILED user=admin src=192.168.38.133')
assert parsed and parsed.groups() == ('LOGIN_FAILED', 'admin', '192.168.38.133')
assert not re.match(child.findtext('regex'), 'INVALID_DATA test=hello')
labshop = ET.parse(DAY2 / 'config/labshop_rules.xml').getroot()
assert {v.get('id'): v.get('level') for v in labshop.findall('rule')} == {'100100': '5', '100101': '10'}
single = labshop.find("rule[@id='100100']");correlated = labshop.find("rule[@id='100101']")
assert single.findtext('action') == 'LOGIN_FAILED'
assert single.find('user').attrib['negate'] == 'yes' and single.findtext('user') == '^monitor$'
assert correlated.get('frequency') == '5' and correlated.get('timeframe') == '60'
assert correlated.findtext('if_matched_sid') == '100100' and correlated.find('same_srcip') is not None
for rule in labshop.findall('rule'):assert rule.findtext('mitre/id') == 'T1110'
assert 'sid:1000001;' in (DAY2 / 'config/labshop-admin.rules').read_text()
assert ET.parse(DAY2 / 'config/suricata-eve-localfile.xml').getroot().findtext('location') == '/var/log/suricata/eve.json'

extra_blocks = re.findall(r'```bash\n(.*?)\n```', day2_text, re.S)
for n, block in enumerate(extra_blocks, 1):
    result = subprocess.run(['bash', '-n'], input=block, text=True, capture_output=True)
    assert result.returncode == 0, f'Day 02 Bash block {n}: {result.stderr}'
for path in DAY2.glob('scripts/*.sh'):
    subprocess.run(['bash', '-n', str(path)], check=True)
yaml_result = 'not run (PyYAML unavailable)'
try:
    import yaml
except ImportError:
    pass
else:
    for path in list(DAY.glob('config/*.yaml')) + list(DAY2.glob('config/*.yaml')):
        yaml.safe_load(path.read_text())
    for block in re.findall(r'```yaml\n(.*?)\n```', day2_text, re.S):yaml.safe_load(block)
    yaml_result = 'passed'

tracked = subprocess.check_output(['git', 'ls-files'], cwd=ROOT, text=True).splitlines()
assert not any(Path(name).suffix.lower() in ['.pdf', '.doc', '.docx', '.zip'] for name in tracked), 'Report/source documents must stay outside Git'

# Inspect the current working tree, avoiding staged deletions from a restructure.
for path in ROOT.rglob('*'):
    if not path.is_file() or '.git' in path.parts or '.venv' in path.parts:
        continue
    name = str(path.relative_to(ROOT))
    assert not re.search(r'(^|/)(\.env(?:\..*)?|id_rsa|id_ed25519)$|\.(key|pem|p12|pfx|crt|cer|vmdk|vdi|qcow2|iso)$', name, re.I), f'Sensitive-file pattern: {name}'
print(f'PASS: 40 source hashes/dimensions; local links; full inline command/config fidelity; 15 chapter anchors; 4 XML rules; 8 regex cases; event-channel XML; {len(blocks)} Bash syntax blocks; sensitive-file patterns.')
print(f'PASS: {new_image_count} Week 2 originals (11 NTP + 72 Day 02); {link_count} local links/anchors; NTP first and unique; 16 Day 02 chapters; XML and LabShop parser structure; {len(extra_blocks)} Day 02 Bash blocks. YAML: {yaml_result}.')
print('Not performed here: live VMware/Wazuh replay, PowerShell execution, comprehensive secret/history scan.')
