# RESOLVER_NOTES.md — Dynamic Token API Investigation (Pass #2, 2026-11-20)

## Question

Can a zero-cost Cloudflare Worker resolve official Sri Lankan broadcaster stream APIs
into fresh `.m3u8` redirects for AnantPlay's IPTV tab, for channels whose direct URLs
rotate (TV Derana, Sirasa TV, Swarnavahini, ITN, Siyatha, Supreme, Rupavahini)?

## What was tested (all from this session's live probes)

| Broadcaster | Web player technology | Public token/stream API found? | Evidence |
|---|---|---|---|
| TV Derana (derana.lk/live) | Sucuri firewall + JS player | **No** | Sucuri "Access Denied, Block ID BLACK02 — Your IP address is listed in our blacklist" for the whole datacenter range; no XHR endpoint is reachable to inspect from outside Sri Lanka. |
| Sirasa TV (live.sirasatv.lk) | Cloudflare (403/522 + JS challenge) | **No** | 403 for foreign IPs; player JSON not exposed pre-challenge. |
| ITN (itn.lk/live) | Cloudflare Managed Challenge | **No** | Even a real headless Chrome could not pass the challenge from a datacenter IP ("Performing security verification" loop). |
| TV 1 (tv1.lk) | Cloudflare challenge | **No** | Same as ITN; the newsroom's actual live distribution is their official Twitch (`player.twitch.tv/?channel=newsfirstsl`, embedded on newsfirst.lk/live) and YouTube. |
| Swarnavahini (swarnavahini.lk) | 403 for foreign IPs; EBC proxy `teledrama.ebc.lk/TTT/proxy.php` | **Partial — no API** | The proxy URL itself IS an HLS manifest (no token parameter, Referer `https://swarnavahini.lk/` accepted), but the host only accepts Asian network connections; there is no JSON API to call. |
| Siyatha TV (siyathatv.lk/live) | WordPress + direct HLS | **No API needed** | The page embeds a **static** m3u8 (`rtmp01.voaplus.com/hls/6x6ik312qk4grfxocfcv.m3u8`) — already published in the M3U, verified 200 + #EXTM3U with any User-Agent. |
| Rupavahini / Channel Eye (SLRC) | Tulix iframe players | **No** | `swf.tulix.tv/iframe/slrclive/index.php` exposes `rpn.tulixcdn.com/slrclive/slrc/slrclive-mobile/index.m3u8` (static, already published). Channel Eye's old `trn07.tulix.tv/slrc2/slrc2/playlist.m3u8` is a confirmed 404; its `dammika.tulix.tv` iframe is HTTP 200 and is used as its site card. |
| Supreme TV (supremetv.lk) | Own host, geo-fenced | **No** | DNS resolves (217.21.94.203) but both HTTP and TLS connections from US/EU are dropped — the site is unreachable outside Asia; no API to interrogate. |
| Ahasa TV (ahasatv.lk) | Next.js + HLS.js | **No** | The "Watch Live" button creates a `blob:` URL at runtime; the playlist is assembled in-page (no stable public JSON endpoint; the old `rewind-3600.m3u8` path is 404). |
| DAN TV (dantv.tv / dantv.lk) | — | **No** | Both domains are now **ParkLogic parked** (serving `router.parklogic.com` monetization scripts). The network's only living presence is its YouTube channels. |

## Conclusion — why no `cloudflare-worker/` is shipped

1. **No broadcaster exposes a public, unauthenticated JSON API that returns a fresh stream URL.**
   Every player either uses a static HLS URL (already captured in the M3U), or sits behind
   a bot-protection layer (Sucuri/Cloudflare/DDoS-Guard) that a Worker cannot pass either —
   a Worker egress IP is a datacenter IP, exactly what these firewalls block.
2. **A Worker that proxies the HLS bytes** would relay copyrighted video through a
   third-party origin — out of scope for a public FTA repository and against the
   no-piracy rules of this project.
3. **AnantPlay already contains the correct resolver**: its WebView + `assets/frame.js`
   stream sniffer runs on the user's own device, with their own IP, cookies and
   Cloudflare clearance. That is why every protected broadcaster is listed in
   `srilanka_sites.json` with an HTTP-200 primary (official `/live` page or the
   broadcaster's verified YouTube live channel), which AnantPlay opens natively.

## What TO do if a Worker is still wanted later

If a broadcaster later launches a documented public API (for example a JSON endpoint on
their player domain returning `{ "url": "https://...m3u8" }`), a Worker skeleton would be:

```js
// cloudflare-worker/worker.js (SKETCH — do not deploy; no broadcaster API exists today)
export default {
  async fetch(req) {
    const api = "https://player.example.lk/api/live";       // hypothetical public endpoint
    const r = await fetch(api, { headers: { "User-Agent": "Mozilla/5.0", "Referer": "https://example.lk/" } });
    const { url } = await r.json();
    return Response.redirect(url, 302);
  }
}
```

Register it in `index.json` as an extra `playlist` source pointing at
`https://<worker>/derana.m3u8` (an M3U the Worker synthesizes). Until such an API is
publicly documented, the honest state is: **web-only extraction via the sites list**.

## Honest channel-state vocabulary (used in `channels_master.json` notes)

* `direct_m3u8_status: verified` — HTTP 200 + `#EXTM3U` seen this session, published.
* `direct_m3u8_status: geo_restricted_sl` — DNS resolves, connection refused/timeouts
  from US/EU probes; kept with `keep_if_missing: true` because the CDN serves Asia.
  (Swarnavahini, Star Tamil, Shraddha, The Buddhist, Charana, Verbum mirror, Asia TV.)
* `direct_m3u8_status: none_public_web_only` — no public direct HLS exists anywhere we
  could find (broadcaster uses protected web player and/or YouTube). These channels are
  fully covered by the sites list, whose primaries all return HTTP 200.
* `dead` — endpoint 404/410 (Channel Eye trn07, Monara 5centscdn, NDTV Lanka 5centscdn,
  Ahasa rewind path); retained as unpublished candidates or removed with a note.
