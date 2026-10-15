# Source and design notes

## Source roles

- `Week1_SOC_Lab (1).docx`: requirements and intended acceptance baseline; not proof of completion.
- `faridexiyetimbrat.docx`: implementation notes and 29 embedded PNG screenshots.
- `ED-Lab04-Executive-Report.pdf`: visual reference for header/footer, page structure, tables and evidence presentation. Its unrelated technical claims and Sentryon identity are not reused.
- User-supplied Tetrion reference: brand name, black-and-white emblem, gold accent and tagline.

The source documents are not committed. The evidence assets are extracted losslessly from the implementation DOCX; their original filenames are retained for traceability. See `evidence/manifest.json` for source pixel dimensions and SHA-256 hashes.

## Branding

The mark in `assets/tetrion-mark.svg` is a vector interpretation of the low-resolution emblem in the supplied brand reference, not an original brand-master file. The same geometry is used in the PDF and the high-resolution PNG. Replace this interpretation with the official SVG when available if exact brand-master fidelity is required. No new company claims, team-member identities or employment history were invented.

Palette: charcoal `#141414`, gold `#D9A514`, white, warm paper `#F5F3ED`. The page frame uses restrained circuit-like lines inspired by the reference document. The professional report title is *Security Monitoring Foundation — Deployment & Operational Handover Report*; academic presentation is confined to requirement traceability in supporting documentation.

## Evidence presentation

All screenshot frames in the PDF are 493.276 × 205 pt. Images fit within those frames proportionally, without cropping or re-encoding source assets. Equal frames do not mean stretching every image into the same aspect ratio. The originals range from 196 × 52 to 1920 × 744 pixels; upscaling cannot create authentic new text detail. Full-resolution originals remain in `evidence/screenshots/`.

The DOCX uses equal table-cell frames with proportional image fit and a gold accent theme. It is editable; the PDF is the reviewed fixed-layout master. Report issue date is 15 October 2026; it is not a claim that the captured work occurred on that date.

## Boundaries of this delivery

The original VMs were not available for live testing. Report generation and repository artifact checks can be validated here; Wazuh health, controlled security events, memory usage and recovery on the original systems cannot be newly certified from documents alone. Source omissions remain visible in the acceptance matrix.
