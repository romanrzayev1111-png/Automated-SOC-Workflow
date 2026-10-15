# Operations handover

This is a procedure for the recorded VMware deployment. It is not a tested bootstrap script, and it does not install or start Wazuh in the report-generation container. Use the existing deployment files and securely stored local credentials.

## Prerequisites

- VMware host capacity sufficient for the recorded 24 GB assigned RAM, guest CPUs and virtual disks. Compare with the intended baseline before changing allocations.
- Correct persistent host-only addresses, server NAT and verified removal of temporary endpoint NAT.
- Docker Engine and the Compose plugin on siem-host; confirm their official installation source and exact versions.
- `vm.max_map_count` at least `262144`, persisted across reboot, as required by the Wazuh indexer.
- Existing certificates, local secrets and data volumes. Do not overwrite a working deployment from a generic example.
- Correct clocks and snapshots. The supplied evidence does not prove these prerequisites complete.

## Startup

1. Start siem-host and confirm its addresses and routes. The recorded path is `/root/wazuh-docker/single-node`; use an account with authorized access to that deployment.
2. Run these commands from that directory:

```bash
docker compose up -d
docker compose ps
docker compose logs --tail=100 wazuh.indexer wazuh.manager wazuh.dashboard
```

3. Verify dashboard HTTPS access, authentication and usable index searches from the operator workstation. Inspect the actual certificate before deciding how to trust the local deployment; do not turn off TLS verification to hide trust errors.
4. Start ubuntu-web and win-client. Confirm services:

```bash
# On ubuntu-web
systemctl is-active wazuh-agent apache2
```

```powershell
# On win-client
Get-Service WazuhSvc, Sysmon64
```

5. Confirm both agents Active and search for a newly generated authorized test event. Verify the Apache page from the workstation. A PID or open port alone does not establish readiness.

## Shutdown and data preservation

Stop endpoint workloads and shut down the endpoints first. From the existing single-node directory on siem-host:

```bash
docker compose stop
```

Then shut down siem-host. Avoid `docker compose down -v`, volume deletion and replacing configuration or certificates. Routine startup uses `docker compose up -d` against the same deployment.

## Recovery acceptance: currently open

1. Retain the agent inventory and a uniquely identifiable alert with timestamp and record identifier.
2. Stop and start the stack. Confirm both agents return Active and the old alert remains searchable.
3. Reboot siem-host. Repeat the same checks, including persistent kernel settings.
4. Record every command and result in the journal; capture failures and corrective actions.

## Memory measurement: currently open

```bash
docker stats --no-stream
```

Record the time, idle observation interval, all three container memory values and the deployment version. Do not populate the table from the VM RAM allocations; allocation and process usage are different measurements.

## Hardening and lifecycle: currently open

Follow the official [Wazuh Docker documentation](https://documentation.wazuh.com/current/deployment-options/docker/wazuh-container.html) for the exact deployment's password changes and dependent service settings. Keep credentials outside Git. Retain a secret-free confirmation of the change, final endpoint routes, snapshot inventories and the Windows evaluation expiry date.
