# Mimulus Greenhouse — cPanel publish package

This folder is the deployable public surface for `mimulus.arctopia.no`.

## What it contains

- `index.html` — Greenhouse UI
- `styles.css` — responsive visual layer
- `app.js` — local branching, lineage trail, export, and Path Lab
- `.htaccess` — routes `/api/explore` to PHP and blocks sensitive config files
- `api/explore.php` — decoder / translator / comparison backend
- `api/config.example.php` — server-side config template

## Public workflow

The primary interaction is deliberately simple:

`Look → Decode → Translate → Branch → Test → Compare`

The research distinctions remain underneath the interface:

- source observation
- representation / transcription
- decoder assumptions
- derived structure
- translation
- interpretation
- falsification / intervention
- lineage

A translation of a decoder result is useful, but it remains a descendant of that decoder and is not treated as independent corroboration.

## Deploy to mimulus.arctopia.no

1. Point the subdomain document root at the intended Mimulus directory.
2. Upload the contents of `hosting/cpanel/` into that document root.
3. Copy `api/config.example.php` to `api/config.php` on the server.
4. Put the API key and optional access token only in `api/config.php`.
5. Confirm `.htaccess` is active and that `api/config.php` is not web-readable.
6. Open the subdomain and test:
   - a text-only Look run;
   - a Decode run;
   - Translate from a decoder card;
   - Branch from the same card;
   - Compare after at least two runs;
   - Path Lab with both histories and the history-gate toggle.

Do not commit `api/config.php`.

## Product boundary

Greenhouse is permissive in discovery and strict about provenance. It may generate bold candidate readings, but it must not silently convert coherence into evidence, downstream translation into independent support, or multiple similar runs into independent replications.

The Path Lab is a synthetic known-answer demonstration. It is not an empirical claim about any historical source or about ArcTopia theory.
