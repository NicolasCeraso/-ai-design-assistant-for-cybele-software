# REFERENCE IMPLEMENTATION: copied 2026-09-28 from deck task task-1790624980817, v3, the version Nick
# accepted after two revisions. It is the WHOLE deck builder for that source; the reusable part is the
# section "ARCHITECTURE ENGINE v2" (Scene, chevron, reference, diag_*). The rules it implements are in
# web-app/data/progress.md > PPTX Generation Pipeline > "Architecture diagrams in a deck".
# Kept here because jobs/ is not versioned.

# -*- coding: utf-8 -*-
"""
task-1790624980817 v2 (revision 1): the architecture diagrams are redrawn with
the thinfinity-architecture skill's own geometry (see ARCHITECTURE ENGINE v2),
so they match what the arch-diagram task produces. Run: py -3.13 build_script.py <out_dir>

Demo Call 2026 - v8  =  v7 + revision 2: the architecture icons now follow the
product, not the adjective.

  REVISION 2. 'Reverse Gateway' pills carried a 'proxy' icon and 'Secondary
  Broker' pills an 'internal-session-brokering' icon, so three names for two
  things read as four different boxes. A Thinfinity Reverse Gateway is a
  gateway and a Secondary Broker is a broker - the icon now says so:
  Reverse Gateway -> 'gateway' (same as the plain Gateway pill) and Secondary
  Broker -> 'broker' (same as Broker / Primary Broker). A third-party
  'Reverse Proxy (Nginx / ALB)' is a different component and keeps 'proxy'.

Carried over from v7, which is where revision 1 landed:

  1. THE REAL BRANDING ICONOGRAPHY.
     v6 drew a solid coloured square in every pill and no icon anywhere else.
     v7 uses the actual brandbook set (131 outline icons from `brand-icon-lib.js`,
     via `_cybele_icons.py`), applied as a system, not as decoration:

       a. INSIDE CONTAINERS ONLY - icons live inside pills and cards, never
          floating on the field (the brand rule the architecture language uses).
       b. THE ICON NAMES THE NODE - in an architecture pill the icon is what the
          box *is*: gateway, broker, firewall, vdi, entra-id, auth0, manufacture...
          resolved from the label by `icon_for()`, so a label and its icon can
          never drift apart.
       c. ONE ICON PER CARD, in the card's own top-left slot, above the title.
       d. COLOUR CARRIES THE CATEGORY - brand blue for Thinfinity components,
          graphite for human actors/endpoints, grey for peripheral infrastructure,
          light azure on navy.
       e. NO ICON WHERE A NUMBER IS THE OBJECT - the 5-facts figures (02), the
          5,000+ slide (03) and the metric ledgers stay bare.

  2. PRECISE ARCHITECTURE GRAPHICS.
     The pill engine was rebuilt around measured geometry instead of hand-typed
     coordinates. What changed, concretely:

       * Nodes are objects with real anchors, so every wire starts and ends on an
         edge midpoint. v6's diagonals that clipped through pills and its arrows
         that died in empty canvas are gone - no arrowhead lands on anything but
         a node.
       * Orthogonal routing only: horizontal -> vertical channel -> horizontal.
         One-to-many and many-to-one fan-outs share a single trunk (a spine in the
         gap between two columns with short stubs), which is how a network diagram
         actually reads.
       * Zones are FITTED to their contents with uniform padding and a reserved
         label band, and sibling zones share one top/bottom. v6 drew every zone at
         a fixed 392 px height whatever was in it, which is where the big empty
         dashed boxes came from, and let the gateway pill straddle a zone border.
       * Wire labels sit centred on the trunk, above the topmost run, on a canvas
         backing, so they never print on top of a wire or a dashed border.
       * The brokers now sit inside the internal-network zone rather than floating
         between two zones - which is also where they belong.
       * Columns, pill size (172x50), gaps and the scale-out ellipsis are on one
         grid across all 26 architecture slides.

Same 54 slides, same content, same language (English) as v6. Everything is real
PowerPoint text + shapes (no image-per-slide) -> fully editable; the icons are the
only raster, transparent PNGs of the brand vectors.

Usage:  py -3.13 build_demo_call_v8_icons.py [OUT_DIR]
"""
import os, sys, math, html
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR
from pptx.oxml.ns import qn

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
import _cybele_icons as bi

DECKGEN = os.environ.get('CYBELE_DECKGEN_DIR') or r"C:/Users/NickCeraso/cybele_deckgen"
OUT_DIR = sys.argv[1] if len(sys.argv) > 1 else SCRIPT_DIR
os.makedirs(OUT_DIR, exist_ok=True)
NAME = "Thinfinity_Demo_Call_2026_Branded"

# ---- 06/26 tokens --------------------------------------------------------
NAVY="#0A1A2F"; CANVAS="#EEF4FB"; BLUE="#0A74D6"; BLUE_LT="#5BAFFF"; MINT="#3DCCA1"
TEXT="#2E2E2E"; TEXT_SEC="#6B7280"; MUTED="#A8B0BC"; FOOT_LT="#9AA6B4"; FOOT_DK="#4A6A90"
CARD_DK="#122542"; WHITE="#FFFFFF"
# ---- architecture pill-system tokens (thinfinity-architecture skill) -----
A_THIN="#0A74D6"      # Thinfinity components (stroke + text + icon)
A_USER="#373737"      # human actors / endpoints
A_SEC="#BDBDBD"       # peripheral infra stroke; its text/icon = A_STXT
A_STXT="#6B7280"
A_CONN="#0AA9FF"      # connector azure
A_ZONE="#BDBDBD"      # zone dashed border
A_ZTXT="#515151"      # zone label text
# Environment zones - where things are hosted (skill 2.2b, Nick 2026-09-28):
# kind -> (dashed stroke, soft fill, label text, label icon)
ENV={'customer':('#3DCCA1','#F5FCFA','#373737','premises'),
     'cloud':   ('#8878ED','#F9F8FE','#373737','cloud-inf'),
     'cybele':  ('#0A74D6','#EFF7FE','#0A74D6','cloud')}
ENV_NAME={'customer':'Customer infrastructure / on-premises',
          'cloud':'Cloud run by the customer','cybele':'Hosted by Cybele'}
# Every slide that carries a diagram gets the in-slide reference (skill 11):
# id(slide) -> [slide, set of environment kinds drawn on it]
ARCH={}
def _arch(s,env=None):
    e=ARCH.setdefault(id(s),[s,set()])
    if env: e[1].add(env)

PXE = 9525
def E(px): return Emu(int(round(px*PXE)))
def PT(px): return Pt(px*0.75)
def C(s): return html.unescape(s)
def rgb(h):
    h=h.lstrip('#'); return RGBColor(int(h[0:2],16),int(h[2:4],16),int(h[4:6],16))
def _font(r,size,bold=False,color=None,name='Inter',italic=False):
    r.font.size=PT(size); r.font.bold=bold; r.font.name=name; r.font.italic=italic
    if color: r.font.color.rgb=rgb(color)
def _anchor(tf,a='t'):
    b=tf._txBody.find(qn('a:bodyPr'))
    if b is not None: b.set('anchor',a)
def rect(slide,x,y,w,h,fill,radius=None,line=None,lw=1.0):
    shp=slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE if radius else MSO_SHAPE.RECTANGLE,E(x),E(y),E(w),E(h))
    if radius: shp.adjustments[0]=radius
    if fill is None: shp.fill.background()
    else:
        shp.fill.solid(); shp.fill.fore_color.rgb=rgb(fill)
    if line: shp.line.color.rgb=rgb(line); shp.line.width=Pt(lw)
    else: shp.line.fill.background()
    shp.shadow.inherit=False
    return shp
def tbox(slide,x,y,w,h,anchor='t'):
    tb=slide.shapes.add_textbox(E(x),E(y),E(w),E(h)); tf=tb.text_frame
    tf.word_wrap=True; tf.auto_size=None; _anchor(tf,anchor)
    tf.margin_left=0; tf.margin_right=0; tf.margin_top=0; tf.margin_bottom=0
    return tf
def para(tf,first=False):
    return tf.paragraphs[0] if first else tf.add_paragraph()
def run(p,text,size,bold=False,color=None,italic=False):
    r=p.add_run(); r.text=C(text); _font(r,size,bold,color,italic=italic); return r
def line_txt(tf,text,size,bold=False,color=None,first=False,after=0,align=PP_ALIGN.LEFT,italic=False,before=0):
    p=para(tf,first); p.alignment=align; p.space_after=Pt(after); p.space_before=Pt(before)
    run(p,text,size,bold,color,italic); return p
def bullet(tf,text,color,first=False,after=3,size=9.6,mk=MINT):
    p=para(tf,first); p.space_after=Pt(after); p.space_before=Pt(0)
    r=p.add_run(); r.text='▪  '; _font(r,size,True,mk)
    r2=p.add_run(); r2.text=C(text); _font(r2,size,False,color)
    return p
def logo(slide,name,x,y,h_px,white=False):
    from PIL import Image
    fn=f"{name}_white.png" if white else f"{name}.png"
    path=os.path.join(DECKGEN,"brand_assets",fn)
    im=Image.open(path); asp=im.size[0]/im.size[1]
    slide.shapes.add_picture(path,E(x),E(y),E(h_px*asp),E(h_px))

# ==========================================================================
# BRAND ICONOGRAPHY
# ==========================================================================
COLLECT=set()          # every (icon, colour) the deck needs; warms the cache once
COLLECT_MODE=False

def bicon(slide,name,x,y,box,color):
    """A brandbook icon, centred in a `box`-px square. Inside containers only."""
    COLLECT.add((name,color))
    if COLLECT_MODE: return None
    return bi.pic_px(slide,name,x,y,box,color)

# The icon names the node: resolved from the pill label, first match wins, so a
# label and its icon can never drift apart. Order is the rule (the narrower
# phrase has to come before the word it contains).
ICON_RULES=[
    ('virtualui','app-virtual-ui'),('thinvnc','thin-vnc'),
    # A Thinfinity Reverse Gateway IS a gateway - same product, same icon as the
    # plain 'Gateway' pill (rev. 2). Only a third-party reverse proxy keeps 'proxy'.
    ('reverse gateway','gateway'),('reverse proxy','proxy'),
    ('cloud gateway','web-cloud'),('gateway','gateway'),
    # A Secondary Broker is a broker: same icon as Broker / Primary Broker (rev. 2).
    ('secondary broker','broker'),('broker','broker'),
    ('firewall','firewall'),('load balanc','load-balancer'),
    ('entra','entra-id'),('azure ad','entra-id'),('azure','cloud-azure'),
    ('auth0','auth0'),('okta','identity-federation'),('saml','saml'),
    ('idp','identity-integration'),('sso','2FA'),('2fa','2FA'),
    ('oci','oracle'),('aws','aws'),('ec2','aws'),
    ('unique remote id','id'),('www','globe'),('remote access','remote-access'),
    ('scada','manufacture'),('plc','manufacture'),('pump','manufacture'),
    ('engineering','pc-star'),
    ('virtualization','app-virtualization'),
    ('daas','daas'),('virtual desktops','vdi'),('vdi','vdi'),
    ('app pool','app-group'),('pool','app-group'),
    ('iis','app-web'),('apache','app-web'),('wordpress','app-web'),('node.js','app-web'),
    ('webdav','app-web'),('wag','app-web'),
    ('windows app','win-app'),('windows','windows'),
    ('erp','web-app'),('web app','web-app'),
    ('terminal svc','server'),('terminal server','server'),('terminal','terminal'),
    ('app server','app-server'),('app. server','app-server'),('session server','server'),
    ('sql','database'),('database','database'),('file server','server'),
    ('routers','network'),('router','network'),('network','network'),
    ('workstation','pc'),('physical','premises'),('on-prem','premises'),
    ('premises','premises'),('local access','premises'),
    ('desktop','desktop'),('virtual machines','vm'),
    ('virtual apps','app-virtualization'),('virtual app','app-virtualization'),
    ('rdp','remote'),('rdc','remote'),('rfb','vnc'),('vnc','vnc'),
    ('ssh','ssh-connection'),('telnet','terminal'),
    ('pwa','html5'),('browser','html5'),('client','html5'),
    ('lic. mgr','key'),('license','key'),
    ('location','access-location'),('resource grp','secure-server'),
    ('authorized','secure-server'),('resources','secure-server'),
    ('testing','user-config'),('user group','user-group'),
    ('remote users','user-group'),('local users','user-group'),('end users','user-group'),
    ('customer','user-group'),('user','user'),
    ('server','server'),('app','app'),
]
def icon_for(label):
    t=C(label).replace('\n',' ').lower()
    for pat,name in ICON_RULES:
        if pat in t: return name
    return 'app'

SLIDE_W=13.333; SLIDE_H=7.5
TOTAL=54

def new_slide(prs,dark=False,cover=False,n=None):
    s=prs.slides.add_slide(prs.slide_layouts[6])
    rect(s,0,0,1280,720,NAVY if dark else CANVAS)
    if not cover and n is not None:
        f=FOOT_DK if dark else FOOT_LT
        tf=tbox(s,64,686,700,20); line_txt(tf,"Cybele Software · Thinfinity Workspace",8.5,False,f,first=True)
        tf2=tbox(s,1016,686,200,20); line_txt(tf2,f"{n:02d} / {TOTAL:02d}",8.5,False,f,first=True,align=PP_ALIGN.RIGHT)
    return s
def head(s,eyebrow,title,dark=False,sub=None):
    tf=tbox(s,64,48,1152,26); line_txt(tf,eyebrow.upper(),9,True,BLUE,first=True)
    tf2=tbox(s,64,70,1152,50); line_txt(tf2,title,22,True,WHITE if dark else NAVY,first=True)
    if sub:
        tf3=tbox(s,64,112,1152,26); line_txt(tf3,sub,12,False,(MUTED if dark else TEXT_SEC),first=True)
def divider(s,label,title,sub,icon):
    """Section divider. The subject's icon, in its own tile so it stays inside a
    container like every other icon in the deck."""
    rect(s,64,232,58,58,CARD_DK,radius=0.16)
    bicon(s,icon,64+15,232+15,28,BLUE_LT)
    tf=tbox(s,64,300,1152,60); line_txt(tf,label,10,True,BLUE_LT,first=True,after=6)
    line_txt(tf,title,44,True,WHITE)
    tf=tbox(s,64,392,1000,40); line_txt(tf,sub,14,False,MUTED,first=True)

# ---- generic content card -------------------------------------------------
ICON_CARD=26            # the card's icon slot
def card_block(s,x,y,w,h,c,dark=False):
    brand=c.get('brand')
    fill=BLUE if brand else (CARD_DK if dark else WHITE)
    rect(s,x,y,w,h,fill,radius=0.06)
    pad=16; icon=c.get('icon')
    ty=y+pad
    if icon:
        bicon(s,icon,x+pad,ty,ICON_CARD,WHITE if brand else (BLUE_LT if dark else BLUE))
        ty+=ICON_CARD+12
    tf=tbox(s,x+pad,ty,w-2*pad,h-(ty-y)-pad)
    title_col = WHITE if (dark or brand) else NAVY
    body_col  = (MUTED if dark else TEXT_SEC) if not brand else "#E6F0FB"
    first=True
    if c.get('num') is not None:
        line_txt(tf,c['num'],9,True,("#CFE3FA" if brand else BLUE),first=first,after=4); first=False
    if c.get('big') is not None:
        line_txt(tf,c['big'],28,True,BLUE,first=first,after=1); first=False
        if c.get('small'): line_txt(tf,c['small'],10,True,title_col,after=6)
    if c.get('title'):
        line_txt(tf,c['title'],11,True,title_col,first=first,after=6); first=False
    if c.get('body'):
        for ln in c['body'].split('\n'):
            line_txt(tf,ln,9.4,False,body_col,first=first,after=2); first=False
    for it in c.get('bullets',[]):
        bullet(tf,it,(MUTED if dark else TEXT),first=first,size=9.2); first=False
    if c.get('price'):
        line_txt(tf,c['price'],8.6,True,("#CFE3FA" if brand else BLUE),after=0)
def _est_card_h(c,cw):
    """Approximate the rendered height of a card's content, in canvas px."""
    inner=max(60.0,cw-32)
    def nlines(t,size):
        return max(1,math.ceil(len(C(t))*size*0.55/inner))
    h=32.0                                   # top + bottom padding
    if c.get('icon'): h+=ICON_CARD+12
    if c.get('num') is not None: h+=9*1.4+4
    if c.get('big') is not None:
        h+=28*1.4+1
        if c.get('small'): h+=10*1.4+6
    if c.get('title'): h+=nlines(c['title'],11)*11*1.4+6
    if c.get('body'):
        for ln in c['body'].splitlines(): h+=nlines(ln,9.4)*9.4*1.4+2
    for it in c.get('bullets',[]): h+=nlines('   '+it,9.2)*9.2*1.4+3
    if c.get('price'): h+=8.6*1.4+2
    return h

def grid(s,cards,cols,top=150,bottom=648,gap=16,dark=False,icons=None):
    """Card grid. Cards are sized to their content (capped by the available
    band) instead of always stretching to the footer. `icons` assigns one
    brandbook icon per card, in order."""
    if icons:
        for c,ic in zip(cards,icons):
            if ic: c.setdefault('icon',ic)
    n=len(cards); rows=math.ceil(n/cols); W=1152; left=64
    cw=(W-gap*(cols-1))/cols
    band=bottom-top
    ch_full=(band-gap*(rows-1))/rows
    need=max(_est_card_h(c,cw) for c in cards)+14
    ch=min(ch_full,max(need,120))
    y0=top+max(0.0,band-(rows*ch+gap*(rows-1)))*0.18
    for i,c in enumerate(cards):
        r=i//cols; col=i%cols
        card_block(s,left+col*(cw+gap),y0+r*(ch+gap),cw,ch,c,dark)
def tags(s,x,y,w,items,fill=WHITE,tcol=NAVY,size=9):
    cx=x; cy=y; gap=8; rowh=26
    for it in items:
        tw=len(C(it))*6.2+22
        if cx+tw>x+w: cx=x; cy+=rowh
        rect(s,cx,cy,tw,20,fill,radius=0.4)
        tf=tbox(s,cx,cy,tw,20,anchor='ctr'); line_txt(tf,it,size,True,tcol,first=True,align=PP_ALIGN.CENTER)
        cx+=tw+gap
    return cy+rowh
def pill_ui(s,x,y,text):
    tw=len(C(text))*7.5+40; rect(s,x,y,tw,40,CARD_DK,radius=0.3)
    tf=tbox(s,x,y,tw,40,anchor='ctr'); line_txt(tf,text,11,True,WHITE,first=True,align=PP_ALIGN.CENTER)
    return x+tw+14
def dark_card(s,x,y,w,h,title,body,icon=None):
    rect(s,x,y,w,h,CARD_DK,radius=0.08)
    tx=x+20
    if icon:
        bicon(s,icon,x+20,y+(h-26)/2,26,BLUE_LT); tx=x+58
    tf=tbox(s,tx,y+14,w-(tx-x)-20,h-28,anchor='ctr')
    line_txt(tf,title,11.5,True,WHITE,first=True,after=5); line_txt(tf,body,9.7,False,MUTED)

# ==========================================================================
# ARCHITECTURE ENGINE v2 -- the thinfinity-architecture skill, 1:1
# --------------------------------------------------------------------------
# Revision 1 asked for diagrams that look like the ones the "arch diagrams"
# task draws. So every diagram is laid out in the skill's own units (pill
# 160x43, zone label band 48, side pad 20, gap 43, stride 54) as a scene, then
# scaled once to fit its box and drawn in the skill's z-order: zones ->
# connectors -> pills. Same vocabulary as SKILL.md and examples/test_08:
#   * white pills, 1.5 px stroke, Inter 12 regular, icon 23 at (10,10)
#   * zones labelled with an icon + Inter Medium 13 in title case
#   * arrows point TOWARD the Gateway (reverse-connection model, skill 3.2):
#     users -> Gateway, Broker -> Gateway, resources -> Broker (one bus)
#   * TLS / "No Inbound Port" wire pills sitting on the line (skill 5.1)
#   * the whole diagram on a white card with its reference inside (skill 5/11)
# ==========================================================================
PW=160; PH=43          # the one pill size (skill 1)
SV=54                  # vertical stride between stacked pills
ZT=48; ZL=20; ZB=24    # zone: label band on top, side pad, bottom pad
GAP=43                 # gap between containers (skill 5)
VS=70                  # stride of a vertical arrow chain (27 px of wire)
A_LAB="#373737"        # zone label text + zone icon
A_PAR="#515151"
CARD=(64,140,1216,672) # the white diagram card on every diagram slide
REF_Y=644              # reference line, inside the card

_FONTS={}
def _font_file(name):
    for d in (os.path.join(os.environ.get('LOCALAPPDATA',''),'Microsoft','Windows','Fonts'),r'C:/Windows/Fonts'):
        p=os.path.join(d,name)
        if os.path.exists(p): return p
    return None
def text_w(text,px,medium=False):
    """Rendered width in px of one line of Inter (for the fit checks)."""
    from PIL import ImageFont
    k=(medium,px)
    if k not in _FONTS:
        f=_font_file('Inter-Medium.ttf' if medium else 'Inter-Regular.ttf')
        _FONTS[k]=ImageFont.truetype(f,int(round(px*4))) if f else None
    f=_FONTS[k]
    if f is None: return len(text)*px*0.56
    return f.getlength(text)/4.0
FIT_WARN=[]

def _arch(s,env=None,auth=False,ref_y=REF_Y):
    e=ARCH.setdefault(id(s),{'slide':s,'envs':set(),'auth':False,'ref_y':ref_y})
    if env: e['envs'].add(env)
    if auth: e['auth']=True
    e['ref_y']=ref_y

def _ln(shape):
    return shape.line._get_or_add_ln()

def stext(s,x,y,w,h,lines,px,color,medium=False,lsp=None,align=PP_ALIGN.LEFT,anchor='ctr'):
    tf=tbox(s,x,y,w,h,anchor=anchor); tf.word_wrap=False
    for i,l in enumerate(lines):
        p=para(tf,first=(i==0)); p.alignment=align
        p.space_after=Pt(0); p.space_before=Pt(0)
        if lsp: p.line_spacing=Pt(lsp*0.75)
        r=p.add_run(); r.text=C(l)
        _font(r,px,False,color,name=('Inter Medium' if medium else 'Inter'))
    return tf

def card(s,y0=CARD[1],y1=CARD[3]):
    rect(s,CARD[0],y0,CARD[2]-CARD[0],y1-y0,WHITE,radius=14.0/(y1-y0))

class P(object):
    """A pill (or a zone) in scene units, with its anchors."""
    def __init__(self,x,y,w,h,label='',cat='sec',icon=None,env=None,zicon=None):
        self.x=x; self.y=y; self.w=w; self.h=h; self.label=label; self.cat=cat
        self.icon=icon; self.env=env; self.zicon=zicon
    l=property(lambda s: s.x); r=property(lambda s: s.x+s.w)
    t=property(lambda s: s.y); b=property(lambda s: s.y+s.h)
    cx=property(lambda s: s.x+s.w/2.0); cy=property(lambda s: s.y+s.h/2.0)

class Scene(object):
    def __init__(self):
        self.zones=[]; self.paths=[]; self.pills=[]; self.dots=[]; self.auth=False
    # -- atoms -------------------------------------------------------------
    def pill(self,x,y,label,cat='sec',icon=None):
        p=P(x,y,PW,PH,label,cat,icon); self.pills.append(p); return p
    def wire(self,x,cy,label,icon='vpn-tunnels'):
        """A wire pill: sits on its connector and names what travels on it."""
        return self.pill(x,cy-PH/2.0,label,'sec',icon)
    def zone(self,x,y,w,h,label,icon,env=None):
        z=P(x,y,w,h,label,'zone',env=env,zicon=icon); self.zones.append(z); return z
    def fit(self,nodes,label,icon,env=None,x0=None,x1=None,y0=None,y1=None,pad=ZL,top=ZT,bot=ZB):
        lx=min(n.l for n in nodes)-pad if x0 is None else x0
        rx=max(n.r for n in nodes)+pad if x1 is None else x1
        ty=min(n.t for n in nodes)-top if y0 is None else y0
        by=max(n.b for n in nodes)+bot if y1 is None else y1
        return self.zone(lx,ty,rx-lx,by-ty,label,icon,env)
    def path(self,pts,arrow=True,dashed=False):
        if dashed: self.auth=True
        self.paths.append((pts,arrow,dashed))
    def ell(self,cx,y):
        self.dots.append((cx,y)); return 26
    # -- composite wiring --------------------------------------------------
    def bus(self,src_pts,bus_x,dst_pts,arrow=True):
        """Convergence/bifurcation (skill 3.4): stubs from every source to one
        vertical spine, and from the spine into every destination edge."""
        ys=[p[1] for p in src_pts]+[p[1] for p in dst_pts]
        for p in src_pts:
            if abs(p[0]-bus_x)>0.5: self.path([p,(bus_x,p[1])],arrow=False)
        if max(ys)-min(ys)>0.5: self.path([(bus_x,min(ys)),(bus_x,max(ys))],arrow=False)
        for p in dst_pts: self.path([(bus_x,p[1]),p],arrow=arrow)
    def up(self,lower,upper):
        """Vertical chain: lower pill's top -> upper pill's bottom."""
        self.path([(upper.cx,lower.t),(upper.cx,upper.b)])
    # -- render ------------------------------------------------------------
    def bbox(self):
        xs=[];ys=[]
        for n in self.zones+self.pills: xs+=[n.l,n.r]; ys+=[n.t,n.b]
        for pts,_,_ in self.paths:
            for x,y in pts: xs.append(x); ys.append(y)
        return min(xs),min(ys),max(xs),max(ys)
    def render(self,s,box,kmax=1.0,valign='ctr'):
        x0,y0,x1,y1=self.bbox(); bw=x1-x0; bh=y1-y0
        K=min(kmax,(box[2]-box[0])/bw,(box[3]-box[1])/bh)
        ox=box[0]+((box[2]-box[0])-bw*K)/2.0-x0*K
        oy=(box[1]+((box[3]-box[1])-bh*K)/2.0 if valign=='ctr' else box[1])-y0*K
        X=lambda v: ox+v*K; Y=lambda v: oy+v*K
        _arch(s)
        for z in sorted(self.zones,key=lambda z: 0 if z.env else 1): self._zone(s,z,X,Y,K)
        for pts,arrow,dashed in self.paths: self._path(s,pts,arrow,dashed,X,Y,K)
        for p in self.pills: self._pill(s,p,X,Y,K)
        for cx,y in self.dots:
            stext(s,X(cx-20),Y(y),40*K,26*K,["⋮"],16*K,"#9E9E9E",align=PP_ALIGN.CENTER)
        if self.auth: _arch(s,auth=True)
        self.K=K
        return X(x0),Y(y0),X(x1),Y(y1)
    def _zone(self,s,z,X,Y,K):
        shp=s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE,E(X(z.x)),E(Y(z.y)),E(z.w*K),E(z.h*K))
        shp.adjustments[0]=min(0.5,11.0/min(z.w,z.h))
        if z.env:
            _arch(s,z.env)
            stroke,fill,tcol,_=ENV[z.env]
            shp.fill.solid(); shp.fill.fore_color.rgb=rgb(fill)
        else:
            stroke,tcol=A_ZONE,A_LAB; shp.fill.background()
        shp.line.color.rgb=rgb(stroke); shp.line.width=Pt(1.5*K*0.75); shp.shadow.inherit=False
        ln=_ln(shp); ln.append(ln.makeelement(qn('a:prstDash'),{'val':'dash'}))
        bicon(s,z.zicon,X(z.x+18),Y(z.y+15),22*K,tcol)
        tw=text_w(z.label,13,True)
        if 47+tw+10>z.w: FIT_WARN.append('zone label too wide: %r (%d > %d)'%(z.label,47+tw+10,z.w))
        stext(s,X(z.x+47),Y(z.y+15),(z.w-57)*K,22*K,[z.label],13*K,tcol,medium=True)
    def _pill(self,s,p,X,Y,K):
        stroke=A_THIN if p.cat=='thin' else (A_USER if p.cat=='user' else A_SEC)
        tcol=A_THIN if p.cat=='thin' else A_USER
        icol=A_THIN if p.cat=='thin' else A_USER      # icon follows the pill (skill 6)
        shp=s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE,E(X(p.x)),E(Y(p.y)),E(PW*K),E(PH*K))
        shp.adjustments[0]=7.0/PH
        shp.fill.solid(); shp.fill.fore_color.rgb=rgb(WHITE)
        shp.line.color.rgb=rgb(stroke); shp.line.width=Pt(1.5*K*0.75); shp.shadow.inherit=False
        bicon(s,p.icon or icon_for(p.label),X(p.x+10),Y(p.y+10),23*K,icol)
        lines=C(p.label).split('\n')
        for l in lines:
            if text_w(l,12)>PW-39-6: FIT_WARN.append('pill label too wide: %r'%l)
        stext(s,X(p.x+39),Y(p.y),(PW-39-6)*K,PH*K,lines,12*K,tcol,lsp=13*K)

def _scene_path(self,s,pts,arrow,dashed,X,Y,K):
    """Orthogonal polyline as straight connectors; square caps close the
    corners. The last run ends in the open chevron, 4 px short of the edge
    (skill 12 #9)."""
    pts=[(float(a),float(b)) for a,b in pts]
    n=len(pts)-1
    for i in range(n):
        (xa,ya),(xb,yb)=pts[i],pts[i+1]
        last=(i==n-1) and arrow
        if last:
            L=math.hypot(xb-xa,yb-ya)
            if L<18: FIT_WARN.append('arrow run under 14 px + air (%.0f)'%L)
            xb-=(xb-xa)/L*4; yb-=(yb-ya)/L*4
        if abs(xa-xb)<0.3 and abs(ya-yb)<0.3: continue
        ex,ey=xb,yb
        if last: ex-=(xb-xa)/L*1.0; ey-=(yb-ya)/L*1.0
        cxn=s.shapes.add_connector(MSO_CONNECTOR.STRAIGHT,E(X(xa)),E(Y(ya)),E(X(ex)),E(Y(ey)))
        cxn.line.color.rgb=rgb(A_CONN); cxn.line.width=Pt((1.5 if dashed else 2)*K*0.75)
        cxn.shadow.inherit=False
        ln=_ln(cxn)
        if not last: ln.set('cap','sq')
        if dashed: ln.append(ln.makeelement(qn('a:prstDash'),{'val':'dash'}))
        if last: chevron(s,X(xa),Y(ya),X(xb),Y(yb),K)
Scene._path=lambda self,s,pts,arrow,dashed,X,Y,K: _scene_path(self,s,pts,arrow,dashed,X,Y,K)

REF_ENV={'customer':'Customer premises','cloud':'Customer cloud','cybele':'Hosted by Cybele'}
def reference(s,envs,auth=False,y=REF_Y):
    """The diagram's own reference (skill 11), inside the card so it travels
    with the slide: the blue arrow, the dashed zone, the dashed secondary flow
    when there is one, and one swatch per environment colour used."""
    cy=y+7
    stext(s,96,y,90,14,["REFERENCE"],11,"#888888",medium=True)
    x=190
    seg(s,x,cy,x+48,cy,arrow=True)
    stext(s,x+58,y,300,14,["Data flow — the tip shows direction"],11,A_PAR); x+=58+text_w("Data flow — the tip shows direction",11)+32
    seg(s,x,cy,x+44,cy,color=A_ZONE,width=1.125,dashed=True)
    stext(s,x+58,y,240,14,["Network / logical zone"],11,A_PAR); x+=58+text_w("Network / logical zone",11)+32
    if auth:
        seg(s,x,cy,x+44,cy,width=1.125,dashed=True)
        stext(s,x+58,y,240,14,["Authentication (secondary flow)"],11,A_PAR); x+=58+text_w("Authentication (secondary flow)",11)+32
    for k in ('customer','cloud','cybele'):
        if k not in envs: continue
        stroke,fill,_,_=ENV[k]
        z=rect(s,x,y+1,30,12,fill,radius=0.25,line=stroke,lw=1.0)
        ln=_ln(z); ln.append(ln.makeelement(qn('a:prstDash'),{'val':'dash'}))
        stext(s,x+38,y,260,14,[REF_ENV[k]],11,A_PAR); x+=38+text_w(REF_ENV[k],11)+28

TIP_AIR=4
def seg(s,x1,y1,x2,y2,color=A_CONN,width=1.5,arrow=False,dashed=False):
    """A straight connector in slide px (reference samples only)."""
    cxn=s.shapes.add_connector(MSO_CONNECTOR.STRAIGHT,E(x1),E(y1),E(x2),E(y2))
    cxn.line.color.rgb=rgb(color); cxn.line.width=Pt(width); cxn.shadow.inherit=False
    ln=_ln(cxn)
    if dashed: ln.append(ln.makeelement(qn('a:prstDash'),{'val':'dash'}))
    if arrow: chevron(s,x1,y1,x2,y2,1.0,color)
    return cxn

def chevron(s,xa,ya,xb,yb,K,color=A_CONN):
    """The skill's open chevron (SKILL 3, marker 'tip': M2 2 L11.5 9 L2 16),
    drawn as its own stroke with round caps and joins -- 9.5 px deep, 14 px
    tall, 2 px wide, tip on (xb,yb). Replaces PowerPoint's built-in 'arrow'
    line end, whose wide mitred head with the shaft through it read wrong."""
    L=math.hypot(xb-xa,yb-ya) or 1.0
    ux,uy=(xb-xa)/L,(yb-ya)/L; nx,ny=-uy,ux
    d,h=9.5*K,7.0*K
    pts=[(xb-ux*d+nx*h,yb-uy*d+ny*h),(xb,yb),(xb-ux*d-nx*h,yb-uy*d-ny*h)]
    ff=s.shapes.build_freeform(E(pts[0][0]),E(pts[0][1]),scale=1.0)
    ff.add_line_segments([(E(x),E(y)) for x,y in pts[1:]],close=False)
    shp=ff.convert_to_shape()
    shp.fill.background(); shp.shadow.inherit=False
    shp.line.color.rgb=rgb(color); shp.line.width=Pt(2*K*0.75)
    ln=_ln(shp); ln.set('cap','rnd')
    ln.append(ln.makeelement(qn('a:round'),{}))
    return shp

def _cat(label):
    """Thinfinity components are blue pills; identity providers that are not
    Thinfinity's own, like every other pill, are graphite (skill 6)."""
    return 'thin' if ('thinfinity' in label.lower() or 'broker' in label.lower()
                      or label.lower().startswith('gateway') or 'wag' == label.lower()
                      or 'idp integration' in label.lower()) else 'sec'

DIAG_BOX=(88,164,1192,624)

# ---- Template: reverse-gateway flow --------------------------------------
# Remote Access -> [TLS wire] -> Gateway (DMZ) <- [No Inbound Port wire] <-
# Broker(s) <- resources, on one horizontal axis; an IdP sits in its own
# Identity zone under the DMZ with the dashed auth line (skill R33 / test_08).
def flow_left(sc,users,gateway,users_zone,dmz_zone,wire_in,cy=0,dmz_env=None):
    un=[sc.pill(ZL,cy-(len(users)-1)*SV/2.0+i*SV-PH/2.0,u,'user') for i,u in enumerate(users)]
    sc.fit(un,users_zone,'remote-access',x0=0,x1=200)
    wx=200+GAP; wi=sc.wire(wx,cy,wire_in,icon=('firewall' if 'firewall' in wire_in.lower() else 'vpn-tunnels'))
    gzx=wx+PW+GAP
    gw=sc.pill(gzx+ZL,cy-PH/2.0,gateway,_cat(gateway))
    zg=sc.fit([gw],dmz_zone,'connect',x0=gzx,x1=gzx+200,env=dmz_env)
    sc.bus([(u.r,u.cy) for u in un],(200+wx)/2.0,[(wi.l,cy)],arrow=False)
    sc.path([(wi.r,cy),(gw.l,cy)])
    return gw,zg

def identity(sc,gw,zg,idp):
    ip=sc.pill(gw.x,zg.b+30+ZT,idp,_cat(idp))
    sc.fit([ip],'Identity','id',x0=zg.l,x1=zg.r)
    sc.path([(gw.cx,ip.t),(gw.cx,gw.b)],arrow=False,dashed=True)
    return ip

def brokers_and_resources(sc,x,cy,brokers,resources,label,env=None,icon='network'):
    """Broker(s) on the axis, resources stacked under them; the resources
    converge on one bus to the right that rises into each broker's right edge."""
    bx=x+ZL; y=cy-PH/2.0; brs=[]
    for i,b in enumerate(brokers):
        if b is None:
            y+=sc.ell(bx+PW/2.0,y-6)-6; continue
        brs.append(sc.pill(bx,y,b,_cat(b))); y+=SV
    y+=16
    res=[]
    for r in resources:
        res.append(sc.pill(bx,y,r,'sec')); y+=SV
    bus_x=bx+PW+28
    sc.bus([(r.r,r.cy) for r in res],bus_x,[(b.r,b.cy) for b in brs])
    z=sc.fit(brs+res,label,(ENV[env][3] if env else icon),env=env,x0=x,x1=bus_x+22)
    return brs,res,z

def diag_flow(s,users,gateway,broker,resources,idp=None,sec_broker=None,
              users_zone='Remote Access',dmz_zone='DMZ',res_zone='Internal Network',
              wire_in='TLS 1.3\nPort 443',wire_rev='Outbound-only TLS\nNo Inbound Port',res_env=None):
    card(s); sc=Scene()
    gw,zg=flow_left(sc,users,gateway,users_zone,dmz_zone,wire_in)
    rx=zg.r+GAP; wr=sc.wire(rx,0,wire_rev)
    sc.path([(wr.l,0),(gw.r,0)])
    izx=rx+PW+GAP
    bl=[broker]+([sec_broker,None] if sec_broker else [])
    brs,res,zi=brokers_and_resources(sc,izx,0,bl,resources,res_zone,env=res_env)
    sc.bus([(b.l,b.cy) for b in brs],izx-14,[(wr.r,0)],arrow=False)
    if idp: identity(sc,gw,zg,idp)
    sc.render(s,DIAG_BOX)

# ---- Template: single machine ---------------------------------------------
def diag_single(s):
    card(s); sc=Scene()
    un=[sc.pill(ZL,-SV/2.0+i*SV-PH/2.0,u,'user') for i,u in enumerate(['Remote User','Local User'])]
    sc.fit(un,'Endpoints','remote-access',x0=0,x1=200)
    wx=200+GAP; wi=sc.wire(wx,0,'SSL\nPort 443')
    zx=wx+PW+GAP; y=-PH/2.0; st=[]
    for lab in ['Thinfinity\nGateway','Primary Broker','Virtualization\nProcess','Windows App\n/ Desktop']:
        st.append(sc.pill(zx+ZL,y,lab,_cat(lab))); y+=VS
    sc.fit(st,'Single Machine','premises',x0=zx,x1=zx+200)
    sc.bus([(u.r,u.cy) for u in un],(200+wx)/2.0,[(wi.l,0)],arrow=False)
    sc.path([(wi.r,0),(st[0].l,0)])
    for i in range(len(st)-1): sc.up(st[i+1],st[i])
    x0,y0,x1,y1=sc.render(s,(88,164,700,624))
    tf=tbox(s,760,y0+10,420,300)
    line_txt(tf,"ALL COMPONENTS IN ONE MACHINE",9,True,BLUE,first=True,after=10)
    for b in ["Gateway, Broker and virtualization run on a single host",
              "Local-host connection between the components",
              "Simplest footprint — ideal for POCs and small deployments",
              "No inbound ports: the browser reaches the Gateway over 443"]:
        bullet(tf,b,TEXT,after=8,size=10.5)

# ---- Template: full component map (protocols + resources) ---------------
def diag_matrix(s,idp_label):
    card(s); sc=Scene()
    gw,zg=flow_left(sc,['Remote Users'],'Thinfinity\nGateway','Remote Access','DMZ or Cloud','Firewall\nSSL 443')
    rx=zg.r+GAP; wr=sc.wire(rx,0,'Outbound-only TLS\nNo Inbound Port')
    sc.path([(wr.l,0),(gw.r,0)])
    vx=rx+PW+GAP
    br=sc.pill(vx+ZL,-PH/2.0,'Primary Broker','thin')
    vp=sc.pill(vx+ZL,-PH/2.0+VS,'Virtualization\nProcess','sec')
    sc.fit([br,vp],'Virtualization','app-virtualization',x0=vx,x1=vx+200)
    sc.path([(br.l,0),(wr.r,0)],arrow=False)
    sc.up(vp,br)
    protos=['RDP / RDC','VNC · RFB','SSH · Telnet','WAG · WebDAV','VirtualUI','ThinVNC']
    res=['Windows Apps','Shared Desktops','Virtual App Pool','VDI / Cloud VDI','Terminal Server','Routers / Consoles']
    px=vx+200+GAP
    pn=[sc.pill(px+ZL,-PH/2.0+i*SV,p,'sec') for i,p in enumerate(protos)]
    sc.fit(pn,'Protocols','connect',x0=px,x1=px+200)
    qx=px+200+GAP
    qn_=[sc.pill(qx+ZL,-PH/2.0+i*SV,r,'sec') for i,r in enumerate(res)]
    sc.fit(qn_,'Resources','secure-server',x0=qx,x1=qx+200)
    # protocols converge on the Virtualization Process; any resource is
    # reachable over any protocol, so the resources share one bus
    sc.bus([(p.l,p.cy) for p in pn],vx+200+GAP/2.0,[(vp.r,vp.cy)])
    sc.bus([(q.l,q.cy) for q in qn_],px+200+GAP/2.0,[(p.r,p.cy) for p in pn])
    identity(sc,gw,zg,idp_label)
    sc.render(s,DIAG_BOX)

# ---- Template: multi-region ----------------------------------------------
def diag_multiregion(s,regions,central='Thinfinity\nGateway',users='Remote\nUsers',
                     hub_broker='Primary Broker'):
    card(s); sc=Scene()
    RH=ZT+PH+30+14; RG=20
    n=min(3,len(regions)); rx0=200+GAP+200+64
    sbs=[]
    for i,reg in enumerate(regions[:3]):
        name,res=reg[0],reg[1]; env=reg[2] if len(reg)>2 else None
        zy=i*(RH+RG); py=zy+ZT
        sb=sc.pill(rx0+ZL,py,'Secondary\nBroker','thin')
        rr=[sc.pill(rx0+ZL+(j+1)*(PW+GAP),py,r,'sec') for j,r in enumerate(res[:2])]
        sc.zone(rx0,zy,ZL+3*PW+2*GAP+ZL,RH,name,(ENV[env][3] if env else 'location'),env=env)
        by=sb.b+30
        for r in rr: sc.path([(r.cx,r.b),(r.cx,by)],arrow=False)
        sc.path([(sb.cx,by),(rr[-1].cx,by)],arrow=False)
        sc.path([(sb.cx,by),(sb.cx,sb.b)])
        sbs.append(sb)
    yc=sbs[len(sbs)//2].cy
    hx=200+GAP
    c=sc.pill(hx+ZL,yc-VS/2.0-PH/2.0,central,_cat(central))
    h=sc.pill(hx+ZL,yc+VS/2.0-PH/2.0,hub_broker,_cat(hub_broker))
    sc.fit([c,h],'Central Hub','connect',x0=hx,x1=hx+200)
    sc.up(h,c)
    u=sc.pill(ZL,c.y,users,'user')
    sc.fit([u],'Remote Access','remote-access',x0=0,x1=200)
    sc.path([(u.r,u.cy),(c.l,c.cy)])
    sc.bus([(b.l,b.cy) for b in sbs],hx+200+32,[(h.r,h.cy)])
    sc.render(s,DIAG_BOX)

# ---- Template: IT / OT -----------------------------------------------------
def diag_itot(s):
    card(s); sc=Scene()
    # IT band on top, OT band below, one DMZ between them
    itu=[sc.pill(ZL,ZT+i*SV,u,'user') for i,u in enumerate(['User Group 1','User Group 2'])]
    ot0=ZT+SV+PH+ZB+30
    otu=[sc.pill(ZL,ot0+ZT+i*SV,u,'user') for i,u in enumerate(['User Group 1','User Group 2'])]
    wx=200+GAP; gzx=wx+PW+GAP; nx=gzx+200+64
    its=sc.pill(nx+ZL,ZT,'Secondary\nBroker','thin')
    itw=sc.pill(nx+ZL+PW+60,ZT,'Engineering\nWorkstation','sec')
    ots=sc.pill(nx+ZL,ot0+ZT,'Secondary\nBroker','thin')
    otr=[sc.pill(nx+ZL+PW+60,ot0+ZT+i*SV,r,'sec') for i,r in enumerate(['SCADA / PLC','Pump / Motor','PLC'])]
    nx1=nx+ZL+2*PW+60+ZL
    it_b=max(itu[-1].b,itw.b)+ZB; ot_b=max(otu[-1].b,otr[-1].b)+ZB
    sc.fit(itu,'IT Users','remote-access',x0=0,x1=200,y0=0,y1=it_b)
    sc.fit(otu,'OT Users','remote-access',x0=0,x1=200,y0=ot0,y1=ot_b)
    sc.fit([its,itw],'IT Network','network',x0=nx,x1=nx1,y0=0,y1=it_b)
    sc.fit([ots]+otr,'OT Network · Manufacturing Plant','manufacture',x0=nx,x1=nx1,y0=ot0,y1=ot_b)
    yc=(it_b+ot0)/2.0
    gw=sc.pill(gzx+ZL,yc-VS/2.0-PH/2.0,'Thinfinity\nGateway','thin')
    br=sc.pill(gzx+ZL,yc+VS/2.0-PH/2.0,'Primary Broker','thin')
    sc.fit([gw,br],'DMZ','connect',x0=gzx,x1=gzx+200)
    wi=sc.wire(wx,gw.cy,'TLS 1.3\nPort 443')
    sc.bus([(u.r,u.cy) for u in itu+otu],(200+wx)/2.0,[(wi.l,gw.cy)],arrow=False)
    sc.path([(wi.r,gw.cy),(gw.l,gw.cy)])
    sc.up(br,gw)
    sc.bus([(its.l,its.cy),(ots.l,ots.cy)],nx-32,[(br.r,br.cy)])
    sc.path([(itw.l,itw.cy),(its.r,its.cy)])
    sc.bus([(r.l,r.cy) for r in otr],ots.r+30,[(ots.r,ots.cy)])
    sc.render(s,DIAG_BOX)

# ---- Template: WAG ---------------------------------------------------------
def diag_wag(s):
    card(s); sc=Scene()
    gw,zg=flow_left(sc,['User 1','User n','Local Access'],'Thinfinity\nGateway','Remote Access','DMZ · Gateway','TLS 1.3\nPort 443')
    br=sc.pill(gw.x,gw.y+VS,'Thinfinity Broker','thin')
    zg.h=br.b+ZB-zg.y
    sc.up(br,gw)
    wz=zg.r+GAP
    wag=sc.pill(wz+ZL,br.y,'WAG','thin')
    apps=['IIS Server','WordPress','ERP · Dynamics','Apache','Node.js']
    ax=wz+ZL+PW+60
    an=[sc.pill(ax,br.cy-(len(apps)-1)*SV/2.0+i*SV-PH/2.0,a,'sec') for i,a in enumerate(apps)]
    sc.fit([wag]+an,'Web Application Servers','app-web',x0=wz)
    sc.path([(wag.l,wag.cy),(br.r,br.cy)])
    sc.bus([(a.l,a.cy) for a in an],wag.r+30,[(wag.r,wag.cy)])
    sc.render(s,DIAG_BOX)

# ---- Template: deployment model -------------------------------------------
# Where each deployment model hosts things (skill 2.2b). The users stay outside
# any environment; the environment wraps the network zones it hosts, one level.
def diag_deploy(s,owner_hdr,desc,brand=False,model=None):
    card(s); sc=Scene()
    hdr_w=text_w(owner_hdr,13,True)+56
    rect(s,640-hdr_w/2.0,158,hdr_w,30,(BLUE if brand else "#EFF7FE"),radius=0.5)
    stext(s,640-hdr_w/2.0,158,hdr_w,30,[owner_hdr],13,(WHITE if brand else BLUE),medium=True,align=PP_ALIGN.CENTER)
    ra=sc.pill(ZL,-PH/2.0,'Web Browser\n/ Client / PWA','user')
    sc.fit([ra],'Remote Access','remote-access',x0=0,x1=200)
    wx=200+GAP; wi=sc.wire(wx,0,'TLS 1.3\nPort 443')
    split=(model=='hybrid')
    ex=wx+PW+GAP                      # environment left edge
    dzx=ex+ZL
    gw=sc.pill(dzx+ZL,-PH/2.0,'Thinfinity\nReverse Gateway','thin')
    rx=dzx+200+(ZL+GAP if split else GAP)
    wr=sc.wire(rx,0,'Outbound-only TLS\nNo Inbound Port')
    lzx=rx+PW+GAP+(ZL if split else 0)
    brs,res,zl=brokers_and_resources(sc,lzx,0,['Primary Broker'],
        ['Virtual Desktops\n& Virtual Apps','Office Desktops','Terminal Servers','Web Apps'],'Local Network · Resources')
    zd=sc.fit([gw],'DMZ','connect',x0=dzx,x1=dzx+200,y0=zl.y)
    sc.path([(ra.r,0),(wi.l,0)],arrow=False)
    sc.path([(wi.r,0),(gw.l,0)])
    sc.path([(wr.l,0),(gw.r,0)])
    sc.path([(brs[0].l,0),(wr.r,0)],arrow=False)
    et=zl.y-ZT; eb=zl.b+ZL
    # each environment is as tall as the network zones it hosts
    envs={'onprem':[('customer','Customer premises',zd.l,zl.r,zl.b)],
          'hybrid':[('cybele','Hosted by Cybele',zd.l,zd.r,zd.b),('customer','Customer premises',zl.l,zl.r,zl.b)],
          'byoc':[('cloud','Customer cloud',zd.l,zl.r,zl.b)],
          'hosted':[('cybele','Hosted by Cybele · private cloud',zd.l,zl.r,zl.b)]}.get(model,[])
    for kind,lab,l,r,b in envs:
        sc.zone(l-ZL,et,r-l+2*ZL,b+ZL-et,lab,ENV[kind][3],env=kind)
    x0,y0,x1,y1=sc.render(s,(88,204,1192,596))
    tf=tbox(s,96,y1+14,1088,40); line_txt(tf,desc,10.5,False,TEXT_SEC,first=True,align=PP_ALIGN.CENTER)

# ---- Zero Trust flow strip (RBAC slide) -----------------------------------
def diag_ztflow(s):
    card(s,474,672); sc=Scene()
    items=[('User','user'),('IdP / SAML','sec'),('Thinfinity\nGateway','thin'),('Authorized\nResource','sec')]
    ps=[sc.pill(ZL+i*(PW+72),0,l,c) for i,(l,c) in enumerate(items)]
    sc.fit(ps,'Zero Trust authentication flow','layered-security')
    for i in range(3): sc.path([(ps[i].r,ps[i].cy),(ps[i+1].l,ps[i+1].cy)])
    sc.render(s,(88,488,1192,626))
    _arch(s,ref_y=644)

# ==========================================================================
def build(prs):
    prs.slide_width=Inches(SLIDE_W); prs.slide_height=Inches(SLIDE_H)

    # 1. COVER
    s=new_slide(prs,dark=True,cover=True)
    logo(s,'cybele_logo',64,52,30,white=True); rect(s,250,54,1,26,"#3A4A5F"); logo(s,'thinfinity_logo',270,49,40,white=True)
    tf=tbox(s,64,250,900,40); line_txt(tf,"ONE PLATFORM, INFINITE SOLUTIONS",11,True,BLUE_LT,first=True)
    tf=tbox(s,64,288,1100,90); line_txt(tf,"Thinfinity® Workspace",46,True,WHITE,first=True)
    tf=tbox(s,64,378,900,60); line_txt(tf,"Advanced Zero Trust Remote Access and Cloud VDI Solutions",16,False,MUTED,first=True)
    x=64
    for p in ["HTML5 Browser Access","Zero Trust · No VPN","Any Cloud · Any Device"]: x=pill_ui(s,x,452,p)
    tf=tbox(s,64,648,900,20); line_txt(tf,"www.cybelesoft.com · Property of Cybele Software, Inc. 2026",9,False,FOOT_DK,first=True)

    # 2. ABOUT  (no icons: here the number is the object)
    s=new_slide(prs,n=2); head(s,"About the company","5 key facts about Cybele Software")
    grid(s,[{'title':'Offices','body':'Draper, UT\nWilmington, DE\nBuenos Aires, ARG\nSão Paulo, BR'},
            {'big':'20+','small':'years','body':'In the Zero Trust virtualization business since 2002'},
            {'big':'+5,000','small':'customers','body':'Active customers worldwide'},
            {'big':'+2,000','small':'partners','body':'MSP, CSP, ISV and system-integrator partners worldwide'},
            {'big':'78','small':'countries','body':'Global presence across 78 countries (2023)'}],5,top=170,bottom=560,gap=14)

    # 3. TRUSTED BY
    s=new_slide(prs,dark=True,n=3); head(s,"Trusted by","Leading companies worldwide",dark=True)
    tf=tbox(s,64,250,520,120); line_txt(tf,"5,000+",84,True,BLUE_LT,first=True)
    tf=tbox(s,64,380,520,60); line_txt(tf,"organizations rely on Thinfinity Workspace",15,False,MUTED,first=True)
    tf=tbox(s,640,258,560,220); line_txt(tf,"From medium enterprises to multinational corporations, Cybele delivers secure, browser-based access to applications, desktops and data — without VPNs, plugins or client software.",15,False,MUTED,first=True)

    # 4. THREE PILLARS
    s=new_slide(prs,n=4); head(s,"What Thinfinity delivers","One platform, three outcomes")
    grid(s,[{'num':'01','title':'Secure Access','body':'Ensure Zero Trust access to your corporate resources across various cloud and on-premises environments, enhancing overall security and efficiency.'},
            {'num':'02','title':'Provision & Scale','body':'Support your automation and scalability needs by streamlining resource deployment and management — VDI, DaaS and other virtual resources across platforms.'},
            {'num':'03','title':'Manage','body':"Enhance your organization's operational agility and optimize resource utilization by centralizing management and reducing administrative overhead."}],3,
         icons=['secure-access','workload','easy-management'])

    # 5. UZTNA OVERVIEW (2x2)
    s=new_slide(prs,n=5); head(s,"Overview","Universal Zero Trust Network Access (UZTNA)")
    grid(s,[{'title':'Universal Zero Trust Network Access','bullets':["Secure & controlled connectivity — no VPN needed","Access & Identity Mgmt: IDP integration, role-based permissions","Scalable ZT architecture: segmentation, multi-tenancy, load balancing, fault tolerance","Security: IP blacklisting, GeoIP, brute-force detection · REST API"]},
            {'title':'Cloud Management','bullets':["Deploy VDI & apps on any infra (OCI, Azure, AWS, GCP, VMware, Hyper-V)","Automatic provisioning · integrated VDI Manager (create/start/stop/scale)","Load balancing & smart application pooling","Seamless integration with existing IT · REST API"]},
            {'title':'Remote Privileged Access Management (RPAM)','bullets':["Monitoring, auditing & session recording","Resource reservation / approval workflows","Just-in-time access · restricted working hours","REST API available"]},
            {'title':'Legacy App Delivery & Modernization','bullets':["Low-code / no-code publishing (Windows, Linux, terminal)","Local-like experience on virtual applications","OT URL integration · jsRO","REST API available"]}],2,
         icons=['layered-security','web-cloud','audit-log','publishing'])

    # 6. USE CASES
    s=new_slide(prs,n=6); head(s,"Use cases","Where teams deploy Thinfinity")
    grid(s,[{'title':'Remote & Hybrid Work Security','bullets':["VPN alternative","Zero Trust Access (ZTNA)","Passwordless / SSO RDC","GPU & graphic-intensive apps","Servers, consoles, routers, mainframes"]},
            {'title':'Virtual App & Desktop Delivery','bullets':["RDS alternative","Citrix NetScaler alternative","Citrix DaaS alternative","VMware alternative","Centralized app & desktop mgmt"]},
            {'title':'Third-Party Access Management','bullets':["Implement RBAC","Secure vendor intranets","Just-in-Time access (JIT)","Legacy system access","Remote support"]},
            {'title':'Move Infrastructure to the Cloud','bullets':["Hybrid & multi-cloud admin","Modernize data center & VDI","Virtual labs & classrooms","SOC & HIPAA compliance","SSE and SASE"]},
            {'title':'Secure Remote Access to OT','bullets':["Real-time monitoring","Access control for critical infra","Remote SCADA monitoring","Secure IT–OT data exchange"]}],5,gap=12,
         icons=['remote-working','app-virtualization','user-guest','cloud','manufacture'])

    # 7. OUR CLIENTS
    s=new_slide(prs,n=7); head(s,"Our clients","Who runs on Thinfinity")
    grid(s,[{'title':'MSPs / MSSPs','body':'Managed Service & Security Providers · General IT, cybersecurity-focused, industry-specific'},
            {'title':'CSPs / Data centers','body':'IaaS, PaaS, SaaS · Private & Hybrid Cloud specialists'},
            {'title':'ISVs','body':'Independent Software Vendors · SMB, enterprise & industry-specific solutions'},
            {'title':'Enterprises','body':'Medium, large & multinational corporations'}],4,top=152,bottom=336,
         icons=['admin','iaas-infrastructure','new-app','premises'])
    tf=tbox(s,64,394,600,20); line_txt(tf,"INDUSTRIES",9,True,BLUE,first=True)
    y=tags(s,64,418,1152,["Financial Services","Healthcare","Government","Telecommunications","Manufacturing","Oil & Energy","Education","Defense","Retail & Insurance","Pharmaceuticals","Aviation","Mining & Metals"])
    tags(s,64,y+8,1152,["IT Teams","Product Teams","Security Teams","OT Teams"],fill="#DCEBFB",tcol=BLUE)

    # 8. CLOUD MANAGER
    s=new_slide(prs,n=8); head(s,"Cloud Manager","Manage, provision and scale virtual applications")
    grid(s,[{'title':'Manage',"body":"Administrate VMs and DaaS models in the public cloud (Azure, AWS, GCP, Ionos).\nAdministrate VMs and VDI on premises (Hyper-V, VMware).\nVM administration: on, off and hibernation based on usage or schedule."},
            {'title':'Provision & Scale',"body":"Automatic provisioning based on golden images.\nAuto-scaling based on usage and schedules.\nAdministrate VDI and DevOps pipelines: production, testing, staging."}],2,top=160,bottom=560,
         icons=['easy-management','assign-VM'])

    # 9. LOCAL-LIKE UX
    s=new_slide(prs,dark=True,n=9); head(s,"UX","Local-like user experience",dark=True)
    tf=tbox(s,64,190,560,360)
    line_txt(tf,"Thinfinity delivers your Windows and legacy applications to the browser with a native, local-like feel — no plugins, no client software.",13,False,MUTED,first=True,after=12)
    for b in ["Smooth, low-latency interaction even on graphic-intensive apps","Full clipboard, printing, file transfer and multi-monitor support","Responsive controls for latency-sensitive OT / control interfaces","Consistent experience across PC, Mac, Chromebook and tablet"]:
        bullet(tf,b,MUTED,after=8,size=11)
    cs=[("Feels native","Users interact with virtual apps as if installed locally.",'usability'),
        ("Any device","One HTML5 browser — desktop, laptop or tablet.",'multi-platform'),
        ("Zero install","No VPN, plugin or agent on the endpoint.",'endpoint-agnostic-access')]
    yy=190
    for t,d,ic in cs:
        dark_card(s,656,yy,560,108,t,d,icon=ic); yy+=120

    # 10. ANALYTICS
    s=new_slide(prs,n=10); head(s,"ZTNA · RPAM","Analytics — Enterprise Audit Log")
    grid(s,[{'title':'Real-time monitoring','body':'Live session tracking and usage statistics with immediate insight into active sessions and app performance.'},
            {'title':'Comprehensive reporting','body':'Detailed reports on user activity, session duration and resource utilization. Customizable to meet specific organizational needs.'},
            {'title':'Security auditing','body':'Detailed logs of access attempts, successful logins and security events. Alerts for unusual or suspicious activity.'},
            {'title':'User behavior analysis','body':'Tracking of user interactions and usage patterns to improve experience and application design.'}],2,
         icons=['view-data','audit-log','shield-ok','all-profiles'])

    # 11. WORKSPACE INTRO
    s=new_slide(prs,dark=True,n=11); head(s,"Thinfinity Workspace","Deliver your Windows applications to any device, anywhere",dark=True)
    tf=tbox(s,64,172,560,380)
    line_txt(tf,"A unified, secure access platform that web-enables your Windows applications, desktops and data. Instant, browser-based access on any device — without installing VPNs, plugins or client software.",13,False,MUTED,first=True,after=10)
    line_txt(tf,"Built on a Zero Trust Network Access (ZTNA) framework, every connection is secure, authenticated and authorized, dramatically reducing your network's attack surface.",13,False,MUTED)
    cs=[("Modernize legacy applications","Instantly convert client-server and legacy Windows apps into modern web apps.",'publishing'),
        ("Embrace hybrid work & BYOD","Consistent access from any location on PC, Mac, Chromebook or tablet.",'remote-working'),
        ("Enhance security","Eliminate open inbound ports (like RDP 3389) with a secure reverse gateway.",'shield-ok'),
        ("Reduce IT overhead","Simplify deployment and management, cutting infrastructure complexity and cost.",'easy-management')]
    yy=172
    for t,d,ic in cs:
        dark_card(s,656,yy,560,86,t,d,icon=ic); yy+=95

    # 12. CENTRALIZED MANAGEMENT
    s=new_slide(prs,n=12); head(s,"Thinfinity Cloud Manager","Centralized management")
    grid(s,[{'title':'Hybrid & multi-cloud control','body':'Manage your entire infrastructure (on-premises, AWS, Azure, GCP) from a single web-based console.'},
            {'title':'Automated provisioning & scaling','body':'Infrastructure-as-Code integrations and intelligent autoscaling dynamically adjust resources to user demand.'},
            {'title':'Application pooling','body':'Pools of pre-launched application sessions for instantaneous access, optimized allocation and high availability.'},
            {'title':'Cost optimization','body':'Automated power scheduling starts/stops VMs, significantly reducing cloud compute costs during off-hours.'}],2,
         icons=['hybrid','refresh','app-group','gear'])

    # 13. SECTION — ARCHITECTURE
    s=new_slide(prs,dark=True,n=13)
    divider(s,"SECTION","Architecture","Reference topologies — secure by design, no inbound ports.",'iaas-infrastructure')

    # 14. SINGLE MACHINE
    s=new_slide(prs,n=14); head(s,"Architecture · deployment","Single machine deployment")
    diag_single(s)

    # 15. FULL COMPONENT MAP
    s=new_slide(prs,n=15); head(s,"Architecture · components","Component & protocol map")
    diag_matrix(s,'IDP')

    # 16. FULL COMPONENT MAP + IDP
    s=new_slide(prs,n=16); head(s,"Architecture · components","Component map with identity provider")
    diag_matrix(s,'Azure AD\nOAuth · Ping')

    # 17. LOAD BALANCING PRIMARY BROKERS
    s=new_slide(prs,n=17); head(s,"Architecture · scale","Load balancing in Primary Brokers")
    diag_flow(s,['User 1','User 2','User n'],'Thinfinity\nGateway','Primary Broker',
              ['Terminal Server','VDI / Cloud VDI','Virtual App Pool'],
              sec_broker='Primary Broker',res_zone='Local-host Connection')

    # 18. GATEWAY ON DMZ OR CLOUD
    s=new_slide(prs,n=18); head(s,"Architecture · gateway","Gateway on DMZ or Cloud")
    diag_flow(s,['Remote Users','PWA'],'Thinfinity\nGateway','Primary Broker',
              ['Virtual Apps','Desktops','Servers'],dmz_zone='DMZ or Cloud')

    # 19. LOAD BALANCING GATEWAYS + BROKERS
    s=new_slide(prs,n=19); head(s,"Architecture · scale","Load balancing Gateways & Primary Brokers")
    diag_flow(s,['User 1','User 2','User n'],'Thinfinity\nGateway','Primary Broker',
              ['VDI Pool','Terminal Server','App Servers'],sec_broker='Primary Broker',
              dmz_zone='Gateways (LB)',res_zone='Local-host Connection')

    # 20. DECENTRALIZED LOAD BALANCING
    s=new_slide(prs,n=20); head(s,"Secondary Brokers & Agents","Decentralized load balancing")
    grid(s,[{'title':'Decentralized load balancing','body':"Secondary Brokers decentralize the virtualization process, enabling Thinfinity to manage connections across a dispersed network infrastructure and distribute workloads efficiently."},
            {'title':'Multi-tenant performance','body':"By using Secondary Brokers, Thinfinity serves a large number of users and sessions simultaneously — optimal performance even in complex, multi-tenant environments."},
            {'title':'Resource pooling','body':"Secondary Brokers pool applications and desktops, dynamically assigned based on demand — a more efficient use of resources that scales to user needs."},
            {'title':'High availability & fault tolerance','body':"With Secondary Brokers and Virtualization Agents, Thinfinity ensures HA and fault tolerance, maintaining service continuity for mission-critical apps."}],2,
         icons=['load-balancer','multi-tenancy','app-group','shield-ok'])

    # 21. SECONDARY BROKERS TOPOLOGY
    s=new_slide(prs,n=21); head(s,"Architecture · secondary brokers","Decentralized virtualization across networks")
    diag_flow(s,['User 1','User 2','User n'],'Thinfinity\nGateway','Primary Broker',
              ['VDI Pool','Windows Apps'],idp='IDP Integration',sec_broker='Secondary\nBroker',
              users_zone='Remote Access',dmz_zone='Cloud or DMZ',res_zone='Thinfinity Portal')

    # 22. SECTION — MULTIPLE NETWORKS
    s=new_slide(prs,dark=True,n=22)
    divider(s,"SECTION","Multiple networks","Single-tenant, multi-tenant, IT/OT and multi-region topologies.",'network')

    # 23. SINGLE TENANT CLOUD OR DATA CENTER
    s=new_slide(prs,n=23); head(s,"Architecture · single tenant","Single tenant — Cloud or Data Center")
    diag_flow(s,['User Group 1','User Group 2','PWA'],'Thinfinity\nGateway','Primary Broker',
              ['Pool 1','Pool 2','Physical\nWorkstations'],dmz_zone='DMZ',res_zone='OCI Tenant',res_env='cloud',
              wire_in='TLS 1.3\nPort 443',wire_rev='TLS 1.3\nNo Inbound Port')

    # 24. OT AND OFFLINE
    s=new_slide(prs,n=24); head(s,"Architecture · OT & offline","Datacenter IT or OT network")
    diag_flow(s,['User Group 1','User Group 2','PWA'],'Thinfinity\nGateway','Primary Broker',
              ['Session Servers','VDI Servers','Physical\nResources'],dmz_zone='DMZ',
              res_zone='IT / OT Datacenter',wire_rev='TLS 1.3\nNo Inbound Port')

    # 25. REMOTE ACCESS SSO/2FA
    s=new_slide(prs,n=25); head(s,"Architecture · ZTNA","Remote access with SSO / 2FA")
    diag_flow(s,['End User','Remote User'],'Thinfinity\nGateway','Primary Broker',
              ['Location A','Location B','App Pool'],idp='Microsoft Entra ID',
              sec_broker='Secondary\nBroker',res_zone='Customer Domain',
              wire_in='TLS 1.3\nSSO / 2FA',wire_rev='Outbound only\nNo Inbound Port')

    # 26. REVERSE GATEWAY SAML
    s=new_slide(prs,n=26); head(s,"Architecture · ZTNA","Reverse Gateway with SAML enforcement")
    diag_flow(s,['End User','Remote User'],'Thinfinity\nReverse Gateway','Primary Broker',
              ['App Pool 1','App Pool 2','Terminal Server'],idp='Microsoft Entra ID',
              sec_broker='Secondary\nBroker',res_zone='Internal Network',
              wire_in='SAML token\n2FA',wire_rev='Outbound only\nNo Inbound Port')

    # 27. IT / OT MANUFACTURING
    s=new_slide(prs,n=27); head(s,"Architecture · IT/OT","IT and OT network segmentation")
    diag_itot(s)

    # 28. MULTI-CLOUD
    s=new_slide(prs,n=28); head(s,"Architecture · multi-cloud","Hybrid multi-cloud with multiple IdPs")
    diag_flow(s,['Local Users','Remote Users'],'Thinfinity\nGateway','Primary Broker',
              ['On-prem Apps','DaaS / Cloud VDI','OCI Resources'],idp='Azure AD · Okta',
              dmz_zone='DMZ · Port 443',res_zone='On-prem + OCI',
              wire_in='TLS 1.3\nOutbound',wire_rev='No inbound port\nrequired')

    # 29. MULTI-TENANT CLOUD GATEWAY
    s=new_slide(prs,n=29); head(s,"Architecture · multi-tenant","Managed cloud gateway — multiple customers")
    diag_flow(s,['Customer 1','Customer 2','End Users'],'Thinfinity\nCloud Gateway','Primary Broker',
              ['Resource Grp 1','Resource Grp 2','ERP · Web Apps'],
              dmz_zone='Managed by Cybele',res_zone='Per-customer · SAML',
              wire_rev='TLS 1.3\nNo Inbound Port')

    # 30. AWS EC2
    s=new_slide(prs,n=30); head(s,"Architecture · AWS","Multiple applications, single database")
    diag_flow(s,['User 1','User n','Testing'],'Gateway (EC2)','Prim. Broker (EC2)',
              ['SQL Database','File Server','OCI Santiago'],dmz_zone='DMZ (AWS)',
              res_zone='Riyadh · Jeddah · Khobar',wire_rev='Reverse\nNo Inbound Port')

    # 31. SECURE AUTHENTICATION
    s=new_slide(prs,n=31); head(s,"Identity","Secure Authentication")
    grid(s,[{'title':'Zero Trust','body':'Every request authenticated and authorized — never trust, always verify.'},
            {'title':'Single Sign-On (SSO)','body':'One identity across all published apps and desktops.'},
            {'title':'Two-Factor Authentication','body':'2FA / MFA enforced at the gateway for every session.'},
            {'title':'SAML & OAuth 2.0','body':'Federate with any standards-based identity provider.'}],4,top=190,bottom=480,
         icons=['layered-security','login','2FA','saml'])
    tf=tbox(s,64,506,1152,40); line_txt(tf,"Standards: SAML · OAuth 2.0 · OpenID Connect — enforced before any resource is reached.",11,False,TEXT_SEC,first=True)

    # 32. RBAC + IDP
    s=new_slide(prs,n=32); head(s,"Identity & access","Role-Based Access Control (RBAC)")
    rect(s,64,158,560,300,WHITE,radius=0.05)
    bicon(s,'RDBAC-access-control',88,180,26,BLUE)
    tf=tbox(s,88,220,512,220); line_txt(tf,"How RBAC works",11,True,BLUE,first=True,after=8)
    for b in ["Admin assigns users to appropriate roles","Users are assigned to roles","Roles define authority level","Permissions are authorized for specific roles"]:
        bullet(tf,b,TEXT,after=8,size=11)
    tf=tbox(s,88,400,512,52); line_txt(tf,"Thinfinity's implementation of RBAC ensures users only access the applications and data necessary for their role.",9.6,False,TEXT_SEC,first=True)
    rect(s,648,158,568,300,WHITE,radius=0.05)
    bicon(s,'identity-federation',672,180,26,BLUE)
    tf=tbox(s,672,220,520,30); line_txt(tf,"Identity sources & providers",11,True,NAVY,first=True)
    tags(s,672,252,520,["Thinfinity IDP","Active Directory","Local / Workgroup","SQL · Mongo users","SAML","OAuth 2.0"],fill="#EEF4FB",tcol=NAVY)
    tf=tbox(s,672,330,520,20); line_txt(tf,"FEDERATED PROVIDERS",8.6,True,BLUE,first=True)
    tags(s,672,352,520,["Microsoft Entra ID","Microsoft AD","Google","Okta","JumpCloud","OneLogin","Auth0","PingID","DUO","ForgeRock","OCI IAM"],fill="#DCEBFB",tcol=BLUE)
    # the Zero Trust flow, on the same grid as every other diagram in the deck
    diag_ztflow(s)

    # 33. OT NETWORKS
    s=new_slide(prs,n=33); head(s,"OT Networks","Secure & controlled access to industrial systems")
    grid(s,[{'title':'Smart Zero Trust enforcement','bullets':["No VPN — browser access to SCADA, ICS, DCS","Granular access control via IdP (Azure AD, LDAP)","Network segmentation isolates OT from IT","Multi-tenancy & fault tolerance for distributed ops"]},
            {'title':'Legacy delivery & modernization in OT','bullets':["Low-code / no-code publishing (Windows, Linux, terminal)","Local-like experience for latency-sensitive controls","OT URL integration + jsRO support","Real-time dashboards, controls & alerts in web apps"]},
            {'title':'Dynamic policy & security','bullets':["Rules by device, identity, geolocation and time","IP blacklisting & GeoIP filtering","Brute-force protection","Continuous session validation"]}],3,
         icons=['granular-access','publishing','RDBAC-access-control'])

    # 34 & 35. SUCCESS CASES
    def success(n,company,sub,overview,highlights,quote,author,metrics):
        s=new_slide(prs,n=n); head(s,"Success case · "+sub,company)
        rect(s,64,158,690,470,WHITE,radius=0.05)
        tf=tbox(s,88,182,642,250); line_txt(tf,"OVERVIEW",9,True,BLUE,first=True,after=4)
        line_txt(tf,overview,10,False,TEXT_SEC,after=12); line_txt(tf,"TECHNICAL SOLUTION HIGHLIGHTS",9,True,BLUE,after=6)
        for b in highlights: bullet(tf,b,TEXT)
        rect(s,772,158,444,470,NAVY,radius=0.05)
        tf=tbox(s,796,182,396,300); line_txt(tf,"KEY METRICS",9,True,BLUE_LT,first=True,after=6)
        for k,v in metrics:
            p=tf.add_paragraph(); p.space_after=Pt(4)
            r=p.add_run(); r.text=C(k)+":  "; _font(r,9.5,False,MUTED)
            r2=p.add_run(); r2.text=C(v); _font(r2,9.5,True,WHITE)
        line_txt(tf,"“"+quote+"”",10,False,WHITE,after=6,italic=True); line_txt(tf,author,9,False,MUTED)
    success(34,"Rockwell Automation","Industrial automation",
        "A global leader in industrial automation required a scalable, secure and efficient remote access solution for its workforce and partners while reducing reliance on traditional VDI and VPN.",
        ["40+ user groups with tailored golden images and Azure scale sets","Replaced VPN and VMware-based VDI","Clientless, Zero Trust-based secure access","Hybrid deployment on Azure, AWS expansion planned"],
        "Thinfinity Workspace has revolutionized our remote access strategy — enhancing security, reducing infrastructure costs, and paving the way for a multi-cloud future without vendor lock-in.",
        "Joseph Morr · Solution Architect",
        [("Total users","10,000"),("Current status","7,000 live"),("Full deployment","by 2026"),("Cloud platform","Azure (+AWS)"),("Outcome","Lower cost, no lock-in")])
    success(35,"AVEVA California","Oil & gas software",
        "A leader in industrial software for oil & gas required a scalable, hybrid VDI solution for 4,000 users running custom-integrated applications, with flexibility between cloud and on-premises.",
        ["Non-persistent virtual desktops with tailored golden images","Replaced VPN and VMware VDI","Clientless, Zero Trust-based secure access","Automated provisioning and load balancing"],
        "With Thinfinity Workspace, we achieved a seamless hybrid virtual application experience, optimizing cost and performance while maintaining security and reliability for oil & gas operations.",
        "Mario Coelho · Program Manager",
        [("Total users","4,000"),("Deployment","Hybrid VDI"),("Cloud platform","Azure (+AWS)"),("Focus","Cost & performance"),("Sector","Energy operations")])

    # 36. MULTIPLE APP SERVERS + SECONDARY BROKERS
    s=new_slide(prs,n=36); head(s,"Architecture · HA","Multiple App Servers with Secondary Brokers")
    diag_flow(s,['User 1','User 2','User n'],'Thinfinity\nGateway','Primary Broker',
              ['App Server','App Server','SQL'],sec_broker='Secondary\nBroker',
              dmz_zone='DMZ',res_zone='Customer Network',wire_rev='Reverse\nNo Inbound Port')

    # 37. REVERSE GATEWAY AUTH0
    s=new_slide(prs,n=37); head(s,"Architecture · ZTNA","Reverse Gateway with Auth0")
    diag_flow(s,['End User','Remote User'],'Thinfinity\nReverse Gateway','Primary Broker',
              ['Location A','Location B','App Pool'],idp='Auth0',sec_broker='Secondary\nBroker',
              res_zone='Customer Domain',wire_in='OAuth token',wire_rev='Outbound only\nNo Inbound Port')

    # 38. REVERSE GATEWAY ENTRA ID
    s=new_slide(prs,n=38); head(s,"Architecture · ZTNA","Reverse Gateway with Microsoft Entra ID")
    diag_flow(s,['End User','Remote User'],'Thinfinity\nReverse Gateway','Primary Broker',
              ['Location A','Location B','App Pool'],idp='Microsoft Entra ID',sec_broker='Secondary\nBroker',
              res_zone='Customer Domain',wire_in='OAuth / SAML',wire_rev='Outbound only\nNo Inbound Port')

    # 39. REVERSE GATEWAY AUTH0 (single)
    s=new_slide(prs,n=39); head(s,"Architecture · ZTNA","Reverse Gateway — Auth0 outbound only")
    diag_flow(s,['End User','Remote User'],'Thinfinity\nReverse Gateway','Prim. Broker',
              ['Location A','Location B'],idp='Auth0',sec_broker='Secondary\nBroker',
              res_zone='Customer Domain',wire_in='OAuth token',wire_rev='Outbound only\nNo Inbound Port')

    # 40. MULTI-REGION
    s=new_slide(prs,n=40); head(s,"Architecture · multi-region","Global multi-region access")
    diag_multiregion(s,[('Europe',['Terminal Svc','Virtual Machines']),
                        ('US · NY',['Terminal Svc','Virtual Machines']),
                        ('Asia · Tokyo',['Terminal Svc','Physical Res.'])])

    # 41. MULTI-REGION MULTI-CLOUD
    s=new_slide(prs,n=41); head(s,"Architecture · multi-region","Multi-region across multiple clouds")
    diag_multiregion(s,[('Azure · Central',['Terminal Svc','Virtual Machines'],'cloud'),
                        ('AWS · Ireland (EAST)',['Terminal Svc','Virtual Machines'],'cloud'),
                        ('On-Prem · Chile',['Terminal Svc','Physical Res.'],'customer')])

    # 42. WAG
    s=new_slide(prs,n=42); head(s,"Architecture · WAG","Web Application Gateway")
    diag_wag(s)

    # 43. MULTI-TENANT UNIQUE REMOTE IDs
    s=new_slide(prs,n=43); head(s,"Architecture · multi-tenant","Unique Remote IDs per region")
    diag_multiregion(s,[('USA',['Unique Remote ID','Virtual Machines']),
                        ('Asia',['Unique Remote ID','Virtual Machines']),
                        ('Europe',['Unique Remote ID','Virtual Machines'])],
                     central='Thinfinity\nGateway',users='Customer 1',hub_broker='www.1/2/3.com')

    # 44. MULTI-CUSTOMER REVERSE PROXY
    s=new_slide(prs,n=44); head(s,"Architecture · multi-tenant","Multiple customers behind a reverse proxy")
    diag_multiregion(s,[('USA · Customer 1',['Unique Remote ID','Virtual Machines']),
                        ('Asia · Customer 2',['Unique Remote ID','Virtual Machines']),
                        ('Europe · Customer 3',['Unique Remote ID','Virtual Machines'])],
                     central='Reverse Proxy\n(Nginx / ALB)',users='Remote\nAccess',hub_broker='Thinfinity\nGateway')

    # 45. FAILOVER
    s=new_slide(prs,n=45); head(s,"Architecture · failover","Primary & backup site with license managers")
    diag_flow(s,['End User 1','End User 2','End User 3'],'Gateway + Primary\nLicense Manager','Primary Broker',
              ['App Server','App Server','App Server'],sec_broker='Secondary\nBroker',
              dmz_zone='Primary Site',res_zone='Backup Site · Sec. LM',
              wire_rev='Reverse\nNo Inbound Port')

    # 46. SECTION — DEPLOYMENT OPTIONS
    s=new_slide(prs,dark=True,n=46)
    divider(s,"SECTION","Deployment options","On-Premises · Hybrid · Bring Your Own Cloud · Fully Hosted.",'hybrid')

    # 47. ON PREMISES
    s=new_slide(prs,n=47); head(s,"Deployment · On Premises","All infrastructure on customer premises")
    diag_deploy(s,"MANAGED BY CUSTOMER  ·  ON PREMISES",
        "All infrastructure is on the customer premises. Cybele provides licenses and support for the deployment. Concurrent-user pricing · 15-day POC.",model='onprem')

    # 48. HYBRID
    s=new_slide(prs,n=48); head(s,"Deployment · Hybrid","Gateway managed by Cybele, desktops split")
    diag_deploy(s,"HYBRID  ·  GATEWAY MANAGED BY CYBELE",
        "The Thinfinity Gateway is hosted and managed by Cybele Software; desktops are split between Cybele and the customer. Gateway + concurrent-user pricing · min. 20 users.",model='hybrid')

    # 49. BRING YOUR OWN CLOUD
    s=new_slide(prs,n=49); head(s,"Deployment · BYOC","Deployment entirely on the customer cloud")
    diag_deploy(s,"MANAGED BY CUSTOMER  ·  BRING YOUR OWN CLOUD",
        "The deployment is done entirely on the customer cloud. Cybele provides licenses and support for the deployment. Concurrent-user pricing · 15-day POC.",model='byoc')

    # 50. FULLY HOSTED
    s=new_slide(prs,n=50); head(s,"Deployment · Fully Hosted","Cloud desktops managed by Cybele")
    diag_deploy(s,"FULLY HOSTED  ·  MANAGED BY CYBELE",
        "Cloud desktops hosted on private cloud, fully managed by Cybele Software. Gateway + cloud-desktop pricing · min. 20 users.",brand=True,model='hosted')

    # 51. SECTION — ADOPTION PROCESS
    s=new_slide(prs,dark=True,n=51)
    divider(s,"SECTION","Adoption process","From demo to production — and VirtualUI integration.",'roadmap')

    # 52. ADOPTION — 3 STEPS
    s=new_slide(prs,n=52); head(s,"Adoption process · Thinfinity Workspace","From demo to production in three steps")
    grid(s,[{'num':'01','title':'Demo','bullets':["Key features aligned to your objectives","Overview of system architecture","Implementation strategies & use cases","Address technical inquiries","Just 30 minutes of your time"]},
            {'num':'02','title':'Free Trial / POC','bullets':["Implement Thinfinity to your requirements","Configure features to demo scope","2-week trial license","Dedicated engineering support","POC meeting: 30–45 minutes"]},
            {'num':'03','title':'Deployment','bullets':["Guide transition from trial to production","Final configuration & integration","Testing, verification & best practices","Smooth integration with existing systems","Knowledge transfer to your team"]}],3,
         icons=['connect','check','roadmap'])

    # 53. VIRTUALUI INTEGRATION
    s=new_slide(prs,n=53); head(s,"Adoption process · VirtualUI integration","Web-enable your own application")
    grid(s,[{'num':'01','title':'Development','bullets':["Embed VirtualUI with a single line of code, recompile","Ensure dependencies & libraries are compatible","Local test of your new web application"]},
            {'num':'02','title':'POC / Workspace','bullets':["Publish the VirtualUI app under Thinfinity Workspace","Configure features to demo-defined scope","2-week trial license · dedicated support","POC meeting: 30–45 minutes"]},
            {'num':'03','title':'Deployment','bullets':["Guide transition from trial to production","Final deployment configuration","Final testing, verification & best practices","Knowledge transfer to your team"]}],3,
         icons=['app-virtual-ui','publishing','roadmap'])

    # 54. THANK YOU / CONTACT
    s=new_slide(prs,dark=True,cover=True)
    logo(s,'cybele_logo',64,150,28,white=True); rect(s,240,150,1,24,"#3A4A5F"); logo(s,'thinfinity_logo',258,148,36,white=True)
    tf=tbox(s,64,220,1000,80); line_txt(tf,"Thank you for watching",42,True,WHITE,first=True)
    tf=tbox(s,64,306,900,40); line_txt(tf,"Contact us or visit our website for more information.",15,False,MUTED,first=True)
    cols=[("Web","www.cybelesoft.com"),("USA & Canada (Toll Free)","+1 (866) 462-9768"),("International","+1 (302) 892-9625")]
    x=64
    for lab,val in cols:
        tf=tbox(s,x,380,320,60); line_txt(tf,lab.upper(),9,True,BLUE_LT,first=True,after=4); line_txt(tf,val,14,True,WHITE)
        x+=320
    tf=tbox(s,64,470,1000,60); line_txt(tf,"OFFICES",9,True,BLUE_LT,first=True,after=4)
    line_txt(tf,"14183 Minuteman Drive, Office 200, Draper, UT 84020, USA\n6350 Libertador Av., 6º, C.A.B.A., Bs. As., CP1428, Arg.",11,False,MUTED)
    tf=tbox(s,64,648,1150,40); line_txt(tf,"©2026 Cybele Software, Inc. All rights reserved. Thinfinity® is a registered trademark of Cybele Software, Inc.",9,False,FOOT_DK,first=True)


def references():
    """Every slide that drew a diagram gets its reference, last, on top."""
    for e in list(ARCH.values()): reference(e['slide'],e['envs'],e['auth'],e['ref_y'])

def to_pdf(pptx_path,pdf_path):
    import win32com.client
    pp=win32com.client.Dispatch("PowerPoint.Application")
    try:
        pres=pp.Presentations.Open(os.path.abspath(pptx_path),WithWindow=False)
        pres.SaveAs(os.path.abspath(pdf_path),32)
        pres.Close()
    finally:
        pp.Quit()

if __name__=="__main__":
    # Pass 1 collects every (icon, colour) the deck asks for, so the brand set is
    # rasterised in a single browser launch before anything is drawn for real.
    COLLECT_MODE=True
    build(Presentation()); references(); ARCH.clear()
    COLLECT_MODE=False
    print("brand icons needed:",len(COLLECT))
    bi.build(COLLECT)

    prs=Presentation(); build(prs); references()
    print('diagram slides with a reference:',len(ARCH))
    pptx=os.path.join(OUT_DIR,NAME+".pptx"); prs.save(pptx); print("PPTX:",pptx)
    print("slides:",len(prs.slides._sldIdLst))
    pdf=os.path.join(OUT_DIR,NAME+".pdf")
    try: to_pdf(pptx,pdf); print("PDF:",pdf)
    except Exception as e: print("PDF conversion failed:",e)
    print("fit warnings:",sorted(set(FIT_WARN)) or "none")
    print("Done: 54 native slides")
