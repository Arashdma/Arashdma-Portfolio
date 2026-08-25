import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';

const base = process.env.BASE_PATH || '/';

export default defineConfig({
  site: 'https://arashdma.github.io',
  base,
  integrations: [sitemap()],
  build: {
    format: 'directory',
  },
});
