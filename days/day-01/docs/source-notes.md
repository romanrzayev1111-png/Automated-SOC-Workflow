# Source and evidence notes

## Implementation sources

- `windows.docx`: corrected primary implementation source, containing **37 embedded PNGs**.
- `faridexiyetimbrat.docx`: earlier source; its first 26 images also appear in the corrected document, and three distinct hostname captures are retained as E38–E40.
- `Week1_SOC_Lab (1).docx`: acceptance baseline; instructions define intended work, not completed work.
- Supplied conversation excerpt: supplementary context. Claims are checked against screenshots and final code rather than accepted as test outcomes.

There are **40 unique screenshots**. E01–E37 map to image1–image37 in windows.docx. E38–E40 map to image27–image29 in the earlier document. `evidence/manifest.json` preserves the source document/member, original dimensions and SHA-256 for each asset. Source documents and the raw conversation are not committed.

## Configuration provenance

`config/windows-discovery-rules.xml` transcribes the four definitions visible in E35. Parent rule 61603 was checked directly in Wazuh v4.14.7's 0595-win-sysmon_rules.xml and is Sysmon Event ID 1 / process creation. E34 shows IDs 100100, 100101 and 100102. It shows built-in 92057 for encoded PowerShell, not custom 100103.

The guide's Compose names, images, certificate generator and ports were checked against wazuh-docker v4.14.7, commit adcc5b57d2f7edfcbe6c399272dc76fbdf12b623. Docker installation commands follow the official Ubuntu repository procedure. Source checks and syntax checks are not live VM replay results.

## Interpretation corrections

- E14 uses localhost; it does not prove physical-workstation HTTP access.
- E21/E24 are intermediate wizards with wrong server addresses/names. E24 also selects RPM rather than the Ubuntu DEB path. The actual manager is .132; inventory confirms win-client and ubuntu-web.
- E29 is an unreachable SSH target; E36 is the corrected genuine failure.
- E30/E31 do not prove successful sudo or user creation.
- Cropped result lists can omit correlation fields. The event register retains those limits.

## Repository and report separation

This repository is Roman Rzayev's personal implementation record, organized by day. The professional company-branded report and its generation assets are delivered separately, outside the current GitHub walkthrough tree. No corporate identity is applied to the personal profile or project documentation.

Original screenshots remain lossless PNGs. The separately delivered report fits them proportionally in equal-size frames; no screenshot text is reconstructed or artificially sharpened. Missing source detail cannot be recovered by upscaling.
