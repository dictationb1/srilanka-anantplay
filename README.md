# Sri Lanka TV Index for AnantPlay

Add Sri Lankan TV and visual-radio sources to [AnantPlay](https://github.com/AnantPlay/android) on Android or Android TV. This repository publishes playlists and links; it does not host video.

## Add both sources

1. In AnantPlay, open **Settings → Sources → Add an index by link**.
2. Paste `https://raw.githubusercontent.com/dictationb1/srilanka-anantplay/main/index.json`.
3. Tap **Add** on **both** sources that appear:
   - **Sri Lanka IPTV Playlist** — direct links in the **IPTV** tab (browse by category or country, or switch to the language view for Sinhala, Tamil and English).
   - **Sri Lanka Official Live Sites** — broadcaster links in **Home → Live TV**. Some cards open a broadcaster's video channel or homepage rather than a dedicated live player. Availability and playback depend on the broadcaster, your network, and whether the channel is on air.

Tap **Add** twice: accepting only one source gives you only one tab. The legacy `sources.txt` imports **only the category playlist**; use `index.json` to add both sources and the alternate language playlist.

## What is published

| AnantPlay tab | Published file | Current content |
|---|---|---|
| **IPTV** | [`srilanka_category.m3u`](srilanka_category.m3u) and [`srilanka_language.m3u`](srilanka_language.m3u) | **15 channels**, **18 direct stream entries** |
| **Home → Live TV** | [`srilanka_sites.json`](srilanka_sites.json) | **69 official broadcaster cards** |

Both playlists carry exactly the same streams, grouped by category in one and by Sinhala/Tamil/English in the other. Every card and every count is regenerated from [`channels_master.json`](channels_master.json); [STATUS.md](STATUS.md) holds the timestamp of the most recent sweep in Sri Lanka Time (UTC+05:30) plus every individual URL result.

## Verification policy

See [STATUS.md](STATUS.md) for the latest recorded timestamp in Sri Lanka Time (UTC+05:30), catalog and playlist counts, and every URL probe result. A confirmed HLS manifest is not a media playback test, and an HTTP 200 on a web page does not prove there is a live video.

- **Confirmed HTTP 404/410 or DNS NXDOMAIN** links are removed from the published files. A channel keeps its working web card in `srilanka_sites.json` even when its direct stream is withdrawn.
- **SL geo-restricted / timeout from a US runner (retained).** Many official Sri Lankan feeds only accept Asian networks. A timeout, 403/451, TLS failure or connection reset from the GitHub Actions runner is *not* treated as a dead link: the curated stream stays in both playlists, is labelled `SL Geo-Restricted / Timeout from US Runner (Retained)` in STATUS.md, and never blocks a release. These links can work from a Sri Lankan network.
- **Primary site swaps.** When a primary site card answers 403/451/522/525/526 or fails TLS but one of its official mirrors answers HTTP 200, STATUS.md lists the verified mirror under *Suggested primary site swaps* so the primary can be corrected from evidence rather than guesswork.

## Maintain the index

- [`channels_master.json`](channels_master.json) is the curated catalog. Each stream has a publication flag, an optional `referer`, a manual exception flag for known ambiguous missing responses, and the V2 curation fields `geo_restricted_sl` / `direct_m3u8_status` (`verified`, `geo_restricted_sl`, `none_public_web_only`, `dead`). Unpublished candidates enter the playlists only after a valid HLS response. There is no automatic ingestion of unreviewed channels. Some IPTV candidates are referenced by [iptv-org](https://github.com/iptv-org/iptv).
- [`srilanka_category.m3u`](srilanka_category.m3u) and [`srilanka_language.m3u`](srilanka_language.m3u) carry the same streams, grouped differently. [`srilanka_sites.json`](srilanka_sites.json) carries the live and language site rows. AnantPlay uses a **boolean** site `index`; the numeric `position` field records the one-based row order for maintenance.
- The updater tests every endpoint with TLS verification enabled, using separate connect and read timeouts plus exponential-backoff retries for transient timeout/TLS/network/5xx results. It retains published links on 403/451, timeouts, DNS or other ambiguous failures; it can exclude individual HTTP 404/410 or non-HLS responses only when the safety floor passes. Channel Eye's confirmed-404 `trn07.tulix.tv` stream was withdrawn and its broadcaster tulix player kept as the card; review official replacements manually before changing a primary site or a mirror.
- Run `.venv/bin/python scripts/verify_release.py` after installing `scripts/requirements.txt` into a virtual environment. Run `.venv/bin/python scripts/update_index.py --dry-run` to check all endpoints and see a diff without editing the repository. Without `--dry-run`, the updater regenerates the source files and `STATUS.md`. `--timeout`, `--connect-timeout` and `--retries` tune the sweep.
- In GitHub, **Actions → Sri Lanka index verification and refresh → Run workflow** can request a refresh on `main`. The same workflow is scheduled every six hours when installed on `main`; pull requests run the offline checks plus a read-only probe.

## Research notes

- [V2_RESEARCH_REPORT.md](V2_RESEARCH_REPORT.md) — channel-by-channel evidence from the second verification pass (direct HLS versus YouTube, geo-fencing, identity corrections such as Jaya TV and Varnam TV).
- [RESOLVER_NOTES.md](RESOLVER_NOTES.md) — why no Cloudflare Worker is shipped: no broadcaster exposes a public token API, and AnantPlay's on-device WebView sniffer already resolves protected players with the user's own IP.
