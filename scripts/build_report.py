#!/usr/bin/env python3
"""Build the Tetrion report from original evidence without resampling screenshots."""
from pathlib import Path
from xml.sax.saxutils import escape
import hashlib
import json

from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph, Table, TableStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.utils import ImageReader
from PIL import Image
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'reports'
SHOTS = ROOT / 'evidence/screenshots'
DATE = '15 OCTOBER 2026'
FONTROOT = Path('/usr/share/fonts/truetype/dejavu')
for name, fname in [('Regular','DejaVuSans.ttf'),('Bold','DejaVuSans-Bold.ttf'),('Italic','DejaVuSans-Oblique.ttf')]:
    pdfmetrics.registerFont(TTFont(name, str(FONTROOT/fname)))
pdfmetrics.registerFontFamily('Regular',normal='Regular',bold='Bold',italic='Italic')
BLACK=colors.HexColor('#141414'); GOLD=colors.HexColor('#D9A514'); MUTED=colors.HexColor('#626262')
LIGHT=colors.HexColor('#F5F3ED'); LINE=colors.HexColor('#DDD7C9')
W,H=595.276,841.89
LEFT,RIGHT=51,544
WIDTH=RIGHT-LEFT

# Vector interpretation of the mark in the user-supplied brand reference.
LOGO_PATH='M12 12H25Q32 12 32 20Q32 12 39 12H52V25Q52 32 44 32Q52 32 52 39V52H39Q32 52 32 44Q32 52 25 52H12V39Q12 32 20 32Q12 32 12 25Z'
def logo(c,x,y,size=25,inverse=False):
    c.saveState();c.translate(x,y);c.scale(size/64,size/64)
    c.setFillColor(colors.white if inverse else BLACK)
    p=c.beginPath();p.moveTo(12,12);p.lineTo(25,12);p.curveTo(32,12,32,17,32,20);p.curveTo(32,12,35,12,39,12);p.lineTo(52,12);p.lineTo(52,25);p.curveTo(52,32,47,32,44,32);p.curveTo(52,32,52,35,52,39);p.lineTo(52,52);p.lineTo(39,52);p.curveTo(32,52,32,47,32,44);p.curveTo(32,52,29,52,25,52);p.lineTo(12,52);p.lineTo(12,39);p.curveTo(12,32,17,32,20,32);p.curveTo(12,32,12,29,12,25);p.close();c.drawPath(p,fill=1,stroke=0)
    c.setFillColor(BLACK if inverse else colors.white)
    for cx,cy in [(26,26),(38,26),(26,38),(38,38)]:c.circle(cx,cy,6.5,fill=1,stroke=0)
    c.setFillColor(colors.white if inverse else BLACK);p=c.beginPath();p.moveTo(32,27);p.lineTo(37,32);p.lineTo(32,37);p.lineTo(27,32);p.close();c.drawPath(p,fill=1,stroke=0)
    c.restoreState()

def write_svg():
    (ROOT/'assets/tetrion-mark.svg').write_text(f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><title>Tetrion brand mark</title><path fill="#141414" d="{LOGO_PATH}"/><g fill="white"><circle cx="26" cy="26" r="6.5"/><circle cx="38" cy="26" r="6.5"/><circle cx="26" cy="38" r="6.5"/><circle cx="38" cy="38" r="6.5"/></g><path fill="#141414" d="m32 27 5 5-5 5-5-5z"/></svg>''')
    (ROOT/'assets/tetrion-banner.svg').write_text(f'''<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="440" viewBox="0 0 1600 440"><title>Tetrion - Security Monitoring Foundation</title><rect width="1600" height="440" rx="12" fill="#141414"/><path d="M0 64H380L405 89H1520L1560 129V440M40 0V310L80 350H1600" stroke="#D9A514" fill="none" stroke-width="2"/><g transform="translate(76 94) scale(1.4)"><path fill="white" d="{LOGO_PATH}"/><g fill="#141414"><circle cx="26" cy="26" r="6.5"/><circle cx="38" cy="26" r="6.5"/><circle cx="26" cy="38" r="6.5"/><circle cx="38" cy="38" r="6.5"/></g><path fill="white" d="m32 27 5 5-5 5-5-5z"/></g><g font-family="Arial,sans-serif"><text x="180" y="151" fill="white" font-size="36" font-weight="bold" letter-spacing="4">TETRION</text><text x="92" y="242" fill="white" font-size="54" font-weight="bold">Security Monitoring Foundation</text><text x="95" y="298" fill="#D9A514" font-size="23">WAZUH 4.14.7  /  WINDOWS + LINUX  /  EVIDENCE-LED DELIVERY</text><text x="95" y="394" fill="#bbb" font-size="21">Four Minds. Infinite Possibilities.</text></g></svg>''')

def para(c,text,x,y,width=WIDTH,size=10.2,color=BLACK,bold=False,leading=None):
    style=ParagraphStyle('p',fontName='Bold' if bold else 'Regular',fontSize=size,leading=leading or size*1.5,textColor=color,spaceAfter=0)
    p=Paragraph(text,style); _,height=p.wrap(width,1000);p.drawOn(c,x,y-height);return y-height

def text(c,t,x,y,size=10,font='Regular',color=BLACK):
    c.setFillColor(color);c.setFont(font,size);c.drawString(x,y,t)

def base(c,page,section):
    c.setFillColor(colors.white);c.rect(0,0,W,H,fill=1,stroke=0)
    c.setFillColor(BLACK);c.rect(0,H-48,W,48,fill=1,stroke=0)
    logo(c,29,H-38,29,True);text(c,'TETRION',66,H-30,12,'Bold',colors.white)
    c.setFont('Regular',7.2);c.setFillColor(colors.white);c.drawRightString(W-32,H-29,section.upper())
    c.setFillColor(GOLD);c.rect(0,H-52,149,4,fill=1,stroke=0)
    c.setStrokeColor(LINE);c.setLineWidth(.6)
    p=c.beginPath();p.moveTo(25,H-70);p.lineTo(25,66);p.lineTo(37,54);p.lineTo(W-37,54);p.lineTo(W-25,66);p.lineTo(W-25,H-70);c.drawPath(p)
    # Fine circuit geometry echoes the supplied layout without crowding content.
    for x,flip in [(17,1),(W-17,-1)]:
        c.setStrokeColor(GOLD);p=c.beginPath();p.moveTo(x,H-93);p.lineTo(x,H-166);p.lineTo(x+8*flip,H-174);p.lineTo(x+8*flip,H-222);c.drawPath(p)
        c.setFillColor(GOLD);c.circle(x+8*flip,H-222,2,fill=1,stroke=0)
    c.setFillColor(BLACK);c.rect(0,0,W,42,fill=1,stroke=0)
    c.setFillColor(GOLD);c.rect(W-149,42,149,3,fill=1,stroke=0)
    text(c,'TETRION  /  SECURITY MONITORING FOUNDATION',32,18,6.8,color=colors.white)
    c.setFont('Bold',9);c.setFillColor(colors.white);c.drawRightString(W-32,17,f'{page:02d}')
    c.bookmarkPage(f'p{page}')

def heading(c,kicker,title):
    text(c,kicker.upper(),LEFT,758,8.5,'Bold',GOLD)
    return para(c,title,LEFT,739,size=24,bold=True,leading=29)-18

def table(c,rows,widths,y,header=True,font=8.5):
    data=[]
    for i,row in enumerate(rows):
        st=ParagraphStyle('cell',fontName='Bold' if i==0 and header else 'Regular',fontSize=font,leading=font*1.45,textColor=colors.white if i==0 and header else BLACK)
        data.append([Paragraph(escape(str(v)),st) for v in row])
    t=Table(data,colWidths=widths,hAlign='LEFT')
    cmds=[('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),9),('RIGHTPADDING',(0,0),(-1,-1),9),('TOPPADDING',(0,0),(-1,-1),9),('BOTTOMPADDING',(0,0),(-1,-1),9),('LINEBELOW',(0,0),(-1,-1),.4,LINE)]
    if header:cmds.append(('BACKGROUND',(0,0),(-1,0),BLACK))
    for i in range(1 if header else 0,len(rows)):
        if i%2:cmds.append(('BACKGROUND',(0,i),(-1,i),LIGHT))
    t.setStyle(TableStyle(cmds));_,h=t.wrap(WIDTH,900);t.drawOn(c,LEFT,y-h);return y-h

def box(c,title,body,y):
    c.setFillColor(LIGHT);c.rect(LEFT,y-94,WIDTH,94,fill=1,stroke=0)
    c.setFillColor(GOLD);c.rect(LEFT,y-94,3,94,fill=1,stroke=0)
    para(c,title,LEFT+15,y-12,width=WIDTH-30,bold=True,size=10)
    para(c,body,LEFT+15,y-34,width=WIDTH-30,size=9.1)
    return y-110

CAPTIONS={
1:('Windows endpoint resources','VMware settings show 4 GB RAM, 4 vCPUs, a 60 GB disk and Custom (VMnet1) networking.'),
2:('Linux endpoint resources','VMware settings show 4 GB RAM, 2 vCPUs, a 500 GB disk and Custom (VMnet1) networking.'),
3:('Monitoring server resources','VMware settings show 16 GB RAM, 6 vCPUs, a 500 GB disk, NAT and Custom (VMnet1) adapters.'),
4:('Virtual network configuration','VMnet1 is Host-only on 192.168.38.0; DHCP is enabled. VMnet8 provides a separate NAT network.'),
5:('Windows address configuration','The Windows endpoint reports 192.168.38.133 with subnet mask 255.255.255.0 and no displayed default gateway.'),
6:('Linux endpoint address configuration','The Linux endpoint reports 192.168.38.131/24. The dynamic flag means static addressing is not demonstrated.'),
7:('Monitoring server interfaces','The server reports 192.168.38.132/24 on ens36 and NAT address 192.168.121.156/24 on ens33; both are marked dynamic.'),
8:('Server-to-endpoint reachability','The monitoring server receives three replies from each endpoint, with 0% packet loss in both short tests.'),
9:('Linux-to-peer reachability','The Linux endpoint receives three replies from the server and three from Windows, with 0% packet loss.'),
10:('Windows-to-peer reachability','Windows receives four replies from the Linux endpoint and four from the server, with 0% packet loss.'),
11:('Windows Sysmon installation','Sysmon v15.22 loads the SwiftOnSecurity configuration; the Sysmon64 service is Running. Dashboard ingestion is not shown.'),
12:('Apache package installation','APT output shows installation of Apache packages on the Linux endpoint; this capture is an installation stage.'),
13:('Apache service state','Apache is enabled and active (running). A ServerName warning is visible; the service remains running.'),
14:('Web-service functional check','A browser displays the Apache2 Ubuntu Default Page at the Linux endpoint address. Browser host identity is not independently shown.'),
15:('Pinned Wazuh source','The recorded git clone selects wazuh-docker tag v4.14.7. Detached HEAD is expected for a release tag.'),
16:('Certificate-generation preparation','The certificate-generation Compose command pulls the Wazuh certificate-tool image for the single-node deployment.'),
17:('Certificate-generation result','The tool reports certificates created for indexer, manager, Filebeat and dashboard, and moves them into the deployment directory.'),
18:('Running single-node stack','Docker Compose lists the dashboard, indexer and manager with 4.14.7 images and Up status. This is a point-in-time startup check.'),
19:('Dashboard sign-in page','The Wazuh sign-in page is accessible in a browser. This does not prove a password change or certificate trust configuration.'),
20:('Authenticated dashboard','The Wazuh overview loads after authentication and shows security-event summary widgets. These are not the five required controlled tests.'),
21:('Windows enrollment settings','The dashboard deployment wizard selects Windows and the manager address 192.168.38.132 for an agent installation.'),
22:('Windows agent service start','The agent install command names win-client. An initial NET HELPMSG 2185 response is followed by a successful WazuhSvc start.'),
23:('Windows agent active','The inventory lists win-client at 192.168.38.133, agent v4.14.7, with active status.'),
24:('Linux enrollment settings','The dashboard deployment wizard selects Linux and the same monitoring-server address.'),
25:('Linux agent service state','systemctl reports wazuh-agent enabled and active (running), with agent processes visible.'),
26:('Two active monitored endpoints','The inventory lists win-client and ubuntu-web as active, both on v4.14.7. The Linux endpoint is Ubuntu 22.04.'),
27:('Monitoring-server naming','The hostnamectl command sets the server hostname to siem-host. A separate post-change hostname query is not shown.'),
28:('Linux endpoint naming','The hostnamectl command sets the Linux endpoint hostname to ubuntu-web.'),
29:('Windows hostname context','whoami returns win-client\\roman, supporting the Windows computer-name context.'),
}

PAGES=[]
def content(kicker,title,blocks):PAGES.append({'kicker':kicker,'title':title,'blocks':blocks})

content('01 / Management overview','Executive summary',[
 ('p','Tetrion\'s security monitoring foundation brings a Windows workstation and an Ubuntu web server into one Wazuh monitoring platform. The supplied implementation record shows a running Wazuh 4.14.7 single-node stack, successful dashboard access and two active endpoint agents.'),
 ('p','Windows Sysmon is installed with a community configuration, and Apache serves its default page on the Linux endpoint. Short bidirectional connectivity checks succeed between all three systems. These results establish the initial platform and endpoint-enrollment baseline.'),
 ('table',[['Capability','Recorded result'],['Central monitoring','Three Wazuh containers Up; dashboard loads.'],['Endpoint coverage','win-client and ubuntu-web Active on 4.14.7.'],['Windows telemetry readiness','Sysmon64 Running; event ingestion still requires proof.'],['Web-service readiness','Apache Running; default page opens.'],['Operational acceptance','Controlled event validation, recovery and hardening evidence outstanding.']], [145,348]),
 ('box','Management decision','Proceed with completion and acceptance testing. Do not treat the platform as production accepted until telemetry delivery, recovery, credentials and isolation controls are verified.'),
 ('p','This is an evidence-based deployment report prepared for Tetrion. It is not a live audit of the original machines; the review is limited to the supplied screenshots and implementation notes.')])

content('02 / Report navigation','Contents & document control',[
 ('toc',None),
 ('table',[['Field','Value'],['Document ID','TET-SOC-001'],['Version / issue date','1.0 / 15 October 2026'],['Prepared for / prepared by','Tetrion / Roman Rzayev'],['Subject','Security Monitoring Foundation - Deployment Report'],['Status','Implementation recorded; acceptance actions open'],['Handling','Internal technical record; repository copy contains selected implementation evidence.']], [145,348]),
 ('p','Source roles: Week1_SOC_Lab (1).docx defines the acceptance baseline; faridexiyetimbrat.docx supplies implementation notes and 29 screenshots. ED-Lab04-Executive-Report.pdf is a visual layout reference only. Its company identity, findings, targets and assessment claims are not carried into this report.')])

content('03 / Scope & interpretation','Scope and assessment basis',[
 ('p','The scope is a three-system VMware environment: one Ubuntu monitoring server, one Ubuntu web endpoint and one Windows endpoint. The implementation uses a host-only network for internal communication and a second NAT interface on the monitoring server.'),
 ('table',[['Included','Outside the demonstrated scope'],['VM resources, addressing and ICMP reachability','Comprehensive routing, firewall and time-synchronization audit'],['Wazuh stack startup and dashboard access','Continuous uptime, load testing and production high availability'],['Agent enrollment and point-in-time Active state','End-to-end validation of all required security events'],['Sysmon and Apache installation evidence','Incident response automation and attack detection effectiveness']], [246,247]),
 ('p','Evidence labels are intentionally precise. Recorded means a capture directly supports the stated observation. Partial means the capture supports only part of a requirement. Open means the supplied material does not establish completion. These labels are not results of new tests against the original systems.'),
 ('box','Implementation variance','The endpoint resource allocations differ from the supplied baseline, and the Linux network captures show dynamically assigned addresses. These differences are documented rather than normalized into an assumed compliant configuration.'),
 ('p','The report date is the document issue date, not an assertion about the date of every source capture. No passwords, private keys, certificates or invented operational measurements are included.')])

content('04 / System design','Architecture & asset inventory',[
 ('diagram',None),
 ('table',[['Asset / IP','Recorded resources','Role'],['siem-host\n192.168.38.132','16 GB / 6 vCPU / 500 GB','Wazuh server; NAT also present'],['ubuntu-web\n192.168.38.131','4 GB / 2 vCPU / 500 GB','Ubuntu 22.04; Apache; agent'],['win-client\n192.168.38.133','4 GB / 4 vCPU / 60 GB','Windows 10 Enterprise Evaluation; agent; Sysmon']], [154,157,182]),
 ('p','The screenshots associate the server with ens36 on 192.168.38.132/24 and ens33 on 192.168.121.156/24. The latter is the recorded NAT-side address and may change. VMnet1 DHCP is enabled; Linux interfaces carry the dynamic flag. Static assignment or reservation is therefore not established.'),
 ('p','Recorded RAM allocation totals 24 GB, compared with the 22 GB baseline. Ubuntu has 4 GB instead of 2 GB; Windows has 4 vCPUs instead of 2 and a 60 GB disk instead of 80 GB. Both Linux virtual disks show 500 GB. The images do not establish physical disk consumption or available host capacity.')])

content('05 / Platform implementation','Deployment & telemetry design',[
 ('p','The implementation clones the official wazuh-docker repository at v4.14.7, generates deployment certificates, and starts the single-node stack using Docker Compose. The visible services are wazuh.manager, wazuh.indexer and wazuh.dashboard; all three use 4.14.7 images and show Up status in the container listing.'),
 ('p','Filebeat runs as part of the manager image in this deployment. A typical event path is: endpoint source -> Wazuh agent -> manager decoding and rule evaluation -> Filebeat alert forwarding -> indexer storage -> dashboard search. This is the expected design; the supplied captures do not trace one controlled event through every stage.'),
 ('table',[['Component','Operational responsibility'],['Agent','Collect configured endpoint logs and forward them to the manager.'],['Manager','Decode events, evaluate rules and produce alerts.'],['Filebeat / indexer','Forward alert records and index them for search.'],['Dashboard','Authenticate analysts and present indexed monitoring information.']], [145,348]),
 ('p','Windows enrollment first shows a service-start error and then a successful WazuhSvc start. A later inventory verifies win-client Active. Linux systemctl output verifies wazuh-agent Running; the final inventory verifies ubuntu-web Active. Both agent versions match the 4.14.7 manager line.'),
 ('box','Visibility boundary','Sysmon64 Running proves installation, not ingestion. A Wazuh event containing the Microsoft-Windows-Sysmon/Operational channel, endpoint name and Event ID is still needed to demonstrate the Windows telemetry pipeline.')])

content('06 / Operational assurance','Validation & acceptance priorities',[
 ('table',[['Control','What the evidence establishes','Next verification'],['Connectivity','All six directed peer checks receive replies.','Record current clocks, routes and final adapter state.'],['Web service','Apache active; default page displayed.','Record the browser host and a dated HTTP response.'],['Agent coverage','Two Active endpoints on v4.14.7.','Recheck after stack restart and server reboot.'],['Security events','Dashboard overview only; no controlled-event records.','Generate and capture the five event cases below.'],['Credential control','Login is shown; password rotation is not.','Use the Docker deployment password-change procedure.']], [106,193,194]),
 ('p','Required event cases are a failed SSH login, a sudo command, Linux local-user creation, a Windows process launch observed through Sysmon, and a failed Windows logon. Each needs the agent name, timestamp, rule description, rule level and screenshot. No rule IDs or levels have been invented in this report.'),
 ('box','Priority before acceptance','Confirm persistent addressing and endpoint isolation; rotate default credentials; demonstrate five event cases and Sysmon ingestion; complete restart/reboot persistence checks; record memory and snapshots.'),
 ('p','A short ping test proves sampled IP reachability. An Up container status proves a process was running at capture time. Neither alone establishes end-to-end security monitoring, sustained service health or recoverability.')])

content('07 / Operational handover','Startup, shutdown & recovery',[
 ('p','The following is the operating procedure for the recorded architecture. It is derived from the visible deployment path and normal Compose behavior; it has not been executed against the original VMs during this document review.'),
 ('steps',[
 'Start siem-host first. Confirm the internal interface is on 192.168.38.132/24 and that vm.max_map_count meets the Wazuh indexer prerequisite (at least 262144).',
 'In the existing single-node deployment directory (recorded as /root/wazuh-docker/single-node), run docker compose up -d, then docker compose ps and inspect service logs if startup fails. Keep deployment credentials local.',
 'Open the configured dashboard URL over HTTPS from the operator workstation. Verify authentication and index availability. Assess the deployment certificate warning using its actual issuer and subject; do not disable TLS verification as a routine workaround.',
 'Start ubuntu-web and win-client. Verify Apache, Wazuh agent services and Sysmon64. Confirm both agents become Active and generate one authorized test event that appears in the dashboard.',
 'For shutdown, stop endpoint workloads and shut down the endpoints first. On siem-host use docker compose stop before shutting down the VM. Do not use docker compose down -v or delete persistent volumes.',
 'For recovery acceptance, record an agent inventory and a uniquely identifiable test alert, restart the stack, then reboot siem-host. Confirm the same agents and pre-existing alert remain searchable after each operation.'
 ]),
 ('p','Record docker stats --no-stream at idle, the exact image versions, snapshot names and Windows evaluation expiry. Stop/start, reboot persistence and memory measurements remain unverified until their outputs are retained.')])

content('08 / Evidence-led handover','Evidence register & next actions',[
 ('p','The following annex retains all 29 embedded screenshots in source order, with one observation per figure. Every screenshot sits in a consistent 493 x 205 pt frame, is fitted proportionally without cropping, and retains its original embedded pixel data. Smaller captures cannot recover detail absent from the original.'),
 ('table',[['Evidence range','Coverage'],['E01-E07','VMware resources, host-only network and interface addresses'],['E08-E10','Peer reachability in all three directions'],['E11-E14','Sysmon installation and Apache service'],['E15-E20','Wazuh release, certificates, containers and dashboard'],['E21-E26','Windows and Linux enrollment and Active inventory'],['E27-E29','System naming commands and Windows identity context']], [115,378]),
 ('p','For review at source resolution, use evidence/screenshots/ in the accompanying repository. evidence/manifest.json records dimensions and SHA-256 digests. The editable document is a companion; the PDF is the fixed-layout presentation master.'),
 ('box','Close-out deliverables','Complete the acceptance matrix in docs/acceptance.md using new screenshots and outputs from the actual VMs. The retrospective journal distinguishes observations from unrecorded troubleshooting; missing events and measurements must be supplied by execution, not reconstruction.'),
 ('p','Official technical references: documentation.wazuh.com/current/deployment-options/docker/wazuh-container.html; docs.docker.com/engine/install/ubuntu/; learn.microsoft.com/sysinternals/downloads/sysmon; github.com/SwiftOnSecurity/sysmon-config. These are implementation references, not claims that all documented steps were performed.')])

GROUPS=[('Compute provisioning',[1,2]),('Server & virtual networking',[3,4]),('Endpoint addressing',[5,6]),('Server network & reachability',[7,8]),('Peer connectivity',[9,10]),('Endpoint service preparation',[11,12]),('Web-service readiness',[13,14]),('Wazuh release & certificates',[15,16]),('Certificate completion & runtime',[17,18]),('Dashboard access',[19,20]),('Windows agent enrollment',[21,22]),('Windows inventory & Linux enrollment',[23,24]),('Linux service & endpoint coverage',[25,26]),('Asset naming',[27,28]),('Windows identity context',[29])]

def diagram(c,x,y,width=WIDTH,height=186):
    c.saveState();c.translate(x,y);c.setFillColor(LIGHT);c.roundRect(0,0,width,height,7,fill=1,stroke=0)
    # Top node and two endpoints, with observed networking rather than unverified ports.
    c.setFillColor(BLACK);c.roundRect(width/2-98,height-67,196,48,4,fill=1,stroke=0)
    text(c,'siem-host  /  Wazuh 4.14.7',width/2-85,height-40,9,'Bold',colors.white)
    text(c,'192.168.38.132  +  NAT',width/2-85,height-55,8,color=colors.white)
    c.setStrokeColor(GOLD);c.setLineWidth(1.4);c.line(width/2,height-67,width/2,91);c.line(113,91,width-113,91);c.line(113,91,113,64);c.line(width-113,91,width-113,64)
    text(c,'VMnet1  /  Host-only  /  192.168.38.0/24',width/2-125,104,8,'Bold',MUTED)
    for cx,title,detail in [(113,'ubuntu-web  /  Apache','192.168.38.131'),(width-113,'win-client  /  Sysmon','192.168.38.133')]:
        c.setFillColor(colors.white);c.setStrokeColor(LINE);c.roundRect(cx-99,17,198,47,4,fill=1,stroke=1)
        text(c,title,cx-87,45,9,'Bold');text(c,detail,cx-87,30,8,color=MUTED)
    c.restoreState()

def build_pdf():
    c=canvas.Canvas(str(OUT/'Tetrion-Security-Monitoring-Report.pdf'),pagesize=(W,H),pageCompression=1)
    c.setTitle('Tetrion | Security Monitoring Foundation');c.setAuthor('Roman Rzayev | Tetrion');c.setSubject('Evidence-based deployment and operational handover')
    base(c,1,'Deployment & Operational Handover')
    text(c,'SECURITY OPERATIONS',LEFT,740,10,'Bold',GOLD)
    para(c,'Security Monitoring<br/>Foundation',LEFT,705,size=34,bold=True,leading=42)
    para(c,'Deployment & Operational Handover Report',LEFT,594,size=13,color=MUTED)
    c.setStrokeColor(GOLD);c.setLineWidth(1.1);c.line(LEFT,563,RIGHT,563)
    logo(c,207,358,180)
    text(c,'TETRION',213,337,25,'Bold')
    para(c,'Four Minds. Infinite Possibilities.',LEFT,305,WIDTH,size=11,color=MUTED)
    para(c,'Wazuh 4.14.7  /  Windows & Linux endpoint coverage',LEFT,246,size=10)
    text(c,'PREPARED FOR TETRION',LEFT,196,9,'Bold')
    text(c,'Prepared by Roman Rzayev',LEFT,174,10)
    text(c,DATE+'  |  TET-SOC-001  |  VERSION 1.0',LEFT,114,8.5,'Bold',GOLD)
    c.showPage()
    for n,page in enumerate(PAGES,2):
        base(c,n,page['kicker'].split(' / ')[1]);y=heading(c,page['kicker'],page['title'])
        for block in page['blocks']:
            kind=block[0]
            if kind=='p':y=para(c,escape(block[1]),LEFT,y)-15
            elif kind=='table':y=table(c,block[1],block[2],y)-20
            elif kind=='box':y=box(c,block[1],block[2],y)
            elif kind=='steps':
                for j,s in enumerate(block[1],1):
                    text(c,f'{j:02d}',LEFT,y-13,10,'Bold',GOLD)
                    y=para(c,escape(s),LEFT+31,y,width=WIDTH-31,size=9.3)-14
            elif kind=='diagram':diagram(c,LEFT,y-186);y-=204
            elif kind=='toc':
                rows=[['Section','Page']]+[[p['title'],str(i)] for i,p in enumerate(PAGES,2) if p['kicker']!='02 / Report navigation']+[['Evidence annex',str(2+len(PAGES))]]
                y=table(c,rows,[440,53],y,font=8)-19
        if y<65:raise RuntimeError(f'Page {n} overflows: {y}')
        c.showPage()
    page_no=len(PAGES)+2
    for group,nums in GROUPS:
        base(c,page_no,'Implementation evidence');heading(c,'Evidence annex',group)
        for slot,num in enumerate(nums):
            top=686-slot*301;title,caption=CAPTIONS[num]
            text(c,f'E{num:02d}',LEFT,top,9,'Bold',GOLD);text(c,title,LEFT+36,top,10.5,'Bold')
            fy=top-220;c.setFillColor(LIGHT);c.setStrokeColor(LINE);c.rect(LEFT,fy,WIDTH,205,fill=1,stroke=1)
            path=SHOTS/f'image{num}.png';im=Image.open(path);iw,ih=im.size
            scale=min((WIDTH-12)/iw,193/ih);dw,dh=iw*scale,ih*scale
            c.drawImage(str(path),LEFT+(WIDTH-dw)/2,fy+(205-dh)/2,width=dw,height=dh,mask='auto')
            end=para(c,escape(f'Figure E{num:02d}. {caption}'),LEFT,fy-10,size=8.8,color=MUTED,leading=12)
            text(c,f'Source: image{num}.png  |  {iw} x {ih} px  |  Original pixels retained',LEFT,end-15,7,color=MUTED)
        c.showPage();page_no+=1
    c.save()

def doc_table(doc,rows):
    t=doc.add_table(rows=0,cols=len(rows[0]));t.style='Light Shading Accent 1'
    for row in rows:
        cells=t.add_row().cells
        for cell,value in zip(cells,row):cell.text=str(value)
    return t

def build_docx():
    d=Document();sec=d.sections[0];sec.page_height=Inches(11.693);sec.page_width=Inches(8.268)
    sec.top_margin=Inches(.8);sec.bottom_margin=Inches(.75);sec.left_margin=sec.right_margin=Inches(.72)
    normal=d.styles['Normal'];normal.font.name='Calibri';normal.font.size=Pt(10);normal.paragraph_format.space_after=Pt(9)
    for name in ['Title','Heading 1','Heading 2']:
        d.styles[name].font.name='Calibri';d.styles[name].font.color.rgb=RGBColor.from_string('141414')
    d.styles['Subtitle'].font.color.rgb=RGBColor.from_string('A47700')
    # Replace Word's default blue accent in the actual document theme.
    from lxml import etree
    for rel in d.part.rels.values():
        if rel.reltype.endswith('/theme'):
            part=rel.target_part;root=etree.fromstring(part.blob)
            for node in root.xpath('//*[local-name()="accent1"]/*'):
                node.set('val','D9A514')
            part._blob=etree.tostring(root,xml_declaration=True,encoding='UTF-8',standalone=True)
    header=sec.header.paragraphs[0]
    header.add_run().add_picture(str(ROOT/'assets/tetrion-mark.png'),width=Inches(.22)) if (ROOT/'assets/tetrion-mark.png').exists() else None
    header.add_run('  TETRION   |   SECURITY MONITORING FOUNDATION')
    foot=sec.footer.paragraphs[0];foot.text='TET-SOC-001  |  15 OCTOBER 2026                                           '
    fld=OxmlElement('w:fldSimple');fld.set(qn('w:instr'),'PAGE');foot._p.append(fld)
    # Render brand mark directly from the same vector drawing at 600 dpi.
    import fitz
    logo_pdf=OUT/'_brand.pdf';lc=canvas.Canvas(str(logo_pdf),pagesize=(180,180));logo(lc,0,0,180);lc.save()
    ld=fitz.open(logo_pdf);ld[0].get_pixmap(matrix=fitz.Matrix(5,5),alpha=True).save(str(ROOT/'assets/tetrion-mark.png'));ld.close();logo_pdf.unlink()
    d.add_paragraph('SECURITY OPERATIONS','Subtitle');d.add_heading('Security Monitoring\nFoundation',0)
    d.add_paragraph('Deployment & Operational Handover Report','Subtitle')
    d.add_picture(str(ROOT/'assets/tetrion-mark.png'),width=Inches(1.65))
    d.add_heading('TETRION',1);d.add_paragraph('Four Minds. Infinite Possibilities.')
    d.add_paragraph('Wazuh 4.14.7 / Windows & Linux endpoint coverage')
    d.add_paragraph('Prepared for Tetrion\nPrepared by Roman Rzayev\n15 October 2026\nTET-SOC-001 | Version 1.0');d.add_page_break()
    for page in PAGES:
        d.add_paragraph(page['kicker'].upper(),'Subtitle');d.add_heading(page['title'],1)
        for b in page['blocks']:
            if b[0]=='p':d.add_paragraph(b[1])
            elif b[0]=='table':doc_table(d,b[1])
            elif b[0]=='box':d.add_heading(b[1],2);d.add_paragraph(b[2])
            elif b[0]=='steps':
                for s in b[1]:d.add_paragraph(s,'List Number')
            elif b[0]=='toc':
                d.add_paragraph('Executive summary / Scope / Architecture / Deployment / Validation / Operations / Evidence register / Evidence annex')
                d.add_paragraph('Use the PDF for fixed pagination; Word pagination depends on the installed fonts.')
            elif b[0]=='diagram':d.add_picture(str(ROOT/'architecture/architecture.png'),width=Inches(6.7))
        d.add_page_break()
    for gi,(group,nums) in enumerate(GROUPS):
        d.add_paragraph('EVIDENCE ANNEX','Subtitle');d.add_heading(group,1)
        for num in nums:
            title,cap=CAPTIONS[num];d.add_heading(f'E{num:02d} | {title}',2)
            # Fixed cell size gives every image the same frame, with proportional fit.
            t=d.add_table(rows=1,cols=1);t.autofit=False;t.columns[0].width=Inches(6.7)
            row=t.rows[0];row.height=Inches(2.8)
            from docx.enum.table import WD_ROW_HEIGHT_RULE,WD_CELL_VERTICAL_ALIGNMENT
            row.height_rule=WD_ROW_HEIGHT_RULE.EXACTLY;cell=row.cells[0];cell.vertical_alignment=WD_CELL_VERTICAL_ALIGNMENT.CENTER
            p=cell.paragraphs[0];p.paragraph_format.space_after=Pt(0)
            from docx.enum.text import WD_ALIGN_PARAGRAPH
            p.alignment=WD_ALIGN_PARAGRAPH.CENTER
            im=Image.open(SHOTS/f'image{num}.png');iw,ih=im.size;factor=min(6.5/iw,2.6/ih)
            p.add_run().add_picture(str(SHOTS/f'image{num}.png'),width=Inches(iw*factor),height=Inches(ih*factor))
            d.add_paragraph(f'Figure E{num:02d}. {cap}',style='Caption')
        if gi<len(GROUPS)-1:d.add_page_break()
    d.core_properties.title='Tetrion | Security Monitoring Foundation';d.core_properties.author='Roman Rzayev';d.core_properties.subject='Deployment & Operational Handover'
    d.save(OUT/'Tetrion-Security-Monitoring-Report.docx')

def build_architecture():
    p=ROOT/'architecture/architecture.pdf';c=canvas.Canvas(str(p),pagesize=(WIDTH+40,226));diagram(c,20,20);c.save()
    import fitz
    d=fitz.open(p);d[0].get_pixmap(matrix=fitz.Matrix(4,4)).save(str(ROOT/'architecture/architecture.png'));d.close()
    svg=f'''<svg xmlns="http://www.w3.org/2000/svg" width="1100" height="510" viewBox="0 0 1100 510"><style>text{{font-family:Arial,sans-serif;fill:#141414}}.h{{font-weight:bold;font-size:23px}}.s{{font-size:20px}}</style><rect width="1100" height="510" rx="16" fill="#F5F3ED"/><text x="40" y="45" class="h">TETRION / SECURITY MONITORING FOUNDATION</text><rect x="330" y="78" width="440" height="110" rx="9" fill="#141414"/><text x="355" y="120" style="fill:white" class="h">siem-host / Wazuh 4.14.7</text><text x="355" y="156" style="fill:white" class="s">192.168.38.132 + NAT interface</text><path d="M550 188V310M240 310H860M240 310V370M860 310V370" stroke="#D9A514" stroke-width="4" fill="none"/><text x="268" y="265" class="s">VMnet1 / Host-only / 192.168.38.0/24</text><rect x="40" y="370" width="400" height="105" rx="8" fill="white"/><rect x="660" y="370" width="400" height="105" rx="8" fill="white"/><text x="65" y="410" class="h">ubuntu-web / Apache</text><text x="65" y="445" class="s">192.168.38.131 / Wazuh agent</text><text x="685" y="410" class="h">win-client / Sysmon</text><text x="685" y="445" class="s">192.168.38.133 / Wazuh agent</text></svg>'''
    (ROOT/'architecture/architecture.svg').write_text(svg)

if __name__=='__main__':
    OUT.mkdir(exist_ok=True);write_svg();build_architecture();build_pdf();build_docx()
    lines=['# Evidence register','', 'Original PNG files extracted losslessly from the supplied implementation DOCX. Captions state what each image establishes; omissions are tracked in the acceptance matrix.','', '| Figure | Evidence | Observation |','| :--- | :--- | :--- |']
    for num,(title,cap) in CAPTIONS.items():lines.append(f'| E{num:02d} | [{title}](screenshots/image{num}.png) | {cap} |')
    lines.extend(['','The source dimensions and SHA-256 hashes are in [manifest.json](manifest.json). The PDF uses equal-size image frames with proportional fit; originals remain available here for source-resolution inspection.',''])
    (ROOT/'evidence/README.md').write_text('\n'.join(lines))
    print('Built PDF, editable DOCX, architecture and brand assets.')
