# Evidence register

Original PNG files extracted losslessly from windows.docx (E01-E37) and three supplementary hostname captures from faridexiyetimbrat.docx (E38-E40). Captions state what each image establishes; omissions are tracked in the acceptance matrix.

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
| E14 | [Web-service functional check](screenshots/image14.png) | A browser displays the Apache2 Ubuntu Default Page at localhost. This does not establish access from the physical operator workstation. |
| E15 | [Pinned Wazuh source](screenshots/image15.png) | The recorded git clone selects wazuh-docker tag v4.14.7. Detached HEAD is expected for a release tag. |
| E16 | [Certificate-generation preparation](screenshots/image16.png) | The certificate-generation Compose command pulls the Wazuh certificate-tool image for the single-node deployment. |
| E17 | [Certificate-generation result](screenshots/image17.png) | The tool reports certificates created for indexer, manager, Filebeat and dashboard, and moves them into the deployment directory. |
| E18 | [Running single-node stack](screenshots/image18.png) | Docker Compose lists the dashboard, indexer and manager with 4.14.7 images and Up status. This is a point-in-time startup check. |
| E19 | [Dashboard sign-in page](screenshots/image19.png) | The Wazuh sign-in page is accessible at localhost in a browser. This does not prove a password change or certificate trust configuration. |
| E20 | [Authenticated dashboard](screenshots/image20.png) | The Wazuh overview loads after authentication and shows security-event summary widgets. These are not the five required controlled tests. |
| E21 | [Windows enrollment settings](screenshots/image21.png) | Intermediate wizard: Windows is selected, but the address is incorrectly set to 192.168.38.133 and name Winagent. The successful command in E22 uses manager .132 and win-client. |
| E22 | [Windows agent service start](screenshots/image22.png) | The agent install command names win-client. An initial NET HELPMSG 2185 response is followed by a successful WazuhSvc start. |
| E23 | [Windows agent active](screenshots/image23.png) | The inventory lists win-client at 192.168.38.133, agent v4.14.7, with active status. |
| E24 | [Linux enrollment settings](screenshots/image24.png) | Intermediate wizard: RPM, endpoint address 192.168.38.131 and Ubuntuagent are selected. These are not the final Ubuntu DEB settings or the correct manager address. |
| E25 | [Linux agent service state](screenshots/image25.png) | systemctl reports wazuh-agent enabled and active (running), with agent processes visible. |
| E26 | [Two active monitored endpoints](screenshots/image26.png) | The inventory lists win-client and ubuntu-web as active, both on v4.14.7. The Linux endpoint is Ubuntu 22.04. |
| E27 | [Windows process launch](screenshots/image27.png) | Notepad is open on Windows. This alone does not show a Sysmon or dashboard event. |
| E28 | [Intentional Windows credential failure](screenshots/image28.png) | runas with an invalid account returns error 1326: the user name or password is incorrect. |
| E29 | [Initial SSH target error](screenshots/image29.png) | SSH attempts to 192.168.99.130 fail with Network is unreachable. No target login occurs in these attempts. |
| E30 | [Unsuccessful sudo authentication](screenshots/image30.png) | The sudo command ends after three incorrect password attempts. Successful privileged command execution is not shown. |
| E31 | [User-creation attempt not executed](screenshots/image31.png) | sudo useradd fails authentication; this capture does not show a new user being created. |
| E32 | [Windows logon alert](screenshots/image32.png) | The dashboard lists win-client with Logon Failure - Unknown user or bad password, rule 60122, level 5. |
| E33 | [Controlled Windows discovery actions](screenshots/image33.png) | PowerShell runs whoami, ipconfig, hostname and a Base64-encoded whoami command on win-client. |
| E34 | [Windows discovery alert results](screenshots/image34.png) | The result list shows custom rules 100100 (level 10), 100101 (9), 100102 (8), plus built-in encoded-PowerShell rule 92057 (12). Rule 92213 (15) is also visible but is not causally attributed. |
| E35 | [Captured custom Sysmon rules](screenshots/image35.png) | Four definitions use parent 61603: custom IDs 100100-100103, levels 10, 9, 8 and 12. A definition is not proof that every ID fired. |
| E36 | [Corrected SSH destination](screenshots/image36.png) | An SSH attempt reaches 192.168.38.131 and ends with Permission denied. The prompt shows ubuntu-web connecting to its own endpoint address. |
| E37 | [Linux authentication alert results](screenshots/image37.png) | The cropped list shows sshd non-existent-user rule 5710 at level 5 and syslog rule 2502 at level 10. Agent and timestamps are outside this crop. |
| E38 | [Monitoring-server naming](screenshots/image38.png) | The hostnamectl command sets siem-host in the supplementary source. A separate post-change query is not shown. |
| E39 | [Linux endpoint naming](screenshots/image39.png) | The hostnamectl command sets ubuntu-web in the supplementary source. |
| E40 | [Windows hostname context](screenshots/image40.png) | whoami returns win-client\roman in the supplementary source. |

The source dimensions and SHA-256 hashes are in [manifest.json](manifest.json). The PDF uses equal-size image frames with proportional fit; originals remain available here for source-resolution inspection.
