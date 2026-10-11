#!/usr/bin/env python3
"""Fix text/content overflow in blog article pages.

Root cause: the article body uses a CSS grid `280px 1fr`. In CSS Grid, `1fr`
expands to `minmax(auto, 1fr)`, so a wide grid item (MathJax display math,
mermaid diagram, reference table, long unbreakable string) forces the track to
grow beyond the viewport -> horizontal overflow / text running off the page.

Fix: give the flexible track `minmax(0, 1fr)`, add `min-width: 0` to the
content column, and add targeted overflow guards for math, mermaid, tables and
long tokens. Applied idempotently to every article + the template.
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
FILES = sorted([f for f in os.listdir(HERE)
                if re.match(r'0\d-.*\.html$', f)] + ['template.html'])

GUARD_MARKER = '/* === overflow-guard === */'

GUARD_CSS = GUARD_MARKER + '''
        /* --- grid overflow fix: allow the flexible column to shrink --- */
        .container { grid-template-columns: 280px minmax(0, 1fr); }
        .content { min-width: 0; max-width: 100%; overflow-wrap: break-word; }
        .content * { min-width: 0; }
        /* long unbreakable strings (ids, urls, formulas-as-text) wrap instead of overflowing */
        .content p, .content li, .content td, .content blockquote, .content .callout {
            overflow-wrap: break-word; word-break: break-word; hyphens: auto;
        }
        /* MathJax display math scrolls horizontally instead of breaking layout */
        .content mjx-container[display="true"] { overflow-x: auto; overflow-y: hidden; max-width: 100%; }
        mjx-container { max-width: 100%; }
        /* mermaid / figures / svg never exceed the column */
        .mermaid { overflow-x: auto; max-width: 100%; }
        figure, .svg-container { max-width: 100%; }
        figure svg, .svg-container svg { max-width: 100%; height: auto; }
        img { max-width: 100%; height: auto; }
        /* tables wrap / scroll */
        .content table { display: block; max-width: 100%; overflow-x: auto; }
        table.ref-table td { overflow-wrap: break-word; word-break: break-word; }
        /* code blocks scroll */
        .content pre { overflow-x: auto; max-width: 100%; }
        .content code { overflow-wrap: break-word; word-break: break-word; }
        /* === /overflow-guard === */'''

def add_guard(css):
    """Append the guard block just before the closing </style> (inside style)."""
    return css + '\n' + GUARD_CSS + '\n'

def process(path):
    with open(path, encoding='utf-8') as f:
        html = f.read()
    if GUARD_MARKER in html:
        return 'skip (already patched)'

    orig = html

    # 1. make the flexible grid track shrinkable (belt-and-suspenders; the
    #    guard CSS also re-declares it, but fix the source rule too).
    html = html.replace(
        'grid-template-columns: 280px 1fr;',
        'grid-template-columns: 280px minmax(0, 1fr);')

    # 2. inject the guard CSS right before the FIRST </style> that belongs to
    #    the article head (the <style> in <head>). We insert before '</style>'.
    idx = html.find('</style>')
    if idx == -1:
        return 'ERROR: no </style> found'
    html = html[:idx] + GUARD_CSS + '\n    ' + html[idx:]

    if html != orig:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(html)
        return 'patched'
    return 'no-change'

def main():
    for fn in FILES:
        p = os.path.join(HERE, fn)
        if not os.path.exists(p):
            print(f'  - {fn}: MISSING')
            continue
        try:
            print(f'  - {fn}: {process(p)}')
        except Exception as e:
            print(f'  - {fn}: ERROR {e}')

if __name__ == '__main__':
    main()
