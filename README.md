# Open File Explorer
![Latest Version](https://img.shields.io/github/v/tag/mbeckh/picard-plugin-open-explorer?sort=semver&filter=v*&style=flat-square&label=latest)
![Supports](https://img.shields.io/badge/dynamic/yaml?url=https%3A%2F%2Fraw.githubusercontent.com%2Fmbeckh%2Fpicard-plugin-open-explorer%2Frefs%2Fheads%2Fmain%2F.works_with.yml&query=%24.picard.from&prefix=picard+%3E%3D&style=flat-square&label=supports&color=orange)
![Tested with](https://img.shields.io/badge/dynamic/yaml?url=https%3A%2F%2Fraw.githubusercontent.com%2Fmbeckh%2Fpicard-plugin-open-explorer%2Frefs%2Fheads%2Fmain%2F.works_with.yml&query=%24.picard.latest&prefix=picard+%3C%3D&style=flat-square&label=tested+with&color=green)

A plugin for [MusicBrainz Picard](https://picard.musicbrainz.org) to open Windows file explorer for a selected file or path.

## What it Does

The plugin adds a context menu action to open Windows Explorer for a selected file or path.

The plugin also patches the Picard FileBrowser for opening source folders.

Please note that this plugin works for Picard running on Windows only. On other systems, it simply does nothing.

> [!IMPORTANT]
> This plugin requires the [Monkey Plugin](https://github.com/mbeckh/picard-plugin-monkey/) as a prerequisite. Please install this plugin first.

This plugin modifies Picard _way beyond_ the level that was intended by the implementers of the official API. It relies heavily on internal and private implementation details and monkey patches its way across the Picard code base to achieve its goals.

> [!WARNING]
> **Even a minor update of Picard can break this plugin** until I'm able to supply an updated version. The plugin is typically tested with the latest version of Picard only.

## License

The code is released under the Apache License Version 2.0. Please see [LICENSE](LICENSE) for details and [NOTICE](NOTICE) for the required information when using picard-plugin-open-explorer in your own work.
