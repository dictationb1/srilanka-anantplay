# Sri Lanka TV Index for AnantPlay

Add Sri Lankan TV and visual-radio sources to [AnantPlay](https://github.com/AnantPlay/android) on Android or Android TV. This repository publishes playlists and links; it does not host video.

## Add both sources

1. In AnantPlay, open **Settings → Sources → Add an index by link**.
2. Paste `https://raw.githubusercontent.com/dictationb1/srilanka-anantplay/main/index.json`.
3. Tap **Add** on **both** sources:
   - **Sri Lanka IPTV Playlist** — direct links in the **IPTV** tab. Browse by category or country, or use the language view for Sinhala, Tamil and English.
   - **Sri Lanka Official Live Sites** — broadcaster links in **Home → Live TV**. Some cards go to a broadcaster's video channel or homepage rather than a dedicated live player. Availability and playback depend on the broadcaster, your network, and whether the channel is currently on air.

If direct playback fails, try that channel's Live TV card and its mirrors. The legacy `sources.txt` imports **only the category playlist**; use `index.json` to add both sources and the alternate language playlist.

## Coverage and verification

See [STATUS.md](STATUS.md) for the latest recorded timestamp in Sri Lanka Time (UTC+05:30), catalog and playlist counts, and every URL probe result. A confirmed HLS manifest is not a media playback test, and an HTTP 200 on a web page does not prove there is a live video. An access restriction, timeout, or connection error on the checker does not prove that a stream is unavailable in Sri Lanka. Some retained CDN links may require a supported player or may be restricted to particular networks.

## Maintain the index

- [`channels_master.json`](channels_master.json) is the curated catalog. Each stream has a publication flag, an optional `referer`, and a manual exception flag for known ambiguous missing responses. Unpublished candidates enter the playlists only after a valid HLS response. There is no automatic ingestion of unreviewed channels. Some IPTV candidates are referenced by [iptv-org](https://github.com/iptv-org/iptv).
- [`srilanka_category.m3u`](srilanka_category.m3u) and [`srilanka_language.m3u`](srilanka_language.m3u) carry the same streams, grouped differently. [`srilanka_sites.json`](srilanka_sites.json) carries the live and language site rows. AnantPlay uses a **boolean** site `index`; the numeric `position` field records the one-based row order for maintenance.
- The updater tests every endpoint with TLS verification enabled. It retains published links on 403/451, timeouts, DNS or other ambiguous failures; it can exclude individual HTTP 404/410 or non-HLS responses only when the safety floor passes. A manual exception protects Channel Eye pending in-country evidence. Review official replacements manually before changing a primary site or a mirror.
- Run `.venv/bin/python scripts/verify_release.py` after installing `scripts/requirements.txt` into a virtual environment. Run `.venv/bin/python scripts/update_index.py --dry-run` to check all endpoints and see a diff without editing the repository. Without `--dry-run`, the updater regenerates the source files and `STATUS.md`.
- In GitHub, **Actions → Sri Lanka index verification and refresh → Run workflow** can request a refresh on `main`. The same workflow is scheduled every six hours when installed on `main`; pull requests run checks and a read-only probe instead.
