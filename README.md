# GeorgeK's Unraid templates

Unraid Community Applications templates for GeorgeK's Docker apps. Community Applications reads
this repository; each app keeps its own code, documentation and issue tracker in its own repo.

| Template | App | Image |
| --- | --- | --- |
| [`pia-qbittorrent.xml`](pia-qbittorrent.xml) | [pia-qbittorrent-docker](https://github.com/GeorgeAL78/pia-qbittorrent-docker) — qBittorrent behind Private Internet Access | `gjergjk/pia-qbittorrent` |
| [`netlens.xml`](netlens.xml) | [NetLens](https://github.com/GeorgeAL78/netlens) — a dashboard for UniFi networks | `gjergjk/netlens` |
| [`pia-iptv.xml`](pia-iptv.xml) | [pia-iptv](https://github.com/GeorgeAL78/pia-iptv) — m3u-editor with a built-in PIA VPN, in one container | `gjergjk/pia-iptv` |
| [`folder2photos.xml`](folder2photos.xml) | [Folder2Photos](https://github.com/GeorgeAL78/folder2photos) — uploads new photos from a folder to Google Photos, once each | `gjergjk/folder2photos` |

`ca_profile.xml` is the repository's profile in Community Applications.

Where each template is edited:

- `pia-iptv.xml` — in pia-iptv (`unraid/`), copied here by hand on release.
- `pia-qbittorrent.xml` — here. pia-qbittorrent-docker copies it from this repository, so
  installs that still point at its old address get the same file.
- `netlens.xml` — in NetLens (`unraid/netlens.xml`); `.github/workflows/sync-templates.yml`
  copies it here every 6 hours, but only a valid template whose `TemplateURL` points at this
  repository.
- `folder2photos.xml` — in Folder2Photos (`unraid/folder2photos.xml`); copied here by the same sync workflow.

Support: open an issue on the app's own repository, not here.
