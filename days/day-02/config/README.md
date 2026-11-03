# Configuration files

These support the [walkthrough](../README.md). Merge fragments into existing configuration; do not replace a working deployment wholesale.

| File | Host / destination | Source and scope |
| :--- | :--- | :--- |
| [labshop-localfile.xml](labshop-localfile.xml) | ubuntu-web · ossec.conf | W2-013; existing ossec_config |
| [labshop_decoders.xml](labshop_decoders.xml) | Manager · etc/decoders | W2-014; multiple top-level decoder elements are valid Wazuh file syntax |
| [labshop_rules.xml](labshop_rules.xml) | Manager · etc/rules | W2-016; resolve historical Day 01 ID overlap first |
| [linux-syscheck.fragment.xml](linux-syscheck.fragment.xml) | ubuntu-web · syscheck | W2-029/046; retain existing ignore/nodiff options |
| [windows-syscheck.fragment.xml](windows-syscheck.fragment.xml) | win-client · syscheck | W2-037; files and Registry |
| [suricata-capture.fragment.yaml](suricata-capture.fragment.yaml) | ubuntu-web · suricata.yaml | W2-070/071; merge vars and AF_PACKET |
| [labshop-admin.rules](labshop-admin.rules) | ubuntu-web · /etc/suricata/rules/suricata.rules | W2-073; SID 1000001; rule-files list is not captured |
| [suricata-eve-localfile.xml](suricata-eve-localfile.xml) | ubuntu-web · ossec.conf | W2-079; JSON input and built-in Wazuh classification |

[Remediation scripts](../scripts/) are transcribed from W2-055 and W2-059. They change local security settings and are not executed by documentation checks. Review the matching baseline/policy and preserve rollback data before use.

Chrony directives and the full [NTP procedure](../../day-01/docs/time-synchronization.md) are in Day 01.
