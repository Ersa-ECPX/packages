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

## Publishing: pkgs-compute.ersa.dev (planned, not yet run)

The packages are published at **https://pkgs-compute.ersa.dev** (GitHub Pages): a page for each package, the current signed RPM
repository, the platform wiki at `/wiki/` and the C++ API reference at `/wiki/api/` (the same layout as pkgs-wearables.ersa.dev).
Each upload is also kept as a GitHub release with its files, so every older version stays downloadable and the package pages
link them. GitHub builds the packages, in a Tumbleweed container (`.github/workflows/build-rpms.yml`):

```sh
git tag r20261112 && git push origin r20261112     # builds, makes the release, signs and publishes
```

Before tagging, whatever a spec downloads must exist (`foundation` builds the tag `v<Version>` of the `foundation` repository). To
build on your own machine instead: `scripts/build-repo-podman repo`, then `scripts/release-rpms r20261112 repo --draft`.

The setup (Pages source, DNS, the signing key from `scripts/make-signing-key`) and the limits are in
[docs/publishing.md](docs/publishing.md); `scripts/build-site OUTPUT` builds the same site locally (`--rpms DIR` to include a
repository). The container takes its packages from openSUSE's own servers (`OPENSUSE_MIRROR`, set by the workflow) instead of the
download.opensuse.org redirector, which once sent a runner to a mirror that was mid-sync. Tested so far: the site generator and its
tests, the signing of RPMs with a throwaway key (rpm 6), the Doxygen reference (`docs/doxygen/Doxyfile`, Doxygen 1.18 on the sources
at the pinned commits: no warnings, about 90 classes), and `scripts/build-repo` in a local container. Not run: anything on GitHub,
`createrepo_c` on the host, the older rpm signing path (Tumbleweed, Ubuntu), and a client using the repository.

The repository file `ersa.repo` it publishes turns on `gpgcheck=1` and `repo_gpgcheck=1`. The image build (`ecp-mkosi`) does not
use this repository yet: it builds the same packages into its local `mkosi.packages/` directory.

Tests: `python3 -m unittest discover -s tests`.
