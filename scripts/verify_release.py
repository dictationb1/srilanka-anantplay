#!/usr/bin/env python3
"""Offline release checks. The updater's --dry-run handles the separate live sweep."""
from collections import Counter
from datetime import datetime
import re
import socket
import subprocess
import sys
import unittest
from unittest.mock import Mock, patch

import requests
import yaml

from update_index import (CATEGORIES, GENERATED, LANGUAGES, PLAYLISTS, RAW, ROOT, SITE_FILE,
                          Endpoint, Result, build_index, classify_http, endpoint_inventory,
                          load_catalog, load_json, probe, render_outputs, render_status,
                          require, select_streams, stream_endpoint, url_ok)

MAJORS = set('TVDerana AdaDerana24x7 SirasaTV TV1 Swarnavahini HiruTV Rupavahini ChannelEye '
             'NethraTV ITN VasanthamTV SiyathaTV ShakthiTV TNLTV SupremeTV MonaraTV CharanaTV '
             'ShraddhaTV TheBuddhist DANTamilOli DANNews DanChannels'.split())
EXTINF = re.compile(
    r'#EXTINF:-1 tvg-id="([A-Za-z0-9_-]+\.lk(?:@(?:HD|SD))?)" tvg-name="([^"\r\n]+)" '
    r'tvg-logo="([^"\r\n]*)" group-title="([^"\r\n]+)",(.+)')


def playlist(path, groups):
    lines = iter(path.read_text(encoding='utf-8').splitlines())
    require(next(lines, None) == '#EXTM3U', f'{path.name}: invalid header')
    entries = {}
    for line in lines:
        match = EXTINF.fullmatch(line)
        require(match, f'{path.name}: invalid EXTINF: {line}')
        tvg, name, logo, group, title = match.groups()
        require(group in groups and (not logo or url_ok(logo)), f'{path.name}: invalid metadata')
        url = next(lines, '')
        ref = ''
        if url.startswith('#EXTVLCOPT:http-referrer='):
            ref = url.split('=', 1)[1]
            require(url_ok(ref), f'{path.name}: invalid Referer')
            url = next(lines, '')
        require(url_ok(url) and url not in entries, f'{path.name}: missing, malformed or repeated stream URL: {url}')
        entries[url] = (tvg, name, logo, title, ref)
    require(bool(entries), f'{path.name} is empty')
    return entries


def verify_files(channels):
    index = load_json(ROOT / 'index.json')
    require(index == build_index(), 'index schema or source metadata differs from generator')
    local_targets = []
    for source in index['sources']:
        for key in ('url', 'languages'):
            if key in source:
                url = source[key]
                require(url.startswith(RAW) and url_ok(url), f'bad index URL: {url}')
                name = url.removeprefix(RAW)
                require(name in GENERATED and (ROOT / name).is_file(), f'missing raw target: {name}')
                local_targets.append(name)
    print(f'Gate 1: {len(index["sources"])} JSON sources, {len(local_targets)} valid local source targets')

    fallback = (ROOT / 'sources.txt').read_text(encoding='utf-8').splitlines()
    require(len(fallback) == 1, 'legacy source list must contain only the playlist')
    label, url = fallback[0].split('|')
    require(label and label == label.strip() and url == index['sources'][0]['url'], 'bad legacy line')
    print('Gate 2: 1 legacy playlist entry, no misclassified sites JSON')

    sites = load_json(ROOT / SITE_FILE)
    row = sites['rows']['live']
    require(MAJORS <= {c['tvg_id'].removesuffix('.lk') for c in channels}, 'required major channels missing')
    require(len(row) == len(channels) and set(sites['languages']) == set(LANGUAGES), 'sites coverage')
    require(sum(map(len, sites['languages'].values())) == len(row), 'site language partition')
    for entries in (row, *sites['languages'].values()):
        require(entries and len({v['url'] for v in entries}) == len(entries)
                and len({v['name'] for v in entries}) == len(entries), 'empty site row or duplicate sites')
        for pos, v in enumerate(entries, 1):
            require(type(v['pick']) is bool and type(v['index']) is bool
                    and type(v['position']) is int and v['position'] == pos and url_ok(v['url'])
                    and type(v['mirrors']) is list and all(map(url_ok, v['mirrors']))
                    and type(v['tags']) is list and all(isinstance(t, str) for t in v['tags'])
                    and isinstance(v['name'], str) and isinstance(v['group'], str), f'bad site: {v}')
    counts = {k: len(v) for k, v in sites['languages'].items()}
    print(f'Gate 3: {len(row)} complete live cards; {counts}; all {len(MAJORS)} named major entries')

    categories = playlist(ROOT / PLAYLISTS['category'], CATEGORIES)
    languages = playlist(ROOT / PLAYLISTS['language'], LANGUAGES)
    require(categories == languages, 'playlist entries or playback metadata differ')
    selected = set(categories)
    for name, expected in render_outputs(channels, selected).items():
        require((ROOT / name).read_text(encoding='utf-8') == expected, f'{name}: drift from master/generator')
    print(f'Gate 4: {len(selected)} matching streams per playlist across '
          f'{len({v[0].split("@")[0] for v in categories.values()})} channel IDs')
    print(f'Gate 5: {len(channels)} catalog channels and {sum(len(c["streams"]) for c in channels)} candidates validated')
    return selected


def verify_workflow():
    workflow_path = ROOT / '.github/workflows/auto-update.yml'
    if not workflow_path.exists():
        workflow_path = ROOT / 'docs/auto-update.yml'  # Only used when GitHub blocks workflow changes.
    workflow = yaml.safe_load(workflow_path.read_text(encoding='utf-8'))
    triggers = workflow['on']
    require(triggers['schedule'] == [{'cron': '0 */6 * * *'}] and 'workflow_dispatch' in triggers
            and triggers['pull_request']['branches'] == ['main'], 'workflow triggers')
    require(workflow['permissions'] == {'contents': 'read'}, 'workflow default permissions')
    verify, update = (workflow['jobs'][k] for k in ('verify', 'update'))
    require(update['permissions'] == {'contents': 'write'} and update['needs'] == 'verify'
            and update['if'] == "github.ref == 'refs/heads/main' && github.event_name != 'pull_request'",
            'write job is not isolated to main')
    for job in (verify, update):
        steps = job['steps']
        require(any(s.get('run') == 'python -m pip install -r scripts/requirements.txt' for s in steps),
                'dependency path')
        require(any(s.get('with', {}).get('cache-dependency-path') == 'scripts/requirements.txt' for s in steps),
                'dependency cache path')
        for step in steps:
            if 'run' in step:
                subprocess.run(['bash', '-n'], input=step['run'], text=True, check=True)
    commit = update['steps'][-1]['run']
    require(all(token in commit for token in ('git config user.name', 'git config user.email',
                                             'git status --porcelain', 'git push origin HEAD:refs/heads/main')),
            'unsafe update commit step')
    print(f'Gate 7: {workflow_path.relative_to(ROOT)} loaded with yaml.safe_load; every shell step parsed')


def verify_status(channels, selected):
    status = (ROOT / 'STATUS.md').read_text(encoding='utf-8')
    readme = (ROOT / 'README.md').read_text(encoding='utf-8')
    count = len(endpoint_inventory(channels, build_index()))
    require(f'Unique probe targets by kind, URL and Referer: **{count}**.' in status, 'status probe count')
    expected = Counter((e.kind, e.url) for e in endpoint_inventory(channels, build_index()))
    details = re.findall(r'^\| (raw|stream|site|logo) \| `([^`]+)` \|', status, re.M)
    require(Counter(details) == expected, 'status log missing/extra endpoint rows')
    require(f'published site cards: **{len(channels)} / {len(channels)}**' in status
            and f'each** playlist: **{len(selected)}**' in status, 'status publication counts')
    timestamp = datetime.fromisoformat(status.splitlines()[2].split()[2])
    require(timestamp.strftime('%z') == '+0530', 'status time zone')
    for text in (readme, status):
        require(RAW + 'index.json' in text and 'UTC+05:30' in text, 'wrong docs URL/timezone')
    for source in build_index()['sources']:
        require(source['name'] in readme, 'README missing source setup')
    print(f'Gates 8/9 (offline): {count} complete endpoint log rows, Sri Lanka timestamp and setup verified')


def verify_hygiene():
    files = subprocess.check_output(['git', 'ls-files', '-z', '--cached', '--others', '--exclude-standard'],
                                    cwd=ROOT, text=True).split('\0')
    banned = re.compile(r'your_user' r'name|dictationb' r'01|example[.]' r'com', re.I)
    for name in set(files) - {''}:
        path = ROOT / name
        require(path.suffix not in ('.zip', '.pyc', '.pyo') and '__pycache__' not in path.parts,
                f'unwanted repository artifact: {name}')
        if path.is_file():
            require(not banned.search(path.read_text(encoding='utf-8')), f'placeholder URL in {name}')
    print('Gate 10 (local): no archive, bytecode or placeholder URLs in tracked/non-ignored files')


class HealthTests(unittest.TestCase):
    def setUp(self):
        self.streams = [dict(url=f'https://streams.invalid/{i}.m3u8', referer='',
                             published=i < 10, keep_if_missing=i == 0) for i in range(11)]
        self.catalog = [dict(tvg_id=f'Test{i}.lk', streams=[s]) for i, s in enumerate(self.streams)]
        self.previous = {s['url'] for s in self.streams if s['published']}
        self.results = {stream_endpoint(s): Result(None, 'timeout') for s in self.streams}

    def test_manifest_and_html(self):
        url = 'https://streams.invalid/check.m3u8'
        self.assertEqual(classify_http('stream', url, 200, b'<html>#EXTM3U</html>').verdict, 'non-hls')
        self.assertEqual(classify_http('site', url, 200, b'#EXTM3U\n#EXT-X-VERSION:3\n').verdict, 'manifest')
        self.assertEqual(classify_http('stream', url, 200, b'line\n#EXTM3U\n#EXT-X-VERSION:3\n').verdict, 'non-hls')

    def test_http_codes(self):
        for code, verdict in [(403, 'restricted'), (451, 'restricted'), (404, 'missing'), (410, 'missing'),
                              (503, 'other-http'), (200, 'reachable')]:
            with self.subTest(code=code):
                result = classify_http('site', 'https://sites.invalid/', code)
                self.assertEqual((result.code, result.verdict), (code, verdict))

    @patch('update_index.requests.get')
    def test_headers_tls_and_cleanup(self, get):
        stream = Endpoint('stream', 'https://streams.invalid/feed', 'https://sites.invalid/live')
        response = get.return_value.__enter__.return_value
        response.status_code = 200
        response.raw.read.return_value = b'#EXTM3U\n#EXT-X-TARGETDURATION:6\n'
        self.assertEqual(probe(stream, 5).verdict, 'manifest')
        self.assertEqual(get.call_args.kwargs['headers']['Referer'], stream.referer)
        self.assertIn('Mozilla/', get.call_args.kwargs['headers']['User-Agent'])
        self.assertTrue(get.call_args.kwargs.get('verify', True))
        get.return_value.__exit__.assert_called_once()

    @patch('update_index.requests.get')
    def test_dns_timeout_tls_distinct(self, get):
        target = Endpoint('site', 'https://sites.invalid/live')
        for error, verdict in [(requests.ConnectionError(Mock(), socket.gaierror(socket.EAI_NONAME, 'not found')),
                                'dns-not-found'), (requests.Timeout(), 'timeout'),
                               (requests.exceptions.SSLError(), 'tls-error')]:
            with self.subTest(verdict=verdict):
                get.side_effect = error
                self.assertEqual(probe(target, 1).verdict, verdict)

    def test_no_success_guard(self):
        self.results = dict.fromkeys(self.results, Result(404, 'missing'))
        selected, message = select_streams(self.catalog, self.results, self.previous)
        self.assertEqual(selected, self.previous)
        self.assertIn('no valid HLS', message)

    def test_mass_loss_guard(self):
        self.results = dict.fromkeys(self.results, Result(410, 'missing'))
        self.results[stream_endpoint(self.streams[0])] = Result(200, 'manifest')
        selected, message = select_streams(self.catalog, self.results, self.previous)
        self.assertGreaterEqual(selected, self.previous)
        self.assertIn('exceeded 20%', message)

    def test_successful_sweep_records_published_manifest_and_site(self):
        target = 'https://sites.invalid/live'
        channels = [dict(self.catalog[0], site=target)]
        stream = stream_endpoint(self.streams[0])
        results = {stream: Result(200, 'manifest'), Endpoint('site', target): Result(200, 'reachable')}
        report = render_status(channels, {stream.url}, results, 'test policy', '2026-11-20T12:00:00+05:30')
        self.assertIn('Published IPTV manifests verified this run: **1** across **1** channels.', report)
        self.assertIn('Primary site HTTP 200 responses: **1/1**;', report)

    def test_individual_failure_geo_dns_and_manual_override(self):
        protected = next(s for s in self.streams if s['keep_if_missing'])
        eligible = [s for s in self.streams if s['url'] in self.previous and not s['keep_if_missing']]
        healthy, gone, access, dns = eligible[:4]
        new = next(s for s in self.streams if s['url'] not in self.previous)
        for s, outcome in [(protected, Result(404, 'missing')), (healthy, Result(200, 'manifest')),
                           (gone, Result(410, 'missing')), (access, Result(451, 'restricted')),
                           (dns, Result(None, 'dns-not-found')), (new, Result(200, 'manifest'))]:
            self.results[stream_endpoint(s)] = outcome
        selected, _ = select_streams(self.catalog, self.results, self.previous)
        self.assertEqual(selected, (self.previous - {gone['url']}) | {new['url']})


def main():
    channels = load_catalog()
    selected = verify_files(channels)
    if not unittest.TextTestRunner(verbosity=2, stream=sys.stdout).run(
            unittest.defaultTestLoader.loadTestsFromTestCase(HealthTests)).wasSuccessful():
        return 1
    print('Gate 6 (regression): health classification, request headers and retention safety verified')
    verify_workflow()
    verify_status(channels, selected)
    verify_hygiene()
    return 0


if __name__ == '__main__':
    sys.exit(main())
