#!/usr/bin/env python3
"""Generate reports hub with featured today's digest + collapsible archive.

Outputs:
  - index.html   (hero today's reports w/ big digest + archive grouped by date)
  - rss.xml      (RSS 2.0)
  - index.json   (full machine-readable index incl. digest text)
  - latest.json  (latest of each series incl. digest text)

Digests are extracted programmatically from the report HTML files
(.summary-banner overview + .insights editor's note) — no LLM needed.
"""
import os, re, json, html as html_mod
from datetime import datetime, timezone
from email.utils import format_datetime

BASE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(BASE)
PAPERS_DIR = os.path.join(BASE, 'papers')
MEDIA_DIR = os.path.join(BASE, 'media')
SITE = 'https://webdrag0n.github.io/reports'

# ── HTML text extraction ─────────────────────────────────────────────

def strip_tags(s):
    s = re.sub(r'<[^>]+>', '', s)
    return html_mod.unescape(s).strip()

def extract_section(content, cls):
    """Extract inner text of <div class="cls">...</div> (first match, non-nested)."""
    m = re.search(rf'<div class="{cls}">(.*?)</div>', content, re.S)
    if not m:
        return ''
    inner = m.group(1)
    inner = re.sub(r'<h3>.*?</h3>', '', inner, flags=re.S)  # drop heading
    return strip_tags(inner)

def extract_overview(content):
    """Extract .summary-banner text, stripping the '今日速览：' prefix."""
    txt = extract_section(content, 'summary-banner')
    txt = re.sub(r'^📌?\s*今日速览[：:]\s*', '', txt)
    return txt

def extract_digest(content):
    """Extract .insights (编辑点评) text."""
    return extract_section(content, 'insights')

def extract_title(content):
    m = re.search(r'<title>(.*?)</title>', content, re.S)
    return strip_tags(m.group(1)) if m else ''

# ── collect reports ──────────────────────────────────────────────────

def collect(d, prefix, subdir, series):
    items = []
    if not os.path.isdir(d):
        return items
    for f in sorted(os.listdir(d), reverse=True):
        m = re.match(rf'{prefix}_(\d{{8}})\.html', f)
        if not m:
            continue
        raw = m.group(1)
        path = os.path.join(d, f)
        try:
            with open(path, encoding='utf-8') as fh:
                content = fh.read()
        except OSError:
            continue
        items.append({
            'file': f,
            'url': f'{SITE}/{subdir}/{f}',
            'date': f'{raw[:4]}-{raw[4:6]}-{raw[6:8]}',
            'raw': raw,
            'series': series,
            'overview': extract_overview(content),
            'digest': extract_digest(content),
            'title': extract_title(content),
        })
    return items

papers = collect(PAPERS_DIR, 'daily_papers', 'papers', 'AI 论文速递')
media = collect(MEDIA_DIR, 'daily_media', 'media', 'AI 科技日报')

# merge & group by date (newest first)
by_date = {}
for it in papers + media:
    by_date.setdefault(it['raw'], {})[it['series']] = it
dates_sorted = sorted(by_date.keys(), reverse=True)
today_raw = dates_sorted[0] if dates_sorted else None

# ── HTML page ────────────────────────────────────────────────────────

def hero_card(it):
    icon = '🤖' if it['series'] == 'AI 论文速递' else '📡'
    digest_html = ''
    if it['digest']:
        digest_html = f'''
        <div class="hero-digest">
          <div class="hero-digest-label">📝 编辑点评</div>
          <p>{html_mod.escape(it['digest'])}</p>
        </div>'''
    overview_html = ''
    if it['overview']:
        overview_html = f'<p class="hero-overview">{html_mod.escape(it["overview"])}</p>'
    return f'''
      <article class="hero-card">
        <div class="hero-card-head">
          <span class="hero-icon">{icon}</span>
          <div>
            <h2 class="hero-title"><a href="{it['series'] == 'AI 论文速递' and 'papers' or 'media'}/{it['file']}">{it['series']}</a></h2>
            <span class="hero-date">{it['date']}</span>
          </div>
          <a class="hero-open" href="{it['series'] == 'AI 论文速递' and 'papers' or 'media'}/{it['file']}">阅读全文 &rarr;</a>
        </div>
        {overview_html}
        {digest_html}
      </article>'''

def archive_item(it):
    icon = '🤖' if it['series'] == 'AI 论文速递' else '📡'
    subdir = 'papers' if it['series'] == 'AI 论文速递' else 'media'
    inner = ''
    if it['digest']:
        inner += f'''
          <div class="arc-digest">
            <span class="arc-digest-label">编辑点评</span>
            <p>{html_mod.escape(it['digest'])}</p>
          </div>'''
    if it['overview']:
        inner += f'''
          <div class="arc-overview">
            <span class="arc-digest-label">速览</span>
            <p>{html_mod.escape(it['overview'])}</p>
          </div>'''
    if not inner:
        inner = '<p class="arc-nodigest">（该日报无可提取的摘要，点击查看全文）</p>'
    return f'''
          <details class="arc-report">
            <summary>
              <span class="arc-icon">{icon}</span>
              <span class="arc-series">{it['series']}</span>
              <span class="arc-chev">▸</span>
            </summary>
            <div class="arc-body">
              {inner}
              <a class="arc-full" href="{subdir}/{it['file']}">阅读全文 &rarr;</a>
            </div>
          </details>'''

# hero: today's reports
hero_html = ''
if today_raw:
    day = by_date[today_raw]
    cards = ''.join(hero_card(it) for it in day.values())
    d = day[list(day.keys())[0]]['date']
    hero_html = f'''
    <section class="hero">
      <div class="hero-head">
        <h1>🔭 今日日报</h1>
        <span class="hero-badge">{d}</span>
      </div>
      {cards}
    </section>'''

# archive: all days (including today), collapsible per day, newest first
archive_days = []
for raw in dates_sorted:
    day = by_date[raw]
    d = day[list(day.keys())[0]]['date']
    n = len(day)
    items_html = ''.join(archive_item(it) for it in day.values())
    open_attr = ' open' if raw == today_raw else ''
    archive_days.append(f'''
      <details class="arc-day"{open_attr}>
        <summary class="arc-day-summary">
          <span class="arc-day-date">📅 {d}</span>
          <span class="arc-day-count">{n} 篇</span>
          <span class="arc-chev">▸</span>
        </summary>
        {items_html}
      </details>''')
archive_html = '\n'.join(archive_days)

page = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Daily | Lin Zexin</title>
    <meta name="description" content="Daily AI paper digests and Chinese AI media roundups.">
    <link rel="alternate" type="application/rss+xml" title="AI Daily RSS" href="rss.xml">
    <link rel="stylesheet" href="../css/style.css">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    <link rel="icon" href="../assets/topBarIcon.png" />
    <style>
        :root {{
            --ad-bg: #f6f7f9; --ad-card: #ffffff; --ad-text: #1f2328;
            --ad-sub: #656d76; --ad-accent: #0969da; --ad-border: #d8dee4;
            --ad-digest-bg: #fff8e6; --ad-digest-border: #f0d48a;
        }}
        @media (prefers-color-scheme: dark) {{
            :root {{
                --ad-bg: #0d1117; --ad-card: #161b22; --ad-text: #e6edf3;
                --ad-sub: #8b949e; --ad-accent: #58a6ff; --ad-border: #30363d;
                --ad-digest-bg: #2a2412; --ad-digest-border: #6b5a1e;
            }}
        }}
        body {{ background: var(--ad-bg); color: var(--ad-text); }}
        .ad-container {{ max-width: 860px; margin: 0 auto; padding: 110px 20px 80px;
            font-family: -apple-system, "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif; }}

        /* ── hero ── */
        .hero-head {{ display: flex; align-items: baseline; gap: 12px; margin-bottom: 18px; }}
        .hero-head h1 {{ font-size: 1.7rem; font-weight: 800; }}
        .hero-badge {{ font-size: .85rem; color: var(--ad-sub); font-family: monospace; }}
        .hero-card {{
            background: var(--ad-card); border: 1px solid var(--ad-border);
            border-radius: 14px; padding: 22px 26px; margin-bottom: 18px;
            box-shadow: 0 2px 10px rgba(0,0,0,.05);
        }}
        .hero-card-head {{ display: flex; align-items: center; gap: 12px; margin-bottom: 10px; }}
        .hero-icon {{ font-size: 1.6rem; }}
        .hero-title {{ font-size: 1.15rem; margin: 0; }}
        .hero-title a {{ color: var(--ad-text); text-decoration: none; }}
        .hero-title a:hover {{ color: var(--ad-accent); }}
        .hero-date {{ font-size: .8rem; color: var(--ad-sub); font-family: monospace; }}
        .hero-open {{ margin-left: auto; font-size: .85rem; color: var(--ad-accent);
            text-decoration: none; white-space: nowrap; }}
        .hero-open:hover {{ text-decoration: underline; }}
        .hero-overview {{ font-size: .95rem; color: var(--ad-sub); line-height: 1.75; margin: 6px 0 0; }}
        .hero-digest {{
            margin-top: 14px; background: var(--ad-digest-bg);
            border: 1px solid var(--ad-digest-border); border-radius: 10px;
            padding: 16px 18px;
        }}
        .hero-digest-label {{ font-size: .8rem; font-weight: 700; color: #9a6700; margin-bottom: 6px; }}
        @media (prefers-color-scheme: dark) {{ .hero-digest-label {{ color: #d4a72c; }} }}
        .hero-digest p {{ font-size: 1.02rem; line-height: 1.9; margin: 0; }}

        /* ── archive ── */
        .archive-head {{ display: flex; align-items: baseline; gap: 10px;
            margin: 46px 0 14px; }}
        .archive-head h2 {{ font-size: 1.25rem; font-weight: 700; }}
        .archive-head span {{ font-size: .8rem; color: var(--ad-sub); }}
        .arc-day {{
            background: var(--ad-card); border: 1px solid var(--ad-border);
            border-radius: 10px; margin-bottom: 10px; overflow: hidden;
        }}
        .arc-day-summary {{
            display: flex; align-items: center; gap: 10px;
            padding: 13px 18px; cursor: pointer; list-style: none;
            user-select: none; font-weight: 600;
        }}
        .arc-day-summary::-webkit-details-marker {{ display: none; }}
        .arc-day-summary:hover {{ background: rgba(127,127,127,.06); }}
        .arc-day-date {{ font-family: monospace; font-size: .95rem; }}
        .arc-day-count {{ margin-left: auto; font-size: .78rem; color: var(--ad-sub); font-weight: 400; }}
        .arc-chev {{ color: var(--ad-sub); transition: transform .18s; font-size: .8rem; }}
        details[open] > summary .arc-chev, details[open] > .arc-day-summary .arc-chev {{ transform: rotate(90deg); }}

        .arc-report {{ border-top: 1px solid var(--ad-border); }}
        .arc-report summary {{
            display: flex; align-items: center; gap: 10px;
            padding: 11px 18px 11px 30px; cursor: pointer; list-style: none;
            font-size: .92rem; user-select: none;
        }}
        .arc-report summary::-webkit-details-marker {{ display: none; }}
        .arc-report summary:hover {{ background: rgba(127,127,127,.06); }}
        .arc-icon {{ font-size: 1rem; }}
        .arc-series {{ font-weight: 500; }}
        .arc-body {{ padding: 4px 22px 16px 52px; }}
        .arc-digest, .arc-overview {{ margin-bottom: 10px; }}
        .arc-digest-label {{
            display: inline-block; font-size: .72rem; font-weight: 700;
            color: #9a6700; background: var(--ad-digest-bg);
            border: 1px solid var(--ad-digest-border);
            padding: 1px 8px; border-radius: 10px; margin-bottom: 5px;
        }}
        @media (prefers-color-scheme: dark) {{ .arc-digest-label {{ color: #d4a72c; }} }}
        .arc-digest p, .arc-overview p {{ font-size: .9rem; line-height: 1.8; color: var(--ad-text); margin: 4px 0 0; }}
        .arc-overview p {{ color: var(--ad-sub); }}
        .arc-nodigest {{ font-size: .85rem; color: var(--ad-sub); }}
        .arc-full {{ display: inline-block; margin-top: 4px; font-size: .85rem;
            color: var(--ad-accent); text-decoration: none; }}
        .arc-full:hover {{ text-decoration: underline; }}

        .ad-footer {{ text-align: center; margin-top: 50px; font-size: .8rem; color: var(--ad-sub); }}
        .ad-footer a {{ color: var(--ad-accent); text-decoration: none; }}
        .ad-footer a:hover {{ text-decoration: underline; }}
    </style>
</head>
<body>
    <nav class="top-nav">
        <div class="top-nav-inner">
            <a href="../index.html" class="top-nav-brand">LZX</a>
            <ul class="top-nav-links">
                <li><a href="../index.html" data-nav="home">Home</a></li>
                <li><a href="../about.html" data-nav="about">About</a></li>
                <li><a href="../blogs/index.html" data-nav="blog">Blog</a></li>
                <li><a href="../AI_ECA/ECA_main.html" data-nav="kb">Knowledge Base</a></li>
                <li><a href="index.html" class="active" data-nav="reports">AI Daily</a></li>
            </ul>
            <button id="lang-toggle" class="btn top-nav-lang">EN | 中</button>
        </div>
    </nav>

    <div class="ad-container">
        {hero_html}

        <div class="archive-head">
            <h2>🗂 往期归档</h2>
            <span>共 {len(dates_sorted)} 天 · 按日期从新到旧 · 点击展开</span>
        </div>
        <div class="archive">
            {archive_html}
        </div>

        <div class="ad-footer">
            <p>📡 <a href="rss.xml">RSS 订阅</a> · 🤖 Agent API: <a href="latest.json">latest.json</a> / <a href="index.json">index.json</a></p>
            <p>Auto-generated daily · digests extracted programmatically</p>
        </div>
    </div>

    <script src="../js/main.js"></script>
</body>
</html>
'''

with open(os.path.join(BASE, 'index.html'), 'w', encoding='utf-8') as f:
    f.write(page)

# ── RSS 2.0 ──────────────────────────────────────────────────────────

all_items = sorted(papers + media, key=lambda x: x['raw'], reverse=True)
rss_entries = []
for it in all_items:
    dt = datetime.strptime(it['raw'], '%Y%m%d').replace(hour=8, tzinfo=timezone.utc)
    desc = it['overview'] or it['title']
    rss_entries.append(f'''    <item>
      <title>{html_mod.escape(it['series'])} — {it['date']}</title>
      <link>{it['url']}</link>
      <guid isPermaLink="true">{it['url']}</guid>
      <pubDate>{format_datetime(dt)}</pubDate>
      <description>{html_mod.escape(desc[:300])}</description>
    </item>''')

rss = f'''<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
  <channel>
    <title>AI Daily — Lin Zexin</title>
    <link>{SITE}/</link>
    <description>Daily AI paper digests and Chinese AI media roundups.</description>
    <language>zh-cn</language>
    <lastBuildDate>{format_datetime(datetime.now(timezone.utc))}</lastBuildDate>
{chr(10).join(rss_entries)}
  </channel>
</rss>
'''
with open(os.path.join(BASE, 'rss.xml'), 'w', encoding='utf-8') as f:
    f.write(rss)

# ── JSON endpoints ───────────────────────────────────────────────────

def json_item(it):
    return {'date': it['date'], 'url': it['url'],
            'overview': it['overview'], 'digest': it['digest']}

idx = {
    'site': SITE,
    'generated_at': datetime.now(timezone.utc).isoformat(),
    'series': {
        'papers': {'title': 'AI 论文速递', 'count': len(papers),
                   'items': [json_item(it) for it in papers]},
        'media': {'title': 'AI 科技日报', 'count': len(media),
                  'items': [json_item(it) for it in media]},
    }
}
with open(os.path.join(BASE, 'index.json'), 'w', encoding='utf-8') as f:
    json.dump(idx, f, indent=2, ensure_ascii=False)

latest = {
    'generated_at': datetime.now(timezone.utc).isoformat(),
    'papers': json_item(papers[0]) if papers else None,
    'media': json_item(media[0]) if media else None,
}
with open(os.path.join(BASE, 'latest.json'), 'w', encoding='utf-8') as f:
    json.dump(latest, f, indent=2, ensure_ascii=False)

n_digest = sum(1 for it in all_items if it['digest'])
print(f'✅ index.html (hero + archive, {len(dates_sorted)} days)')
print(f'   papers: {len(papers)}  media: {len(media)}  digests extracted: {n_digest}/{len(all_items)}')
print('   rss.xml · index.json · latest.json also written')
