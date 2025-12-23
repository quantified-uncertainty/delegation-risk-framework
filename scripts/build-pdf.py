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

# Sidebar order matching astro.config.mjs
SIDEBAR_ORDER = [
    # Getting Started
    ("Getting Started", [
        "getting-started/index.md",
        "getting-started/five-minute-intro.md",
        "getting-started/core-concepts.md",
        "getting-started/introduction.md",
        "getting-started/faq.md",
        "getting-started/glossary.md",
    ]),
    # The Framework
    ("The Framework", [
        "framework/index.md",
        # Capability Formalization
        "framework/capability/index.md",
        "framework/capability/agent-power-formalization.md",
        "framework/capability/agency-power-examples.md",
        "framework/capability/strong-tools-hypothesis.md",
        # Risk Formalization
        "framework/risk/index.md",
        "framework/risk/overview.md",
        "framework/risk/walkthrough.md",
        "framework/risk/delegation-accounting.md",
        "framework/risk/risk-decomposition.md",
        "framework/risk/exposure-cascade.md",
        "framework/risk/insurers-dilemma.md",
    ]),
    # Applying the Framework
    ("Applying the Framework", [
        "applying/index.md",
        "applying/principles-to-practice.md",
        "applying/decomposed-coordination.md",
        "applying/safety-mechanisms.md",
        "applying/forecasting-navigation.md",
        "applying/least-x-principles.md",
        "applying/coordinator-constraints.md",
        # Design Patterns
        "applying/patterns/index.md",
        "applying/patterns/structural.md",
        "applying/patterns/verification.md",
        "applying/patterns/information.md",
        "applying/patterns/temporal.md",
        "applying/patterns/monitoring.md",
        "applying/patterns/multi-agent.md",
        "applying/patterns/incentive.md",
        "applying/patterns/recovery.md",
        "applying/patterns/channel-integrity.md",
        # Entanglements
        "applying/interconnection/index.md",
        "applying/interconnection/types.md",
        "applying/interconnection/challenges.md",
        "applying/interconnection/modeling.md",
        "applying/interconnection/examples.md",
        "applying/interconnection/solutions.md",
        "applying/interconnection/decision-framework.md",
        # Worked Examples
        "applying/examples/research-assistant-example.md",
        "applying/examples/code-deployment-example.md",
        "applying/examples/trading-system-example.md",
        "applying/examples/healthcare-bot-example.md",
        # Tools & Guides
        "applying/tools/quick-start.md",
        "applying/tools/decision-guide.md",
        "applying/tools/delegation-risk-calculator.mdx",
        "applying/tools/trust-propagation.mdx",
        "applying/tools/tradeoff-frontier.mdx",
        "applying/tools/cost-benefit.md",
        "applying/tools/empirical-tests.md",
    ]),
    # Cross-Domain Methods
    ("Cross-Domain Methods", [
        "cross-domain-methods/overview.md",
        "cross-domain-methods/euler-allocation.md",
        "cross-domain-methods/nuclear-safety-pra.md",
        "cross-domain-methods/mechanism-design.md",
        "cross-domain-methods/asil-decomposition.md",
        "cross-domain-methods/carbon-budgets.md",
        "cross-domain-methods/attack-surface-metrics.md",
        "cross-domain-methods/linear-logic-types.md",
        "cross-domain-methods/lessons-from-failures.md",
        "cross-domain-methods/access-control-systems.md",
    ]),
    # Case Studies
    ("Case Studies", [
        "case-studies/index.md",
        # AI Systems
        "case-studies/ai-systems/case-study-sydney.md",
        "case-studies/ai-systems/case-study-success.md",
        "case-studies/ai-systems/case-study-near-miss.md",
        "case-studies/ai-systems/case-study-drift.md",
        "case-studies/ai-systems/anti-patterns.md",
        # Human Systems
        "case-studies/human-systems/organizational-trust.md",
        "case-studies/human-systems/nuclear-launch-authority.md",
        "case-studies/human-systems/criminal-trust.md",
        "case-studies/human-systems/jury-trust.md",
        "case-studies/human-systems/open-source-trust.md",
        "case-studies/human-systems/oversight-dilemma.md",
        "case-studies/human-systems/trust-across-civilizations.md",
        # Anomaly Chronicles
        "case-studies/anomaly-chronicles/index.md",
        "case-studies/anomaly-chronicles/power-struggles.md",
        "case-studies/anomaly-chronicles/containing-mr-x.md",
        "case-studies/anomaly-chronicles/five-years-later.md",
        "case-studies/anomaly-chronicles/task-architecture.md",
        "case-studies/anomaly-chronicles/year-ten.md",
        "case-studies/anomaly-chronicles/mr-x-perspective.md",
        "case-studies/anomaly-chronicles/protocol-catalog.md",
        "case-studies/anomaly-chronicles/insurance-bot-spec.md",
    ]),
    # Deep Dives
    ("Deep Dives", [
        "deep-dives/index.md",
        # Theoretical Foundations
        "deep-dives/theory/index.md",
        "deep-dives/theory/trust-accounting.md",
        "deep-dives/theory/trust-propagation.md",
        "deep-dives/theory/trust-dynamics.md",
        "deep-dives/theory/trust-optimization.md",
        "deep-dives/theory/trust-economics.md",
        "deep-dives/theory/trust-interfaces.md",
        "deep-dives/theory/trust-protocols.md",
        "deep-dives/theory/trust-at-scale.md",
        "deep-dives/theory/human-ai-trust.md",
        # Background Research
        "deep-dives/research/index.md",
        # Risk & Financial Methods
        "deep-dives/research/risk-methods/financial-risk-budgeting.md",
        "deep-dives/research/risk-methods/fidelity-insurance.md",
        "deep-dives/research/risk-methods/compositional-risk-measures.md",
        "deep-dives/research/risk-methods/alignment-tax-quantification.md",
        # Technical Safety
        "deep-dives/research/technical-safety/ai-safety-frameworks.md",
        "deep-dives/research/technical-safety/formal-verification-limits.md",
        "deep-dives/research/technical-safety/runtime-monitoring-architectures.md",
        "deep-dives/research/technical-safety/capability-elicitation-sandbagging.md",
        "deep-dives/research/technical-safety/steganography-detection-prevention.md",
        # System Design
        "deep-dives/research/system-design/mechanism-design.md",
        "deep-dives/research/system-design/nuclear-aerospace-deep-dive.md",
        "deep-dives/research/system-design/byzantine-coordinator-voting.md",
        "deep-dives/research/system-design/prototype-architecture-feasibility.md",
        # Trust & Behavior
        "deep-dives/research/trust-behavior/human-trust-calibration.md",
        "deep-dives/research/trust-behavior/trust-dynamics-adversarial-pressure.md",
        "deep-dives/research/trust-behavior/empirical-scheming-reduction.md",
        "deep-dives/research/trust-behavior/correlated-failure-modeling.md",
        "deep-dives/research/trust-behavior/linear-logic-trust-budgets.md",
        # Other
        "deep-dives/research/hierarchy-visualization.md",
        "deep-dives/research/potential-projects.md",
    ]),
    # Reference
    ("Reference", [
        "reference/index.md",
        "reference/bibliography.md",
        "reference/related-approaches.md",
        "reference/roadmap.md",
        "reference/site-map.md",
        "reference/coordinator-constraints-brainstorm.md",
        "reference/potential-examples.md",
    ]),
]

def get_ordered_chapters():
    """Get chapters in sidebar order, falling back to discovery for missing files."""
    chapters = []

    for part_name, files in SIDEBAR_ORDER:
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
    content = re.sub(r'\{`[^`]*`\}', '', content)
    content = re.sub(r'\{[^}]*\}', '', content)

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

    # Handle mermaid diagrams
    def replace_mermaid(match):
        _mermaid_counter[0] += 1
        mermaid_code = match.group(1)
        img_path = render_mermaid(mermaid_code, _mermaid_counter[0])
        if img_path:
            return f'\n![Diagram]({img_path})\n'
        else:
            return '\n*[Diagram could not be rendered]*\n'

    content = re.sub(r'```mermaid\s*\n(.*?)```', replace_mermaid, content, flags=re.DOTALL)

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
