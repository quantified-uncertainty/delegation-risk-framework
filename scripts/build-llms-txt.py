#!/usr/bin/env python3
"""
Generate llms txt files - documentation as plain text for LLM context.

Outputs:
- llms-core.txt: Essential pages (~50-100K chars) - fits in chat context
- llms-full.txt: Complete documentation - for embeddings/fine-tuning
"""

import re
import json
from pathlib import Path
from datetime import datetime

# Project root
ROOT = Path(__file__).parent.parent
DOCS_DIR = ROOT / "src" / "content" / "docs"
OUTPUT_FULL = ROOT / "public" / "llms-full.txt"
OUTPUT_CORE = ROOT / "public" / "llms-core.txt"
VERSION_FILE = ROOT / "version.json"

# Top-level sections in display order
SECTION_ORDER = [
    "getting-started",
    "framework",
    "applying",
    "cross-domain-methods",
    "case-studies",
    "deep-dives",
    "reference",
]

# Core pages for llms-core.txt - essential content that fits in chat context
CORE_PAGES = [
    "getting-started/index.md",
    "getting-started/five-minute-intro.md",
    "getting-started/core-concepts.md",
    "getting-started/introduction.md",
    "getting-started/faq.md",
    "framework/overview.md",
    "framework/delegation-accounting.md",
    "framework/risk-decomposition.md",
    "applying/index.md",
    "applying/least-x-principles.md",
]


def get_version_string():
    """Get version string from version.json."""
    if VERSION_FILE.exists():
        try:
            version = json.loads(VERSION_FILE.read_text())
            return f"{version['major']}.{version['minor']}.{version['patch']}"
        except Exception:
            pass
    return "0.0.0"


def get_sidebar_order(content):
    """Extract sidebar order from frontmatter, default to 999."""
    match = re.search(r'sidebar:\s*\n\s*order:\s*(\d+)', content)
    if match:
        return int(match.group(1))
    return 999


def discover_docs():
    """Auto-discover all markdown files, grouped by top-level section."""
    sections = {}

    for file_path in DOCS_DIR.rglob("*.md"):
        rel_path = file_path.relative_to(DOCS_DIR)
        parts = rel_path.parts

        # Get top-level section
        section = parts[0] if len(parts) > 1 else "root"

        if section not in sections:
            sections[section] = []

        # Read file to get sidebar order
        content = file_path.read_text(encoding='utf-8')
        order = get_sidebar_order(content)

        sections[section].append((order, str(rel_path), file_path))

    # Also check .mdx files
    for file_path in DOCS_DIR.rglob("*.mdx"):
        rel_path = file_path.relative_to(DOCS_DIR)
        parts = rel_path.parts
        section = parts[0] if len(parts) > 1 else "root"

        if section not in sections:
            sections[section] = []

        content = file_path.read_text(encoding='utf-8')
        order = get_sidebar_order(content)

        sections[section].append((order, str(rel_path), file_path))

    # Sort files within each section by sidebar order, then by path
    for section in sections:
        sections[section].sort(key=lambda x: (x[0], x[1]))

    # Build ordered list of (section_name, files) tuples
    result = []

    # First, add sections in preferred order
    for section in SECTION_ORDER:
        if section in sections:
            # Convert section slug to display name
            display_name = section.replace("-", " ").title()
            files = [f[1] for f in sections[section]]
            result.append((display_name, files))
            del sections[section]

    # Then add any remaining sections alphabetically
    for section in sorted(sections.keys()):
        if section != "root":
            display_name = section.replace("-", " ").title()
            files = [f[1] for f in sections[section]]
            result.append((display_name, files))

    # Handle root-level files last
    if "root" in sections:
        files = [f[1] for f in sections["root"]]
        if files:
            result.append(("Other", files))

    return result


def extract_title(content):
    """Extract title from frontmatter."""
    match = re.search(r'^---\s*\n.*?title:\s*["\']?([^"\'\n]+)["\']?.*?\n---', content, re.DOTALL)
    return match.group(1).strip() if match else "Untitled"


def process_markdown(content):
    """Process markdown content for plain text output."""
    # Remove frontmatter
    content = re.sub(r'^---\s*\n.*?\n---\s*\n', '', content, flags=re.DOTALL)

    # Remove MDX imports
    content = re.sub(r'^import\s+.*?[\'"];?\s*$', '', content, flags=re.MULTILINE)
    content = re.sub(r'^import\s*\{[^}]*\}\s*from\s*[\'"][^\'"]*[\'"];?\s*$', '', content, flags=re.MULTILINE)

    # Convert Starlight Card components to text
    content = re.sub(r'<Card\s+title="([^"]+)"[^>]*>', r'\n**\1**\n\n', content)
    content = re.sub(r'<Card\s+title=\'([^\']+)\'[^>]*>', r'\n**\1**\n\n', content)
    content = re.sub(r'</Card>', '\n', content)
    content = re.sub(r'<CardGrid[^>]*>', '', content)
    content = re.sub(r'</CardGrid>', '', content)

    # Remove JSX/React component blocks (interactive calculators, etc.)
    def remove_jsx_block(text):
        result = []
        i = 0
        while i < len(text):
            match = re.match(r'<div\s+id="[^"]*"[^>]*>', text[i:])
            if match:
                depth = 1
                j = i + len(match.group(0))
                while j < len(text) and depth > 0:
                    if text[j:j+4] == '<div':
                        depth += 1
                        j += 4
                    elif text[j:j+6] == '</div>':
                        depth -= 1
                        j += 6
                    else:
                        j += 1
                result.append('\n[Interactive component - see web version]\n')
                i = j
            else:
                result.append(text[i])
                i += 1
        return ''.join(result)

    content = remove_jsx_block(content)

    # Remove style/script blocks
    content = re.sub(r'<style[^>]*>[\s\S]*?</style>', '', content)
    content = re.sub(r'<script[^>]*>[\s\S]*?</script>', '', content)

    # Convert HTML elements to text
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

    # Convert mermaid diagrams to text description
    def describe_mermaid(match):
        mermaid_code = match.group(1)
        # Extract first line as diagram type
        first_line = mermaid_code.strip().split('\n')[0]
        return f'\n[Diagram: {first_line}]\n'

    content = re.sub(r'```mermaid\s*\n(.*?)```', describe_mermaid, content, flags=re.DOTALL)

    # Clean up multiple blank lines
    content = re.sub(r'\n{4,}', '\n\n\n', content)

    return content.strip()


def build_llms_full():
    """Build the complete llms-full.txt file."""
    output_parts = []

    # Get version info
    version = get_version_string()
    date = datetime.now().strftime("%Y-%m-%d")

    # Header
    output_parts.append("# Delegation Risk Framework - Complete Documentation")
    output_parts.append("")
    output_parts.append(f"> Version: {version} | Generated: {date}")
    output_parts.append(">")
    output_parts.append("> A structured approach to managing risk in delegation relationships,")
    output_parts.append("> with AI systems as the primary application.")
    output_parts.append("")
    output_parts.append("Website: https://delegation-risk.org")
    output_parts.append("GitHub: https://github.com/quantified-uncertainty/delegation-risk-framework")
    output_parts.append("")
    output_parts.append("=" * 80)
    output_parts.append("")

    # Auto-discover all docs
    sections = discover_docs()

    # Process each section
    for section_name, files in sections:
        print(f"Processing: {section_name} ({len(files)} files)")
        output_parts.append(f"\n{'=' * 80}")
        output_parts.append(f"PART: {section_name.upper()}")
        output_parts.append(f"{'=' * 80}\n")

        for file_path in files:
            full_path = DOCS_DIR / file_path

            content = full_path.read_text(encoding='utf-8')
            title = extract_title(content)
            processed = process_markdown(content)

            output_parts.append(f"\n{'-' * 60}")
            output_parts.append(f"## {title}")
            output_parts.append(f"Source: {file_path}")
            output_parts.append(f"{'-' * 60}\n")
            output_parts.append(processed)
            output_parts.append("")

    # Write output
    output_content = '\n'.join(output_parts)
    OUTPUT_FULL.write_text(output_content)

    # Stats
    word_count = len(output_content.split())
    line_count = output_content.count('\n')
    file_count = sum(len(files) for _, files in sections)

    print(f"\nGenerated: {OUTPUT_FULL}")
    print(f"  {word_count:,} words")
    print(f"  {line_count:,} lines")
    print(f"  {file_count} source files")
    print(f"  {len(output_content):,} characters")


def build_llms_core():
    """Build llms-core.txt with just essential pages for chat context."""
    output_parts = []

    # Get version info
    version = get_version_string()
    date = datetime.now().strftime("%Y-%m-%d")

    # Header
    output_parts.append("# Delegation Risk Framework - Core Documentation")
    output_parts.append("")
    output_parts.append(f"> Version: {version} | Generated: {date}")
    output_parts.append(">")
    output_parts.append("> Essential pages for understanding the framework.")
    output_parts.append("> For complete documentation, see: https://delegation-risk.org")
    output_parts.append("")
    output_parts.append("=" * 80)
    output_parts.append("")

    # Process core pages
    processed_count = 0
    for file_path in CORE_PAGES:
        full_path = DOCS_DIR / file_path

        if not full_path.exists():
            print(f"  Warning: {file_path} not found")
            continue

        content = full_path.read_text(encoding='utf-8')
        title = extract_title(content)
        processed = process_markdown(content)

        output_parts.append(f"\n{'-' * 60}")
        output_parts.append(f"## {title}")
        output_parts.append(f"Source: {file_path}")
        output_parts.append(f"{'-' * 60}\n")
        output_parts.append(processed)
        output_parts.append("")
        processed_count += 1

    # Write output
    output_content = '\n'.join(output_parts)
    OUTPUT_CORE.write_text(output_content)

    # Stats
    word_count = len(output_content.split())
    char_count = len(output_content)
    approx_tokens = char_count // 4  # rough estimate

    print(f"\nGenerated: {OUTPUT_CORE}")
    print(f"  {word_count:,} words")
    print(f"  {char_count:,} characters (~{approx_tokens:,} tokens)")
    print(f"  {processed_count} source files")


if __name__ == "__main__":
    print("Building llms-core.txt (essential pages)...")
    build_llms_core()
    print()
    print("Building llms-full.txt (complete documentation)...")
    build_llms_full()
