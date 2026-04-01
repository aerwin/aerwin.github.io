# Tony Erwin's Tech Blog

A technical blog focused on AI, machine learning, agentic systems, cloud architecture, microservices, and modern software engineering practices.

## Technology Stack

- **Jekyll**: 4.4.1
- **Ruby**: 3.3.6
- **Theme**: [Chirpy](https://github.com/cotes2020/jekyll-theme-chirpy) 7.5.0
- **Hosting**: GitHub Pages with custom domain (www.tonyerwin.com)

## Local Development

### Prerequisites

1. Install rbenv and Ruby 3.3.6:
   ```bash
   rbenv install 3.3.6
   rbenv local 3.3.6
   ```

2. Install dependencies:
   ```bash
   bundle install
   ```

### Running Locally

Start the development server:
```bash
eval "$(rbenv init - bash)"
bundle exec jekyll serve --host 0.0.0.0
```

The site will be available at `http://localhost:4000`

### Local Configuration Overrides

If you need to override any configuration settings for local development (without committing them), create a `_config_local.yml` file:

```yaml
# _config_local.yml (this file is gitignored)
# Add any local overrides here, for example:

# Enable drafts and future posts
show_drafts: true
future: true

# Or override other settings as needed
```

To use the local config:
```bash
bundle exec jekyll serve --config _config.yml,_config_local.yml
```

**Note**: The `baseurl` setting should remain empty (`""`) for both local and production since we use a custom domain. You don't need to change it.

## Deployment

The site automatically deploys to GitHub Pages when changes are pushed to the main branch. GitHub Pages builds and serves the site at www.tonyerwin.com.

## Writing Posts

1. Create a new file in `_posts/` with the format: `YYYY-MM-DD-title.md`
2. Add front matter:
   ```yaml
   ---
   title: "Your Post Title"
   date: YYYY-MM-DD HH:MM:SS -0500
   categories: [Category1, Category2]
   tags: [tag1, tag2, tag3]
   image:
     path: /images/YYYY-MM-DD-post-name/preview-image.png
     alt: "Image description"
   ---
   ```
3. Write your content in Markdown

### Preview Images

Preview images are used for:
- Home page post listings
- Social media sharing (Open Graph/Twitter Cards)

They are automatically hidden from the post content itself via custom CSS.

## Custom Styling

Custom CSS is located in:
- `assets/css/custom.scss` - Custom styles (compiled to CSS)
- `_layouts/default.html` - Modified to include custom CSS

## Theme Customization

The Chirpy theme can be customized by:
1. Overriding layouts in `_layouts/`
2. Adding custom styles in `assets/css/custom.scss`
3. Modifying configuration in `_config.yml`

## Maintenance

### Updating Dependencies

```bash
bundle update
```

### Updating Ruby Version

1. Update `.ruby-version` file
2. Install new Ruby version: `rbenv install X.X.X`
3. Update dependencies: `bundle install`

## Documentation

- [Jekyll Documentation](https://jekyllrb.com/docs/)
- [Chirpy Theme Documentation](https://chirpy.cotes.page/)
- [Markdown Guide](https://www.markdownguide.org/)

## License

Content is © Tony Erwin. Theme is MIT licensed.
