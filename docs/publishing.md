# Publishing

How a package gets from a spec to this site. Nothing on this page has run end to end yet; it is the plan the files in this
repository implement.

## The idea

- **Releases hold the files.** Each upload is a GitHub release (tag such as `r20261112`) with the RPMs attached. They stay
  there, so an old version is always one link away.
- **This site holds the current repository.** When a release is published, a workflow downloads that release's RPMs,
  signs them, builds the repository metadata and deploys the result with GitHub Pages. Only the newest release is in `/repo/`.
- **The wiki and the API reference are built at the same time.** `/wiki/` is the platform documentation (the Markdown of
  `ecp-mkosi` plus the `foundation` README, by `ecp-mkosi/scripts/build-wiki`). `/wiki/api/` is Doxygen over the sources of
  `ersa-bluetooth` and the Dialer at the commits their specs pin (`docs/doxygen/Doxyfile`). Both come from the public
  repositories as they are when a release is published, so a release always carries current documentation.
- **Nothing is built by the workflow.** Building is done in a Tumbleweed container on a developer's machine
  (`scripts/build-repo-podman`). A first attempt to build on GitHub's runners failed because of an incomplete openSUSE mirror, and
  this way it cannot.

## To publish

```
scripts/build-repo-podman repo                 # build everything in a container (or use the RPMs of an image build)
scripts/release-rpms r20261112 repo            # create the release and attach the RPMs (add --draft to look first)
```

Publishing the release starts the workflow `Publish packages site`. You can also start it by hand from the Actions tab.

## One-time setup

1. **Pages.** Settings, Pages, Source: *GitHub Actions*. Custom domain: `pkgs-compute.ersa.dev`.
2. **DNS.** A `CNAME` record for `packages` pointing at `ersa-ecpx.github.io`. Enable *Enforce HTTPS* once the certificate is issued.
3. **Signing key.** `scripts/make-signing-key` creates a key pair and prints what to do with it. The secret half goes into two
   repository secrets (`GPG_PRIVATE_KEY`, `GPG_PASSPHRASE`) and never anywhere else. Without them the workflow still publishes, but
   the repository is **unsigned**, the site says so, and `foundation` will not use it.
4. **A licence for every package.** The pages show each package's licence from its spec. Several specs still say
   `LicenseRef-Unknown` (the package pages show "not decided yet"); choose the licence of each project and set it before publishing.

## What is where

| File | Purpose |
| --- | --- |
| `scripts/build-site` | builds this site (and the repository, when given RPMs) |
| `scripts/release-rpms` | creates a release with the RPMs |
| `scripts/make-signing-key` | makes the signing key |
| `docs/doxygen/Doxyfile` | the C++ API reference |
| `.github/workflows/pages.yml` | publishes on every release |
| `.github/workflows/build-rpms.yml` | the old build workflow, manual only |

## Limits

- The C++ code has no Doxygen comments yet, so `/wiki/api/` shows structure (files, classes, include graphs) and the Markdown
  documents, not prose. It fills in as `///` comments are written.
- The wiki and the API reference are not part of a release's files; they are rebuilt from the repositories each time.

- Only the newest release is a repository. A system that needs an older version installs the file from its release.
- The site is rebuilt from scratch each time; there is no history of the site itself, only of the releases.
