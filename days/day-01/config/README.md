# Configuration examples

These small examples support the [Day 01 guide](../step-by-step.md). They contain no credentials. They are not automatically applied.

- `netplan-ubuntu-web.example.yaml`: observed endpoint interface name and desired persistent host-only address.
- `netplan-siem-host.example.yaml`: observed server interface names, NAT DHCP and fixed host-only address.
- `sysmon-eventchannel.xml`: an ossec.conf fragment; merge inside the existing ossec_config element without duplicating a channel.
- `windows-discovery-rules.xml`: all four custom definitions captured in image35 of windows.docx. IDs 100100/100101/100102 have matching alert rows; 100103 is defined but its own ID is not observed in the supplied results.

Check local interface names, renderer, existing Netplan files, DHCP pool and address conflicts before applying any network change. Use the VM console and `netplan try` so a bad configuration can roll back. Do not replace unrelated networking or use these examples on the cloud report-generation machine.
