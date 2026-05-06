# Beta App Description copy

Plain-text descriptions for App Store Connect → TestFlight → Test
Information → Localizations. One file per supported locale.

The TestFlight description field renders newlines but **no markdown**
— anything you'd write as `**bold**` or `# heading` ends up on screen
as literal asterisks / hashes. These files are kept in plain text so
they paste straight into the form without manual cleanup.

## Folder layout

Each round of the description copy lives in its own subfolder so we
keep a paper trail across rewrites:

```
beta_description/
├── README.md           ← this file
├── beta-1/             ← copy used for the first public-beta cycle
│   ├── en.txt
│   ├── nl.txt
│   ├── fr.txt
│   ├── es.txt
│   └── it.txt
└── beta-2/             ← created when the description gets a rewrite
    └── …
```

The numbering is independent of the TestFlight build number — bump
to `beta-2/` only when the description copy itself changes. Most new
builds just rotate the per-build "What to Test" field (separate to
the description) and reuse whatever's in the latest `beta-N/`.

## How to use

1. Open App Store Connect → Pelori → TestFlight → Test Information.
2. Pick the language slot (English, Dutch, French, Spanish, Italian).
3. Copy the matching `<latest>/<lang>.txt` body into "Beta App
   Description".
4. Save.

## Editing rules

- Keep all five locale files in lock-step — if you tweak the English
  copy, mirror the change in the other four. The marketing site
  already ships these languages and tonal drift between channels is
  jarring.
- Watch the character count if you add features: TestFlight allows
  10,000 chars but the join page only previews the first ~400.
