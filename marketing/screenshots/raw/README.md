# Marketing screenshots — raw captures

Plain simulator screenshots, one per panel, before any caption or
brand background is composited on top. Captures from here feed into
`marketing/screenshots/composed-6.9/<lang>/` via `composer.py`.

The captures themselves come out of the Flutter app — `flutter run`
lives in the `velora_app` repo (sibling of this one). Run the
simulator there, capture each panel, then drop the PNGs into the
`raw/6.9-inch/<lang>/` directories in this repo.

## Folder layout

```
raw/
├── 6.9-inch/    1290 × 2796 — iPhone 16 Pro Max simulator (required)
│   ├── en/    ← 7 panels for English
│   ├── nl/    ← 7 panels for Dutch
│   ├── fr/    ← 7 panels for French
│   ├── es/    ← 7 panels for Spanish
│   └── it/    ← 7 panels for Italian
└── 6.5-inch/    1242 × 2688 — iPhone 11 Pro Max simulator (optional)
    └── en/, nl/, fr/, es/, it/
```

Apple **requires** the 6.9" set for new submissions. The 6.5" set is
optional and only worth doing if listing previews look cropped on
older devices.

## Naming convention

```
01-onboarding-hero.png
02-my-rides.png
03-chat.png
04-going-list.png
05-discover.png
06-where-tab.png
07-public-preview.png
```

Numeric prefix sets ordering on the App Store listing. Same names in
every `<lang>/` directory so `composer.py` can match them up.

## What to capture (the seven panels)

Sign in as **`reuben@example.com`** in the simulator pointed at the
dev API. Re-run `python3 /tmp/seed_pelori_dev.py` first if the seed
data has drifted.

| # | Surface | Setup | Frame should show |
|---|---------|-------|-------------------|
| 1 | Onboarding hero | Sign out so the auth gate routes here | Lime equalizer mark on Electric Blue, the localized "Ride together / We've got the rest." headline, the localized "Get started" pill |
| 2 | My Rides list | Sign in as Reuben | Three ride cards (Saturday Shop, Sunday Long Loop, Tuesday Coffee Spin); notification bell with badge in top-right |
| 3 | Group chat | Tap the chat bubble on Saturday Shop Ride | Seeded thread between Reuben/Marcus/Priya, compose box visible at the bottom |
| 4 | Going-list popup | On a My Rides card, tap "3 going · 1 not going" | Bottom sheet with the localized "GOING · 3" header and three avatar rows |
| 5 | Discover | Tap the Discover tab | List of public rides — Saturday Shop and Battersea Bunch — search field at the top |
| 6 | Where tab on ride settings | Tap a ride card body, land on Where tab | Name/description fields filled, meeting-point card with embedded OSM map showing the pin |
| 7 | Public ride preview | Discover → tap a ride card the caller isn't a member of | Schedule + meeting + ability + going-count summary, "Join this ride" button at the bottom |

## What to skip

Premium / PTT-only surfaces:

- Live group map during a ride.
- Push-to-talk button on the PTT screen.
- Drop-off alert configuration on the When tab.

Apple has rejected apps where a screenshot showed something not
reachable from the free path. Treat the standard-tier surfaces as
the canonical screenshot story until the upgrade flow exists.

## Capturing per language

Five locales ship: **en**, **nl**, **fr**, **es**, **it**. Repeat the
seven captures once per locale.

The app's locale is driven by:

- **Signed-out screens** (panel 1, the onboarding hero): the device's
  primary locale via `Localizations.localeOf(context)`. To capture
  panel 1 in language X, set the simulator's language to X first.
- **Signed-in screens** (panels 2–7): the user's `custom:language`
  Cognito attribute via the override in `lib/l10n/app_locale.dart`.
  Change Reuben's language in the app's *Profile → Language* picker
  before capturing the rest.

### Per-locale checklist

For each language **X** in `[en, nl, fr, es, it]`:

1. **Set the simulator's language to X.** *Simulator → Settings →
   General → Language & Region → iPhone Language → X.* The simulator
   restarts. Skip this step for English if your simulator is already
   English.
2. `flutter run --release`. Release-mode renders avatars, fonts, and
   tile maps the way TestFlight users will see them — debug mode
   sometimes shows debug banners or skipped paint warnings.
3. **Sign out** of the app if a previous session is active so the auth
   gate routes to the onboarding hero.
4. **Capture panel 1 (`01-onboarding-hero.png`).** The headline + CTA
   should be in language X (signed-out screens follow the device
   locale via the resolver in `main.dart`). `Cmd + S` saves a PNG to
   the Desktop. Move it to `raw/6.9-inch/<X>/01-onboarding-hero.png`.
5. **Sign in as `reuben@example.com`** with password
   `RideTogether2026!`.
6. **Set Reuben's language to X.** Tap *Profile* in the bottom nav,
   tap the *Language* field, pick **X**, tap *Save*. The app rebuilds
   in X immediately (the override in
   `lib/l10n/app_locale.dart::refreshAppLocaleOverride()` re-reads
   `custom:language` after Save). Confirm by checking that the
   AppBar titles and buttons read in X.
7. **Capture panels 2–7** by navigating the surfaces in the table
   above. Save each PNG with the matching numeric name into
   `raw/6.9-inch/<X>/`.
8. **Sign out** again so the next iteration starts cleanly. (Steps 4
   and 6 of the next iteration would still work without this, but
   signing out is a cheap safety check that the override is actually
   driven by `custom:language` and not stale state.)
9. Move on to the next language.

A full pass for one language takes ~10 minutes once you've done it
once. A full five-language sweep is ~50 minutes plus the simulator
locale-change restarts.

### Tips and gotchas

- **The status bar.** The simulator pins 9:41 (Apple's house style)
  whenever you take a screenshot via `Cmd + S`. A real device shows
  your battery level + carrier name and Apple sometimes objects to
  that. Always capture on the simulator.
- **The simulator's locale change is sticky.** It survives `flutter
  run` so you don't need to set it before each Flutter rebuild —
  just before the panel-1 capture for each language.
- **Reuben's `custom:language` overrides device locale once
  signed in.** That's the design — it lets a user in
  London-with-French-iPhone keep the app in their preferred reading
  language. For screenshots that means: panel 1 follows the
  simulator locale, panels 2–7 follow the picker setting in the
  app, and they should all match. If panel 1 reads in a different
  language to panel 2, you forgot one of those two steps.
- **Empty seed data.** Panels 2 / 3 / 4 / 5 / 6 / 7 all assume
  Reuben has rides and chat history. If you wiped DynamoDB recently,
  re-run `/tmp/seed_pelori_dev.py` before capturing.
- **Per-locale incremental capture is supported.** `composer.py`
  skips panels whose raw PNG isn't in place yet, so you can capture
  one language at a time and run the composer in between to spot-
  check the captioning.

## Compositing

Once at least one `<lang>/` directory has raw PNGs, compose them with:

```bash
python3 marketing/composer.py            # every locale that has captures
python3 marketing/composer.py fr         # just French
python3 marketing/composer.py en nl      # English + Dutch
```

Captions, accent words, and subheads live in the
`CAPTIONS_BY_LOCALE` dict at the top of `composer.py`. Edit there
to tweak copy; re-run for a fresh composite.

The composer reads from `raw/6.9-inch/<lang>/` and writes to
`composed-6.9/<lang>/`. The output PNGs are what you upload to App
Store Connect's per-language screenshot slots.

## Publishing to the marketing site

The website (this same repo) embeds a 4-screenshot subset on the
home page — `02-my-rides.png`, `03-chat.png`, `05-discover.png`,
`06-where-tab.png` — under `assets/screenshots/<lang>/`. After a
fresh capture + compose pass, copy the four panels into the site's
matching folder. See the top-level `README.md` for which panels the
site uses and how the JS swaps the active set.
