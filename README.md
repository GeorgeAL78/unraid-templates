# GeorgeK's Unraid templates

Unraid Community Applications templates for GeorgeK's Docker apps. Community Applications reads
this repository; each app keeps its own code, documentation and issue tracker in its own repo.

| Template | App | Image |
| --- | --- | --- |
| [`pia-qbittorrent.xml`](pia-qbittorrent.xml) | [pia-qbittorrent-docker](https://github.com/GeorgeAL78/pia-qbittorrent-docker) — qBittorrent behind Private Internet Access | `gjergjk/pia-qbittorrent` |
| [`netlens.xml`](netlens.xml) | [NetLens](https://github.com/GeorgeAL78/netlens) — a dashboard for UniFi networks | `gjergjk/netlens` |

`ca_profile.xml` is the repository's profile in Community Applications.

Each app keeps its template in its own repository (`unraid/netlens.xml` in NetLens,
`pia-qbittorrent.xml` in pia-qbittorrent-docker); `.github/workflows/sync-templates.yml` copies
them here every 6 hours, but only a valid template whose `TemplateURL` points at this repository.

Support: open an issue on the app's own repository, not here.
