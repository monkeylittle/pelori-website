# Beta App Description copy

Plain-text descriptions for App Store Connect → TestFlight → Test
Information → Localizations. One file per supported locale.

The TestFlight description field renders newlines but **no markdown**
— anything you'd write as `**bold**` or `# heading` ends up on screen
as literal asterisks / hashes. These files are kept in plain text so
they paste straight into the form without manual cleanup.

## How to use

1. Open App Store Connect → Pelori → TestFlight → Test Information.
2. Pick the language slot (English, Dutch, French, Spanish, Italian).
3. Copy the matching `<lang>.txt` body into "Beta App Description".
4. Save.

## Updating between builds

The description itself rarely changes — it's the elevator pitch for
the open beta and stays stable across builds. The "What to Test"
field is the per-build one; that copy lives in
`build_notes/<build>.txt` (TODO: add when build 2 ships).

## Editing rules

- Keep all five locale files in lock-step — if you tweak the English
  copy, mirror the change in the other four. The marketing site
  already ships these languages and tonal drift between channels is
  jarring.
- Watch the character count if you add features: TestFlight allows
  10,000 chars but the join page only previews the first ~400.
