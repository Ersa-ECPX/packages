# Building

Packages are built in an openSUSE Tumbleweed container, never on the host: a compiled package must link against the libraries of the
image it is installed in.

```
scripts/build-repo-podman                       # every package into repo/ (needs podman and network access)
ONLY="ersa-boot-splash" scripts/build-repo-podman      # a subset
SOURCES_DIR=/path/to/tarballs scripts/build-repo-podman  # use local source tarballs named as each Source0
```

`scripts/build-repo` does the work inside the container. It installs each spec's build dependencies, downloads the sources
named by `Source0` (`rpmdev-spectool`), runs `rpmbuild -ba` (the `foundation` spec's `%check` runs the foundation unit tests), copies
the RPMs and source RPMs to one directory and runs `createrepo_c`. With `GPG_PRIVATE_KEY` set it signs the RPMs and writes the
repository signature.

## Releasing a new `foundation`

Tag `v<Version>` in the `foundation` repository, bump `Version:` and `Release:` in `foundation/foundation.spec` here, push. A compiled
package (`ersa-bluetooth`, `ersa-dialer`) is updated by changing its pinned `%global commit`.

## The packages

| Directory | Package | Source |
| --- | --- | --- |
| `foundation/` | `foundation`, `foundationd`, `foundation-installer` | the tag `v<Version>` of the `foundation` repository |
| `ersa-boot-splash/` | `ersa-boot-splash` | `SOURCES/` in the directory; logos rendered from the SVGs at build time |
| `ersa-bluetooth/` | `ersa-bluetooth` | the commit pinned in `%global commit` |
| `ersa-dialer/` | `ersa-dialer` | the commit pinned in `%global commit` |

Descriptions say "Ersa Compute Platform"; `ECP` is only for code.
