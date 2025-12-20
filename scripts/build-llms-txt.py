#!/usr/bin/env python3
"""
Generate llms-full.txt - complete documentation as plain text for LLM context.
"""

import re
from pathlib import Path

# Project root
ROOT = Path(__file__).parent.parent
DOCS_DIR = ROOT / "src" / "content" / "docs"
OUTPUT_FILE = ROOT / "public" / "llms-full.txt"

# Sidebar order matching astro.config.mjs (same as build-pdf.py)
SIDEBAR_ORDER = [
    ("Getting Started", [
        "getting-started/index.md",
        "getting-started/five-minute-intro.md",
        "getting-started/core-concepts.md",
        "getting-started/introduction.md",
        "getting-started/faq.md",
        "getting-started/glossary.md",
    ]),
    ("The Framework", [
        "framework/overview.md",
        "framework/walkthrough.md",
        "framework/delegation-accounting.md",
        "framework/risk-decomposition.md",
        "framework/exposure-cascade.md",
        "framework/insurers-dilemma.md",
    ]),
    ("Applying the Framework", [
        "applying/index.md",
        "applying/principles-to-practice.md",
        "applying/decomposed-coordination.md",
        "applying/safety-mechanisms.md",
        "applying/forecasting-navigation.md",
        "applying/least-x-principles.md",
        "applying/coordinator-constraints.md",
        "applying/examples/research-assistant-example.md",
        "applying/examples/code-deployment-example.md",
        "applying/examples/trading-system-example.md",
        "applying/examples/healthcare-bot-example.md",
        "applying/tools/quick-start.md",
        "applying/tools/decision-guide.md",
        "applying/tools/delegation-risk-calculator.mdx",
        "applying/tools/trust-propagation.mdx",
        "applying/tools/tradeoff-frontier.mdx",
        "applying/tools/cost-benefit.md",
        "applying/tools/empirical-tests.md",
    ]),
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
    ]),
    ("Case Studies", [
        "case-studies/index.md",
        "case-studies/ai-systems/case-study-sydney.md",
        "case-studies/ai-systems/case-study-success.md",
        "case-studies/ai-systems/case-study-near-miss.md",
        "case-studies/ai-systems/case-study-drift.md",
        "case-studies/ai-systems/anti-patterns.md",
        "case-studies/human-systems/organizational-trust.md",
        "case-studies/human-systems/nuclear-launch-authority.md",
        "case-studies/human-systems/criminal-trust.md",
        "case-studies/human-systems/jury-trust.md",
        "case-studies/human-systems/open-source-trust.md",
        "case-studies/human-systems/oversight-dilemma.md",
        "case-studies/human-systems/trust-across-civilizations.md",
        "case-studies/anomaly-chronicles/index.md",
        "case-studies/anomaly-chronicles/power-struggles.md",
        "case-studies/anomaly-chronicles/containing-mr-x.md",
        "case-studies/anomaly-chronicles/five-years-later.md",
        "case-studies/anomaly-chronicles/task-architecture.md",
        "case-studies/anomaly-chronicles/year-ten.md",
        "case-studies/anomaly-chronicles/mr-x-perspective.md",
    ]),
    ("Deep Dives", [
        "deep-dives/index.md",
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
        "deep-dives/research/index.md",
        "deep-dives/research/ai-safety-frameworks.md",
        "deep-dives/research/mechanism-design.md",
        "deep-dives/research/nuclear-aerospace-deep-dive.md",
        "deep-dives/research/financial-risk-budgeting.md",
        "deep-dives/research/fidelity-insurance.md",
        "deep-dives/research/compositional-risk-measures.md",
        "deep-dives/research/correlated-failure-modeling.md",
        "deep-dives/research/linear-logic-trust-budgets.md",
        "deep-dives/research/formal-verification-limits.md",
        "deep-dives/research/runtime-monitoring-architectures.md",
        "deep-dives/research/capability-elicitation-sandbagging.md",
        "deep-dives/research/steganography-detection-prevention.md",
        "deep-dives/research/empirical-scheming-reduction.md",
        "deep-dives/research/human-trust-calibration.md",
        "deep-dives/research/trust-dynamics-adversarial-pressure.md",
        "deep-dives/research/alignment-tax-quantification.md",
        "deep-dives/research/byzantine-coordinator-voting.md",
        "deep-dives/research/prototype-architecture-feasibility.md",
        "deep-dives/research/potential-projects.md",
    ]),
    ("Reference", [
        "reference/index.md",
        "reference/bibliography.md",
        "reference/related-approaches.md",
        "reference/protocol-catalog.md",
        "reference/roadmap.md",
    ]),
]


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

    # Header
    output_parts.append("# Delegation Risk Framework - Complete Documentation")
    output_parts.append("")
    output_parts.append("> A structured approach to managing risk in delegation relationships,")
    output_parts.append("> with AI systems as the primary application.")
    output_parts.append("")
    output_parts.append("Website: https://delegation-risk.org")
    output_parts.append("GitHub: https://github.com/quantified-uncertainty/delegation-risk-framework")
    output_parts.append("")
    output_parts.append("=" * 80)
    output_parts.append("")

    # Process each section
    for section_name, files in SIDEBAR_ORDER:
        print(f"Processing: {section_name}")
        output_parts.append(f"\n{'=' * 80}")
        output_parts.append(f"PART: {section_name.upper()}")
        output_parts.append(f"{'=' * 80}\n")

        for file_path in files:
            full_path = DOCS_DIR / file_path
            if not full_path.exists():
                # Try .mdx extension
                mdx_path = full_path.with_suffix('.mdx')
                if mdx_path.exists():
                    full_path = mdx_path
                else:
                    print(f"  Warning: {file_path} not found")
                    continue

            content = full_path.read_text()
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
    OUTPUT_FILE.write_text(output_content)

    # Stats
    word_count = len(output_content.split())
    line_count = output_content.count('\n')
    file_count = sum(len(files) for _, files in SIDEBAR_ORDER)

    print(f"\nGenerated: {OUTPUT_FILE}")
    print(f"  {word_count:,} words")
    print(f"  {line_count:,} lines")
    print(f"  {file_count} source files")
    print(f"  {len(output_content):,} characters")


if __name__ == "__main__":
    build_llms_full()
