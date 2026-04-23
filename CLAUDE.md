# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Jekyll 4.4.1 static blog using the [Chirpy](https://github.com/cotes2020/jekyll-theme-chirpy) 7.5.0 theme, hosted on GitHub Pages with the custom domain `www.tonyerwin.com`. Content focuses on AI, cloud architecture, microservices, and modern software engineering.

## Commands

```bash
# Install dependencies (requires rbenv + Ruby 3.3.6)
bundle install

# Start development server
eval "$(rbenv init - bash)"
bundle exec jekyll serve --host 0.0.0.0

# Start with drafts and future posts visible
bundle exec jekyll serve --config _config.yml,_config_local.yml

# Production build
bundle exec jekyll b -d "_site"

# Update gems
bundle update
```

`_config_local.yml` is gitignored. Use it for local overrides such as `show_drafts: true` and `future: true`. The `baseurl` must stay `""` in both local and production since the site uses a custom domain.

## Architecture

The site relies entirely on the upstream Chirpy gem — there are no vendored theme files. Customization happens through a small set of override files:

- `_layouts/default.html` — overrides Chirpy's default layout to inject `custom.css`
- `_includes/head-custom.html` — included by Chirpy's `head.html`; currently injects the custom CSS link
- `assets/css/custom.scss` and `_sass/addon/custom.scss` — both exist as a redundancy; they hide post preview images from appearing in post body content while preserving them for Open Graph/social sharing

**Why the duplicate SCSS?** Chirpy's include path behavior varies, so both files are kept to ensure the custom CSS is always picked up regardless of theme version behavior.

Posts get the `post` layout, comments enabled, TOC enabled, and the permalink `/:year/:month/:title.html` by default via `_config.yml` defaults. Tabs (`_tabs/`) use the `page` layout.

Deployment is fully automated: pushes to `master` trigger `.github/workflows/pages-deploy.yml`, which builds with `JEKYLL_ENV=production` and runs `htmlproofer` (non-blocking) before deploying to GitHub Pages.

## Writing Posts

### File naming
`_posts/YYYY-MM-DD-slug-with-hyphens.md`

### Front matter
```yaml
---
layout: post
title: "Post Title"
date: 'YYYY-MM-DDTHH:MM:SS.000-0600'
description: "SEO-focused description shown in search results and social previews."
tags:
- tag-one
- tag-two
categories: [Category]
image:
  path: "/images/YYYY-MM-DD-post-slug/preview-image.png"
  show: false
---
```

- `image.show: false` — hides the image from rendering in post content (the custom CSS does this via `:has()`), while still exposing it as the Open Graph image for social sharing.
- `modified_time` — optional; add when updating an existing post.
- Timezone offset: `-0500` (CDT) or `-0600` (CST).
- Categories are capitalized; tags are lowercase and hyphenated.

### Draft workflow
Place drafts in `_drafts/` with the same front matter format but no date in the filename. Move to `_posts/` with a date prefix to publish.

### Images
Store images in `/images/YYYY-MM-DD-post-slug/` (one directory per post). The preview image referenced in front matter is the canonical location used by both Jekyll and the Open Graph tags.
