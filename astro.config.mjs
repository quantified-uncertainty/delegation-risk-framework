// @ts-check
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';
import mermaid from 'astro-mermaid';
import react from '@astrojs/react';

// https://astro.build/config
export default defineConfig({
	integrations: [
		react(),
		mermaid(),
		starlight({
			title: 'Delegation Risk',
			components: {
				Footer: './src/components/Footer.astro',
			},
			social: [
				{ icon: 'document', label: 'Download PDF', href: 'https://github.com/quantified-uncertainty/delegation-risk-framework/releases/latest/download/delegation-risk-framework-book.pdf' },
				{ icon: 'github', label: 'GitHub', href: 'https://github.com/quantified-uncertainty/delegation-risk-framework' },
			],
			sidebar: [
				{
					label: 'Getting Started',
					collapsed: false,
					autogenerate: { directory: 'getting-started' },
				},
				{
					label: 'The Framework',
					collapsed: true,
					autogenerate: { directory: 'framework' },
				},
				{
					label: 'Applying the Framework',
					collapsed: true,
					items: [
						{ label: 'Overview', slug: 'applying' },
						{ label: 'Principles to Practice', slug: 'applying/principles-to-practice' },
						{ label: 'Architecture Overview', slug: 'applying/decomposed-coordination' },
						{ label: 'Safety Mechanisms', slug: 'applying/safety-mechanisms' },
						{ label: 'Forecasting & Navigation', slug: 'applying/forecasting-navigation' },
						{ label: 'Least-X Principles', slug: 'applying/least-x-principles' },
						{ label: 'Coordinator Constraints', slug: 'applying/coordinator-constraints' },
						{
							label: 'Worked Examples',
							collapsed: true,
							autogenerate: { directory: 'applying/examples' },
						},
						{
							label: 'Tools & Guides',
							collapsed: true,
							autogenerate: { directory: 'applying/tools' },
						},
					],
				},
				{
					label: 'Cross-Domain Methods',
					collapsed: true,
					autogenerate: { directory: 'cross-domain-methods' },
				},
				{
					label: 'Case Studies',
					collapsed: true,
					items: [
						{ label: 'Overview', slug: 'case-studies' },
						{
							label: 'AI Systems',
							collapsed: true,
							autogenerate: { directory: 'case-studies/ai-systems' },
						},
						{
							label: 'Human Systems',
							collapsed: true,
							autogenerate: { directory: 'case-studies/human-systems' },
						},
						{
							label: 'The Anomaly Chronicles',
							collapsed: true,
							autogenerate: { directory: 'case-studies/anomaly-chronicles' },
						},
					],
				},
				{
					label: 'Deep Dives',
					collapsed: true,
					items: [
						{ label: 'Overview', slug: 'deep-dives' },
						{
							label: 'Theoretical Foundations',
							collapsed: true,
							autogenerate: { directory: 'deep-dives/theory' },
						},
						{
							label: 'Background Research',
							collapsed: true,
							items: [
								{ label: 'Overview', slug: 'deep-dives/research' },
								{
									label: 'Risk & Financial Methods',
									collapsed: true,
									autogenerate: { directory: 'deep-dives/research/risk-methods' },
								},
								{
									label: 'Technical Safety',
									collapsed: true,
									autogenerate: { directory: 'deep-dives/research/technical-safety' },
								},
								{
									label: 'System Design',
									collapsed: true,
									autogenerate: { directory: 'deep-dives/research/system-design' },
								},
								{
									label: 'Trust & Behavior',
									collapsed: true,
									autogenerate: { directory: 'deep-dives/research/trust-behavior' },
								},
								{ label: 'Hierarchy Visualization', slug: 'deep-dives/research/hierarchy-visualization' },
								{ label: 'Potential Projects', slug: 'deep-dives/research/potential-projects' },
							],
						},
					],
				},
				{
					label: 'Experimental',
					collapsed: true,
					items: [
						{ label: 'Overview', slug: 'experimental' },
						{
							label: 'Probabilistic Estimation',
							collapsed: true,
							items: [
								{ label: 'Overview', slug: 'experimental/probabilistic-estimation' },
								{
									label: 'Interactive Tools',
									collapsed: true,
									autogenerate: { directory: 'experimental/probabilistic-estimation/tools' },
								},
								{
									label: 'Estimates Registry',
									collapsed: true,
									autogenerate: { directory: 'experimental/probabilistic-estimation/estimates' },
								},
							],
						},
					],
				},
				{
					label: 'Reference',
					collapsed: true,
					autogenerate: { directory: 'reference' },
				},
			],
		}),
	],
});
