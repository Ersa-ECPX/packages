# Pinned source: the build script exports exactly this commit with `git archive`.
%global commit      0605858a8c1252d73a1904b043cbd6af96ad890e
%global shortcommit %(c=%{commit}; echo ${c:0:7})

Name:           ersa-dialer
Version:        0.1.0
Release:        1.git%{shortcommit}%{?dist}
Summary:        Phone dialer for GNOME, a client of ersa-bluetooth

License:        GPL-3.0-or-later
URL:            https://github.com/Ersa-ECPX/Dialer
Source0:        %{url}/archive/%{commit}/dialer-%{commit}.tar.gz

BuildRequires:  meson >= 1.0.0
BuildRequires:  gcc-c++
BuildRequires:  pkgconfig(libadwaita-1) >= 1.4
BuildRequires:  pkgconfig(gio-2.0)
BuildRequires:  pkgconfig(gio-unix-2.0)
BuildRequires:  pkgconfig(json-glib-1.0)
BuildRequires:  pkgconfig(sqlite3)
# Used by the meson tests that validate the desktop and AppStream files.
BuildRequires:  desktop-file-utils
%if 0%{?suse_version}
BuildRequires:  AppStream
%else
BuildRequires:  appstream
%endif

# All telephony, phonebook and device management goes through this service.
Requires:       ersa-bluetooth
Requires:       hicolor-icon-theme

%description
A phone dialer for GNOME built with GTK 4 and libadwaita. It owns no Bluetooth, HFP or
PBAP code: it talks to ersa-bluetoothd over D-Bus (org.openersa.Bluetooth) for calls,
contacts and call history, and handles incoming calls with native notifications.

%prep
%autosetup -n dialer-%{commit}

%build
%meson
%meson_build

%install
%meson_install

%check
# Skip the `database` test: it asserts that default contacts are seeded, but upstream commit
# e952e6d ("remove default contacts") removed the seeding without updating the test.
# Remove this exclusion once tests/test-database.cpp is fixed upstream.
%meson_test json-parsing 'Validate desktop file' 'Validate appstream file'

%files
%license COPYING
%doc README.md
%{_bindir}/dialer
%{_datadir}/applications/dev.ersa.Dialer.desktop
%{_datadir}/metainfo/dev.ersa.Dialer.metainfo.xml
%{_datadir}/icons/hicolor/scalable/apps/dev.ersa.Dialer.svg
%{_datadir}/icons/hicolor/symbolic/apps/dev.ersa.Dialer-symbolic.svg

%changelog
* Wed Nov 04 2026 Ersa Compute Platform <ecp@ersa.local> - 0.1.0-1.git0605858
- Initial RPM of the Ersa dialer at commit 0605858
