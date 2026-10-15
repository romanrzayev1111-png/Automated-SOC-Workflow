#!/usr/bin/env python3
"""Validate actual report artifacts, source image fidelity and local document links."""
from pathlib import Path
from zipfile import ZipFile
from io import BytesIO
import hashlib
import json
import re
import subprocess

import fitz
from PIL import Image

ROOT=Path(__file__).resolve().parents[1]
records=json.loads((ROOT/'evidence/manifest.json').read_text())
assert len(records)==29, 'Expected all 29 source screenshots'
for item in records:
    p=ROOT/'evidence/screenshots'/item['file']
    assert hashlib.sha256(p.read_bytes()).hexdigest()==item['sha256'],p
    assert Image.open(p).size==(item['width'],item['height']),p

pdf=fitz.open(ROOT/'reports/Tetrion-Security-Monitoring-Report.pdf')
assert len(pdf)==24,f'Unexpected page count: {len(pdf)}'
alltext='\n'.join(p.get_text() for p in pdf)
for term in ['TETRION','Roman Rzayev','4.14.7','Executive summary','Architecture & asset inventory','E29']:
    assert term in alltext,term
assert 'SENTRYON' not in alltext, 'Reference company branding carried over'
assert 'ACADEMIC REPORT' not in alltext, 'Academic footer carried over'
for n in range(1,30):assert f'Figure E{n:02d}.' in alltext, f'Missing caption E{n:02d}'

# Match each PDF-embedded screenshot's decoded pixels to the source. Compression
# can change the container bytes; the pixel buffer must remain identical.
seen=[]
for page in pdf:
    for info in page.get_images(full=True):
        data=pdf.extract_image(info[0]);im=Image.open(BytesIO(data['image'])).convert('RGB')
        seen.append((im.size,hashlib.sha256(im.tobytes()).hexdigest()))
for item in records:
    im=Image.open(ROOT/'evidence/screenshots'/item['file']).convert('RGB')
    key=(im.size,hashlib.sha256(im.tobytes()).hexdigest())
    assert key in seen,f'Original source pixels absent from PDF: {item["file"]}'

with ZipFile(ROOT/'reports/Tetrion-Security-Monitoring-Report.docx') as z:
    blobs=[z.read(n) for n in z.namelist() if n.startswith('word/media/')]
    assert len(blobs)>=29,'DOCX missing screenshots'
    for item in records:
        assert any(hashlib.sha256(b).hexdigest()==item['sha256'] for b in blobs),f'DOCX source image changed: {item["file"]}'
    assert b'D9A514' in z.read('word/theme/theme1.xml'),'DOCX gold theme absent'

# Validate relative Markdown/image links used by the delivered repository.
for p in ROOT.rglob('*.md'):
    if '.venv' in p.parts:continue
    for link in re.findall(r'\]\(([^)]+)\)',p.read_text()):
        if '://' in link or link.startswith('#'):continue
        target=link.split('#')[0]
        assert (p.parent/target).exists(),f'Broken link: {p.relative_to(ROOT)} -> {link}'
    for link in re.findall(r'src="([^"]+)"',p.read_text()):
        if '://' not in link:assert (p.parent/link).exists(),f'Broken image: {link}'

names=subprocess.check_output(['git','ls-files','--cached','--others','--exclude-standard'],cwd=ROOT,text=True).splitlines()
for name in names:
    assert not re.search(r'(^|/)(\.env(?:\..*)?|id_rsa|id_ed25519)$|\.(key|pem|p12|pfx|crt|cer|vmdk|vdi|qcow2|iso)$',name,re.I),f'Sensitive-file pattern: {name}'
print('PASS: 29 source hashes and dimensions; 24 PDF pages; 29 PDF pixel matches; 29 byte-identical DOCX screenshots; gold theme; local links; sensitive-file patterns.')
print('This artifact check is not a live Wazuh test or a comprehensive secret/history scan.')
