import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';

export default defineConfig({
  site: 'https://thundergate.io',
  integrations: [
    sitemap({
      // /og/ is the social-card render target; not for indexing.
      filter: (page) => !page.includes('/og/'),
    }),
  ],
});
