#!/usr/bin/env python3
"""Generate cover (wp-page-01.html) and closing (wp-page-99.html) pages."""

import os, base64, tempfile

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(SCRIPT_DIR)   # deckgen/
DASHBOARD = os.environ.get('WP_DASHBOARD', os.path.join(tempfile.gettempdir(), 'wp_pages'))
BRAND = os.path.join(REPO_ROOT, 'brand_assets')

# Cover text — set via env vars by the orchestrator
COVER_TITLE = os.environ.get('WP_COVER_TITLE', 'Whitepaper')
COVER_SUBTITLE = os.environ.get('WP_COVER_SUBTITLE', '')

def b64(path):
    with open(path, 'rb') as f:
        d = base64.b64encode(f.read()).decode()
    ext = os.path.splitext(path)[1].lstrip('.')
    mime = {'png':'image/png','svg':'image/svg+xml'}.get(ext,'image/png')
    return f'data:{mime};base64,{d}'

THIN      = b64(f'{BRAND}/thinfinity_logo.png')
THIN_W    = b64(f'{BRAND}/thinfinity_logo_white_real.png')
CYBELE    = b64(f'{BRAND}/cybele_logo.png')
CYBELE_W  = b64(f'{BRAND}/cybele_logo_white.png')

COVER = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
<script src="https://mcp.figma.com/mcp/html-to-design/capture.js" async></script>
<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{
    width: 795px; height: 1125px;
    font-family: 'Inter', sans-serif;
    overflow: hidden; position: relative;
}}
.navy {{
    position: absolute; top: 0; left: 0; right: 0; height: 86%;
    background: linear-gradient(160deg, #0A1628 0%, #112244 40%, #0B1A3B 100%);
    padding: 90px 60px;
}}
.badge {{
    display: inline-block;
    background: #558BEE;
    color: white; border-radius: 24px;
    padding: 11px 30px; font-size: 16px;
    font-weight: 500; margin-bottom: 90px;
}}
.title {{
    font-weight: 700; font-size: 40px;
    color: white; line-height: 1.15;
}}
.subtitle {{
    font-size: 17px; color: rgba(255,255,255,0.5);
    margin-top: 18px; font-weight: 400;
}}
.white {{
    position: absolute; bottom: 0; left: 0; right: 0; height: 14%;
    background: white;
    display: flex; align-items: center;
    padding: 0 60px; gap: 14px;
}}
.white img {{ height: 36px; }}
.white .by {{ color: #888; font-size: 14px; }}
</style>
</head>
<body>
<div class="navy">
    <div class="badge">Whitepaper</div>
    <h1 class="title">{COVER_TITLE}</h1>
    <p class="subtitle">{COVER_SUBTITLE}</p>
</div>
<div class="white">
    <img src="{THIN}" alt="Thinfinity">
    <span class="by">by</span>
    <img src="{CYBELE}" alt="Cybele Software">
</div>
</body>
</html>"""

CLOSING = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<script src="https://mcp.figma.com/mcp/html-to-design/capture.js" async></script>
<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{
    width: 795px; height: 1125px;
    font-family: 'Inter', sans-serif;
    overflow: hidden; position: relative;
    padding: 50px 60px 0 60px;
    color: #373737;
}}
h2 {{
    font-weight: 600; font-size: 18px;
    color: #373737; margin-bottom: 20px;
}}
.contact-row {{
    display: flex; gap: 24px; margin-top: 16px;
    align-items: flex-start;
}}
.contact-left {{ flex: 1; }}
.ci {{
    display: flex; gap: 10px;
    align-items: center;
    margin-bottom: 10px;
    color: #0A74D6; font-size: 12px; line-height: 1.5;
}}
.ci svg {{
    width: 16px; height: 16px; flex-shrink: 0;
}}
.cta {{
    flex: 0 0 345px;
    background: linear-gradient(135deg, #1E88E5 0%, #42A5F5 40%, #2196F3 100%);
    color: white; border-radius: 9px;
    padding: 15px;
    display: flex; flex-direction: column;
    align-items: flex-start; justify-content: space-between;
    min-height: 103px;
    overflow: hidden; position: relative;
}}
.cta-top {{
    display: flex; align-items: center; gap: 14px;
    width: 100%;
}}
.cta-top img {{ height: 18px; }}
.cta-top p {{
    color: white; font-size: 11px; font-weight: 500;
    margin: 0; line-height: 1.4; text-align: left;
}}
.cta-btns {{
    display: flex; gap: 6px; margin-top: 12px;
}}
.cta-btn {{
    display: inline-block; padding: 6px 14px;
    border-radius: 57px; font-size: 10.5px; font-weight: 500;
    color: white; text-decoration: none;
    background: rgba(255,255,255,0.2);
}}
.cta-btn:first-child {{
    background: rgba(3,7,53,0.15);
}}
.footer {{
    position: absolute; bottom: 0; left: 0; right: 0;
    background: #0B1A3B;
    color: rgba(255,255,255,0.6);
    padding: 14px 60px;
    font-size: 8px; line-height: 1.5;
    display: flex; align-items: center;
    justify-content: space-between;
}}
.footer img {{ height: 22px; }}
</style>
</head>
<body>
<h2>Contact</h2>
<div class="contact-row">
    <div class="contact-left">
        <div class="ci">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" fill="none" stroke="#0A74D6" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round"><path d="M8 1.5C5.5 1.5 3.5 3.5 3.5 6c0 3.5 4.5 8.5 4.5 8.5s4.5-5 4.5-8.5c0-2.5-2-4.5-4.5-4.5z"/><circle cx="8" cy="6" r="1.5"/></svg>
            <span>Tech Center, 14183 Minuteman Drive Office 200,<br>#2000, Draper, UT 84020, United States</span>
        </div>
        <div class="ci">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" fill="none" stroke="#0A74D6" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round"><path d="M14.5 11.2v2a1.3 1.3 0 01-1.4 1.3A13 13 0 011.5 2.9 1.3 1.3 0 012.8 1.5h2a1.3 1.3 0 011.3 1c.2.8.4 1.6.8 2.3a1.3 1.3 0 01-.3 1.4l-.8.9a10.4 10.4 0 004.8 4.8l.9-.9a1.3 1.3 0 011.4-.3c.7.3 1.5.6 2.3.8a1.3 1.3 0 011 1.3z"/></svg>
            <span>+1 (302) 892-9625</span>
        </div>
        <div class="ci">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" fill="none" stroke="#0A74D6" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round"><rect x="1.5" y="3" width="13" height="10" rx="1.5"/><path d="M1.5 4.5L8 9l6.5-4.5"/></svg>
            <span>sales@cybelesoft.com</span>
        </div>
    </div>
    <div class="cta">
        <div class="cta-top">
            <img src="{THIN_W}" alt="Thinfinity">
            <p>Contact us and get the latest version of Thinfinity Workspace today</p>
        </div>
        <div class="cta-btns">
            <span class="cta-btn">Get a quote</span>
            <span class="cta-btn">Free trial</span>
            <span class="cta-btn">Book a call</span>
        </div>
    </div>
</div>
<div class="footer">
    <span>&copy;2026 Cybele Software Inc. All rights reserved. Thinfinity&reg; is a registered trademark of Cybele Software Inc.<br>All other brands and logos are trademarks of their respective owners. Rev. 03/2026.</span>
    <img src="{CYBELE_W}" alt="Cybele Software">
</div>
</body>
</html>"""

def main():
    with open(os.path.join(DASHBOARD, 'wp-page-01.html'), 'w', encoding='utf-8') as f:
        f.write(COVER)
    print("  wp-page-01.html (cover)")

    with open(os.path.join(DASHBOARD, 'wp-page-99.html'), 'w', encoding='utf-8') as f:
        f.write(CLOSING)
    print("  wp-page-99.html (closing)")

if __name__ == '__main__':
    main()
