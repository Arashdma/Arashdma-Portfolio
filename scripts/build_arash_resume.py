from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import Paragraph


ROOT = Path('/Users/arash/Documents/Portfolio')
OUT = ROOT / 'output' / 'pdf' / 'arash-daman-afshan-resume-final-v2.pdf'
OUT.parent.mkdir(parents=True, exist_ok=True)

INTER_DIR = Path('/Users/arash/Library/Fonts')
MONTSERRAT_DIR = Path('/Users/arash/Library/Fonts')
pdfmetrics.registerFont(TTFont('Inter', str(INTER_DIR / 'Inter-Regular-slnt=0.ttf')))
pdfmetrics.registerFont(TTFont('Inter-Medium', str(INTER_DIR / 'Inter-Medium-slnt=0.ttf')))
pdfmetrics.registerFont(TTFont('Inter-SemiBold', str(INTER_DIR / 'Inter-SemiBold-slnt=0.ttf')))
pdfmetrics.registerFont(TTFont('Inter-Bold', str(INTER_DIR / 'Inter-Bold-slnt=0.ttf')))
pdfmetrics.registerFont(TTFont('Montserrat', str(MONTSERRAT_DIR / 'Montserrat-Regular.ttf')))
pdfmetrics.registerFont(TTFont('Montserrat-Medium', str(MONTSERRAT_DIR / 'Montserrat-Medium.ttf')))
pdfmetrics.registerFont(TTFont('Montserrat-SemiBold', str(MONTSERRAT_DIR / 'Montserrat-SemiBold.ttf')))
pdfmetrics.registerFont(TTFont('Montserrat-Bold', str(MONTSERRAT_DIR / 'Montserrat-Bold.ttf')))
pdfmetrics.registerFontFamily('Inter', normal='Inter', bold='Inter-Bold')

PAGE_W, PAGE_H = letter
MARGIN_X = 48
TOP = 52
BOTTOM = 42
BLUE = colors.HexColor('#1769D1')
INK = colors.HexColor('#151515')
MUTED = colors.HexColor('#60656B')
LIGHT = colors.HexColor('#E6E9ED')


def style(name, **kwargs):
    base = dict(fontName='Inter', textColor=INK, leading=12, alignment=TA_LEFT)
    base.update(kwargs)
    return ParagraphStyle(name, **base)


BODY = style('Body', fontSize=8.7, leading=12.2, textColor=MUTED)
BODY_DARK = style('BodyDark', parent=BODY, textColor=INK)
SMALL = style('Small', fontSize=7.6, leading=10.2, textColor=MUTED)
SMALL_DARK = style('SmallDark', parent=SMALL, textColor=INK)
ROLE = style('Role', fontName='Montserrat-SemiBold', fontSize=9.1, leading=12, textColor=INK)
COMPANY = style('Company', fontName='Montserrat-Bold', fontSize=12.4, leading=15, textColor=INK)
SECTION = style('Section', fontName='Montserrat-SemiBold', fontSize=9.3, leading=12, textColor=BLUE)
SIDEBAR_HEAD = style('SidebarHead', fontName='Montserrat-SemiBold', fontSize=9.3, leading=12, textColor=BLUE)
SUMMARY = style('Summary', fontSize=10.1, leading=14.3, textColor=INK)
HEADER = style('Header', fontName='Inter-Bold', fontSize=30, leading=32, textColor=INK)


def draw_para(c, text, x, y, width, pstyle, gap=0):
    p = Paragraph(text, pstyle)
    _, h = p.wrap(width, PAGE_H)
    p.drawOn(c, x, y - h)
    return y - h - gap


def draw_rule(c, x, y, width, color=LIGHT, thickness=0.7):
    c.setStrokeColor(color)
    c.setLineWidth(thickness)
    c.line(x, y, x + width, y)


def draw_bullets(c, bullets, x, y, width, font_size=8.6, leading=11.7, gap=3.5):
    bullet_style = style('Bullet', fontSize=font_size, leading=leading, textColor=MUTED, leftIndent=12, firstLineIndent=-8)
    for item in bullets:
        y = draw_para(c, f'•  {item}', x, y, width, bullet_style, gap=gap)
    return y


def draw_sidebar_list(c, items, x, y, width, gap=5.2):
    item_style = style('SidebarItem', fontSize=7.9, leading=10.4, textColor=MUTED, leftIndent=9, firstLineIndent=-7)
    for item in items:
        y = draw_para(c, f'<font color="#1769D1">•</font>  {item}', x, y, width, item_style, gap=gap)
    return y


def draw_sidebar_link(c, label, url, x, y, width):
    link_style = style('SidebarLink', fontName='Montserrat-Medium', fontSize=8.1, leading=10.5, textColor=BLUE)
    p = Paragraph(f'<u><b>{label}</b></u>', link_style)
    _, h = p.wrap(width, PAGE_H)
    p.drawOn(c, x, y - h)
    c.linkURL(url, (x, y - h, x + width, y), relative=0)
    return y - h - 5.5


def draw_sidebar_links_inline(c, x, y):
    font_name = 'Montserrat-Medium'
    font_size = 7.4
    rows = [
        [('LinkedIn', 'https://www.linkedin.com/in/arashdma/'), ('Portfolio', 'https://arashdma.github.io/Arashdma-Portfolio/')],
        [('Medium', 'https://medium.com/@Arashdma'), ('Dribbble', 'https://dribbble.com/Arashdma')],
    ]
    c.setFont(font_name, font_size)
    for row in rows:
        baseline = y - 8
        cursor = x
        for index, (label, url) in enumerate(row):
            c.setFillColor(BLUE)
            c.drawString(cursor, baseline, label)
            label_width = pdfmetrics.stringWidth(label, font_name, font_size)
            c.setStrokeColor(BLUE)
            c.setLineWidth(0.6)
            c.line(cursor, baseline - 1.5, cursor + label_width, baseline - 1.5)
            c.linkURL(url, (cursor, baseline - 3, cursor + label_width, baseline + 7), relative=0)
            cursor += label_width
            if index < len(row) - 1:
                c.setFillColor(MUTED)
                c.drawString(cursor + 7, baseline, '·')
                cursor += 16
        y = baseline - 8
    return y


def draw_job(c, x, y, width, company, subtitle, roles, intro, bullets, gap_after=12):
    y = draw_para(c, f'<b>{company}</b> <font color="#60656B">— {subtitle}</font>', x, y, width, COMPANY, gap=4)
    for role, dates in roles:
        y = draw_para(c, f'<b>{role}</b> <font color="#60656B">| <i>{dates}</i></font>', x, y, width, ROLE, gap=0)
    if intro:
        y -= 5
        y = draw_para(c, intro, x, y, width, BODY, gap=5)
    y = draw_bullets(c, bullets, x, y, width)
    return y - gap_after


def draw_sidebar(c, x, y, width, page_num):
    y = draw_para(c, 'CORE STRENGTHS', x, y, width, SIDEBAR_HEAD, gap=7)
    strengths = [
        'Product discovery & problem framing',
        'UX research & product analytics',
        'Interaction & interface design',
        'Design systems & scalable UI',
        'Prototyping & usability testing',
        'AI-assisted prototyping & vibe coding',
        'Product strategy & prioritization',
        'Cross-functional leadership & mentoring',
    ]
    y = draw_sidebar_list(c, strengths, x, y, width, gap=4.5)
    y -= 8

    y = draw_para(c, 'TOOLS', x, y, width, SIDEBAR_HEAD, gap=7)
    y = draw_para(c, '<b>Design</b><br/>Figma · FigJam · Sketch · Adobe XD<br/><br/><b>Analytics</b><br/>Google Analytics<br/><br/><b>AI workflows</b><br/>Claude · Codex · Cursor', x, y, width, SMALL, gap=12)

    y = draw_para(c, 'EDUCATION', x, y, width, SIDEBAR_HEAD, gap=7)
    y = draw_para(c, '<b>Azad University</b><br/>B.A. Industrial &amp; Product Design<br/><font color="#1769D1"><b>2025</b></font>', x, y, width, SMALL, gap=12)

    y = draw_para(c, 'LANGUAGES', x, y, width, SIDEBAR_HEAD, gap=7)
    y = draw_para(c, '<b>Persian</b> · Native<br/><b>English</b> · Professional working proficiency', x, y, width, SMALL, gap=12)

    y = draw_para(c, 'CONNECT', x, y, width, SIDEBAR_HEAD, gap=7)
    draw_sidebar_links_inline(c, x, y)

    c.setFillColor(MUTED)
    c.setFont('Inter', 7.4)
    c.drawRightString(PAGE_W - MARGIN_X, 22, f'{page_num} / 2')


def build():
    c = Canvas(str(OUT), pagesize=letter)
    c.setTitle('Arash DamanAfshan - Senior Product Designer')
    c.setAuthor('Arash DamanAfshan')

    # Page 1
    c.setFillColor(INK)
    c.setFont('Montserrat-Bold', 30)
    c.drawString(MARGIN_X, PAGE_H - TOP - 28, 'Arash DamanAfshan')
    c.setFillColor(BLUE)
    c.setFont('Montserrat-SemiBold', 11)
    c.drawString(MARGIN_X, PAGE_H - TOP - 51, 'SENIOR PRODUCT DESIGNER')

    c.setFillColor(INK)
    c.setFont('Inter', 8.6)
    c.drawRightString(PAGE_W - MARGIN_X, PAGE_H - TOP - 17, 'Tehran, Iran')
    c.drawRightString(PAGE_W - MARGIN_X, PAGE_H - TOP - 31, '+98 936 618 3493')
    c.drawRightString(PAGE_W - MARGIN_X, PAGE_H - TOP - 45, 'arashdma@gmail.com')
    c.setFillColor(BLUE)
    c.drawRightString(PAGE_W - MARGIN_X, PAGE_H - TOP - 59, 'linkedin.com/in/arashdma')

    rule_y = PAGE_H - TOP - 76
    draw_rule(c, MARGIN_X, rule_y, PAGE_W - (2 * MARGIN_X), color=BLUE, thickness=1.2)
    y = rule_y - 18
    y = draw_para(c, 'Senior Product Designer at Football360, focused on turning complex product problems into clear, intuitive digital experiences. I work across discovery, UX research, interaction design, and design systems, partnering closely with product and engineering teams to build products that are easier to understand and use.', MARGIN_X, y, PAGE_W - (2 * MARGIN_X), SUMMARY, gap=20)

    content_w = 365
    sidebar_x = 438
    sidebar_w = PAGE_W - MARGIN_X - sidebar_x
    # Start the sidebar below the summary so it never competes with the intro copy.
    draw_sidebar(c, sidebar_x, y, sidebar_w, 1)

    y = draw_para(c, 'EXPERIENCE', MARGIN_X, y, content_w, SECTION, gap=14)
    y = draw_job(
        c, MARGIN_X, y, content_w,
        'Football360', 'Iran\'s leading football app',
        [('Senior Product Designer (Part-time)', 'Nov 2023 - Present'), ('Senior Product Designer (Full-time)', 'Nov 2022 - Nov 2023')],
        'Sole product designer, owning the end-to-end design of the product across web, Android, and iOS.',
        [
            'Led a full product redesign from discovery through delivery, including the design system, CMS, and Football Fantasy.',
            'Design new features end-to-end, from framing the problem and exploring flows to prototyping, handoff, and iteration.',
            'Redesigned onboarding, contributing to a <b>40% reduction in drop-off</b>.',
            'Designed Sarzarb, which became the third most visited feature within three months, reaching <b>20M+ monthly visits</b>.',
            'Contributed to a product redesign that increased users by <b>475%</b>.',
        ], gap_after=15,
    )

    y = draw_job(
        c, MARGIN_X, y, content_w,
        'Hamsaa', 'Tech company & venture studio',
        [('Product Design Lead (Full-time)', 'Mar 2025 - Jul 2026'), ('Design Advisor (Consulting)', 'Dec 2022 - Mar 2025'), ('Senior Product Designer (Full-time)', 'Nov 2021 - Nov 2022')],
        'Worked across Ubank, Ham-Gozar, and Hamsaa Enterprise Social Network, leading design direction across discovery, product decisions, and cross-functional delivery.',
        [
            'Designed an automated solution that streamlined workflows and reduced support overhead by <b>50%</b>.',
            'Led design and workflow orchestration for Ubank, contributing to <b>40% of offline VIP users moving online within three months</b> and an NPS increase from <b>4.3 to 4.7</b>.',
            'Defined product strategy and led end-to-end discovery for Ham-Gozar, a commercial-complex management ecosystem spanning Admin, Tenant, and Contractor apps.',
            'Led delivery and sprint planning across four concurrent products, translating complex business requirements into scalable design architectures and backlogs.',
        ], gap_after=0,
    )
    c.showPage()

    # Page 2
    c.setFillColor(INK)
    c.setFont('Montserrat-Bold', 18)
    c.drawString(MARGIN_X, PAGE_H - TOP - 4, 'Arash DamanAfshan')
    c.setFillColor(BLUE)
    c.setFont('Montserrat-SemiBold', 9)
    c.drawString(MARGIN_X, PAGE_H - TOP - 21, 'SENIOR PRODUCT DESIGNER')
    draw_rule(c, MARGIN_X, PAGE_H - TOP - 38, PAGE_W - (2 * MARGIN_X), color=LIGHT, thickness=0.8)

    content_y = PAGE_H - TOP - 58
    content_w = PAGE_W - (2 * MARGIN_X)

    y = draw_para(c, 'EXPERIENCE (CONTINUED)', MARGIN_X, content_y, content_w, SECTION, gap=14)
    y = draw_job(
        c, MARGIN_X, y, content_w,
        'Asroon / Ahangar', 'Metal marketplace',
        [('Senior Product Designer', 'Dec 2020 - Feb 2022')],
        'Owned design outcomes across the marketplace and internal operations, from discovery and UX through interface design and post-launch analysis.',
        [
            'Redesigned the product-list page, contributing to a conversion-rate increase from approximately <b>0.8-1% to 2%</b>.',
            'Redesigned internal flows and helped shape a web-based CRM, contributing to a <b>20% decrease in order-submission time</b>.',
            'Worked directly with the CPO and CTO on product structure, design sprints, and a scalable UI foundation.',
        ], gap_after=17,
    )

    y = draw_job(
        c, MARGIN_X, y, content_w,
        'UniPlato', 'CPaaS collaboration platform',
        [('Product Designer', 'Mar 2020 - Aug 2021')],
        '',
        [
            'Applied quantitative analysis, design thinking, decision documentation, and feedback sessions while creating a scalable Material 2.0-based design system.',
        ], gap_after=17,
    )

    y = draw_job(
        c, MARGIN_X, y, content_w,
        'Purple Hachure', 'Design & creative studio',
        [('UI/UX Designer', 'Feb 2017 - Jan 2020')],
        'Designed digital products, brands, and campaigns for clients across fintech, e-commerce, health, and communications, including Jibimo, Pipekala, Sharjbook, Paklean, and Tinext.',
        [], gap_after=18,
    )

    y = draw_para(c, 'WORKING STYLE', MARGIN_X, y, content_w, SECTION, gap=14)
    draw_para(c, '<b>Problem-first and collaborative:</b> I work closely with product and engineering teams to turn ambiguous problems into clear flows, scalable systems, and shippable experiences.', MARGIN_X, y, content_w, BODY_DARK, gap=0)

    c.setFillColor(MUTED)
    c.setFont('Inter', 7.4)
    c.drawRightString(PAGE_W - MARGIN_X, 22, '2 / 2')

    c.showPage()
    c.save()


if __name__ == '__main__':
    build()
