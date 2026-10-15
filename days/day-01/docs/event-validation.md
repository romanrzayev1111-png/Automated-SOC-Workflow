# Controlled-event capture register

Status reflects the supplied screenshots, not a new live VM test. A complete record retains agent, timestamp, command/source event, rule description, level and screenshot.

| Test | Agent / context | Rule description | ID / level | Evidence | Result |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Failed SSH login | ubuntu-web terminal targets its own .131 address; alert crop has no agent/time | sshd: Attempt to login using a non-existent user | 5710 / 5 | [E36](../evidence/screenshots/image36.png), [E37](../evidence/screenshots/image37.png) | Attempt and alert listing recorded; full correlation context needed |
| Successful sudo command | ubuntu-web | Not supplied | Not supplied | [E30](../evidence/screenshots/image30.png) instead shows authentication failure | Open |
| Linux local-user creation | ubuntu-web | Not supplied | Not supplied | [E31](../evidence/screenshots/image31.png) instead shows authentication failure | Open |
| Windows process through Sysmon | win-client; descriptions include hostname | Windows user / network / system discovery | 100100 / 10; 100101 / 9; 100102 / 8 | [E33–E35](../evidence/README.md) | Commands, definitions and matching custom alerts recorded; retain expanded raw event |
| Failed Windows logon | win-client, 9 October 2026 11:47:05.217 as displayed; timezone not established | Logon Failure - Unknown user or bad password | 60122 / 5 | [E28](../evidence/screenshots/image28.png), [E32](../evidence/screenshots/image32.png) | Recorded |

E34 also shows built-in encoded-PowerShell rule 92057 / level 12. The custom encoded-PowerShell definition 100103 / level 12 is present in E35, but its own rule ID is not shown firing. E34's 92213 / level 15 row is visible without enough context to tie it to a deliberate test.

The parent 61603 used by the custom definitions is the Wazuh 4.14.7 Sysmon Event ID 1 rule. For complete traceability, retain an expanded raw event with Microsoft-Windows-Sysmon/Operational, Event ID, command line, agent name and timestamp. Do not infer complete ingestion from the installed service alone.

New screenshots should retain original pixels and omit passwords/session tokens. Update the evidence manifest only after review.
