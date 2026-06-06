# Lazy AI Agency

AI-powered sales & marketing department for local service businesses.

## Sales Funnel
1. **Prospect** — Scrape Google Maps for local businesses (roofers, plumbers, dentists, etc.)
2. **Free 30-day website** — Deploy a beautiful single-page site template + AI workers run in background
3. **Convert to paid** — 30 days later, show results and convert to subscription

## Structure
```
website-template/    Netlify-ready single-page site
  ├── index.html     Template (customizable per client)
  ├── netlify.toml   Deploy config
  └── netlify/functions/lead-capture.js
scraper/             Google Maps prospecting tool
  └── maps_scraper.py
```

## Quick Start
```bash
# Find prospects
python3 scraper/maps_scraper.py --service plumber --location "Austin, TX"

# Deploy a client site
cd website-template && npx netlify deploy
```
