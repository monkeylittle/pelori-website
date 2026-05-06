# App Store + TestFlight copy, per locale

Plain-text store copy for App Store Connect. One file per supported
locale; each file is a four-section bundle covering every text field
the listing + TestFlight pages need.

The folder is named `beta_description/` for historical reasons —
the first version only carried the TestFlight Beta App Description
— but each file now also holds the App Store Description,
Promotional Text, and Keywords for that language.

The fields render newlines but **no markdown** — anything you'd
write as `**bold**` or `# heading` ends up on screen as literal
asterisks / hashes. Files are kept in plain text so they paste
straight into the App Store Connect forms without cleanup.

## File format

Each `<lang>.txt` is divided into six sections, each with its own
banner explaining which app-store form field it maps to:

```
Apple
1. BETA APP DESCRIPTION    →  App Store Connect → TestFlight →
                              Test Information
                              (≤ 10,000 chars; rarely changes)
2. APP STORE DESCRIPTION   →  App Store Connect → App Store →
                              Localization → Description
                              (≤ 4,000 chars; long-form pitch.
                              Section 6 below points back here —
                              same body covers Play too)
3. PROMOTIONAL TEXT        →  App Store Connect → App Store →
                              Localization → Promotional Text
                              (≤ 170 chars; editable without a
                              new build, shown above the
                              description on the listing)
4. KEYWORDS                →  App Store Connect → App Store →
                              Localization → Keywords
                              (≤ 100 chars total, comma-separated,
                              no spaces after commas — every char
                              counts; avoid competitor names and
                              "free"/"best" or Apple may reject)

Google
5. PLAY SHORT DESCRIPTION  →  Play Console → Grow users → Main
                              store listing → Short description
                              (≤ 80 chars; one-liner above the
                              full description)
6. PLAY FULL DESCRIPTION   →  Play Console → Grow users → Main
                              store listing → Full description
                              (≤ 4,000 chars; identical body to
                              Section 2 — Play has no separate
                              keywords or promo-text fields)
```

Copy each section's body — between the closing `====` line and the
next `====` banner — into the matching form field.

## Folder layout

Each round of the copy lives in its own subfolder so we keep a paper
trail across rewrites:

```
beta_description/
├── README.md           ← this file
├── beta-1/             ← copy used for the first public-beta cycle
│   ├── en.txt
│   ├── nl.txt
│   ├── fr.txt
│   ├── es.txt
│   └── it.txt
└── beta-2/             ← created when the copy gets a rewrite
    └── …
```

The numbering is independent of the TestFlight build number — bump
to `beta-2/` only when the copy itself changes. Most new builds just
rotate the per-build "What to Test" field (separate to everything in
this folder) and reuse the latest `beta-N/` for the rest.

## How to use

1. Open App Store Connect → Pelori → TestFlight (for section 1) or
   → App Store → Localization (for sections 2–4).
2. Pick the language slot (English, Dutch, French, Spanish, Italian).
3. Open the matching `beta-1/<lang>.txt`, copy the relevant section's
   body into the corresponding form field.
4. Save.

## Editing rules

- Keep all five locale files in lock-step — if you tweak the English
  copy, mirror the change in the other four. The marketing site
  already ships these languages and tonal drift between channels is
  jarring.
- The Promotional Text and Keywords have hard char ceilings; verify
  with `wc -c` (or count manually) before pasting. Apple silently
  rejects keyword strings that overflow.
- Apple auto-pluralises keywords, so don't add both `bike` and
  `bikes` — pick the singular and Apple covers both. Same for
  upper/lower case.
