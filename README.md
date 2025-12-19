# Delegation Risk Framework

A structured approach to managing risk in delegation relationships—with AI systems as the primary application.

**[Read Online](https://delegation-risk.org)** | **[Download PDF](https://github.com/quantified-uncertainty/delegation-risk-framework/releases/latest/download/delegation-risk-framework-book.pdf)** | **[Download EPUB](https://github.com/quantified-uncertainty/delegation-risk-framework/releases/latest/download/delegation-risk-framework-book.epub)**

## Overview

Every delegation involves risk. When you delegate a task—to an employee, a contractor, a software system, or an AI agent—you're accepting potential downside in exchange for capability.

This framework proposes **structural constraints** as the foundation for managing delegation risk:

- **Delegation Risk** = Σ P(harm) × Damage — quantify what you're betting on each delegate
- **Decomposition** — many limited components instead of one powerful delegate
- **Least-X Principles** — minimize capability, context, autonomy, connectivity
- **Cross-domain methods** — adapt proven approaches from nuclear safety, finance, and mechanism design

## Documentation Structure

| Section | Description |
|---------|-------------|
| **Getting Started** | Introduction, core concepts, FAQ, glossary |
| **The Framework** | Delegation risk theory, accounting, decomposition |
| **Applying the Framework** | Principles, architecture, worked examples, tools |
| **Cross-Domain Methods** | Finance, nuclear safety, mechanism design |
| **Case Studies** | AI systems, human systems, Anomaly Chronicles |
| **Deep Dives** | Theoretical foundations, research background |
| **Reference** | Bibliography, protocols, roadmap |

## Stats

- ~100,000 words of content
- 99 documentation pages
- 146 diagrams

## Development

This is an [Astro](https://astro.build/) site using [Starlight](https://starlight.astro.build/).

```bash
# Install dependencies
pnpm install

# Start dev server
pnpm dev

# Build for production
pnpm build
```

## Generating PDF/EPUB

The documentation can be exported as a PDF or EPUB book.

### Prerequisites

```bash
# macOS
brew install pandoc
brew install --cask basictex  # or mactex for full install
npm install -g @mermaid-js/mermaid-cli
```

### Generate

```bash
python3 scripts/build-pdf.py
```

This generates:
- `delegation-risk-framework-book.pdf` (~9 MB)
- `delegation-risk-framework-book.epub` (~9 MB)

Features:
- Proper sidebar ordering matching the website
- Pre-rendered Mermaid diagrams
- Internal links converted to PDF anchors
- External links as footnotes (print-friendly)
- Colored headers, running page headers
- Custom EPUB styling

## Project Structure

```
src/content/docs/
├── getting-started/     # Introduction, core concepts, FAQ
├── framework/           # Delegation risk theory
├── applying/            # Principles, examples, tools
│   ├── examples/        # Worked examples
│   └── tools/           # Interactive calculators
├── cross-domain-methods/# Finance, nuclear, mechanism design
├── case-studies/        # Real-world examples
│   ├── ai-systems/      # Sydney, code review bot, etc.
│   ├── human-systems/   # Organizations, nuclear authority
│   └── anomaly-chronicles/  # Fiction series
├── deep-dives/          # Advanced topics
│   ├── theory/          # Theoretical foundations
│   └── research/        # Background research
└── reference/           # Bibliography, roadmap, protocols
```

## License

Content is available under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).

## Contributing

Contributions welcome! Please open an issue to discuss significant changes before submitting a PR.
