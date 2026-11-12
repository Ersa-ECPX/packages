# Ersa Compute Platform packages

This is where the packages of the Ersa Compute Platform come from: the management tools (`foundation`, `foundationd`, the
installer), the boot splash, the Bluetooth bridge and the phone dialer. The platform image already carries them. This site is for
three things:

- **Getting an update to one of them** without waiting for a new image.
- **Using them on another openSUSE Tumbleweed system.**
- **Finding an older version**: every upload is kept as a release with its files.

Packages are built for openSUSE Tumbleweed in a clean container, never on a developer's machine, so that a compiled package is
linked against the same libraries as the image it goes into.

## How it is organised

| Where | What |
| --- | --- |
| This site, [`/repo/`](repo/) | the **current** packages as an ordinary RPM repository, signed, for `zypper`, `dnf` and `foundation` |
| [GitHub releases](https://github.com/Ersa-ECPX/packages/releases) | **every** upload with its files, so any earlier version can still be downloaded |
| [The wiki](wiki/) | the platform's documentation: architecture, installer, foundation, updates, storage |
| [C++ API reference](wiki/api/) | generated from the sources of `ersa-bluetooth` and the Dialer |
| [The source](https://github.com/Ersa-ECPX/packages) | the RPM specs, patches and small sources |

Start with [using the repository](using.md). The list below shows what is in it now.
