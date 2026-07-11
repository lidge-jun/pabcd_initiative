#!/usr/bin/env python3
"""
PABCD Initiative docs-site static builder.
Reads source .md files from the pabcd_initiative repo and generates HTML pages
with a shared sidebar layout. No framework — just string templates.
"""

import os, re, json, html as htmlmod, textwrap
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent  # pabcd_initiative/
SITE = ROOT / "docs-site"
PAGES = SITE / "pages"
SKILLS_DIR = ROOT / "skills"
DEVLOG_DIR = ROOT / "devlog"
BACKLOG_DIR = ROOT / "backlog"
REFS_DIR = ROOT / "skills" / "dev-pabcd" / "references"

# ---- helpers ----

def read_md(path):
    """Read a markdown file, strip YAML frontmatter, return (title, body)."""
    text = path.read_text(encoding="utf-8")
    # strip frontmatter
    if text.startswith("---"):
        end = text.find("---", 3)
        if end > 0:
            text = text[end+3:].strip()
    # extract first heading as title
    m = re.match(r"^#\s+(.+)", text, re.M)
    title = m.group(1).strip() if m else path.stem
    return title, text

def md_to_html_simple(md):
    """Minimal markdown -> HTML. Handles headings, paragraphs, bold, code, links, lists."""
    lines = md.split("\n")
    out = []
    list_stack = []  # stack of 'ul' or 'ol'
    in_code = False
    code_buf = []
    
    for line in lines:
        # fenced code blocks
        if line.strip().startswith("```"):
            if in_code:
                out.append("<pre><code>" + htmlmod.escape("\n".join(code_buf)) + "</code></pre>")
                code_buf = []
                in_code = False
            else:
                in_code = True
            continue
        if in_code:
            code_buf.append(line)
            continue
        
        stripped = line.strip()
        
        # headings
        hm = re.match(r"^(#{1,4})\s+(.+)", stripped)
        if hm:
            while list_stack:
                out.append(f"</{list_stack.pop()}>")
            level = len(hm.group(1)) + 1  # h2-h5
            if level > 5: level = 5
            hid = re.sub(r"[^a-z0-9]+", "-", hm.group(2).lower()).strip("-")
            out.append(f'<h{level} id="{hid}">{inline_fmt(hm.group(2))}</h{level}>')
            continue
        
        # detect indent level (2 spaces per level)
        indent = len(line) - len(line.lstrip())
        target_depth = indent // 2 + 1 if indent > 0 else 1
        
        # unordered list items
        lm = re.match(r"^(\s*)[-*]\s+(.+)", line)
        if lm:
            # close deeper lists
            while len(list_stack) > target_depth:
                out.append(f"</{list_stack.pop()}>")
            # open lists to reach target depth
            while len(list_stack) < target_depth:
                out.append("<ul>")
                list_stack.append("ul")
            # if current level is an ol, close it and open ul
            if list_stack and list_stack[-1] != "ul":
                out.append(f"</{list_stack.pop()}>")
                out.append("<ul>")
                list_stack.append("ul")
            out.append(f"<li>{inline_fmt(lm.group(2))}</li>")
            continue
        
        # ordered list items
        nm = re.match(r"^(\s*)\d+\.\s+(.+)", line)
        if nm:
            # close deeper lists
            while len(list_stack) > target_depth:
                out.append(f"</{list_stack.pop()}>")
            # open lists to reach target depth
            while len(list_stack) < target_depth:
                out.append("<ol>")
                list_stack.append("ol")
            # if current level is a ul, close it and open ol
            if list_stack and list_stack[-1] != "ol":
                out.append(f"</{list_stack.pop()}>")
                out.append("<ol>")
                list_stack.append("ol")
            out.append(f"<li>{inline_fmt(nm.group(2))}</li>")
            continue
        
        if list_stack and not stripped:
            while list_stack:
                out.append(f"</{list_stack.pop()}>")
            continue
        
        # table rows (simple)
        if stripped.startswith("|") and stripped.endswith("|"):
            if "---" in stripped:
                continue  # separator row
            cells = [c.strip() for c in stripped.split("|")[1:-1]]
            tag = "th" if not any("<td>" in o for o in out[-3:] if "<t" in o) else "td"
            # detect header row
            row = "<tr>" + "".join(f"<{tag}>{inline_fmt(c)}</{tag}>" for c in cells) + "</tr>"
            if out and "</table>" not in out[-1] and "<table" not in str(out[-5:]):
                out.append('<table class="rules"><tbody>')
            out.append(row)
            continue
        
        # blank line: close table if open
        if not stripped:
            if out and "<tr>" in str(out[-1]):
                out.append("</tbody></table>")
            continue
        
        # paragraph
        while list_stack:
            out.append(f"</{list_stack.pop()}>")
        out.append(f"<p>{inline_fmt(stripped)}</p>")
    
    while list_stack:
        out.append(f"</{list_stack.pop()}>")
    if in_code:
        out.append("<pre><code>" + htmlmod.escape("\n".join(code_buf)) + "</code></pre>")
    
    return "\n".join(out)

def inline_fmt(text):
    """Inline formatting: bold, code, links."""
    text = htmlmod.escape(text)
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"`(.+?)`", r"<code>\1</code>", text)
    # links [text](url)
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', text)
    return text


# ---- navigation structure ----

NAV = [
    ("Overview", [
        ("Introduction", "index.html"),
        ("Origin Story", "pages/origin.html"),
    ]),
    ("Methodology", [
        ("Skill Architecture", "pages/skills.html"),
        ("Delegation Economy", "pages/delegation.html"),
        ("Loop Contract", "pages/loop.html"),
    ]),
    ("Skills Reference", []),  # filled dynamically
    ("Dev Guides", []),  # filled from references
    ("Devlog", []),  # filled dynamically
    ("Backlog", []),  # filled dynamically
    ("References", [
        ("arXiv Claim Ledger", "index.html#references"),
    ]),
]


def build_sidebar_html(current_page, base=""):
    """Generate sidebar HTML for a page."""
    parts = []
    parts.append('<nav class="sidebar" id="sidebar">')
    parts.append(f'<div class="sidebar-brand"><a href="{base}index.html">PA<span class="sq"></span><br>BCD</a></div>')
    parts.append('<div class="sidebar-search"><input type="text" id="docs-search" placeholder="Search docs..." autocomplete="off"><ul id="search-results" class="search-results"></ul></div>')
    
    for group_name, items in NAV:
        if not items:
            continue
        collapsed = "" 
        parts.append(f'<div class="nav-group {collapsed}">')
        parts.append(f'<button class="nav-group-label">{group_name} <span class="chevron">&#9660;</span></button>')
        parts.append('<ul class="nav-items">')
        for title, href in items:
            full_href = base + href
            active = "active" if href == current_page else ""
            parts.append(f'<li><a href="{full_href}" class="{active}">{title}</a></li>')
        parts.append('</ul></div>')
    
    parts.append('</nav>')
    return "\n".join(parts)


def doc_page_html(title, body_html, current_page, base="", prev_link=None, next_link=None):
    """Wrap content in the docs shell template."""
    sidebar = build_sidebar_html(current_page, base)
    
    nav_footer = ""
    if prev_link or next_link:
        nav_footer = '<nav class="page-nav">'
        if prev_link:
            nav_footer += f'<a href="{base}{prev_link[1]}">&larr; {prev_link[0]}</a>'
        else:
            nav_footer += '<span></span>'
        if next_link:
            nav_footer += f'<a href="{base}{next_link[1]}">{next_link[0]} &rarr;</a>'
        nav_footer += '</nav>'
    
    return f'''<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{htmlmod.escape(title)} — PABCD Initiative</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo:wght@500;700;800;900&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/variable/pretendardvariable-dynamic-subset.min.css">
<link rel="stylesheet" href="{base}assets/site.css?v=4">
<link rel="stylesheet" href="{base}assets/docs.css?v=1">
</head>
<body>

<header class="meta-bar">
  <a href="{base}index.html" style="text-decoration:none;color:inherit"><span>PABCD Initiative</span></a>
  <span class="hide-m grow">Documentation Hub</span>
  <span class="right">2026-07-11</span>
</header>

<div class="docs-shell">
{sidebar}
<div class="sidebar-overlay" id="sidebar-overlay"></div>
<main class="docs-content">
<section class="page-head">
  <div class="band-inner">
    <h1>{htmlmod.escape(title)}</h1>
  </div>
</section>
<section class="page-body">
  <div class="band-inner">
{body_html}
  </div>
</section>
{nav_footer}
</main>
</div>

<button class="sidebar-toggle" id="sidebar-toggle" aria-label="Toggle sidebar">&#9776;</button>
<script src="{base}assets/search-index.js"></script>
<script src="{base}assets/docs.js"></script>
</body>
</html>'''


# ---- build skills pages ----

def build_skill_pages():
    """Generate HTML pages for each skill."""
    skills_out = PAGES / "skills"
    skills_out.mkdir(parents=True, exist_ok=True)
    
    entries = []
    skill_dirs = sorted(SKILLS_DIR.iterdir())
    for sd in skill_dirs:
        skill_md = sd / "SKILL.md"
        if not skill_md.exists():
            continue
        
        title, body = read_md(skill_md)
        # use skill name from directory
        skill_name = sd.name
        page_file = f"pages/skills/{skill_name}.html"
        
        body_html = md_to_html_simple(body)
        
        # add references if they exist
        refs_dir = sd / "references"
        if refs_dir.is_dir():
            ref_links = []
            for rf in sorted(refs_dir.iterdir()):
                if rf.suffix == ".md":
                    ref_title, _ = read_md(rf)
                    ref_page = f"pages/skills/{skill_name}-{rf.stem}.html"
                    ref_links.append((ref_title, ref_page, rf))
            
            if ref_links:
                body_html += '\n<h2 id="references">References</h2>\n<ul>'
                for rt, rp, _ in ref_links:
                    body_html += f'\n<li><a href="../../{rp}">{htmlmod.escape(rt)}</a></li>'
                body_html += '\n</ul>'
                
                # build reference pages
                for rt, rp, rf in ref_links:
                    ref_body = md_to_html_simple(read_md(rf)[1])
                    ref_body = f'<p class="refnote">Source: {skill_name}/references/{rf.name}</p>\n' + ref_body
                    ref_html = doc_page_html(rt, ref_body, rp, base="../../")
                    (SITE / rp).parent.mkdir(parents=True, exist_ok=True)
                    (SITE / rp).write_text(ref_html, encoding="utf-8")
        
        page_html = doc_page_html(
            f"{skill_name}",
            f'<p class="refnote">Source: skills/{skill_name}/SKILL.md</p>\n' + body_html,
            page_file,
            base="../../"
        )
        (SITE / page_file).write_text(page_html, encoding="utf-8")
        entries.append((skill_name, page_file))
    
    return entries


# ---- build devlog pages ----

def build_devlog_pages():
    """Generate pages for key devlog entries."""
    devlog_out = PAGES / "devlog"
    devlog_out.mkdir(parents=True, exist_ok=True)
    
    entries = []
    
    # top-level devlog .md files
    for f in sorted(DEVLOG_DIR.glob("*.md")):
        title, body = read_md(f)
        slug = f.stem
        page_file = f"pages/devlog/{slug}.html"
        body_html = f'<p class="refnote">Source: devlog/{f.name}</p>\n' + md_to_html_simple(body)
        html = doc_page_html(title, body_html, page_file, base="../../")
        (SITE / page_file).write_text(html, encoding="utf-8")
        entries.append((title, page_file))
    
    # _plan and _fin subdirectories — key specs
    for subdir in [DEVLOG_DIR / "_plan", DEVLOG_DIR / "_fin"]:
        if not subdir.is_dir():
            continue
        for unit_dir in sorted(subdir.iterdir()):
            if not unit_dir.is_dir():
                continue
            spec = unit_dir / "00_spec.md"
            plan = unit_dir / "000_plan.md" if not spec.exists() else spec
            # try first .md file
            if not plan.exists():
                mds = sorted(unit_dir.glob("*.md"))
                if mds:
                    plan = mds[0]
                else:
                    continue
            
            title, body = read_md(plan)
            slug = unit_dir.name
            page_file = f"pages/devlog/{slug}.html"
            body_html = f'<p class="refnote">Source: devlog/{subdir.name}/{slug}/{plan.name}</p>\n'
            body_html += md_to_html_simple(body)
            
            # link other files in the unit
            other_files = [f for f in sorted(unit_dir.glob("*.md")) if f != plan]
            if other_files:
                body_html += '\n<h2 id="unit-files">Other files in this unit</h2>\n<ul>'
                for of in other_files:
                    ot, _ = read_md(of)
                    body_html += f'\n<li>{htmlmod.escape(ot)} <span class="refnote">({of.name})</span></li>'
                body_html += '\n</ul>'
            
            html = doc_page_html(title, body_html, page_file, base="../../")
            (SITE / page_file).write_text(html, encoding="utf-8")
            entries.append((f"{slug}: {title}", page_file))
    
    return entries


# ---- build backlog pages ----

def build_backlog_pages():
    """Generate pages for backlog entries."""
    backlog_out = PAGES / "backlog"
    backlog_out.mkdir(parents=True, exist_ok=True)
    
    entries = []
    if not BACKLOG_DIR.is_dir():
        return entries
    
    for f in sorted(BACKLOG_DIR.glob("*.md")):
        title, body = read_md(f)
        slug = f.stem
        page_file = f"pages/backlog/{slug}.html"
        body_html = f'<p class="refnote">Source: backlog/{f.name}</p>\n' + md_to_html_simple(body)
        html = doc_page_html(title, body_html, page_file, base="../../")
        (SITE / page_file).write_text(html, encoding="utf-8")
        entries.append((title, page_file))
    
    return entries


# ---- build search index ----

def build_search_index(all_pages):
    """Generate search-index.js with all page titles and text snippets."""
    entries = []
    for title, url in all_pages:
        # read the generated HTML and extract text
        html_path = SITE / url
        if html_path.exists():
            content = html_path.read_text(encoding="utf-8")
            # strip tags for search text
            text = re.sub(r"<[^>]+>", " ", content)
            text = re.sub(r"\s+", " ", text).strip()[:500]  # first 500 chars
        else:
            text = title
        entries.append({"title": title, "url": url, "text": text})
    
    js = "window.DOCS_SEARCH_INDEX = " + json.dumps(entries, ensure_ascii=False, indent=None) + ";\n"
    (SITE / "assets" / "search-index.js").write_text(js, encoding="utf-8")


# ---- main ----

def main():
    print("Building PABCD Initiative docs-site...")
    
    # 1. Build skill pages
    skill_entries = build_skill_pages()
    print(f"  Skills: {len(skill_entries)} pages")
    
    # 2. Build devlog pages
    devlog_entries = build_devlog_pages()
    print(f"  Devlog: {len(devlog_entries)} pages")
    
    # 3. Build backlog pages
    backlog_entries = build_backlog_pages()
    print(f"  Backlog: {len(backlog_entries)} pages")
    
    # 4. Update NAV
    NAV[2] = ("Skills Reference", [(name, page) for name, page in skill_entries])
    NAV[4] = ("Devlog", [(name, page) for name, page in devlog_entries])
    NAV[5] = ("Backlog", [(name, page) for name, page in backlog_entries])
    
    # Collect reference pages from dev-pabcd
    ref_entries = []
    if REFS_DIR.is_dir():
        for rf in sorted(REFS_DIR.glob("*.md")):
            if rf.suffix == ".yaml":
                continue
            title, _ = read_md(rf)
            page = f"pages/skills/dev-pabcd-{rf.stem}.html"
            ref_entries.append((title, page))
    NAV[3] = ("Dev Guides", ref_entries)
    
    # 5. Build all pages list for search
    all_pages = [
        ("Introduction", "index.html"),
        ("Origin Story", "pages/origin.html"),
        ("Skill Architecture", "pages/skills.html"),
        ("Delegation Economy", "pages/delegation.html"),
        ("Loop Contract", "pages/loop.html"),
    ]
    all_pages.extend(skill_entries)
    all_pages.extend(ref_entries)
    all_pages.extend(devlog_entries)
    all_pages.extend(backlog_entries)
    
    # 6. Regenerate all doc pages with updated NAV
    # (skill/devlog/backlog pages were already built; now rebuild with correct NAV)
    # We need to re-write all pages since NAV was updated after initial build
    for name, page in skill_entries:
        skill_md = SKILLS_DIR / name / "SKILL.md"
        if not skill_md.exists():
            continue
        title, body = read_md(skill_md)
        body_html = f'<p class="refnote">Source: skills/{name}/SKILL.md</p>\n' + md_to_html_simple(body)
        refs_dir = SKILLS_DIR / name / "references"
        if refs_dir.is_dir():
            ref_links = [(read_md(rf)[0], f"pages/skills/{name}-{rf.stem}.html") 
                        for rf in sorted(refs_dir.glob("*.md"))]
            if ref_links:
                body_html += '\n<h2 id="references">References</h2>\n<ul>'
                for rt, rp in ref_links:
                    body_html += f'\n<li><a href="../../{rp}">{htmlmod.escape(rt)}</a></li>'
                body_html += '\n</ul>'
        html = doc_page_html(name, body_html, page, base="../../")
        (SITE / page).write_text(html, encoding="utf-8")
    
    # 6b. Rebuild devlog pages with complete NAV
    devlog_entries_rebuild = build_devlog_pages()
    
    # 6c. Rebuild backlog pages with complete NAV
    backlog_entries_rebuild = build_backlog_pages()
    
    # 6d. Rebuild reference pages with complete NAV
    if REFS_DIR.is_dir():
        for rf in sorted(REFS_DIR.glob("*.md")):
            if rf.suffix == ".yaml":
                continue
            ref_title, ref_body = read_md(rf)
            ref_page = f"pages/skills/dev-pabcd-{rf.stem}.html"
            ref_body_html = f'<p class="refnote">Source: dev-pabcd/references/{rf.name}</p>\n' + md_to_html_simple(ref_body)
            ref_html = doc_page_html(ref_title, ref_body_html, ref_page, base="../../")
            (SITE / ref_page).write_text(ref_html, encoding="utf-8")
    
    print(f"  Rebuilt with complete NAV: {len(skill_entries)} skills + {len(devlog_entries_rebuild)} devlog + {len(backlog_entries_rebuild)} backlog + {len(ref_entries)} refs")
    
    # 7. Build search index
    build_search_index(all_pages)
    print(f"  Search index: {len(all_pages)} entries")
    
    # 8. Wrap existing doc pages with sidebar
    wrap_existing_pages()
    
    print("Done!")


def wrap_existing_pages():
    """Add sidebar to the existing 4 doc pages (origin/skills/delegation/loop)."""
    existing = [
        "pages/origin.html",
        "pages/skills.html", 
        "pages/delegation.html",
        "pages/loop.html",
    ]
    for page_path in existing:
        full = SITE / page_path
        if not full.exists():
            continue
        content = full.read_text(encoding="utf-8")
        
        # check if already wrapped
        if "docs-shell" in content:
            continue
        
        # inject docs.css link after site.css
        if "docs.css" not in content:
            content = content.replace(
                'site.css?v=3">', 
                'site.css?v=4">\n<link rel="stylesheet" href="../assets/docs.css?v=1">'
            )
        
        # inject sidebar after meta-bar header
        sidebar_html = build_sidebar_html(page_path, base="../")
        
        # find the closing </header> and inject after it
        header_end = content.find("</header>")
        if header_end == -1:
            continue
        
        insert_pos = header_end + len("</header>")
        
        shell_open = f'\n<div class="docs-shell">\n{sidebar_html}\n<div class="sidebar-overlay" id="sidebar-overlay"></div>\n<main class="docs-content">\n'
        shell_close = '\n</main>\n</div>\n<button class="sidebar-toggle" id="sidebar-toggle" aria-label="Toggle sidebar">&#9776;</button>\n<script src="../assets/search-index.js"></script>\n<script src="../assets/docs.js"></script>\n'
        
        # find the </body> to insert shell_close before it
        body_end = content.rfind("</body>")
        
        new_content = (
            content[:insert_pos] +
            shell_open +
            content[insert_pos:body_end] +
            shell_close +
            content[body_end:]
        )
        
        full.write_text(new_content, encoding="utf-8")
        print(f"  Wrapped: {page_path}")


if __name__ == "__main__":
    main()
