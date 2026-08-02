# Arash DamanAfshan — Portfolio

Personal portfolio website for Arash DamanAfshan, a product designer working across product discovery, UX, interaction design, and design systems.

**Live site:** [arashdma.github.io/Arashdma-Portfolio](https://arashdma.github.io/Arashdma-Portfolio/)

## Built with

- [Astro](https://astro.build/)
- TypeScript
- Plain CSS
- Markdown content collections
- GitHub Pages

## Run locally

```bash
npm install
npm run dev
```

Astro will print the local development URL in the terminal. To create and preview a production build:

```bash
npm run build
npm run preview
```

## Project structure

```text
src/
├── components/       Reusable site components
├── content/work/     Case-study content in Markdown
├── pages/            Homepage and case-study routes
└── styles/           Global design system and responsive styles
public/
├── images/           Profile and project imagery
└── resume/           Downloadable resume
```

## Update the portfolio

### Case studies

Edit or add Markdown files in `src/content/work/`. Each case study uses frontmatter for its title, company, role, year, cover image, external article link, and display order. The shared route in `src/pages/work/[...slug].astro` renders the detail page.

### Profile and experience

Homepage experience entries and social links live in `src/pages/index.astro`. Header and footer navigation are maintained in `src/components/Header.astro` and `src/components/Footer.astro`.

### Images and resume

Place public assets in `public/images/` or `public/resume/`. Files in `public/` are copied directly into the final static build.

## GitHub Pages deployment

The repository includes a GitHub Actions workflow at `.github/workflows/deploy.yml`. Pushes to `main` build the site with the repository base path and deploy the generated `dist/` directory to GitHub Pages.

For a manual static upload, build with the repository base path:

```bash
BASE_PATH=/Arashdma-Portfolio ASTRO_TELEMETRY_DISABLED=1 npm run build
touch dist/.nojekyll
```

Then upload the **contents** of `dist/` to the root of the `main` branch. Do not upload the `dist` folder itself as a nested directory.

## Links

- [LinkedIn](https://www.linkedin.com/in/arashdma/)
- [Medium](https://medium.com/@Arashdma)
- [Dribbble](https://dribbble.com/Arashdma)

## Copyright

© 2026 Arash DamanAfshan. Portfolio content, case studies, and project imagery are not licensed for reuse without permission.
