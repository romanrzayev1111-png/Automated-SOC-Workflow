# Sources and reconstruction notes

## Available sources

1. **Week 2 execution handoff**, pasted in this chat: conversation-derived commands, corrections, DNS repair, time-service output and the rule-ID migration.
2. **WEEK2.docx**, the uploaded file: 3,248,299 bytes, Word metadata reports **25 pages**, and **83 PNG media objects**. Its final images contain the Suricata EVE-origin Wazuh alert. The request/handoff calls the updated document `WEEK2(1).docx`; the available filename is `WEEK2.docx`. We use its supplied 25-page content, not the earlier 23-page version discussed in the handoff.
3. Repository commit `5049acd`: Day 01 presentation and preliminary Day 02 README/journal/acceptance. Draft claims were reviewed rather than treated as proof.

The complete private Week 2 conversation is not in this session. The handoff is the available conversation-derived source; no claim is made that the original chat was opened remotely.

DOCX SHA-256:

```text
e81724f790bd3a058298a3557b823e228bb11b0a7aae46e41c27c8e2441500a5
```

## Evidence mapping

- Images 1–11: [Day 01 NTP evidence](../../day-01/evidence/ntp/README.md).
- Images 12–83: [Day 02 screenshots](../evidence/screenshots).
- Files are copied directly from DOCX word/media entries. Manifests preserve original member names, paragraph indices, dimensions, hashes and captions.
- Mapping was checked against adjacent text and pixels. Image numbering is traceability, not an inferred timestamp or a one-image-per-page assumption.
- Cached Word page-break data is incomplete; exact per-image page numbers are not invented.

## Labels

**Captured** means visible in a screenshot. **Handoff-reported** means execution context supplied by the conversation compilation but not independently visible in that capture. **Replay / verification procedure** means a documented command without a claim of new VM execution.

Explicit adjustments are labelled, such as using `rm --` rather than captured `rm -rf` for a known regular test file. The original generator body, exact Windows Registry test interval and effective Suricata rule-files list are not supplied and are not presented as recovered code.

## Corrections to the draft

| Issue | Reviewed treatment |
| :--- | :--- |
| All six LabShop cases passed | Separate positive tests, generic fallback, source-only proof and unresolved split-source result |
| Monitor produces no rule | W2-022 shows generic 1002/2 |
| Split-source negative accepted | W2-024 includes 100101/10; expanded fields and an isolated retest are needed |
| Malformed message parsed successfully | W2-028 shows pre-decoding only, not structured fields or final verdict |
| Decoder expression / extra rule groups | Follow W2-014/016, including `\w+`, static action, exact user exclusion and T1110 |
| Custom ID overlap | Preserve historical Day 01 evidence; handoff reports active migration to 100200–100203 |
| Registry implied realtime | Scan-based; exact shortened Windows frequency is absent |
| Whole-host vulnerability totals | Views are agent-specific and Critical-filtered |
| Latest Suricata/PPA implied | Runtime 6.0.4 is captured; PPA execution is not |
| HTTP EVE record used as alert proof | W2-077 is HTTP; W2-080–083 prove alert-type JSON, eve.json source and 86601/3 |
| Same timezone equated with NTP | Source selection, startup transient, listener, drift/dispersion and isolation are separate checks |

## Validation boundaries

No VM was operated by this documentation work. Static checks cover assets, XML/YAML/Bash/Markdown and source integrity. Rule-engine behavior, PowerShell, packet capture, reboot recovery and remediation require the actual environment. A configured frequency or an alert description is not an exact measured trigger threshold.

No PDF/Word source or report, credentials, private keys or certificate files are added to the current repository tree.
