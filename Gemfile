source "https://rubygems.org"

# Use the latest stable Ruby version
ruby "3.3.6"

# Jekyll 4.x - latest stable version
gem "jekyll", "~> 4.3"

# Chirpy theme - modern, feature-rich theme perfect for technical blogs
gem "jekyll-theme-chirpy", "~> 7.2"

# Essential Jekyll plugins (many required by Chirpy)
group :jekyll_plugins do
  gem "jekyll-feed", "~> 0.17"
  gem "jekyll-seo-tag", "~> 2.8"
  gem "jekyll-sitemap", "~> 1.4"
  gem "jekyll-paginate", "~> 1.1"
  gem "jekyll-include-cache", "~> 0.2"
  gem "jekyll-archives", "~> 2.2"
  gem "jekyll-redirect-from", "~> 0.16"
end

# Required for serving the site locally
gem "webrick", "~> 1.8"

# Performance and compatibility
gem "kramdown-parser-gfm", "~> 1.1"

# HTML processing (required by Chirpy)
gem "html-proofer", "~> 5.0", group: :test
