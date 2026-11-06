# Ersa Compute Platform packages

RPM specs, patches and small sources for the packages of the Ersa Compute Platform, built for
openSUSE Tumbleweed. Two other repositories belong to the platform: `ecp-mkosi` (the image build and the
architecture documentation) and `foundation` (the management command line, service and installer).

| Directory | Package | Source |
| --- | --- | --- |
| `foundation/` | `foundation`, `foundationd`, `foundation-installer` (one spec) | the tag `v<Version>` of the `foundation` repository (`Source0` is its GitHub archive) |
| `ersa-boot-splash/` | `ersa-boot-splash` (Plymouth theme) | in this directory (`SOURCES/`); the logo PNGs are rendered from `SOURCES/ersa-logo.svg` and `ersa-dark-logo.svg` at build time; two Plymouth themes, `ersa` and `ersa-dark` |
| `ersa-bluetooth/` | `ersa-bluetooth` (compiled) | GitHub archive of the commit pinned in `%global commit` (`Ersa-ECPX/ersa-bluetooth`) |
| `ersa-dialer/` | `ersa-dialer` (compiled) | GitHub archive of the commit pinned in `%global commit` (`Ersa-ECPX/Dialer`) |

`ersa-logo.svg` and `ersa-dark-logo.svg` are copies of `branding/ersa-mark-light.svg` and `ersa-mark-dark.svg` in
`ecp-mkosi`, which stays the logos' master; copy them again when the logo changes. Package descriptions say "Ersa Compute Platform"; `ECP` is only for code.

## Building

Packages are built in an openSUSE Tumbleweed container, never on the host (a compiled package must link against the
libraries of the image it is installed in):

```sh
scripts/build-repo-podman            # all packages -> repo/ (needs podman and network access)
ONLY="ersa-boot-splash" scripts/build-repo-podman       # a subset
SOURCES_DIR=/path/to/tarballs scripts/build-repo-podman  # use local source tarballs named as each Source0
```

`scripts/build-repo` does the work inside the container: it installs each spec's build dependencies, downloads the
sources named by `Source0` URLs (`rpmdev-spectool`), runs `rpmbuild -ba` (the `foundation` spec's `%check` runs the
foundation unit tests), copies the RPMs and source RPMs to one directory, and runs `createrepo_c`. If
`GPG_PRIVATE_KEY` (and `GPG_PASSPHRASE`) are set in the environment, it signs the RPMs and writes
`repodata/repomd.xml.asc` and `ersa-ecpx.asc` (the public key). Without a key the repository is unsigned and
foundation refuses to use it (`foundation` requires a valid detached signature of `repomd.xml`).

Releasing a new `foundation`: tag `v<Version>` in the `foundation` repository, bump `Version:` and `Release:` in
`foundation/foundation.spec` here, push. A compiled package is updated by changing its pinned `%global commit`.

## Publishing (workflow, untested)

`.github/workflows/build-rpms.yml` builds on every push and pull request, and on pushes to `main` and `v*` tags
pushes the result to the `gh-pages` branch (served at `https://ersa-ecpx.github.io/packages/`). It has **never run**
on GitHub: see the comments at its top for what is verified, the secrets (`GPG_PRIVATE_KEY`, `GPG_PASSPHRASE`; no
signing key exists yet) and the manual steps (enable Pages for the `gh-pages` branch; the tag `v0.5.0` of
`foundation` must exist; the source repositories must be readable). Each publish replaces the branch, so only the
latest RPMs are served.

The published `ersa.repo` file is a zypp/dnf repository definition with `gpgcheck=1` and `repo_gpgcheck=1`.
The image build (`ecp-mkosi`) does not use this repository yet: it builds the same packages into its local
`mkosi.packages/` directory (see that repository's README).
