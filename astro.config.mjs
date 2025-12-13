// @ts-check
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';

// https://astro.build/config
export default defineConfig({
	integrations: [
		starlight({
			title: 'AI Safety Framework',
			social: [
				{ icon: 'github', label: 'GitHub', href: 'https://github.com/ozziegooen/trust-website' },
			],
			sidebar: [
				{
					label: 'Overview',
					items: [
						{ label: 'Introduction', slug: 'index' },
					],
				},
				{
					label: 'Trust Calculus',
					autogenerate: { directory: 'trust-calculus' },
				},
				{
					label: 'Principles',
					autogenerate: { directory: 'principles' },
				},
				{
					label: 'Architecture',
					autogenerate: { directory: 'architecture' },
				},
				{
					label: 'Risk Budgeting',
					autogenerate: { directory: 'risk-budgeting' },
				},
				{
					label: 'Implementation',
					autogenerate: { directory: 'implementation' },
				},
			],
		}),
	],
});
