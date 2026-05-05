# Pelori marketing site

Static landing page for **pelori.fit**. Pure HTML + CSS, no build
step, deploys anywhere that serves files.

## Layout

```
pelori_website/
├── index.html        landing
├── privacy.html      rendered from velora_app/docs/privacy.md
├── terms.html        rendered from velora_app/docs/terms.md
├── styles.css        brand styling (mirrors the in-app design tokens)
├── robots.txt
├── sitemap.xml
├── .well-known/
│   └── apple-app-site-association
└── assets/
    ├── apple-touch-icon.png
    ├── logos/
    └── screenshots/  (subset of the App Store marketing PNGs)
```

## Deploy

Pick whichever's easiest — all are free for a single static site:

### Cloudflare Pages (recommended)

```bash
# From this folder, push to a git repo and connect via the
# Cloudflare dashboard. Build settings:
#   Build command:   (leave blank)
#   Output directory: /
```

Cloudflare auto-issues TLS for `pelori.fit`; add it as a custom domain
in the Pages project settings and it will manage the DNS.

### GitHub Pages

```bash
# Push to a github repo, enable Pages on main branch root, point
# pelori.fit's CNAME at <user>.github.io.
```

### Plain S3 + CloudFront

```bash
aws s3 sync . s3://pelori.fit/ --delete --exclude README.md
# then attach a CloudFront distribution + ACM cert + Route53 record
```

## Local preview

```bash
python3 -m http.server 8000 --directory pelori_website
open http://localhost:8000
```

## Re-rendering legal pages

`privacy.html` and `terms.html` are generated from
`velora_app/docs/privacy.md` and `velora_app/docs/terms.md`. To
regenerate after editing the source markdown:

```bash
python3 /tmp/render_legal.py
```

(That script lives in /tmp and just wraps the markdown body in the
site's HTML chrome. Re-run anytime the source changes; commit the
resulting .html files.)

## Things that need real values before launch

- **`<meta name="apple-itunes-app" content="app-id=PLACEHOLDER">`** in
  `index.html`. Replace `PLACEHOLDER` with the App Store Connect
  numeric app id once Pelori is published. Lets iOS Safari show the
  Smart Banner that opens the app if installed.
- **TestFlight invite link** in `index.html` (the "Join the
  TestFlight" button). Replace
  `https://testflight.apple.com/join/PLACEHOLDER` with the public
  beta URL from App Store Connect → TestFlight → Public Link.
- **`apple-app-site-association`** has the team id `U2D4FG73A9`
  hard-coded — confirm that's correct for the App Store Connect
  team id before deploying. Universal Links to `/rides/*` will then
  open the iOS app instead of the web page.
- **Custom Open Graph image** — currently re-uses `02-my-rides.png`.
  Worth designing a dedicated 1200×630 social-card image once the
  brand is settled.

## Things deliberately not done

- **Email capture form** — would need a backend (Mailchimp, Buttondown,
  ConvertKit, …). Skipped to keep the site static.
- **Blog / changelog** — same reason, plus there's nothing to write
  about yet.
- **Premium / IAP messaging** — gated until the upgrade flow ships in
  the app. The current copy reflects only the standard tier.
