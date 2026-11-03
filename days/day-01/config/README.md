# Configuration examples

These small examples support the [Day 01 guide](../step-by-step.md). They contain no credentials. They are not automatically applied.

- `netplan-ubuntu-web.example.yaml`: observed endpoint interface name and desired persistent host-only address.
- `netplan-siem-host.example.yaml`: observed server interface names, NAT DHCP and fixed host-only address.
- `sysmon-eventchannel.xml`: an ossec.conf fragment; merge inside the existing ossec_config element without duplicating a channel.
- `windows-discovery-rules.xml`: all four custom definitions captured in image35 of windows.docx. IDs 100100/100101/100102 have matching alert rows; 100103 is defined but its own ID is not observed in the supplied results.

Check local interface names, renderer, existing Netplan files, DHCP pool and address conflicts before applying any network change. Use the VM console and `netplan try` so a bad configuration can roll back. Do not replace unrelated networking or use these examples on the cloud report-generation machine.


The [NTP procedure](../docs/time-synchronization.md) uses `chrony-server.fragment.conf` and `chrony-client.fragment.conf`. The server pool directives are supplied by the Week 2 handoff; the subnet ACL and client peer line are captured in the DOCX. Merge with the existing Chrony configuration.

Historical Sysmon IDs in this folder match Day 01 screenshots. The Week 2 handoff reports their active migration to 100200–100203; do not install both the historical 100100/100101 definitions and the Day 02 LabShop block on one manager. [Details](../../day-02/README.md#step-02).
