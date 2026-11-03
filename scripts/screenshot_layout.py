"""Present key evidence inline; keep originals intact and supporting views folded."""
from html import escape, unescape
from pathlib import Path
import re
import struct

NTP_PRIMARY = {
    '004-chrony-upstream-tracking.png',
    '006-chrony-server-subnet-acl.png',
    '009-chrony-client-selected-source.png',
    '011-windows-ntp-source-status.png',
}
DAY2_PRIMARY = {
    '015-labshop-decoder-logtest.png',
    '016-labshop-rule-definitions.png',
    '018-test1-single-failure-dashboard.png',
    '020-test2-brute-force-dashboard.png',
    '022-test3-monitor-logtest-fallback.png',
    '024-test4-split-source-dashboard.png',
    '029-linux-realtime-fim-config.png',
    '032-linux-fim-realtime-detail.png',
    '037-windows-fim-registry-config.png',
    '043-windows-fim-delete-dashboard.png',
    '045-registry-modification-dashboard.png',
    '057-ubuntu-sca-after-remediation.png',
    '061-windows-sca-after-remediation.png',
    '065-ubuntu-vulnerability-inventory.png',
    '070-suricata-af-packet-config.png',
    '071-suricata-home-net-config.png',
    '073-suricata-admin-signature.png',
    '078-suricata-fast-log-alert.png',
    '079-suricata-agent-eve-localfile.png',
    '082-suricata-wazuh-http-fields.png',
    '083-suricata-wazuh-rule-86601.png',
}


def prioritize(text, primary):
    """Split image-only evidence groups, retaining each original caption once."""
    pattern = r'<details>\s*<summary><strong>(.*?)</strong></summary>\s*(.*?)\s*</details>'

    def split_group(match):
        title, body = match.groups()
        if '<img ' not in body:
            return match.group(0)
        chunks = re.split(r'(?=^\*\*(?:NTP|W2)-\d+\.\*\*)', body, flags=re.M)
        visible, supporting = [], []
        for chunk in chunks:
            if not chunk.strip():
                continue
            src = re.search(r'<img\b[^>]*src="([^"]+)"', chunk)
            target = visible if src and Path(src[1]).name in primary else supporting
            target.append(chunk.strip())
        if not visible:
            return match.group(0)
        result = '\n\n'.join(visible)
        if supporting:
            result += '\n\n<details>\n<summary><strong>Supporting screenshots · ' + title + '</strong></summary>\n\n'
            result += '\n\n'.join(supporting) + '\n\n</details>'
        return result

    return re.sub(pattern, split_group, text, flags=re.S)


def screenshot(src, alt, page_dir):
    """Use a common frame width, keeping small captures at their native size."""
    path = Path(page_dir) / src
    data = path.read_bytes()
    if data[:8] != b'\x89PNG\r\n\x1a\n':
        raise ValueError(f'Expected an original PNG screenshot: {src}')
    native_width = struct.unpack('>I', data[16:20])[0]
    width = min(native_width, 860)
    url = escape(src, quote=True)
    return (
        '<table width="900"><tr><td width="900" align="center">'
        f'<a href="{url}"><img src="{url}" width="{width}" alt="{escape(alt, quote=True)}"></a>'
        '</td></tr></table>'
    )


def frame_screenshots(text, page_dir):
    """Frame PNG screenshots, leaving SVG banners and diagrams unchanged."""
    def html_image(match):
        tag = match.group(0)
        src = re.search(r'\bsrc="([^"]+)"', tag)
        if not src or not src[1].lower().endswith('.png'):
            return tag
        alt = re.search(r'\balt="([^"]*)"', tag)
        return screenshot(src[1], unescape(alt[1]) if alt else '', page_dir)

    text = re.sub(r'<img\b[^>]*>', html_image, text)

    def markdown_image(match):
        alt, src = match.groups()
        if not src.lower().endswith('.png'):
            return match.group(0)
        return screenshot(src, alt, page_dir)

    return re.sub(r'!\[([^\]]*)\]\(([^)]+)\)', markdown_image, text)
