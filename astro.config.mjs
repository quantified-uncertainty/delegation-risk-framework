// @ts-check
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';
import mermaid from 'astro-mermaid';

// https://astro.build/config
export default defineConfig({
	integrations: [
		mermaid(),
		starlight({
			title: 'Delegation Risk Framework',
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
						{ label: 'Glossary', slug: 'overview/glossary' },
					],
				},
				{
					label: 'Delegation Risk Theory',
					collapsed: true,
					items: [
						{ label: 'Overview', slug: 'delegation-risk/overview' },
						{ label: 'Walkthrough: The $1,000 Delivery', slug: 'delegation-risk/walkthrough' },
						{ label: 'Delegation Accounting', slug: 'delegation-risk/delegation-accounting' },
						{ label: 'Risk Decomposition', slug: 'delegation-risk/risk-decomposition' },
						{ label: 'Exposure Cascade', slug: 'delegation-risk/exposure-cascade' },
						{ label: "The Insurer's Dilemma", slug: 'delegation-risk/insurers-dilemma' },
						{
							label: 'The Anomaly Chronicles',
							collapsed: true,
							autogenerate: { directory: 'delegation-risk/anomaly-chronicles' },
						},
						{
							label: 'Technical Reference',
							collapsed: true,
							autogenerate: { directory: 'delegation-risk/reference' },
						},
						{
							label: 'Theoretical Foundations',
							collapsed: true,
							autogenerate: { directory: 'delegation-risk/theory' },
						},
					],
				},
				{
					label: 'Cross-Domain Methods',
					collapsed: true,
					autogenerate: { directory: 'risk-budgeting' },
				},
				{
					label: 'Design Principles',
					collapsed: true,
					autogenerate: { directory: 'principles' },
				},
				{
					label: 'Applications',
					collapsed: true,
					autogenerate: { directory: 'applications' },
				},
				{
					label: 'AI Systems',
					collapsed: true,
					items: [
						{ label: 'Principles to Practice', slug: 'overview/principles-to-practice' },
						{ label: 'Architecture Overview', slug: 'architecture/decomposed-coordination' },
						{ label: 'Safety Mechanisms', slug: 'architecture/safety-mechanisms' },
						{ label: 'Forecasting Navigation', slug: 'architecture/forecasting-navigation' },
						{
							label: 'Worked Examples',
							collapsed: true,
							items: [
								{ label: 'Research Assistant', slug: 'architecture/research-assistant-example' },
								{ label: 'Code Deployment', slug: 'architecture/code-deployment-example' },
								{ label: 'Healthcare Bot', slug: 'architecture/healthcare-bot-example' },
								{ label: 'Trading System', slug: 'architecture/trading-system-example' },
							],
						},
					],
				},
				{
					label: 'Implementation',
					collapsed: true,
					autogenerate: { directory: 'implementation' },
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
