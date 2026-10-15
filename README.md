# Automated SOC Workflow

A personal, day-by-day security monitoring project by **Roman Rzayev**. Each day keeps its own implementation guide, configuration examples, architecture, evidence and journal. Professional PDF reports are delivered separately from the GitHub walkthroughs.

## Project timeline

| Day | Focus | Guide | Implementation record |
| :--- | :--- | :--- | :--- |
| **01** | Wazuh platform, Windows/Linux agents, Sysmon and Apache | [Step-by-step](days/day-01/step-by-step.md) | [Overview & evidence](days/day-01/README.md) |

Only Day 01 has been supplied. Later days will be added when their material is available; no future work is marked complete in advance.

## Day 01 at a glance

- **Wazuh 4.14.7:** single-node Docker deployment; manager, indexer and dashboard shown running.
- **Two Active agents:** `win-client` and `ubuntu-web`, both 4.14.7.
- **Endpoint preparation:** Sysmon 15.22 Running; Apache default page opens.
- **Evidence:** 40 original screenshots (37 in the revised document plus three distinct hostname captures), source dimensions, SHA-256 hashes and precise captions.
- **Acceptance:** missing event captures, recovery tests and hardening checks remain visible in the [matrix](days/day-01/docs/acceptance.md).

![Day 01 architecture](days/day-01/architecture/architecture.svg)

## Repository layout

```text
days/
  day-01/
    README.md           Implementation summary
    step-by-step.md     Ordered technical guide, commands and expected checks
    config/             Small configuration examples; no credentials
    architecture/       Diagram and address/resource inventory
    evidence/           Original screenshots, captions and integrity manifest
    docs/               Operations, acceptance and event-validation records
    journal.md          Evidence-based retrospective
profile/                Prepared profile README and account bio
scripts/                Evidence, link and rule verification
```

For subsequent work, use `days/day-02/`, `days/day-03/` and so on. Keep each day's changes and evidence in its own directory and add one row to the timeline. Reuse shared brand assets rather than duplicating them.

## Reading the evidence

**Recorded** observations come from supplied captures. **Reported** observations come from a conversation without matching artifacts. **Documented procedures** are implementation instructions, not proof that a command was executed. The distinction is preserved throughout the project.

The guide has been checked against the release's source files and official documentation. The original VMware machines were not available in this workspace, so new Linux/Windows deployment commands and controlled-event tests are not labeled as live-tested here.

## Repository checks

```bash
python3 scripts/verify_artifacts.py
```

The check validates source screenshot hashes/dimensions, relative links, the four custom rule definitions and representative regex matches. It does not replace an actual Wazuh event replay or a live VM acceptance test. The professional PDF is delivered separately and is not part of the current walkthrough tree.

## Profile

Prepared profile name: **Roman Rzayev**. The short [bio and display-name settings](profile/settings.json) and [profile README](profile/README.md) are ready; account-level application depends on GitHub API access. Their presence in this repository does not change the account profile automatically.


