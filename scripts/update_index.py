#!/usr/bin/env python3
"""Probe the curated catalog and render AnantPlay sources from any working directory."""
from __future__ import annotations

import argparse
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from datetime import datetime
import difflib
import json
import os
from pathlib import Path
import re
import socket
import time
from tempfile import NamedTemporaryFile
from urllib.parse import urlsplit
from zoneinfo import ZoneInfo

import requests
import urllib3

ROOT = Path(__file__).resolve().parents[1]
RAW = 'https://raw.githubusercontent.com/dictationb1/srilanka-anantplay/main/'
LANGUAGES = ('Sinhala', 'Tamil', 'English')
CATEGORIES = ('National', 'News', 'General', 'Entertainment', 'Tamil', 'English',
              'Sports', 'Religious', 'Education', 'Kids', 'Culture', 'Visual Radio')
PRIORITY = ('Rupavahini.lk', 'TVDerana.lk', 'AdaDerana24x7.lk', 'SirasaTV.lk', 'TV1.lk',
            'ITN.lk', 'Swarnavahini.lk', 'HiruTV.lk', 'SiyathaTV.lk', 'TNLTV.lk',
            'ChannelEye.lk', 'NethraTV.lk', 'VasanthamTV.lk', 'ShakthiTV.lk', 'NewsFirst.lk')
PLAYLISTS = {'category': 'srilanka_category.m3u', 'language': 'srilanka_language.m3u'}
SITE_FILE = 'srilanka_sites.json'
GENERATED = ('index.json', 'sources.txt', SITE_FILE, *PLAYLISTS.values(), 'STATUS.md')
UA = ('Mozilla/5.0 (Linux; Android 14) AppleWebKit/537.36 (KHTML, like Gecko) '
      'Chrome/131.0.0.0 Mobile Safari/537.36')
ID = re.compile(r'[A-Za-z0-9_-]+\.lk')
MIN_RETAIN_PERCENT = 80
# V2 catalog vocabulary: how a curated direct stream behaved in the last live pass.
STREAM_STATES = ('verified', 'geo_restricted_sl', 'none_public_web_only', 'dead')
# Optional V2 keys. They are validated and then given explicit defaults so the
# renderer never depends on their presence (older catalogs keep working).
CHANNEL_OPTIONAL = {'geo_restricted_sl': bool, 'web_only': bool, 'direct_m3u8_status': str,
                    'youtube_channel_id': str}
STREAM_OPTIONAL = {'geo_restricted_sl': bool, 'direct_m3u8_status': str}
RETRYABLE_VERDICTS = frozenset({'timeout', 'tls-error', 'network-error'})
RETRYABLE_CODES = frozenset({429, 500, 502, 503, 504})
# A published stream seen in one of these states in a probe from outside Sri Lanka is
# kept and reported as geo-restricted/timeout, never treated as confirmed dead.
GEO_VERDICTS = frozenset({'timeout', 'restricted', 'tls-error', 'network-error', 'dns-not-found'})
GEO_LABEL = 'SL Geo-Restricted / Timeout from US Runner (Retained)'


def json_text(data):
    return json.dumps(data, indent=2, ensure_ascii=False) + '\n'


def require(condition, message):
    if not condition:
        raise ValueError(message)


def load_json(path):
    def unique(items):
        out = {}
        for key, value in items:
            require(key not in out, f'{path.name}: duplicate JSON key {key!r}')
            out[key] = value
        return out

    return json.loads(path.read_text(encoding='utf-8'), object_pairs_hook=unique)


def url_ok(url):
    if (not isinstance(url, str) or not url.startswith(('http://', 'https://'))
            or re.search(r'[\s<>"\\|`\x00-\x1f\x7f]', url)
            or re.search(r'%(?![0-9a-fA-F]{2})', url) or '](' in url):
        return False
    try:
        p = urlsplit(url)
        return bool(p.hostname and '.' in p.hostname and not p.username and not p.password
                    and re.fullmatch(r'[a-zA-Z0-9.-]+', p.hostname)
                    and (p.port is None or p.port > 0))
    except ValueError:
        return False


def _check_optional(owner, item, allowed, label):
    """Validate optional V2 keys, then fill explicit defaults.

    The V2 catalog adds curation vocabulary (`geo_restricted_sl`,
    `direct_m3u8_status`, `youtube_channel_id`, `web_only`) without removing any
    V1 field, so both shapes must load and render identically.
    """
    unknown = set(item) - set(allowed)
    require(not unknown, f'{label}: unsupported field(s) {sorted(unknown)}')
    for key, kind in owner.items():
        value = item.setdefault(key, False if kind is bool else '')
        require(isinstance(value, kind), f'{label}: {key} must be {kind.__name__}')
        if key == 'direct_m3u8_status' and value:
            require(value in STREAM_STATES, f'{label}: unknown direct_m3u8_status {value!r}')
        if key == 'youtube_channel_id' and value:
            require(re.fullmatch(r'UC[A-Za-z0-9_-]{22}', value), f'{label}: bad YouTube channel id')
    return item


def stream_is_protected(stream):
    """Curated SL feeds that a US/EU runner cannot reach are never auto-pruned."""
    return bool(stream.get('keep_if_missing') or stream.get('geo_restricted_sl')
                or stream.get('direct_m3u8_status') == 'geo_restricted_sl')


def load_catalog(root=ROOT):
    catalog = load_json(root / 'channels_master.json')
    require(set(catalog) == {'country', 'maintainer', 'channels'}
            and catalog['country'] == 'Sri Lanka'
            and catalog['maintainer'] == 'dictationb1/srilanka-anantplay', 'catalog metadata')
    channels = catalog['channels']
    require(isinstance(channels, list) and channels, 'empty catalog')
    ids, names, sites, streams = set(), set(), set(), set()
    required = {'tvg_id', 'name', 'category', 'language', 'logo', 'site', 'youtube',
                'mirrors', 'streams', 'note'}
    stream_required = {'url', 'quality', 'note', 'published', 'keep_if_missing', 'referer'}
    for c in channels:
        require(isinstance(c, dict) and required <= set(c), f'channel fields: {c}')
        _check_optional(CHANNEL_OPTIONAL, c, required | set(CHANNEL_OPTIONAL), 'channel')
        cid = c['tvg_id']
        require(isinstance(cid, str) and ID.fullmatch(cid) and cid.casefold() not in ids, f'bad ID: {cid}')
        ids.add(cid.casefold())
        name = c['name']
        require(isinstance(name, str) and name and name == name.strip()
                and not re.search(r'[",|\x00-\x1f]', name) and name.casefold() not in names, f'bad name: {name}')
        names.add(name.casefold())
        require(c['category'] in CATEGORIES and c['language'] in LANGUAGES, f'{cid}: unknown group')
        require(isinstance(c['note'], str), f'{cid}: note type')
        require(url_ok(c['site']) and c['site'] not in sites, f'{cid}: invalid/duplicate site')
        sites.add(c['site'])
        for key in ('logo', 'youtube'):
            require(c[key] == '' or url_ok(c[key]), f'{cid}: invalid {key}')
        require(isinstance(c['mirrors'], list) and all(map(url_ok, c['mirrors'])), f'{cid}: invalid mirrors')
        mirrors = [u for u in [c['site'], c['youtube'], *c['mirrors']] if u]
        require(len(set(mirrors)) == len(mirrors), f'{cid}: duplicate mirror')
        require(isinstance(c['streams'], list), f'{cid}: streams type')
        for s in c['streams']:
            require(isinstance(s, dict) and stream_required <= set(s), f'{cid}: stream fields')
            _check_optional(STREAM_OPTIONAL, s, stream_required | set(STREAM_OPTIONAL), f'{cid}: stream')
            require(url_ok(s['url']) and s['url'] not in streams, f'{cid}: invalid/duplicate stream URL')
            streams.add(s['url'])
            require(re.fullmatch(r'[1-9][0-9]{2,3}[pi]|SD|HD', s['quality']) and isinstance(s['note'], str),
                    f'{cid}: stream metadata')
            require(type(s['published']) is bool and type(s['keep_if_missing']) is bool,
                    f'{cid}: stream policy flags')
            require(s['referer'] == '' or url_ok(s['referer']), f'{cid}: invalid Referer')
            require(not (s['geo_restricted_sl'] and s['direct_m3u8_status'] == 'dead'),
                    f'{cid}: geo-restricted stream cannot also be marked dead')
            if s['geo_restricted_sl'] or s['direct_m3u8_status'] == 'geo_restricted_sl':
                require(not s['published'] or s['keep_if_missing'],
                        f'{cid}: a published geo-restricted stream must set keep_if_missing')
    return channels


@dataclass(frozen=True, order=True)
class Endpoint:
    kind: str
    url: str
    referer: str = ''


@dataclass(frozen=True)
class Result:
    code: int | None
    verdict: str
    detail: str = ''
    attempts: int = 1


def stream_endpoint(s):
    return Endpoint('stream', s['url'], s['referer'])


def is_hls(url):
    return urlsplit(url).path.lower().endswith('.m3u8')


def classify_http(kind, url, code, prefix=b''):
    if code in (403, 451):
        return Result(code, 'restricted', 'possible geo/access restriction; location not inferred')
    if code in (404, 410):
        return Result(code, 'missing')
    if code != 200:
        return Result(code, 'other-http')
    if kind == 'stream' or is_hls(url):
        if (prefix.decode('utf-8-sig', errors='replace').splitlines()[:1] == ['#EXTM3U']
                and re.search(rb'(?m)^#EXT-X-[A-Z-]+:', prefix)):
            return Result(code, 'manifest')
        return Result(code, 'non-hls', 'body did not start with an HLS manifest')
    return Result(code, 'reachable', 'HTTP only; content and playback not verified')


def error_chain(exc):
    pending, seen = [exc], set()
    while pending:
        item = pending.pop()
        if not isinstance(item, BaseException) or id(item) in seen:
            continue
        seen.add(id(item))
        yield item
        pending.extend([item.__cause__, item.__context__, *item.args])


def probe_once(endpoint, timeout, connect_timeout):
    headers = {'User-Agent': UA}
    if endpoint.referer:
        headers['Referer'] = endpoint.referer
    code = None
    try:
        # A separate connect timeout keeps slow-but-alive Sri Lankan edges from
        # consuming the whole read budget, and vice versa.
        with requests.get(endpoint.url, headers=headers, timeout=(connect_timeout, timeout),
                          stream=True) as response:
            code = response.status_code
            prefix = (response.raw.read(4096, decode_content=True)
                      if code == 200 and (endpoint.kind == 'stream' or is_hls(endpoint.url)) else b'')
            return classify_http(endpoint.kind, endpoint.url, code, prefix)
    except (requests.RequestException, urllib3.exceptions.HTTPError, OSError) as exc:
        errors = list(error_chain(exc))
        if any(isinstance(e, socket.gaierror) and e.errno == socket.EAI_NONAME for e in errors):
            return Result(code, 'dns-not-found', 'resolver reported name not found; retry from another network')
        if any(isinstance(e, (requests.Timeout, urllib3.exceptions.TimeoutError, TimeoutError)) for e in errors):
            return Result(code, 'timeout')
        if any(isinstance(e, (requests.exceptions.SSLError, urllib3.exceptions.SSLError)) for e in errors):
            return Result(code, 'tls-error')
        return Result(code, 'network-error', type(exc).__name__)


def probe(endpoint, timeout, retries=0, connect_timeout=None, sleep=time.sleep):
    """Probe one endpoint, retrying only transient outcomes.

    Confirmed HTTP answers (404/410, 403/451, any other code) and DNS NXDOMAIN are
    never retried: they are deterministic for this runner and must not slow the
    sweep. Timeouts, TLS handshake failures, connection errors and 429/5xx are
    retried with exponential backoff, so a single slow Sri Lankan edge does not
    get misclassified as dead.
    """
    connect_timeout = timeout if connect_timeout is None else connect_timeout
    result = probe_once(endpoint, timeout, connect_timeout)
    attempts = 1
    for attempt in range(1, max(0, retries) + 1):
        if result.verdict not in RETRYABLE_VERDICTS and result.code not in RETRYABLE_CODES:
            break
        sleep(min(0.5 * 2 ** (attempt - 1), 4))
        result = probe_once(endpoint, timeout, connect_timeout)
        attempts += 1
    return Result(result.code, result.verdict, result.detail, attempts)


def build_index():
    return {'name': 'Sri Lanka TV Index', 'sources': [
        {'id': 'sl-iptv-all', 'name': 'Sri Lanka IPTV Playlist',
         'description': 'Curated direct streams by category, country and language. See STATUS.md for checks.',
         'type': 'playlist', 'url': RAW + PLAYLISTS['category'], 'languages': RAW + PLAYLISTS['language'],
         'adult': False, 'default': True},
        {'id': 'sl-official-live-sites', 'name': 'Sri Lanka Official Live Sites',
         'description': 'Broadcaster websites and video-channel links. Live coverage varies by broadcaster.',
         'type': 'sites', 'url': RAW + SITE_FILE, 'adult': False, 'default': True},
    ]}


def build_sites(channels):
    rank = {cid: i for i, cid in enumerate(PRIORITY)}
    ordered = sorted(channels, key=lambda c: rank.get(c['tvg_id'], len(rank)))

    def entries(row):
        return [dict(name=c['name'], url=c['site'], mirrors=[u for u in [c['youtube'], *c['mirrors']] if u],
                     tags=list(dict.fromkeys((c['language'], c['category']))), group='Sri Lanka ' + c['category'],
                     pick=True, index=False, position=i) for i, c in enumerate(row, 1)]

    return {'rows': {'live': entries(ordered)},
            'languages': {lang: entries(c for c in ordered if c['language'] == lang) for lang in LANGUAGES}}


def endpoint_inventory(channels, index):
    endpoints = {Endpoint('raw', RAW + path) for path in ('index.json', 'sources.txt')}
    for src in index['sources']:
        endpoints.add(Endpoint('raw', src['url']))
        if 'languages' in src:
            endpoints.add(Endpoint('raw', src['languages']))
    for c in channels:
        endpoints.update(Endpoint('site', u) for u in [c['site'], c['youtube'], *c['mirrors']] if u)
        if c['logo']:
            endpoints.add(Endpoint('logo', c['logo']))
        for s in c['streams']:
            endpoints.add(stream_endpoint(s))
            if s['referer']:
                endpoints.add(Endpoint('site', s['referer']))
    return sorted(endpoints)


def select_streams(channels, results, previous):
    streams = {s['url']: (c['tvg_id'], s) for c in channels for s in c['streams']}
    baseline = {url for url, (_, s) in streams.items() if s['published']}
    require(bool(baseline) and previous <= streams.keys(),
            'empty curated baseline or published URL missing from master; review playlist edits manually')
    healthy = {url for url, (_, s) in streams.items() if results[stream_endpoint(s)].verdict == 'manifest'}
    confirmed_failure = {url for url, (_, s) in streams.items() if not stream_is_protected(s)
                         and results[stream_endpoint(s)].verdict in {'missing', 'non-hls'}}
    retained = previous or baseline
    guard_reference = baseline | retained
    proposed = (retained - confirmed_failure) | healthy
    kept_channels = {streams[u][0] for u in proposed}
    prior_channels = {streams[u][0] for u in guard_reference}
    if not healthy:
        return retained, 'Safety guard active: no valid HLS manifests; retained all curated and previously published streams.'
    if (len(proposed) * 100 < MIN_RETAIN_PERCENT * len(guard_reference)
            or len(kept_channels) * 100 < MIN_RETAIN_PERCENT * len(prior_channels)):
        return retained | healthy, 'Safety guard active: proposed loss exceeded 20%; retained existing streams and added verified candidates only.'
    return proposed, 'Safety guard passed: allowed individual HTTP 404/410 or non-HLS exclusions. DNS failures are reviewed, not auto-pruned.'


def make_playlist(channels, selected, group_by):
    lines = ['#EXTM3U']
    groups = CATEGORIES if group_by == 'category' else LANGUAGES
    for group in groups:
        for c in channels:
            if c[group_by] != group:
                continue
            streams = sorted((s for s in c['streams'] if s['url'] in selected),
                             key=lambda s: -int(re.match(r'\d+', s['quality']).group()) if s['quality'][0].isdigit() else 0)
            for i, s in enumerate(streams):
                quality = 'HD' if s['quality'] == 'HD' or (s['quality'][0].isdigit() and
                                                           int(s['quality'][:-1]) >= 720) else 'SD'
                label = c['name'] + (f' (Mirror {i})' if i else '')
                lines.append(f'#EXTINF:-1 tvg-id="{c["tvg_id"]}@{quality}" tvg-name="{c["name"]}" '
                             f'tvg-logo="{c["logo"]}" group-title="{group}",{label}')
                if s['referer']:
                    lines.append(f'#EXTVLCOPT:http-referrer={s["referer"]}')
                lines.append(s['url'])
    return '\n'.join(lines) + '\n'


def render_status(channels, selected, results, policy, stamp):
    manifests = {e.url for e, r in results.items() if e.kind == 'stream' and r.verdict == 'manifest'}
    published_channels = sum(any(s['url'] in selected for s in c['streams']) for c in channels)
    confirmed_channels = sum(any(s['url'] in manifests & selected for s in c['streams']) for c in channels)
    site_http = sum(results[Endpoint('site', c['site'])].code == 200 for c in channels)
    retained = sorted(((c, s, results[stream_endpoint(s)]) for c in channels for s in c['streams']
                       if s['url'] in selected and results[stream_endpoint(s)].verdict in GEO_VERDICTS),
                      key=lambda row: (row[0]['name'].casefold(), row[1]['url']))
    swaps, unswapped = [], []
    for c in channels:
        primary = results[Endpoint('site', c['site'])]
        if primary.code not in (403, 451, 522, 525, 526) and primary.verdict != 'tls-error':
            continue
        verified = next((m for m in [c['youtube'], *c['mirrors']]
                         if m and results.get(Endpoint('site', m), Result(None, '')).code == 200), None)
        if verified:
            swaps.append((c, verified, primary))
        else:
            unswapped.append((c, primary))
    swaps.sort(key=lambda row: row[0]['name'].casefold())
    unswapped.sort(key=lambda row: row[0]['name'].casefold())
    lines = ['# Sri Lanka source health', '', f'Run timestamp: {stamp} (Sri Lanka Time, UTC+05:30)', '',
             f'Index: `{RAW}index.json`', '',
             f'- Catalog channels / published site cards: **{len(channels)} / {len(channels)}**.',
             f'- Published IPTV entries in **each** playlist: **{len(selected)}** across **{published_channels}** channels.',
             f'- Published IPTV manifests verified this run: **{len(manifests & selected)}** across **{confirmed_channels}** channels.',
             f'- Primary site HTTP 200 responses: **{site_http}/{len(channels)}**; not a live-video playback test.',
             f'- Unique probe targets by kind, URL and Referer: **{len(results)}**.',
             f'- Total direct IPTV channels in the **IPTV tab**: **{published_channels}** '
             f'(`{PLAYLISTS["category"]}` / `{PLAYLISTS["language"]}`).',
             f'- Total official live TV channels in the **Home / Live Sites tab**: **{len(channels)}** '
             f'(`{SITE_FILE}`).',
             f'- Retained geo-restricted / timeout streams: **{len(retained)}** (listed below).', '',
             policy, '',
             '## Retained SL geo-restricted / timeout streams', '',
             'These curated Sri Lankan feeds resolve, but this probe runner sits outside Sri Lanka '
             '(GitHub Actions, US/EU), so they time out, return 403/451, or fail TLS. They are '
             f'**retained**, labelled `{GEO_LABEL}`, and can play from a Sri Lankan network. '
             'They are never a release blocker.', '',
             '| Channel | Stream | Probed HTTP | Verdict | Curation |',
             '|---|---|---:|---|---|']
    if retained:
        lines.extend(f'| {c["name"]} | `{s["url"]}` | {r.code or "—"} | {r.verdict} | {GEO_LABEL} |'
                     for c, s, r in retained)
    else:
        lines.append('| — | — | — | — | None this run |')
    lines.extend(['', '## Suggested primary site swaps', '',
                  'Advisory only: only a confirmed HTTP 403/451/522/525/526 or TLS failure on a primary '
                  'site is listed, and only when an official mirror answered HTTP 200 to this runner.', ''])
    if swaps:
        lines.extend(['| Channel | Current primary | Verified mirror | Primary verdict |', '|---|---|---|---|'])
        lines.extend(f'| {c["name"]} | `{c["site"]}` | `{u}` | {r.verdict} {r.code or ""} |'
                     for c, u, r in swaps)
    if unswapped:
        lines.extend(['', '| Channel | Retained primary | Primary verdict | Action |', '|---|---|---|---|'])
        lines.extend(f'| {c["name"]} | `{c["site"]}` | {r.verdict} {r.code or ""} | '
                     f'{GEO_LABEL}; no verified HTTP 200 alternative exists |' for c, r in unswapped)
    if not swaps and not unswapped:
        lines.append('No swap suggested: every primary that failed has no verified HTTP 200 mirror, '
                     'or every primary answered.')
    lines.extend(['', 'Results reflect the probing network only. HTTP 403/451 can indicate geo or other '
                  'access restrictions. DNS, TLS and timeout results are not proof of a dead URL. '
                  'An HLS header does not prove media segments, rights, DRM compatibility or playback. '
                  'Raw links point to `main`, not the local candidate.', '',
                  '| Target | Attempts | HTTP 200 | HTTP 403/451 | HTTP 404/410 | Other HTTP | No HTTP |',
                  '|---|---:|---:|---:|---:|---:|---:|'])
    for kind in ('raw', 'stream', 'site', 'logo', 'all'):
        codes = Counter(r.code for e, r in results.items() if kind == 'all' or e.kind == kind)
        restricted, missing = codes[403] + codes[451], codes[404] + codes[410]
        count = sum(codes.values())
        lines.append(f'| {kind} | {count} | {codes[200]} | {restricted} | {missing} | '
                     f'{count - codes[200] - restricted - missing - codes[None]} | {codes[None]} |')
    counts = Counter(r.verdict for r in results.values())
    lines.extend(['', 'Verdict totals: ' + ', '.join(f'{k}={v}' for k, v in sorted(counts.items())), '',
                  '## All probe results', '', '| Kind | URL | HTTP | Verdict | Detail / playlist action |',
                  '|---|---|---:|---|---|'])
    for endpoint, result in sorted(results.items()):
        detail = result.detail
        if result.attempts > 1:
            detail = (detail + '; ' if detail else '') + f'{result.attempts} attempts'
        if endpoint.kind == 'stream':
            detail = (detail + '; ' if detail else '') + ('published' if endpoint.url in selected else 'not published')
            if endpoint.referer:
                detail += f'; Referer `{endpoint.referer}`'
        lines.append(f'| {endpoint.kind} | `{endpoint.url}` | {result.code or "—"} | {result.verdict} | {detail} |')
    return '\n'.join(lines) + '\n'


def atomic_write(path, data):
    with NamedTemporaryFile(mode='w', encoding='utf-8', newline='\n', dir=path.parent, delete=False) as tmp:
        temp = Path(tmp.name)
        try:
            tmp.write(data)
            tmp.close()
            temp.chmod(0o644)
            os.replace(temp, path)
        finally:
            temp.unlink(missing_ok=True)


def read_previous(root):
    # On first extraction or if one playlist is absent, use the curated baseline too.
    return {line for name in PLAYLISTS.values() if (root / name).is_file()
            for line in (root / name).read_text(encoding='utf-8').splitlines() if url_ok(line)}


def render_outputs(channels, selected):
    index = build_index()
    playlist = index['sources'][0]
    # Legacy Sources.parseIndex treats every normal label as a playlist, not sites JSON.
    return {'index.json': json_text(index), 'sources.txt': f'{playlist["name"]}|{playlist["url"]}\n',
            SITE_FILE: json_text(build_sites(channels)),
            **{filename: make_playlist(channels, selected, group) for group, filename in PLAYLISTS.items()}}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dry-run', action='store_true', help='check every endpoint and print the full diff without writing files')
    parser.add_argument('--timeout', type=float, default=10, help='per read timeout in seconds')
    parser.add_argument('--connect-timeout', type=float, default=10,
                        help='per connect timeout in seconds (Sri Lankan edges can be slow)')
    parser.add_argument('--retries', type=int, default=2,
                        help='retries for transient timeout/TLS/network/5xx outcomes (0-5)')
    args = parser.parse_args()
    for name in ('timeout', 'connect_timeout'):
        value = getattr(args, name)
        if not 0 < value <= 60:
            parser.error(f'--{name.replace("_", "-")} must be greater than 0 and no more than 60 seconds')
    if not 0 <= args.retries <= 5:
        parser.error('--retries must be between 0 and 5')
    try:
        channels = load_catalog()
        previous = read_previous(ROOT)
        endpoints = endpoint_inventory(channels, build_index())
        with ThreadPoolExecutor(max_workers=16) as pool:
            results = dict(zip(endpoints, pool.map(
                lambda e: probe(e, args.timeout, args.retries, args.connect_timeout), endpoints), strict=True))
        selected, policy = select_streams(channels, results, previous)
        stamp = datetime.now(ZoneInfo('Asia/Colombo')).isoformat(timespec='seconds')
        outputs = render_outputs(channels, selected)
        status = render_status(channels, selected, results, policy, stamp)
        outputs['STATUS.md'] = status
        print(status, end='')  # Always include the entire sweep in the Actions log.
        for file, text in outputs.items():
            path = ROOT / file
            old = path.read_text(encoding='utf-8') if path.exists() else ''
            if file == 'STATUS.md' and old.splitlines()[3:] == text.splitlines()[3:]:
                continue  # Do not make timestamp-only commits.
            if old == text:
                continue
            if args.dry_run:
                print(''.join(difflib.unified_diff(old.splitlines(True), text.splitlines(True),
                                                fromfile=f'a/{file}', tofile=f'b/{file}')), end='')
            else:
                atomic_write(path, text)
    except (OSError, ValueError) as exc:
        parser.exit(1, f'Update refused: {exc}\n')


if __name__ == '__main__':
    main()
