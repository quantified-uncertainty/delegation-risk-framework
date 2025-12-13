// @ts-check
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';
import mermaid from 'astro-mermaid';

// https://astro.build/config
export default defineConfig({
	integrations: [
		mermaid(),
		starlight({
			title: 'AI Safety Framework',
			components: {
				Footer: './src/components/Footer.astro',
			},
			social: [
				{ icon: 'github', label: 'GitHub', href: 'https://github.com/ozziegooen/trust-website' },
			],
			sidebar: [
				{
					label: 'Overview',
					collapsed: true,
					items: [
						{ label: 'Home', slug: 'index' },
						{ label: 'Introduction', slug: 'overview/introduction' },
						{ label: 'Core Concepts', slug: 'overview/core-concepts' },
						{ label: 'Principles to Practice', slug: 'overview/principles-to-practice' },
						{ label: 'Glossary', slug: 'overview/glossary' },
					],
				},
				{
					label: 'Principles',
					collapsed: true,
					autogenerate: { directory: 'principles' },
				},
				{
					label: 'Architecture',
					collapsed: true,
					autogenerate: { directory: 'architecture' },
				},
				{
					label: 'Trust Calculus',
					collapsed: true,
					autogenerate: { directory: 'trust-calculus' },
				},
				{
					label: 'Risk Budgeting',
					collapsed: true,
					autogenerate: { directory: 'risk-budgeting' },
				},
				{
					label: 'Implementation',
					collapsed: true,
					autogenerate: { directory: 'implementation' },
				},
				{
					label: 'Applications',
					collapsed: true,
					autogenerate: { directory: 'applications' },
				},
				{
					label: 'Background Research',
					collapsed: true,
					autogenerate: { directory: 'background-research' },
				},
				{
					label: 'Notes',
					collapsed: true,
					autogenerate: { directory: 'notes' },
				},
			],
		}),
	],
});
