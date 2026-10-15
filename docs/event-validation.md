# Controlled-event capture register

Status: **not executed in this document review**. Complete on the original authorized endpoints. Use a narrow time window and the relevant agent filter in the dashboard. Retain each alert's rule description and level exactly as displayed; event presence alone may not imply an alert at the expected level.

| Test | Agent | UTC timestamp | Event / rule description | Rule level | Screenshot | Result |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| Failed SSH login | ubuntu-web | Not recorded | Not recorded | Not recorded | Not supplied | Open |
| Command run with sudo | ubuntu-web | Not recorded | Not recorded | Not recorded | Not supplied | Open |
| Linux local-user creation | ubuntu-web | Not recorded | Not recorded | Not recorded | Not supplied | Open |
| Windows process launch via Sysmon | win-client | Not recorded | Not recorded | Not recorded | Not supplied | Open |
| Failed Windows logon | win-client | Not recorded | Not recorded | Not recorded | Not supplied | Open |

For Sysmon, retain the `Microsoft-Windows-Sysmon/Operational` channel, Event ID, agent name and process context. Verify the Wazuh agent actually reads the channel. An installed Sysmon service is not sufficient.

Name new screenshots descriptively, for example `sysmon-process-create.png`. Keep the original source pixels, avoid passwords and session tokens, and update the evidence manifest only after review. Record a genuine failed result rather than replacing it with a success claim.
