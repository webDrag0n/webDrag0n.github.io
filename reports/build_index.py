#!/usr/bin/env python3
"""Scan reports/ and generate:
  - reports/index.html  (human-readable hub)
  - reports/rss.xml     (RSS 2.0 feed for both series)
  - reports/index.json  (machine-readable full index)
  - reports/latest.json (latest entry of each series, for agents)
"""
import os, re, json
from datetime import datetime, timezone
from email.utils import format_datetime

BASE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(BASE)
PAPERS_DIR = os.path.join(BASE, 'papers')
MEDIA_DIR = os.path.join(BASE, 'media')
SITE = 'https://webdrag0n.github.io/reports'

def collect(d, prefix):
    items = []
    if not os.path.isdir(d):
        return items
    for f in sorted(os.listdir(d), reverse=True):
        m = re.match(rf'{prefix}_(\d{{8}})\.html', f)
        if m:
            date = m.group(1)
            items.append({
                'file': f,
                'date': f'{date[:4]}-{date[4:6]}-{date[6:8]}',
                'raw': date,
            })
    return items

papers = collect(PAPERS_DIR, 'daily_papers')
media = collect(MEDIA_DIR, 'daily_media')

def rows(items, subdir):
    out = []
    for it in items:
        out.append(f'''        <a class="report-card" href="{subdir}/{it['file']}">
          <span class="report-date">{it['date']}</span>
          <span class="report-arrow">&rarr;</span>
        </a>''')
    return '\n'.join(out)

papers_html = rows(papers, 'papers')
media_html = rows(media, 'media')

html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Daily | Lin Zexin</title>
    <meta name="description" content="Daily AI paper digests and Chinese AI media roundups.">
    <link rel="stylesheet" href="../css/style.css">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    <link rel="icon" href="../assets/topBarIcon.png" />
    <style>
        body {{ background: var(--bg, #0a192f); color: var(--text, #ccd6f6); }}
        .reports-container {{ max-width: 800px; margin: 0 auto; padding: 120px 24px 60px; }}
        .reports-header {{ text-align: center; margin-bottom: 48px; }}
        .reports-header h1 {{ font-size: 2rem; font-weight: 700; margin-bottom: 8px; }}
        .reports-header p {{ color: var(--text-secondary, #8892b0); }}
        .section-title {{ font-size: 1.25rem; font-weight: 600; margin: 40px 0 16px; padding-bottom: 8px; border-bottom: 1px solid var(--border, #233554); }}
        .report-grid {{ display: flex; flex-direction: column; gap: 8px; }}
        .report-card {{
            display: flex; justify-content: space-between; align-items: center;
            padding: 14px 18px; border-radius: 8px;
            background: var(--card-bg, #112240); border: 1px solid var(--border, #233554);
            text-decoration: none; color: inherit; transition: transform .15s, box-shadow .15s;
        }}
        .report-card:hover {{ transform: translateY(-2px); box-shadow: 0 4px 16px rgba(0,0,0,.3); }}
        .report-date {{ font-family: 'SF Mono', 'Fira Code', monospace; font-size: 0.9rem; }}
        .report-arrow {{ color: var(--accent, #64ffda); }}
        .empty-msg {{ color: var(--text-secondary, #8892b0); padding: 16px 0; }}
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

    <div class="reports-container">
        <div class="reports-header">
            <h1>&#128302; AI Daily</h1>
            <p>Daily AI paper digests &amp; Chinese AI media roundups, auto-generated.</p>
        </div>

        <h2 class="section-title">&#129302; AI Paper Digest</h2>
        <div class="report-grid" id="papers-grid">
{papers_html if papers_html else '            <p class="empty-msg">No reports yet.</p>'}
        </div>

        <h2 class="section-title">&#128225; AI Media Daily</h2>
        <div class="report-grid" id="media-grid">
{media_html if media_html else '            <p class="empty-msg">No reports yet.</p>'}
        </div>
    </div>

    <script src="../js/main.js"></script>
</body>
</html>
'''

out = os.path.join(BASE, 'index.html')
with open(out, 'w', encoding='utf-8') as f:
    f.write(html)

# ── RSS 2.0 ──────────────────────────────────────────────────────────
def rss_items(items, subdir, series_title):
    rows = []
    for it in items:
        dt = datetime.strptime(it['raw'], '%Y%m%d').replace(hour=8, tzinfo=timezone.utc)
        url = f"{SITE}/{subdir}/{it['file']}"
        rows.append(f'''    <item>
      <title>{series_title} — {it['date']}</title>
      <link>{url}</link>
      <guid isPermaLink="true">{url}</guid>
      <pubDate>{format_datetime(dt)}</pubDate>
      <description>{series_title} for {it['date']}</description>
    </item>''')
    return '\n'.join(rows)

all_items = []
for it in papers: all_items.append(('papers', it))
for it in media:  all_items.append(('media', it))
all_items.sort(key=lambda x: x[1]['raw'], reverse=True)

rss_entries = []
for subdir, it in all_items:
    title = 'AI Paper Digest' if subdir == 'papers' else 'AI Media Daily'
    dt = datetime.strptime(it['raw'], '%Y%m%d').replace(hour=8, tzinfo=timezone.utc)
    url = f"{SITE}/{subdir}/{it['file']}"
    rss_entries.append(f'''    <item>
      <title>{title} — {it['date']}</title>
      <link>{url}</link>
      <guid isPermaLink="true">{url}</guid>
      <pubDate>{format_datetime(dt)}</pubDate>
      <description>{title} for {it['date']}</description>
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

# ── JSON index (for agents) ─────────────────────────────────────────
idx = {
    'site': SITE,
    'generated_at': datetime.now(timezone.utc).isoformat(),
    'series': {
        'papers': {'title': 'AI Paper Digest', 'url_prefix': f'{SITE}/papers/', 'count': len(papers),
                   'items': [{'date': it['date'], 'url': f'{SITE}/papers/{it["file"]}'} for it in papers]},
        'media':  {'title': 'AI Media Daily', 'url_prefix': f'{SITE}/media/', 'count': len(media),
                   'items': [{'date': it['date'], 'url': f'{SITE}/media/{it["file"]}'} for it in media]},
    }
}
with open(os.path.join(BASE, 'index.json'), 'w', encoding='utf-8') as f:
    json.dump(idx, f, indent=2, ensure_ascii=False)

# ── latest.json (quick poll endpoint) ────────────────────────────────
latest = {
    'generated_at': datetime.now(timezone.utc).isoformat(),
    'papers': {'date': papers[0]['date'], 'url': f'{SITE}/papers/{papers[0]["file"]}'} if papers else None,
    'media':  {'date': media[0]['date'],  'url': f'{SITE}/media/{media[0]["file"]}'}  if media  else None,
}
with open(os.path.join(BASE, 'latest.json'), 'w', encoding='utf-8') as f:
    json.dump(latest, f, indent=2, ensure_ascii=False)

print(f'✅ Generated {out}')
print(f'   papers: {len(papers)}  media: {len(media)}')
print(f'   rss.xml · index.json · latest.json also written')
