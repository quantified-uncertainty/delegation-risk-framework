#!/usr/bin/env python3
"""
Build a professional PDF book from the Delegation Risk Framework markdown files.
Uses Pandoc with XeLaTeX for proper book formatting.
"""

import os
import re
import subprocess
import tempfile
import hashlib
import json
from pathlib import Path
from datetime import datetime

# Directory for rendered mermaid diagrams
MERMAID_CACHE_DIR = Path(__file__).parent.parent / ".mermaid-cache"

# Project root
ROOT = Path(__file__).parent.parent
DOCS_DIR = ROOT / "src" / "content" / "docs"
VERSION_FILE = ROOT / "version.json"


def get_git_short_hash():
    """Get the short git commit hash."""
    try:
        result = subprocess.run(
            ['git', 'rev-parse', '--short', 'HEAD'],
            capture_output=True,
            text=True,
            cwd=ROOT
        )
        if result.returncode == 0:
            return result.stdout.strip()
    except Exception:
        pass
    return "unknown"


def compute_docs_hash():
    """Compute a hash of all documentation content."""
    hasher = hashlib.sha256()

    # Get all markdown files in docs directory
    md_files = sorted(DOCS_DIR.rglob("*.md")) + sorted(DOCS_DIR.rglob("*.mdx"))

    for file_path in md_files:
        try:
            content = file_path.read_text(encoding='utf-8')
            hasher.update(content.encode('utf-8'))
        except Exception:
            pass

    return hasher.hexdigest()[:12]


def load_version():
    """Load version info from version.json."""
    if VERSION_FILE.exists():
        try:
            return json.loads(VERSION_FILE.read_text(encoding='utf-8'))
        except Exception:
            pass
    return {"major": 1, "minor": 0, "patch": 0, "contentHash": "", "lastBuildDate": ""}


def save_version(version_info):
    """Save version info to version.json."""
    VERSION_FILE.write_text(json.dumps(version_info, indent=2) + "\n", encoding='utf-8')


def get_version_string():
    """
    Get the full version string, auto-incrementing patch if content changed.
    Returns tuple of (version_string, version_info).
    """
    version = load_version()
    current_hash = compute_docs_hash()
    git_hash = get_git_short_hash()

    # Check if content has changed
    if version.get("contentHash") and version["contentHash"] != current_hash:
        version["patch"] = version.get("patch", 0) + 1
        print(f"  Content changed (was {version['contentHash'][:8]}..., now {current_hash[:8]}...) - bumping to patch {version['patch']}")
    elif not version.get("contentHash"):
        print(f"  First build - initializing content hash")
    else:
        print(f"  Content unchanged - keeping patch {version.get('patch', 0)}")

    # Update version info
    version["contentHash"] = current_hash
    version["lastBuildDate"] = datetime.now().isoformat()
    version["gitHash"] = git_hash

    # Save updated version
    save_version(version)

    # Build version string: 1.0.3+abc1234
    version_str = f"{version['major']}.{version['minor']}.{version['patch']}+{git_hash}"

    return version_str, version

# ============================================================================
# SIDEBAR PARSING - Dynamically reads from astro.config.mjs
# ============================================================================

ASTRO_CONFIG = ROOT / "astro.config.mjs"

def get_frontmatter_order(file_path):
    """Extract sidebar.order from frontmatter, return large number if not found."""
    try:
        content = file_path.read_text(encoding='utf-8')
        # Match sidebar: { order: N } or sidebar:\n  order: N
        match = re.search(r'sidebar:\s*(?:\{[^}]*order:\s*(\d+)|order:\s*(\d+))', content)
        if match:
            return int(match.group(1) or match.group(2))
        # Also check for simple order: N in frontmatter
        fm_match = re.search(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
        if fm_match:
            order_match = re.search(r'^\s*order:\s*(\d+)', fm_match.group(1), re.MULTILINE)
            if order_match:
                return int(order_match.group(1))
    except Exception:
        pass
    return 999  # Default: put at end

def get_files_in_directory(directory):
    """Get all .md/.mdx files in a directory, sorted by frontmatter order then filename."""
    dir_path = DOCS_DIR / directory
    if not dir_path.exists():
        return []

    files = []
    for ext in ['*.md', '*.mdx']:
        files.extend(dir_path.glob(ext))

    # Sort by frontmatter order, then by filename
    files_with_order = [(f, get_frontmatter_order(f), f.name) for f in files]
    files_with_order.sort(key=lambda x: (x[1], x[2]))

    return [str(f.relative_to(DOCS_DIR)) for f, _, _ in files_with_order]

def slug_to_filepath(slug):
    """Convert a Starlight slug to a file path."""
    # Try with index.md first, then .md, then .mdx
    for suffix in ['/index.md', '.md', '/index.mdx', '.mdx']:
        path = DOCS_DIR / (slug + suffix)
        if path.exists():
            return slug + suffix
    # Fallback
    return slug + '.md'

def parse_sidebar_items(items_str):
    """Parse a JavaScript array of sidebar items."""
    files = []

    # Find all slug entries: { label: '...', slug: '...' }
    slug_pattern = r"\{\s*label:\s*['\"]([^'\"]+)['\"],\s*slug:\s*['\"]([^'\"]+)['\"]"
    for match in re.finditer(slug_pattern, items_str):
        slug = match.group(2)
        files.append(slug_to_filepath(slug))

    # Find all autogenerate entries: autogenerate: { directory: '...' }
    auto_pattern = r"autogenerate:\s*\{\s*directory:\s*['\"]([^'\"]+)['\"]"
    for match in re.finditer(auto_pattern, items_str):
        directory = match.group(1)
        files.extend(get_files_in_directory(directory))

    # Find nested items arrays and recurse
    # This handles: items: [ ... ]
    nested_items_pattern = r"items:\s*\[((?:[^\[\]]|\[(?:[^\[\]]|\[[^\]]*\])*\])*)\]"
    for match in re.finditer(nested_items_pattern, items_str):
        nested = match.group(1)
        # Avoid re-processing the same content
        if 'slug:' in nested or 'autogenerate:' in nested:
            files.extend(parse_sidebar_items(nested))

    return files

def parse_astro_sidebar():
    """Parse the sidebar configuration from astro.config.mjs."""
    if not ASTRO_CONFIG.exists():
        print("Warning: astro.config.mjs not found, using empty sidebar")
        return []

    content = ASTRO_CONFIG.read_text(encoding='utf-8')

    # Extract the sidebar array
    sidebar_match = re.search(r'sidebar:\s*\[(.*)\]', content, re.DOTALL)
    if not sidebar_match:
        print("Warning: Could not find sidebar in astro.config.mjs")
        return []

    sidebar_content = sidebar_match.group(1)

    # Split into top-level sections by finding { label: '...' patterns at the right nesting level
    sections = []

    # Find each top-level section
    # Pattern: { label: 'Name', ... items/autogenerate ... }
    section_pattern = r"\{\s*label:\s*['\"]([^'\"]+)['\"][^{}]*(?:autogenerate:\s*\{\s*directory:\s*['\"]([^'\"]+)['\"][^{}]*\}|items:\s*\[((?:[^\[\]]|\[(?:[^\[\]]|\[[^\]]*\])*\])*)\])"

    for match in re.finditer(section_pattern, sidebar_content):
        label = match.group(1)
        autogen_dir = match.group(2)
        items_content = match.group(3)

        files = []
        if autogen_dir:
            # Simple autogenerate section
            files = get_files_in_directory(autogen_dir)
        elif items_content:
            # Section with explicit items
            files = parse_sidebar_items(items_content)

        if files:
            sections.append((label, files))

    return sections

def get_sidebar_order():
    """Get the sidebar order, parsing from astro.config.mjs."""
    sections = parse_astro_sidebar()
    if not sections:
        print("Warning: No sections found in sidebar, check astro.config.mjs")
    return sections

# Legacy constant for compatibility - now dynamically generated
SIDEBAR_ORDER = None  # Will be set at runtime

def get_ordered_chapters():
    """Get chapters in sidebar order by parsing astro.config.mjs."""
    chapters = []
    sidebar_order = get_sidebar_order()

    for part_name, files in sidebar_order:
        found_files = []
        for rel_path in files:
            full_path = DOCS_DIR / rel_path
            if full_path.exists():
                found_files.append(f"src/content/docs/{rel_path}")
            else:
                # Try .mdx extension
                mdx_path = DOCS_DIR / rel_path.replace('.md', '.mdx')
                if mdx_path.exists():
                    found_files.append(f"src/content/docs/{rel_path.replace('.md', '.mdx')}")

        if found_files:
            chapters.append((part_name, found_files))

    return chapters

# Global mapping of URL paths to anchor IDs
URL_TO_ANCHOR = {}
CHAPTERS = []

def build_url_mapping():
    """Build mapping from URL paths to document anchors."""
    global URL_TO_ANCHOR
    URL_TO_ANCHOR = {}

    for part_name, files in CHAPTERS:
        for file_path in files:
            full_path = ROOT / file_path
            if not full_path.exists():
                continue

            content = full_path.read_text(encoding='utf-8')
            title = extract_title(content)

            # Generate anchor ID (same algorithm Pandoc uses)
            anchor = title.lower()
            anchor = re.sub(r'[^\w\s-]', '', anchor)  # Remove special chars
            anchor = re.sub(r'\s+', '-', anchor)  # Spaces to hyphens
            anchor = anchor.strip('-')

            # Build URL path from file path
            rel_path = file_path.replace('src/content/docs/', '').replace('.mdx', '').replace('.md', '')
            if rel_path.endswith('/index'):
                rel_path = rel_path[:-6]
            url_path = f"/{rel_path}/"

            URL_TO_ANCHOR[url_path] = f"#{anchor}"
            URL_TO_ANCHOR[url_path.rstrip('/')] = f"#{anchor}"

    return URL_TO_ANCHOR

def convert_internal_links(content):
    """Convert internal URL links to document anchors."""
    def replace_link(match):
        prefix = match.group(1)
        text = match.group(2)
        url = match.group(3)

        if prefix == '!':
            return match.group(0)

        if url.startswith('/'):
            anchor = URL_TO_ANCHOR.get(url) or URL_TO_ANCHOR.get(url.rstrip('/'))
            if anchor:
                return f'[{text}]({anchor})'
            else:
                return f'*{text}*'

        return match.group(0)

    return re.sub(r'(!?)\[([^\]]+)\]\(([^)]+)\)', replace_link, content)

# Global footnote counter for unique footnote IDs across entire document
_footnote_counter = [0]

def convert_external_links_to_footnotes(content):
    """Convert external links to footnotes for print-friendliness."""
    def replace_external_link(match):
        prefix = match.group(1)
        text = match.group(2)
        url = match.group(3)

        # Don't modify images or internal links
        if prefix == '!' or url.startswith('#') or url.startswith('/'):
            return match.group(0)

        # External link - convert to footnote
        if url.startswith('http'):
            _footnote_counter[0] += 1
            return f'{text}[^fn{_footnote_counter[0]}]\n\n[^fn{_footnote_counter[0]}]: {url}'

        return match.group(0)

    return re.sub(r'(!?)\[([^\]]+)\]\(([^)]+)\)', replace_external_link, content)

# Unicode replacements for LaTeX compatibility
UNICODE_REPLACEMENTS = {
    'Σ': 'Σ', '→': '→', '←': '←', '↔': '↔',  # Keep these for XeLaTeX
    '≤': '≤', '≥': '≥', '×': '×', '÷': '÷',
    '∞': '∞', '≈': '≈', '≠': '≠', '±': '±',
    '—': '—', '–': '–', ''': "'", ''': "'", '"': '"', '"': '"',
    '…': '…', '•': '•', '≡': '≡', '∈': '∈',
}

def clean_unicode(text):
    """Clean problematic unicode for XeLaTeX (much less needed than pdflatex)."""
    for char, replacement in UNICODE_REPLACEMENTS.items():
        text = text.replace(char, replacement)
    return text

def render_mermaid(code, diagram_id):
    """Render a mermaid diagram to PNG and return the path."""
    MERMAID_CACHE_DIR.mkdir(exist_ok=True)

    # Mermaid CLI has issues with <br/> in labels - normalize and quote labels
    code = re.sub(r'<br\s*/?>', '<br>', code)
    # Wrap labels containing <br> in quotes to prevent parse errors
    def quote_br_labels(m):
        node_id = m.group(1)
        label = m.group(2)
        # If label contains <br> and isn't already quoted, quote it
        if '<br>' in label and not label.startswith('"'):
            return f'{node_id}["{label}"]'
        return m.group(0)
    code = re.sub(r'(\w+)\[([^\]]+)\]', quote_br_labels, code)

    code_hash = hashlib.md5(code.encode()).hexdigest()[:12]
    output_path = MERMAID_CACHE_DIR / f"diagram-{diagram_id}-{code_hash}.png"

    if output_path.exists():
        return str(output_path)

    with tempfile.NamedTemporaryFile(mode='w', suffix='.mmd', delete=False) as f:
        f.write(code)
        temp_mmd = f.name

    try:
        result = subprocess.run(
            ['mmdc', '-i', temp_mmd, '-o', str(output_path), '-b', 'white', '-s', '2'],
            capture_output=True,
            text=True,
            timeout=30
        )
        if result.returncode == 0 and output_path.exists():
            return str(output_path)
        else:
            print(f"    Warning: Mermaid render failed: {result.stderr[:100] if result.stderr else 'unknown error'}")
            return None
    except Exception as e:
        print(f"    Warning: Mermaid render error: {e}")
        return None
    finally:
        os.unlink(temp_mmd)

def extract_title(content):
    """Extract title from frontmatter."""
    match = re.search(r'^---\s*\n.*?title:\s*["\']?([^"\'\n]+)["\']?.*?\n---', content, re.DOTALL)
    return match.group(1).strip() if match else "Untitled"

_mermaid_counter = [0]

def process_markdown(content, file_path):
    """Process markdown content for LaTeX compatibility."""
    # Remove frontmatter
    content = re.sub(r'^---\s*\n.*?\n---\s*\n', '', content, flags=re.DOTALL)

    # Remove MDX imports
    content = re.sub(r'^import\s+.*?[\'"];?\s*$', '', content, flags=re.MULTILINE)
    content = re.sub(r'^import\s*\{[^}]*\}\s*from\s*[\'"][^\'"]*[\'"];?\s*$', '', content, flags=re.MULTILINE)

    # Convert Starlight components
    content = re.sub(r'<Card\s+title="([^"]+)"[^>]*>', r'\n**\1**\n\n', content)
    content = re.sub(r'<Card\s+title=\'([^\']+)\'[^>]*>', r'\n**\1**\n\n', content)
    content = re.sub(r'</Card>', '\n', content)
    content = re.sub(r'<CardGrid[^>]*>', '', content)
    content = re.sub(r'</CardGrid>', '', content)

    # Remove JSX/React component blocks
    def remove_jsx_block(content):
        result = []
        i = 0
        while i < len(content):
            match = re.match(r'<div\s+id="[^"]*"[^>]*>', content[i:])
            if match:
                depth = 1
                j = i + len(match.group(0))
                while j < len(content) and depth > 0:
                    if content[j:j+4] == '<div':
                        depth += 1
                        j += 4
                    elif content[j:j+6] == '</div>':
                        depth -= 1
                        j += 6
                    else:
                        j += 1
                result.append('\n*[Interactive component - see web version]*\n')
                i = j
            else:
                result.append(content[i])
                i += 1
        return ''.join(result)

    content = remove_jsx_block(content)

    # Handle mermaid diagrams FIRST (before HTML tag removal, since Mermaid uses <br/> for line breaks)
    def replace_mermaid(match):
        _mermaid_counter[0] += 1
        mermaid_code = match.group(1)
        img_path = render_mermaid(mermaid_code, _mermaid_counter[0])
        if img_path:
            return f'\n![Diagram]({img_path})\n'
        else:
            return '\n*[Diagram could not be rendered]*\n'

    content = re.sub(r'```mermaid\s*\n(.*?)```', replace_mermaid, content, flags=re.DOTALL)

    # Remove remaining style/script blocks
    content = re.sub(r'<style[^>]*>[\s\S]*?</style>', '', content)
    content = re.sub(r'<script[^>]*>[\s\S]*?</script>', '', content)

    # Remove HTML tags
    content = re.sub(r'<details[^>]*>', '\n', content)
    content = re.sub(r'</details>', '\n', content)
    content = re.sub(r'<summary[^>]*>(.*?)</summary>', r'**\1**\n', content)
    content = re.sub(r'<br\s*/?>', '\n', content)
    content = re.sub(r'</?div[^>]*>', '', content)
    content = re.sub(r'</?span[^>]*>', '', content)
    content = re.sub(r'<input[^>]*/?>', '', content)
    content = re.sub(r'<button[^>]*>.*?</button>', '', content)
    content = re.sub(r'<label[^>]*>.*?</label>', '', content, flags=re.DOTALL)
    content = re.sub(r'<select[^>]*>.*?</select>', '', content, flags=re.DOTALL)
    content = re.sub(r'<textarea[^>]*>.*?</textarea>', '', content, flags=re.DOTALL)
    content = re.sub(r'<form[^>]*>.*?</form>', '', content, flags=re.DOTALL)

    # Protect math environments from JSX cleanup
    math_blocks = []
    def save_math(match):
        math_blocks.append(match.group(0))
        return f'__MATH_BLOCK_{len(math_blocks)-1}__'

    # Protect display math ($$...$$) and inline math ($...$)
    content = re.sub(r'\$\$[^$]+\$\$', save_math, content)
    content = re.sub(r'\$[^$\n]+\$', save_math, content)

    # Now safe to remove JSX expressions
    content = re.sub(r'\{`[^`]*`\}', '', content)
    content = re.sub(r'\{[^}]*\}', '', content)

    # Restore math blocks
    for i, block in enumerate(math_blocks):
        content = content.replace(f'__MATH_BLOCK_{i}__', block)

    # Convert asides/callouts to blockquotes
    def convert_aside(match):
        aside_type = match.group(1)
        title = match.group(2)
        body = match.group(3).strip()
        header = title if title else aside_type.upper()
        body_lines = body.split('\n')
        quoted = '\n'.join(f'> {line}' if line.strip() else '>' for line in body_lines)
        return f'\n> **{header}**\n>\n{quoted}\n'

    content = re.sub(
        r'^:::(\w+)(?:\[([^\]]*)\])?\s*\n(.*?)\n^:::[ ]*$',
        convert_aside,
        content, flags=re.DOTALL | re.MULTILINE
    )

    # Clean unicode
    content = clean_unicode(content)

    return content

def build_combined_markdown():
    """Build a single combined markdown file with all chapters."""
    combined = []

    for part_name, files in CHAPTERS:
        # Add part title page (will be styled specially)
        combined.append(f"\n\n\\newpage\n\n# {part_name}\n\n\\newpage\n\n")

        for file_path in files:
            full_path = ROOT / file_path
            if not full_path.exists():
                print(f"  Warning: {file_path} not found, skipping")
                continue

            content = full_path.read_text(encoding='utf-8')
            title = extract_title(content)
            processed = process_markdown(content, file_path)

            # Convert internal links to anchors
            processed = convert_internal_links(processed)

            # Convert external links to footnotes
            processed = convert_external_links_to_footnotes(processed)

            # Add chapter
            combined.append(f"\n## {title}\n")
            combined.append(processed)
            print(f"  Added: {title}")

    return '\n'.join(combined)

# LaTeX header for XeLaTeX with custom fonts and running headers
LATEX_HEADER_XELATEX = r'''
\usepackage{fontspec}
\usepackage{xcolor}
\usepackage{longtable}
\usepackage{booktabs}
\usepackage{graphicx}
\usepackage{fancyhdr}
\usepackage{titlesec}

% Use system fonts
\setmainfont{Georgia}
\setsansfont{Helvetica Neue}
\setmonofont{Menlo}[Scale=0.9]

% Define colors
\definecolor{partblue}{RGB}{30, 58, 138}
\definecolor{chapterblue}{RGB}{30, 64, 175}
\definecolor{sectionblue}{RGB}{37, 99, 235}

% Part styling - full page
\titleformat{\part}[display]
  {\centering\Huge\bfseries\color{partblue}}
  {}
  {0pt}
  {}

% Section styling
\titleformat{\section}
  {\Large\bfseries\color{chapterblue}}
  {\thesection}
  {1em}
  {}

\titleformat{\subsection}
  {\large\bfseries\color{sectionblue}}
  {\thesubsection}
  {1em}
  {}

% Running headers
\pagestyle{fancy}
\fancyhf{}
\fancyhead[L]{\small\leftmark}
\fancyhead[R]{\small Delegation Risk Framework}
\fancyfoot[C]{\thepage}
\renewcommand{\headrulewidth}{0.4pt}
\renewcommand{\footrulewidth}{0pt}

% Plain style for chapter starts
\fancypagestyle{plain}{
  \fancyhf{}
  \fancyfoot[C]{\thepage}
  \renewcommand{\headrulewidth}{0pt}
}

% Ensure images fit
\makeatletter
\def\maxwidth{\ifdim\Gin@nat@width>\linewidth\linewidth\else\Gin@nat@width\fi}
\makeatother
\setkeys{Gin}{width=\maxwidth,keepaspectratio}

% Reduce widow/orphan lines
\widowpenalty=10000
\clubpenalty=10000
'''

# LaTeX header for pdflatex (fallback - no fontspec)
LATEX_HEADER_PDFLATEX = r'''
\usepackage{xcolor}
\usepackage{longtable}
\usepackage{booktabs}
\usepackage{graphicx}
\usepackage{fancyhdr}
\usepackage{titlesec}

% Define colors
\definecolor{partblue}{RGB}{30, 58, 138}
\definecolor{chapterblue}{RGB}{30, 64, 175}
\definecolor{sectionblue}{RGB}{37, 99, 235}

% Part styling - full page
\titleformat{\part}[display]
  {\centering\Huge\bfseries\color{partblue}}
  {}
  {0pt}
  {}

% Section styling
\titleformat{\section}
  {\Large\bfseries\color{chapterblue}}
  {\thesection}
  {1em}
  {}

\titleformat{\subsection}
  {\large\bfseries\color{sectionblue}}
  {\thesubsection}
  {1em}
  {}

% Running headers
\pagestyle{fancy}
\fancyhf{}
\fancyhead[L]{\small\leftmark}
\fancyhead[R]{\small Delegation Risk Framework}
\fancyfoot[C]{\thepage}
\renewcommand{\headrulewidth}{0.4pt}
\renewcommand{\footrulewidth}{0pt}

% Plain style for chapter starts
\fancypagestyle{plain}{
  \fancyhf{}
  \fancyfoot[C]{\thepage}
  \renewcommand{\headrulewidth}{0pt}
}

% Ensure images fit
\makeatletter
\def\maxwidth{\ifdim\Gin@nat@width>\linewidth\linewidth\else\Gin@nat@width\fi}
\makeatother
\setkeys{Gin}{width=\maxwidth,keepaspectratio}

% Reduce widow/orphan lines
\widowpenalty=10000
\clubpenalty=10000
'''

def get_cover_page(version_str):
    """Generate cover page LaTeX with version."""
    return r'''
\begin{titlepage}
\centering
\vspace*{2in}

{\Huge\bfseries\color{partblue} Delegation Risk Framework}

\vspace{0.5in}

{\Large\itshape A structured approach to managing risk\\in delegation relationships}

\vspace{1.5in}

{\large With applications to AI safety, organizational design,\\and multi-agent systems}

\vspace{\fill}

{\small Version ''' + version_str + r''' \\ Generated \today}

\end{titlepage}
\newpage
'''

def main():
    global CHAPTERS
    print("Building Delegation Risk Framework PDF & EPUB...")
    print()

    # Get version (auto-increments patch if content changed)
    print("Checking version:")
    version_str, version_info = get_version_string()
    print(f"  Version: {version_str}")
    print()

    # Reset global counters
    _footnote_counter[0] = 0
    _mermaid_counter[0] = 0

    # Get chapters in sidebar order
    CHAPTERS = get_ordered_chapters()
    total_files = sum(len(files) for _, files in CHAPTERS)
    print(f"Found {len(CHAPTERS)} parts with {total_files} files in sidebar order")

    # Build URL to anchor mapping
    build_url_mapping()
    print(f"Built {len(URL_TO_ANCHOR)} URL-to-anchor mappings")
    print()

    # Build combined markdown
    print("Processing chapters:")
    combined_md = build_combined_markdown()

    # Write to temp file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False, encoding='utf-8') as f:
        f.write(combined_md)
        temp_md = f.name

    # Save debug copy
    debug_md = ROOT / "debug-combined.md"
    debug_md.write_text(combined_md, encoding='utf-8')
    print(f"\nDebug markdown saved to: {debug_md}")

    # Output paths
    output_pdf = ROOT / "delegation-risk-framework-book.pdf"
    output_epub = ROOT / "delegation-risk-framework-book.epub"

    # Set PATH to include TeX
    env = os.environ.copy()
    env['PATH'] = '/Library/TeX/texbin:' + env.get('PATH', '')

    # Try XeLaTeX first, then fall back to pdflatex
    pdf_success = False

    for engine, header in [('xelatex', LATEX_HEADER_XELATEX), ('pdflatex', LATEX_HEADER_PDFLATEX)]:
        print(f"\nGenerating PDF with Pandoc + {engine}...")

        # Write LaTeX header with cover page (includes version)
        full_header = header + "\n\\AtBeginDocument{" + get_cover_page(version_str) + "}"
        with tempfile.NamedTemporaryFile(mode='w', suffix='.tex', delete=False, encoding='utf-8') as f:
            f.write(full_header)
            temp_header = f.name

        pdf_cmd = [
            '/opt/homebrew/bin/pandoc',
            temp_md,
            '-o', str(output_pdf),
            f'--pdf-engine={engine}',
            '--from', 'markdown+pipe_tables+grid_tables+simple_tables+multiline_tables+table_captions+footnotes',
            '--toc',
            '--toc-depth=2',
            '--highlight-style=tango',
            '-V', 'documentclass=report',
            '-V', 'geometry:margin=1in',
            '-V', 'fontsize=11pt',
            '-V', 'linkcolor=blue',
            '-V', 'urlcolor=blue',
            '-V', 'toccolor=black',
            '--metadata', 'title=Delegation Risk Framework',
            '--metadata', 'subtitle=A structured approach to managing risk in delegation relationships',
            '-H', temp_header,
        ]

        try:
            proc = subprocess.run(
                pdf_cmd,
                capture_output=True,
                text=True,
                env=env,
                timeout=600
            )
            os.unlink(temp_header)

            if proc.returncode == 0:
                pdf_success = True
                print(f"PDF generated successfully with {engine}")
                break
            else:
                # Check if it's just warnings or actual errors
                if output_pdf.exists() and output_pdf.stat().st_size > 100000:
                    pdf_success = True
                    print(f"PDF generated with warnings using {engine}")
                    break
                print(f"{engine} failed:", proc.stderr[:500] if proc.stderr else "Unknown error")
        except subprocess.TimeoutExpired:
            os.unlink(temp_header)
            print(f"{engine} timed out")

    if not pdf_success:
        print("PDF generation failed with all engines")

    if output_pdf.exists():
        print(f"PDF generated: {output_pdf}")
        print(f"PDF size: {output_pdf.stat().st_size / 1024:.1f} KB")

    # Build EPUB - need to clean LaTeX commands from markdown first
    print("\nGenerating EPUB...")

    # Create EPUB-clean version of markdown (remove LaTeX commands)
    epub_md = combined_md
    epub_md = re.sub(r'\\newpage\s*', '\n\n', epub_md)  # Remove \newpage entirely (no page breaks)
    epub_md = re.sub(r'\\[a-zA-Z]+\{[^}]*\}', '', epub_md)  # Remove other LaTeX commands
    epub_md = re.sub(r'\\[a-zA-Z]+', '', epub_md)  # Remove LaTeX commands without args
    epub_md = re.sub(r'\n---\n', '\n\n', epub_md)  # Remove horizontal rules (they can cause breaks)

    # Write EPUB-specific markdown
    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False, encoding='utf-8') as f:
        f.write(epub_md)
        temp_epub_md = f.name

    # Create custom EPUB CSS
    epub_css = '''
/* EPUB Stylesheet for Delegation Risk Framework */

body {
    font-family: Georgia, "Times New Roman", serif !important;
    line-height: 1.6 !important;
    margin: 1em !important;
    color: #1a1a1a !important;
    background: #ffffff !important;
    background-color: #ffffff !important;
}

h1 {
    color: #1e3a8a;
    border-bottom: 2px solid #3b82f6;
    padding-bottom: 0.3em;
    margin-top: 1.5em;
    font-size: 1.8em;
}

h2 {
    color: #1e40af;
    border-bottom: 1px solid #60a5fa;
    padding-bottom: 0.2em;
    margin-top: 1.2em;
    font-size: 1.4em;
}

h3 {
    color: #2563eb;
    margin-top: 1em;
    font-size: 1.2em;
}

h4, h5, h6 {
    color: #3730a3;
    margin-top: 0.8em;
}

p {
    margin: 0.8em 0;
    text-align: justify;
}

code {
    font-family: "Courier New", Courier, monospace;
    background: #f3f4f6;
    padding: 0.1em 0.3em;
    border-radius: 3px;
    font-size: 0.9em;
}

pre {
    background: #1f2937;
    color: #e5e7eb;
    padding: 1em;
    border-radius: 4px;
    overflow-x: auto;
    font-size: 0.85em;
    line-height: 1.4;
}

pre code {
    background: none;
    padding: 0;
    color: inherit;
}

blockquote {
    margin: 1em 0;
    padding: 0.5em 1em;
    border-left: 4px solid #3b82f6;
    background: #eff6ff;
    font-style: normal;
}

table {
    width: 100%;
    border-collapse: collapse;
    margin: 1em 0;
    font-size: 0.9em;
}

th, td {
    border: 1px solid #d1d5db;
    padding: 0.5em;
    text-align: left;
}

th {
    background: #f3f4f6;
    font-weight: bold;
}

a {
    color: #2563eb;
    text-decoration: none;
}

hr {
    border: none;
    border-top: 1px solid #d1d5db;
    margin: 2em 0;
}

ul, ol {
    margin: 0.8em 0;
    padding-left: 1.5em;
}

li {
    margin: 0.3em 0;
}

img {
    max-width: 100%;
    height: auto;
}

strong {
    color: #1e40af;
}

/* Part/Chapter titles */
h1:first-of-type {
    text-align: center;
    border-bottom: none;
    margin-top: 2em;
    margin-bottom: 2em;
}
'''

    with tempfile.NamedTemporaryFile(mode='w', suffix='.css', delete=False, encoding='utf-8') as f:
        f.write(epub_css)
        temp_css = f.name

    epub_cmd = [
        '/opt/homebrew/bin/pandoc',
        temp_epub_md,
        '-o', str(output_epub),
        '--from', 'markdown+pipe_tables+footnotes',
        '--toc',
        '--toc-depth=2',
        '--highlight-style=tango',
        '--metadata', f'title=Delegation Risk Framework (v{version_str})',
        '--metadata', 'subtitle=A structured approach to managing risk in delegation relationships',
        '--metadata', 'author=',
        '--epub-chapter-level=1',  # Only h1 (Parts) create page breaks, not h2 (chapters)
        '--css', temp_css,
        '--embed-resources',  # Embed CSS directly
    ]

    try:
        proc = subprocess.run(
            epub_cmd,
            capture_output=True,
            text=True,
            timeout=300
        )
        if proc.returncode != 0:
            print("EPUB Error:", proc.stderr[:1000])
    except subprocess.TimeoutExpired:
        print("EPUB generation timed out")
    finally:
        os.unlink(temp_epub_md)
        os.unlink(temp_css)

    if output_epub.exists():
        print(f"EPUB generated: {output_epub}")
        print(f"EPUB size: {output_epub.stat().st_size / 1024:.1f} KB")

    # Cleanup
    os.unlink(temp_md)

    print("\nDone!")
    return 0

if __name__ == '__main__':
    exit(main())
