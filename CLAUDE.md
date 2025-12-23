# Project Guide for Claude

## Overview

This is the **Delegation Risk Framework** website - a documentation site about managing risk in delegation relationships, with applications to AI safety.

Built with Astro + Starlight. 162 pages of documentation.

## Key Commands

```bash
pnpm dev          # Start dev server (usually port 4321)
pnpm build        # Build site (runs Pagefind for search)
```

## Build Artifacts

### Version Management
- `version.json` - Auto-increments patch when content changes
- Run `python3 scripts/build-pdf.py` to bump version and rebuild PDF/EPUB

### Generated Files
- `scripts/build-pdf.py` - Builds PDF and EPUB from markdown using Pandoc + XeLaTeX
- `scripts/build-llms-txt.py` - Builds `/public/llms-core.txt` and `/public/llms-full.txt`
- PDF/EPUB are generated locally (no GitHub Action yet)

## Content Structure

```
src/content/docs/
├── getting-started/     # Intro, FAQ, glossary
├── delegation-risk/     # Core framework theory
├── power-dynamics/      # Agent power formalization
├── entanglements/       # 26 pages on component correlation
│   ├── fundamentals/    # Types, challenges, definitions
│   ├── detection/       # Metrics, detecting influence
│   ├── mitigation/      # Solutions, audit guides
│   ├── research/        # Academic connections
│   ├── case-studies/    # Historical examples
│   └── cross-domain/    # Org patterns, psychology
├── design-patterns/     # 28 implementation patterns
├── case-studies/        # AI and human system examples
├── research/            # Theoretical foundations
├── experimental/        # Probabilistic estimation tools
└── reference/           # Bibliography, roadmap
```

## Style Guidelines

### Content
- Accessible "informed practitioner" voice
- No unnecessary code blocks or mathematical notation
- Tables for comparisons, not formulas
- Keep files focused - if > 300 lines, consider splitting
- Avoid redundancy across files - use cross-references

### Entanglements Section (Recently Cleaned)
- Heavily trimmed in Dec 2024 (3800 lines removed)
- Code and formulas replaced with plain English
- Historical examples condensed
- If adding content, keep it concise

## Common Tasks

### After Editing Content
1. Run `pnpm build` to verify
2. Run `python3 scripts/build-llms-txt.py` to update llms.txt
3. Version auto-bumps on next PDF build

### Reorganizing Sections
1. Move files to new directories
2. Update `astro.config.mjs` sidebar configuration
3. Run `sed` to update internal links across all files
4. Verify build succeeds

## Notes

- Site uses KaTeX for math rendering (via `remark-math` + `rehype-katex`)
- Mermaid diagrams supported via `astro-mermaid`
- Interactive components use React (Squiggle, XYFlow)
