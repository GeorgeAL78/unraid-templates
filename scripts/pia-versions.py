#!/usr/bin/env python3
"""Keeps the version text in pia-qbittorrent.xml in step with the latest STABLE
release of GeorgeAL78/pia-qbittorrent-docker (the one marked Latest on GitHub, which
is created only after its image is published).

Reads that release's Dockerfile (qBittorrent, libtorrent, Boost, Alpine) and Alpine's
package index (OpenVPN, WireGuard, iptables), rewrites the four strings in the
Overview, and leaves the file untouched when nothing changed. Prints CHANGED or
UNCHANGED. Exits non-zero if a string it expects is missing.
"""
import io, json, os, re, sys, tarfile, urllib.request
import xml.etree.ElementTree as ET

SRC = 'GeorgeAL78/pia-qbittorrent-docker'
FILE = 'pia-qbittorrent.xml'
PKGS = ('openvpn', 'wireguard-tools', 'iptables')


def get(url):
    headers = {'Accept': 'application/vnd.github+json'}
    # Authenticated GitHub API calls: anonymous ones share a 60/hour limit per runner
    # address and fail with 403 "rate limit exceeded" on busy runners.
    token = os.environ.get('GITHUB_TOKEN')
    if token and url.startswith('https://api.github.com/'):
        headers['Authorization'] = 'Bearer ' + token
    req = urllib.request.Request(url, headers=headers)
    return urllib.request.urlopen(req, timeout=60).read()


def one(rx, text, what):
    found = re.findall(rx, text)
    if len(set(found)) != 1:
        sys.exit(f'::error::{what}: expected one value, found {found or "none"}')
    return found[0]


def alpine(branch):
    versions = {}
    for repo in ('main', 'community'):
        data = get(f'https://dl-cdn.alpinelinux.org/alpine/v{branch}/{repo}/x86_64/APKINDEX.tar.gz')
        with tarfile.open(fileobj=io.BytesIO(data), mode='r:gz') as t:
            index = t.extractfile('APKINDEX').read().decode('utf-8', 'replace')
        for block in index.split('\n\n'):
            f = dict(l.split(':', 1) for l in block.splitlines() if len(l) > 1 and l[1] == ':')
            if f.get('P') in PKGS:
                versions[f['P']] = re.sub(r'-r\d+$', '', f['V'])
    missing = [p for p in PKGS if p not in versions]
    if missing:
        sys.exit(f'::error::not in the Alpine {branch} index: {missing}')
    return versions


def main():
    tag = json.loads(get(f'https://api.github.com/repos/{SRC}/releases/latest'))['tag_name']
    df = get(f'https://raw.githubusercontent.com/{SRC}/{tag}/Dockerfile').decode()
    qbt = one(r'qBittorrent/tarball/release-(\d+\.\d+\.\d+)\b', df, 'qBittorrent pin')
    lt = one(r'libtorrent/releases/download/v(\d+\.\d+\.\d+)/', df, 'libtorrent pin')
    boost = one(r'boost/releases/download/boost-(\d+\.\d+\.\d+(?:-\d+)?)/', df, 'Boost pin')
    branch = one(r'(?m)^FROM alpine:(\d+\.\d+)', df, 'Alpine base')
    pk = alpine(branch)
    print(f'{SRC} {tag}: qBittorrent {qbt}, libtorrent {lt}, Boost {boost}, Alpine {branch}, '
          f'OpenVPN {pk["openvpn"]}, WireGuard {pk["wireguard-tools"]}, iptables {pk["iptables"]}')

    text = io.open(FILE, encoding='utf-8', newline='').read()
    new = text
    for rx, repl in (
        (r'qBittorrent [0-9][0-9A-Za-z.]* combined', f'qBittorrent {qbt} combined'),
        (r'qBittorrent [0-9][0-9A-Za-z.]* with libtorrent [0-9.]+', f'qBittorrent {qbt} with libtorrent {lt}'),
        (r'Alpine Linux [0-9.]+, Boost [0-9.\-]+', f'Alpine Linux {branch}, Boost {boost}'),
        (r'OpenVPN [0-9.]+, WireGuard [0-9.]+, iptables [0-9.]+',
         f'OpenVPN {pk["openvpn"]}, WireGuard {pk["wireguard-tools"]}, iptables {pk["iptables"]}'),
    ):
        if len(re.findall(rx, new)) != 1:
            sys.exit(f'::error::{FILE}: expected exactly one match for "{rx}"')
        new = re.sub(rx, repl, new)
    if new == text:
        print('UNCHANGED')
        return
    ET.fromstring(new.encode('utf-8'))       # must still parse
    io.open(FILE, 'w', encoding='utf-8', newline='').write(new)
    print('CHANGED')


if __name__ == '__main__':
    main()
