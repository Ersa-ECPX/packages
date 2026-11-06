Name:           foundation
Version:        0.5.0
Release:        1%{?dist}
Summary:        Ersa Compute Platform management command line
License:        LicenseRef-Unknown
BuildArch:      noarch
Source0:        %{name}-%{version}.tar.gz

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
# Compat packages are inspected and unpacked with the rpm tools; boot slots are relabelled with
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
install -Dpm0644 data/systemd/foundation-bundles-select.service %{buildroot}/usr/lib/systemd/system/foundation-bundles-select.service
install -Dpm0644 data/systemd/foundation-bundles-refresh.service %{buildroot}/usr/lib/systemd/system/foundation-bundles-refresh.service
install -Dpm0644 data/systemd-user/foundation-update-notify.service %{buildroot}/usr/lib/systemd/user/foundation-update-notify.service
install -Dpm0644 data/systemd-user/foundation-update-notify.path %{buildroot}/usr/lib/systemd/user/foundation-update-notify.path
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
install -Dpm0644 data/catalog.d/codecs.json %{buildroot}/usr/lib/foundation/catalog.d/codecs.json
install -Dpm0644 README.md %{buildroot}/usr/share/doc/foundation/README.md

%files
%dir /usr/lib/foundation
%{_bindir}/foundation
/usr/lib/foundation/foundation/
%doc /usr/share/doc/foundation/README.md

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

%changelog
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
