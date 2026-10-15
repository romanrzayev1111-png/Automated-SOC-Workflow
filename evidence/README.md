# Evidence register

Original PNG files extracted losslessly from the supplied implementation DOCX. Captions state what each image establishes; omissions are tracked in the acceptance matrix.

| Figure | Evidence | Observation |
| :--- | :--- | :--- |
| E01 | [Windows endpoint resources](screenshots/image1.png) | VMware settings show 4 GB RAM, 4 vCPUs, a 60 GB disk and Custom (VMnet1) networking. |
| E02 | [Linux endpoint resources](screenshots/image2.png) | VMware settings show 4 GB RAM, 2 vCPUs, a 500 GB disk and Custom (VMnet1) networking. |
| E03 | [Monitoring server resources](screenshots/image3.png) | VMware settings show 16 GB RAM, 6 vCPUs, a 500 GB disk, NAT and Custom (VMnet1) adapters. |
| E04 | [Virtual network configuration](screenshots/image4.png) | VMnet1 is Host-only on 192.168.38.0; DHCP is enabled. VMnet8 provides a separate NAT network. |
| E05 | [Windows address configuration](screenshots/image5.png) | The Windows endpoint reports 192.168.38.133 with subnet mask 255.255.255.0 and no displayed default gateway. |
| E06 | [Linux endpoint address configuration](screenshots/image6.png) | The Linux endpoint reports 192.168.38.131/24. The dynamic flag means static addressing is not demonstrated. |
| E07 | [Monitoring server interfaces](screenshots/image7.png) | The server reports 192.168.38.132/24 on ens36 and NAT address 192.168.121.156/24 on ens33; both are marked dynamic. |
| E08 | [Server-to-endpoint reachability](screenshots/image8.png) | The monitoring server receives three replies from each endpoint, with 0% packet loss in both short tests. |
| E09 | [Linux-to-peer reachability](screenshots/image9.png) | The Linux endpoint receives three replies from the server and three from Windows, with 0% packet loss. |
| E10 | [Windows-to-peer reachability](screenshots/image10.png) | Windows receives four replies from the Linux endpoint and four from the server, with 0% packet loss. |
| E11 | [Windows Sysmon installation](screenshots/image11.png) | Sysmon v15.22 loads the SwiftOnSecurity configuration; the Sysmon64 service is Running. Dashboard ingestion is not shown. |
| E12 | [Apache package installation](screenshots/image12.png) | APT output shows installation of Apache packages on the Linux endpoint; this capture is an installation stage. |
| E13 | [Apache service state](screenshots/image13.png) | Apache is enabled and active (running). A ServerName warning is visible; the service remains running. |
| E14 | [Web-service functional check](screenshots/image14.png) | A browser displays the Apache2 Ubuntu Default Page at the Linux endpoint address. Browser host identity is not independently shown. |
| E15 | [Pinned Wazuh source](screenshots/image15.png) | The recorded git clone selects wazuh-docker tag v4.14.7. Detached HEAD is expected for a release tag. |
| E16 | [Certificate-generation preparation](screenshots/image16.png) | The certificate-generation Compose command pulls the Wazuh certificate-tool image for the single-node deployment. |
| E17 | [Certificate-generation result](screenshots/image17.png) | The tool reports certificates created for indexer, manager, Filebeat and dashboard, and moves them into the deployment directory. |
| E18 | [Running single-node stack](screenshots/image18.png) | Docker Compose lists the dashboard, indexer and manager with 4.14.7 images and Up status. This is a point-in-time startup check. |
| E19 | [Dashboard sign-in page](screenshots/image19.png) | The Wazuh sign-in page is accessible in a browser. This does not prove a password change or certificate trust configuration. |
| E20 | [Authenticated dashboard](screenshots/image20.png) | The Wazuh overview loads after authentication and shows security-event summary widgets. These are not the five required controlled tests. |
| E21 | [Windows enrollment settings](screenshots/image21.png) | The dashboard deployment wizard selects Windows and the manager address 192.168.38.132 for an agent installation. |
| E22 | [Windows agent service start](screenshots/image22.png) | The agent install command names win-client. An initial NET HELPMSG 2185 response is followed by a successful WazuhSvc start. |
| E23 | [Windows agent active](screenshots/image23.png) | The inventory lists win-client at 192.168.38.133, agent v4.14.7, with active status. |
| E24 | [Linux enrollment settings](screenshots/image24.png) | The dashboard deployment wizard selects Linux and the same monitoring-server address. |
| E25 | [Linux agent service state](screenshots/image25.png) | systemctl reports wazuh-agent enabled and active (running), with agent processes visible. |
| E26 | [Two active monitored endpoints](screenshots/image26.png) | The inventory lists win-client and ubuntu-web as active, both on v4.14.7. The Linux endpoint is Ubuntu 22.04. |
| E27 | [Monitoring-server naming](screenshots/image27.png) | The hostnamectl command sets the server hostname to siem-host. A separate post-change hostname query is not shown. |
| E28 | [Linux endpoint naming](screenshots/image28.png) | The hostnamectl command sets the Linux endpoint hostname to ubuntu-web. |
| E29 | [Windows hostname context](screenshots/image29.png) | whoami returns win-client\roman, supporting the Windows computer-name context. |

The source dimensions and SHA-256 hashes are in [manifest.json](manifest.json). The PDF uses equal-size image frames with proportional fit; originals remain available here for source-resolution inspection.
