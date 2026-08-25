import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

const work = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/work' }),
  schema: z.object({
    title: z.string(),
    slug: z.string(),
    summary: z.string(),
    company: z.string(),
    role: z.string(),
    year: z.string(),
    duration: z.string().optional(),
    featured: z.boolean().default(false),
    coverImage: z.string().optional(),
    coverAlt: z.string().optional(),
    outcome: z.string().optional(),
    mediumUrl: z.string().url().optional(),
    order: z.number(),
    kind: z.enum(['hamgozar', 'asroon', 'football360', 'placeholder']).default('placeholder'),
  }),
});

export const collections = { work };
