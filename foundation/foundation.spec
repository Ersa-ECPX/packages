Name:           foundation
Version:        0.6.0
Release:        2%{?dist}
Summary:        Ersa Compute Platform management command line
License:        LicenseRef-Unknown
BuildArch:      noarch
URL:            https://github.com/Ersa-ECPX/foundation
# The tag v<Version> of the foundation repository (its root is the source tree). The archive's top-level
# directory is foundation-<Version>, which the %%autosetup below expects.
Source0:        %{url}/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz

# For %check (the unit tests run a private D-Bus session bus; tests of tools that are missing are skipped).
BuildRequires:  python3 >= 3.9
BuildRequires:  python3-gobject
BuildRequires:  python3-solv
BuildRequires:  dbus-1-daemon
BuildRequires:  gpg2
BuildRequires:  zstd
BuildRequires:  systemd
BuildRequires:  util-linux
BuildRequires:  rpm

Requires:       python3 >= 3.9
# GLib/GDBus bindings (Tumbleweed names the real package per Python version, python313-gobject, and
# provides python3-gobject for all of them). The command line is a client of foundationd.
Requires:       python3-gobject
Requires:       foundationd = %{version}-%{release}

%description
Foundation is the command line of the Ersa Compute Platform: it shows the system and its boot
slots, manages the A/B boot slots, installs applications, runs legacy RPMs as system extensions,
manages system extensions and settings, and follows long operations. It changes nothing itself; every
command is a request to the Ersa Compute Platform management service (foundationd).
Output is human-readable by default and machine-readable with --json.

%package -n foundationd
Summary:        Ersa Compute Platform management service
Requires:       python3 >= 3.9
Requires:       python3-gobject
Requires:       polkit
Requires:       python3-solv
Requires:       gpg2
Requires:       zstd
Requires:       dbus-1
# Compat packages are inspected and unpacked with the rpm tools; the GPT UUIDs of boot slots are set with
# sfdisk; the unified kernel images and the default boot entry are handled with bootctl.
Requires:       rpm
Requires:       util-linux
# Deploy (installing to a disk): partitions, the ESP and the data volume
Requires:       mtools
Requires:       dosfstools
Requires:       btrfsprogs
Requires:       systemd
Recommends:     systemd-boot
# Applications use libflatpak; without it the Apps interface reports that it is unavailable.
Recommends:     flatpak
Recommends:     typelib-1_0-Flatpak-1_0

%package -n foundation-installer
Summary:        Ersa Compute Platform graphical installer
Requires:       python3 >= 3.9
Requires:       python3-gobject
Requires:       typelib-1_0-Gtk-4_0
Requires:       typelib-1_0-Adw-1
Requires:       foundation = %{version}-%{release}

%package -n foundation-updater
Summary:        Ersa Compute Platform system update window
Requires:       python3 >= 3.9
Requires:       python3-gobject
Requires:       typelib-1_0-Gtk-4_0
Requires:       typelib-1_0-Adw-1
Requires:       foundation = %{version}-%{release}
Requires:       polkit

%description -n foundation-updater
A window for updating the Ersa Compute Platform: check for an update at the configured update source, install it into the
spare slot, and restart into it, or install an update file by hand. It is a client of foundationd (the Updates interface)
and holds no policy of its own; foundationd asks polkit for the administrator's password before it installs anything.

%description -n foundation-installer
A window for installing the Ersa Compute Platform on a disk: choose the disk, review
what will be erased, install with a progress bar. It is a client of foundationd (the Deploy
interface) and holds no policy of its own.

%description -n foundationd
The D-Bus service behind the foundation command line and other Ersa Compute Platform clients: a root
service, started on demand by D-Bus activation, that authorizes every change with polkit and runs
long operations as jobs in separate worker processes. It manages boot slots, applications, compat
packages, system extensions and settings.

%prep
%autosetup -n %{name}-%{version}

%build

%check
python3 -m unittest discover -s tests

%install
install -Dpm0755 bin/foundation %{buildroot}%{_bindir}/foundation
install -d %{buildroot}/usr/lib/foundation/foundation
install -pm0644 foundation/*.py %{buildroot}/usr/lib/foundation/foundation/

install -d %{buildroot}/usr/lib/foundation/foundationd/api %{buildroot}/usr/lib/foundation/foundationd/backends %{buildroot}/usr/lib/foundation/foundationd/workers
install -pm0644 foundationd/*.py %{buildroot}/usr/lib/foundation/foundationd/
install -pm0644 foundationd/api/*.py %{buildroot}/usr/lib/foundation/foundationd/api/
install -pm0644 foundationd/backends/*.py %{buildroot}/usr/lib/foundation/foundationd/backends/
install -pm0644 foundationd/workers/*.py %{buildroot}/usr/lib/foundation/foundationd/workers/
install -d %{buildroot}/usr/lib/foundation/foundation_updater
install -pm0644 foundation_updater/*.py %{buildroot}/usr/lib/foundation/foundation_updater/
install -pm0644 foundation_updater/*.svg %{buildroot}/usr/lib/foundation/foundation_updater/
install -Dpm0755 bin/ersa-updater %{buildroot}%{_bindir}/ersa-updater
install -Dpm0644 data/applications/org.ersa.Updater.desktop %{buildroot}/usr/share/applications/org.ersa.Updater.desktop
install -Dpm0644 data/icons/org.ersa.Updater.svg %{buildroot}/usr/share/icons/hicolor/scalable/apps/org.ersa.Updater.svg
install -d %{buildroot}/usr/lib/foundation/foundation_installer
install -pm0644 foundation_installer/*.py %{buildroot}/usr/lib/foundation/foundation_installer/
install -pm0644 foundation_installer/*.svg %{buildroot}/usr/lib/foundation/foundation_installer/
install -Dpm0755 bin/ersa-installer %{buildroot}%{_bindir}/ersa-installer
install -Dpm0644 data/applications/org.ersa.Installer.desktop %{buildroot}/usr/share/applications/org.ersa.Installer.desktop
install -Dpm0644 data/icons/org.ersa.Installer.svg %{buildroot}/usr/share/icons/hicolor/scalable/apps/org.ersa.Installer.svg
install -Dpm0755 data/live/live-session %{buildroot}/usr/libexec/ecp/live-session
install -Dpm0644 data/live/ersa-live-session.service %{buildroot}/usr/lib/systemd/system/ersa-live-session.service
install -Dpm0755 data/libexec/foundationd %{buildroot}/usr/libexec/foundationd
install -Dpm0755 data/libexec/foundationd-worker %{buildroot}/usr/libexec/foundationd-worker
install -Dpm0755 data/libexec/foundation-bundles %{buildroot}/usr/libexec/foundation-bundles
install -Dpm0755 data/libexec/foundation-update-notify %{buildroot}/usr/libexec/foundation-update-notify
install -Dpm0755 data/libexec/foundation-splash-sync %{buildroot}/usr/libexec/foundation-splash-sync
install -Dpm0644 data/systemd/foundation-bundles-select.service %{buildroot}/usr/lib/systemd/system/foundation-bundles-select.service
install -Dpm0644 data/systemd/foundation-bundles-refresh.service %{buildroot}/usr/lib/systemd/system/foundation-bundles-refresh.service
install -Dpm0644 data/systemd-user/foundation-update-notify.service %{buildroot}/usr/lib/systemd/user/foundation-update-notify.service
install -Dpm0644 data/systemd-user/foundation-update-notify.path %{buildroot}/usr/lib/systemd/user/foundation-update-notify.path
install -Dpm0644 data/systemd-user/foundation-splash-sync.service %{buildroot}/usr/lib/systemd/user/foundation-splash-sync.service
install -Dpm0644 data/dbus/org.ersa.Foundation1.xml %{buildroot}/usr/share/dbus-1/interfaces/org.ersa.Foundation1.xml
install -Dpm0644 data/dbus/org.ersa.Foundation1.service %{buildroot}/usr/share/dbus-1/system-services/org.ersa.Foundation1.service
install -Dpm0644 data/dbus/org.ersa.Foundation1.conf %{buildroot}/usr/share/dbus-1/system.d/org.ersa.Foundation1.conf
install -Dpm0644 data/polkit/org.ersa.foundation.policy %{buildroot}/usr/share/polkit-1/actions/org.ersa.foundation.policy
install -Dpm0644 data/systemd/foundationd.service %{buildroot}/usr/lib/systemd/system/foundationd.service
install -Dpm0644 data/systemd-user/foundation-provisioning.service %{buildroot}/usr/lib/systemd/user/foundation-provisioning.service
install -Dpm0644 data/systemd-user/foundation-provisioning.path %{buildroot}/usr/lib/systemd/user/foundation-provisioning.path
install -Dpm0644 data/config/schema.d/10-foundation.json %{buildroot}/usr/lib/foundation/schema.d/10-foundation.json
install -d %{buildroot}/usr/lib/foundation/defaults.d
install -Dpm0644 data/repos.d/opensuse-oss.repo %{buildroot}/usr/lib/foundation/repos.d/opensuse-oss.repo
install -Dpm0644 data/repos.d/packman-essentials.repo %{buildroot}/usr/lib/foundation/repos.d/packman-essentials.repo
install -Dpm0644 data/keys/opensuse.asc %{buildroot}/usr/share/foundation/keys/opensuse.asc
install -Dpm0644 data/keys/packman.asc %{buildroot}/usr/share/foundation/keys/packman.asc
# the keys system image updates are verified with (scripts/make-image-signing-key in ecp-mkosi makes one; with none here,
# updates can only be installed with --unsigned)
for key in data/keys/ersa-image-*.asc; do [ -e "$key" ] || continue; install -Dpm0644 "$key" %{buildroot}/usr/share/foundation/keys/$(basename "$key"); done
install -Dpm0644 data/catalog.d/codecs.json %{buildroot}/usr/lib/foundation/catalog.d/codecs.json
install -Dpm0644 data/post-merge.d/10-gsettings.json %{buildroot}/usr/lib/foundation/post-merge.d/10-gsettings.json
install -Dpm0644 README.md %{buildroot}/usr/share/doc/foundation/README.md

%files
%dir /usr/lib/foundation
%{_bindir}/foundation
/usr/lib/foundation/foundation/
%doc /usr/share/doc/foundation/README.md

%files -n foundation-updater
%{_bindir}/ersa-updater
/usr/lib/foundation/foundation_updater/
/usr/share/applications/org.ersa.Updater.desktop
/usr/share/icons/hicolor/scalable/apps/org.ersa.Updater.svg

%files -n foundation-installer
%{_bindir}/ersa-installer
/usr/lib/foundation/foundation_installer/
/usr/share/applications/org.ersa.Installer.desktop
/usr/libexec/ecp/live-session
/usr/share/icons/hicolor/scalable/apps/org.ersa.Installer.svg
/usr/lib/systemd/system/ersa-live-session.service

%files -n foundationd
%dir /usr/lib/foundation
/usr/lib/foundation/foundationd/
/usr/lib/foundation/schema.d/
/usr/lib/foundation/defaults.d/
/usr/lib/foundation/repos.d/
/usr/lib/foundation/catalog.d/
/usr/lib/foundation/post-merge.d/
/usr/share/foundation/keys/
/usr/libexec/foundationd
/usr/libexec/foundationd-worker
/usr/share/dbus-1/interfaces/org.ersa.Foundation1.xml
/usr/share/dbus-1/system-services/org.ersa.Foundation1.service
/usr/share/dbus-1/system.d/org.ersa.Foundation1.conf
/usr/share/polkit-1/actions/org.ersa.foundation.policy
/usr/lib/systemd/system/foundationd.service
/usr/lib/systemd/user/foundation-provisioning.service
/usr/lib/systemd/user/foundation-provisioning.path
/usr/lib/systemd/system/foundation-bundles-select.service
/usr/lib/systemd/system/foundation-bundles-refresh.service
/usr/libexec/foundation-bundles
/usr/libexec/foundation-update-notify
/usr/lib/systemd/user/foundation-update-notify.service
/usr/lib/systemd/user/foundation-update-notify.path
/usr/libexec/foundation-splash-sync
/usr/lib/systemd/user/foundation-splash-sync.service

%changelog
* Fri Nov 13 2026 Ersa Compute Platform <ecp@ersa.local> - 0.6.0-2
- Add the foundation-updater subpackage: a window with Check for Updates / Update (reads the feed at ota.url) and
  Install from a File in its menu; asks polkit through foundationd before installing
- Slots are named a and b; the version they hold is a separate field (GetSlots version, GetBootState running_version)
- A waiting update is cleared once its version runs, so the notification stops
- Updates.Restart: restart into an installed update under the same authorization as the install; the updates action is now kept by polkit
- foundation_installer's D-Bus backend moved to foundation.gbackend (shared with the updater)
* Fri Nov 13 2026 Ersa Compute Platform <ecp@ersa.local> - 0.6.0-1
- Slots are dm-verity pairs (root and hash partition) with fixed labels, named by the root hash; one update archive format
  carrying the hash tree; kernel images are installed unchanged (signed for Secure Boot); `slot copy` removed
- `foundation deploy` installs the installer medium's payload (the normal image's update archive)
- Update signatures: refuse expired and revoked keys; image signing key script
- Add `foundation remote` (SSH), scriptlet handling and post-merge jobs for compat packages, splash theme as a UEFI variable
* Sat Nov 07 2026 Ersa Compute Platform <ecp@ersa.local> - 0.5.0-2
- Add `foundation splash light|dark` (Boot.SetSplash) and foundation-splash-sync.service, which makes the boot splash follow the desktop style
* Thu Nov 05 2026 Ersa Compute Platform <ecp@ersa.local> - 0.5.0-1
- Add `foundation deploy` and the Deploy interface: install the running system to a disk
- Add the foundation-installer subpackage: a step-by-step graphical installer (GTK 4, libadwaita)
* Thu Nov 05 2026 Ersa Compute Platform <ecp@ersa.local> - 0.4.0-1
- foundation is now a client of foundationd (D-Bus): status, slot, reboot, apps, compat, ext, config, job
- foundationd: jobs and worker processes, boot slots (state, selection, copy, release), Flatpak
  applications through libflatpak, compat RPMs as system extensions, sysext/confext management
- Remove `foundation pkg` (replaced by `foundation apps` and `foundation base`)

* Thu Nov 05 2026 Ersa Compute Platform <ecp@ersa.local> - 0.3.0-1
- Add the foundationd subpackage: D-Bus contract, Manager and Config interfaces, polkit action

* Wed Nov 04 2026 Ersa Compute Platform <ecp@ersa.local> - 0.2.0-1
- Rewrite in Python: styled status with boot-slot and boot-assessment state, --json output
- Add `foundation pkg` for system-wide Flatpak applications and a read-only base package view
