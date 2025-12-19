#!/usr/bin/env node
/**
 * Generate a book-style PDF from markdown content
 * Uses Puppeteer for PDF generation with proper print styling
 */

import { readFileSync, writeFileSync, readdirSync, statSync } from 'fs';
import { join, basename } from 'path';
import { execSync } from 'child_process';

// Sidebar order from astro.config.mjs (simplified extraction)
const sidebarOrder = [
  // Overview
  'src/content/docs/index.mdx',
  'src/content/docs/overview/introduction.md',
  'src/content/docs/overview/core-concepts.md',
  'src/content/docs/overview/glossary.md',

  // Delegation Risk Theory
  'src/content/docs/delegation-risk/overview.md',
  'src/content/docs/delegation-risk/walkthrough.md',
  'src/content/docs/delegation-risk/delegation-accounting.md',
  'src/content/docs/delegation-risk/risk-decomposition.md',
  'src/content/docs/delegation-risk/exposure-cascade.md',
  'src/content/docs/delegation-risk/insurers-dilemma.md',

  // Anomaly Chronicles (auto-ordered)
  'src/content/docs/delegation-risk/anomaly-chronicles/index.md',
  'src/content/docs/delegation-risk/anomaly-chronicles/power-struggles.md',
  'src/content/docs/delegation-risk/anomaly-chronicles/containing-mr-x.md',
  'src/content/docs/delegation-risk/anomaly-chronicles/five-years-later.md',
  'src/content/docs/delegation-risk/anomaly-chronicles/task-architecture.md',
  'src/content/docs/delegation-risk/anomaly-chronicles/year-ten.md',
  'src/content/docs/delegation-risk/anomaly-chronicles/mr-x-perspective.md',
];

// Get all markdown files if we want the full book
function getAllMarkdownFiles(dir, files = []) {
  const items = readdirSync(dir);
  for (const item of items) {
    const fullPath = join(dir, item);
    if (statSync(fullPath).isDirectory()) {
      getAllMarkdownFiles(fullPath, files);
    } else if (item.endsWith('.md') || item.endsWith('.mdx')) {
      files.push(fullPath);
    }
  }
  return files;
}

// Extract title from frontmatter
function extractTitle(content) {
  const match = content.match(/^---\s*\n[\s\S]*?title:\s*['"]?([^'"\n]+)['"]?[\s\S]*?\n---/);
  return match ? match[1].trim() : 'Untitled';
}

// Strip frontmatter and MDX components
function processMarkdown(content) {
  // Remove frontmatter
  content = content.replace(/^---[\s\S]*?---\n/, '');

  // Remove MDX imports
  content = content.replace(/^import\s+.*$/gm, '');

  // Convert MDX components to styled divs
  content = content.replace(/<Card\s+title="([^"]+)"[^>]*icon="[^"]*"[^>]*>/g, '\n**$1**\n');
  content = content.replace(/<\/Card>/g, '\n');
  content = content.replace(/<CardGrid>/g, '');
  content = content.replace(/<\/CardGrid>/g, '');

  // Handle Starlight asides/callouts
  content = content.replace(/:::(tip|note|caution|danger|info)(?:\[([^\]]*)\])?\n([\s\S]*?):::/g,
    (_, type, title, body) => `> **${title || type.toUpperCase()}:** ${body.trim()}\n`);

  // Handle mermaid code blocks - convert to placeholder
  content = content.replace(/```mermaid[\s\S]*?```/g, '\n*[Diagram - see web version]*\n');

  return content;
}

// Convert markdown to HTML
function markdownToHtml(markdown) {
  // Basic markdown to HTML conversion
  let html = markdown;

  // Headers
  html = html.replace(/^######\s+(.*)$/gm, '<h6>$1</h6>');
  html = html.replace(/^#####\s+(.*)$/gm, '<h5>$1</h5>');
  html = html.replace(/^####\s+(.*)$/gm, '<h4>$1</h4>');
  html = html.replace(/^###\s+(.*)$/gm, '<h3>$1</h3>');
  html = html.replace(/^##\s+(.*)$/gm, '<h2>$1</h2>');
  html = html.replace(/^#\s+(.*)$/gm, '<h1>$1</h1>');

  // Bold and italic
  html = html.replace(/\*\*\*([^*]+)\*\*\*/g, '<strong><em>$1</em></strong>');
  html = html.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');
  html = html.replace(/\*([^*]+)\*/g, '<em>$1</em>');

  // Code blocks
  html = html.replace(/```(\w*)\n([\s\S]*?)```/g, '<pre><code class="language-$1">$2</code></pre>');
  html = html.replace(/`([^`]+)`/g, '<code>$1</code>');

  // Blockquotes
  html = html.replace(/^>\s+(.*)$/gm, '<blockquote>$1</blockquote>');

  // Lists
  html = html.replace(/^[-*]\s+(.*)$/gm, '<li>$1</li>');
  html = html.replace(/(<li>.*<\/li>\n?)+/g, '<ul>$&</ul>');

  // Numbered lists
  html = html.replace(/^\d+\.\s+(.*)$/gm, '<li>$1</li>');

  // Links
  html = html.replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2">$1</a>');

  // Paragraphs (lines not already tagged)
  html = html.replace(/^(?!<[hupablo])(.+)$/gm, '<p>$1</p>');

  // Clean up empty paragraphs
  html = html.replace(/<p>\s*<\/p>/g, '');

  // Horizontal rules
  html = html.replace(/^---$/gm, '<hr>');

  return html;
}

// Generate the full HTML document
function generateBookHtml(files) {
  let chapters = [];

  for (const filePath of files) {
    try {
      const content = readFileSync(filePath, 'utf-8');
      const title = extractTitle(content);
      const processed = processMarkdown(content);
      const html = markdownToHtml(processed);

      chapters.push({
        title,
        path: filePath,
        html
      });
    } catch (e) {
      console.error(`Error processing ${filePath}:`, e.message);
    }
  }

  const bookHtml = `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Delegation Risk Framework</title>
  <style>
    @page {
      size: letter;
      margin: 0.75in 0.75in 1in 0.75in;

      @top-center {
        content: "Delegation Risk Framework";
        font-size: 9pt;
        color: #666;
      }

      @bottom-center {
        content: counter(page);
        font-size: 9pt;
      }
    }

    @page :first {
      @top-center { content: none; }
    }

    * {
      box-sizing: border-box;
    }

    body {
      font-family: 'Georgia', 'Times New Roman', serif;
      font-size: 11pt;
      line-height: 1.5;
      color: #1a1a1a;
      max-width: 100%;
    }

    /* Title page */
    .title-page {
      page-break-after: always;
      text-align: center;
      padding-top: 3in;
    }

    .title-page h1 {
      font-size: 28pt;
      color: #2563eb;
      margin-bottom: 0.5in;
      border: none;
    }

    .title-page .subtitle {
      font-size: 14pt;
      color: #666;
      font-style: italic;
    }

    /* Table of contents */
    .toc {
      page-break-after: always;
    }

    .toc h2 {
      color: #2563eb;
      border-bottom: 2px solid #2563eb;
    }

    .toc ul {
      list-style: none;
      padding-left: 0;
    }

    .toc li {
      margin: 0.3em 0;
      padding-left: 1em;
    }

    .toc a {
      color: #1a1a1a;
      text-decoration: none;
    }

    /* Chapters */
    .chapter {
      page-break-before: always;
    }

    .chapter:first-of-type {
      page-break-before: auto;
    }

    /* Headers with colors */
    h1 {
      font-size: 20pt;
      color: #1e40af;
      border-bottom: 3px solid #3b82f6;
      padding-bottom: 0.3em;
      margin-top: 0;
      margin-bottom: 0.8em;
    }

    h2 {
      font-size: 16pt;
      color: #1e3a8a;
      border-bottom: 2px solid #60a5fa;
      padding-bottom: 0.2em;
      margin-top: 1.2em;
      margin-bottom: 0.6em;
    }

    h3 {
      font-size: 13pt;
      color: #1e40af;
      margin-top: 1em;
      margin-bottom: 0.4em;
    }

    h4 {
      font-size: 11pt;
      color: #3730a3;
      margin-top: 0.8em;
      margin-bottom: 0.3em;
    }

    p {
      margin: 0.5em 0;
      text-align: justify;
      hyphens: auto;
    }

    /* Lists */
    ul, ol {
      margin: 0.5em 0;
      padding-left: 1.5em;
    }

    li {
      margin: 0.2em 0;
    }

    /* Code */
    code {
      font-family: 'Consolas', 'Monaco', monospace;
      font-size: 9pt;
      background: #f3f4f6;
      padding: 0.1em 0.3em;
      border-radius: 3px;
    }

    pre {
      background: #1f2937;
      color: #e5e7eb;
      padding: 0.8em;
      border-radius: 4px;
      overflow-x: auto;
      font-size: 9pt;
      line-height: 1.4;
      margin: 0.8em 0;
    }

    pre code {
      background: none;
      padding: 0;
      color: inherit;
    }

    /* Blockquotes / callouts */
    blockquote {
      margin: 0.8em 0;
      padding: 0.6em 1em;
      border-left: 4px solid #3b82f6;
      background: #eff6ff;
      font-style: normal;
    }

    blockquote p {
      margin: 0;
    }

    /* Tables */
    table {
      width: 100%;
      border-collapse: collapse;
      margin: 0.8em 0;
      font-size: 10pt;
    }

    th, td {
      border: 1px solid #d1d5db;
      padding: 0.4em 0.6em;
      text-align: left;
    }

    th {
      background: #f3f4f6;
      font-weight: bold;
    }

    /* Links */
    a {
      color: #2563eb;
      text-decoration: none;
    }

    /* Horizontal rule */
    hr {
      border: none;
      border-top: 1px solid #d1d5db;
      margin: 1.5em 0;
    }

    /* Print optimizations */
    @media print {
      .chapter {
        page-break-before: always;
      }

      h1, h2, h3, h4 {
        page-break-after: avoid;
      }

      pre, blockquote, table {
        page-break-inside: avoid;
      }
    }
  </style>
</head>
<body>
  <!-- Title Page -->
  <div class="title-page">
    <h1>Delegation Risk Framework</h1>
    <p class="subtitle">A structured approach to managing risk in delegation relationships</p>
  </div>

  <!-- Table of Contents -->
  <div class="toc">
    <h2>Table of Contents</h2>
    <ul>
      ${chapters.map((ch, i) => `<li>${i + 1}. ${ch.title}</li>`).join('\n      ')}
    </ul>
  </div>

  <!-- Chapters -->
  ${chapters.map((ch, i) => `
  <div class="chapter" id="chapter-${i + 1}">
    <h1>${ch.title}</h1>
    ${ch.html}
  </div>
  `).join('\n')}
</body>
</html>`;

  return bookHtml;
}

// Main
const allFiles = getAllMarkdownFiles('src/content/docs');
console.log(`Found ${allFiles.length} markdown files`);

// Use sidebar order for main content, or all files
const filesToProcess = sidebarOrder.filter(f => {
  try {
    readFileSync(f);
    return true;
  } catch {
    return false;
  }
});

console.log(`Processing ${filesToProcess.length} files in sidebar order`);

const html = generateBookHtml(filesToProcess);
writeFileSync('book-output.html', html);
console.log('Generated book-output.html');
console.log('To generate PDF, run: npx puppeteer-cli print book-output.html book.pdf');
