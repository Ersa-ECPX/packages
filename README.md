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

## Publishing: packages.ersa.dev (planned, not yet run)

The packages are published at **https://packages.ersa.dev** (GitHub Pages): the documentation, a page for each package and
the current signed RPM repository. Each upload is also kept as a GitHub release with its files, so every older version stays
downloadable and the package pages link them. Nothing is built on GitHub: you build in the container, then

```sh
scripts/build-repo-podman repo            # or use the RPMs an image build made (ecp-mkosi: mkosi.packages/)
scripts/release-rpms r20261112 repo       # create the release and attach the RPMs (--draft to look first)
```

Publishing the release starts `.github/workflows/pages.yml`, which downloads its RPMs, signs them and the repository metadata
and deploys the site. The setup (Pages source, DNS, the signing key from `scripts/make-signing-key`) and the limits are in
[docs/publishing.md](docs/publishing.md); `scripts/build-site OUTPUT` builds the same site locally (`--rpms DIR` to include a
repository). Tested so far: the site generator and its tests, the signing of RPMs with a throwaway key (rpm 6). Not run: anything
on GitHub, `createrepo_c`, the older rpm signing path (Tumbleweed, Ubuntu), and a client using the repository.

The repository file `ersa.repo` it publishes turns on `gpgcheck=1` and `repo_gpgcheck=1`. The image build (`ecp-mkosi`) does not
use this repository yet: it builds the same packages into its local `mkosi.packages/` directory.

`.github/workflows/build-rpms.yml` is the earlier idea (build everything on GitHub's runners); it stays manual-only because the
openSUSE mirror served an incomplete index to the runner.

Tests: `python3 -m unittest discover -s tests`.
