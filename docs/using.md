# Use the repository

The repository is signed. Your system refuses it without the signing key, and that is on purpose: a package manager that
installs unsigned code as root has no defence against a tampered download.

> **Status.** This page describes the intended setup. The signing key does not exist yet and the repository has not been
> published, so none of the commands below has been run against the real address.

## On the Ersa Compute Platform

The image has the platform's packages already. To follow updates between images, add the repository with `foundation`, which
checks the key's fingerprint with you first:

```
curl -LO https://packages.ersa.dev/ersa-ecpx.asc
foundation repo add ersa https://packages.ersa.dev/repo/ --key ersa-ecpx.asc --name "Ersa Compute Platform packages"
foundation repo refresh ersa
```

The image itself is read-only, so a newer `foundation` or splash theme arrives with the next image (see updates in the
platform's own documentation). The repository matters for bundles and for other systems.

## On another openSUSE Tumbleweed system

```
curl -LO https://packages.ersa.dev/ersa-ecpx.asc
sudo rpm --import ersa-ecpx.asc
sudo zypper addrepo --check --refresh https://packages.ersa.dev/ersa.repo
sudo zypper install foundation
```

`ersa.repo` turns on both checks (`gpgcheck=1` for each package, `repo_gpgcheck=1` for the repository's list).

## Check the key

The key's fingerprint is shown on the home page of this site once a key exists. Compare it with
`gpg --show-keys ersa-ecpx.asc` before you trust it.

## An older version

Open the package's page from the [package list](index.html#packages). It links every version that was ever released, with the
file itself. Install one with `sudo zypper install ./file.rpm` (it is still checked against the key).
