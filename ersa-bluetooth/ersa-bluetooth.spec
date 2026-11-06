# Pinned source: the build script exports exactly this commit with `git archive`.
%global commit      51858bc03a3625d6d5713eacfe9fa9a58c5df951
%global shortcommit %(c=%{commit}; echo ${c:0:7})

# Run the regression tests (needs dbus-run-session): rpmbuild --with check
%bcond_with check

Name:           ersa-bluetooth
Version:        0.1.0
Release:        1.git%{shortcommit}%{?dist}
Summary:        BlueZ D-Bus bridge with AVRCP, HFP, PBAP and Apple ANCS notifications

# The upstream PKGBUILD declares license=('unknown') and the repository has no LICENSE file.
# Confirm and set the real license before publishing this package.
License:        LicenseRef-Unknown
URL:            https://github.com/Ersa-ECPX/ersa-bluetooth
Source0:        %{url}/archive/%{commit}/%{name}-%{commit}.tar.gz

BuildRequires:  cmake >= 3.20
%if 0%{?suse_version}
BuildRequires:  ninja
%else
BuildRequires:  ninja-build
%endif
BuildRequires:  gcc-c++
# sdbus-cpp: openSUSE Tumbleweed has sdbus-cpp-devel; on EL10 it comes from EPEL.
BuildRequires:  pkgconfig(sdbus-c++)
BuildRequires:  systemd-rpm-macros
%if %{with check}
%if 0%{?suse_version}
BuildRequires:  dbus-1-daemon
%else
BuildRequires:  dbus-daemon
%endif
%endif

Requires:       bluez
Recommends:     wireplumber
Recommends:     bluez-obexd

%description
ersa-bluetoothd is a D-Bus bridge that unifies BlueZ device management, AVRCP media
control (republished as MPRIS2 players), HFP call control through WirePlumber's native
backend, PBAP phonebook and call history, and Apple ANCS notifications behind one
MAC-address-addressed API, org.openersa.Bluetooth. It runs as a user service on the
desktop session bus. ersa-bluetoothctl is the reference command-line client.

%prep
%autosetup -n %{name}-%{commit}

%build
%cmake \
%if !0%{?suse_version}
    -G Ninja \
%endif
    -DCMAKE_BUILD_TYPE=Release \
    -DSYSTEMD_UNIT_DIR=lib/systemd/user \
%if %{with check}
    -DBUILD_TESTING=ON
%else
    -DBUILD_TESTING=OFF
%endif
%cmake_build

%install
%cmake_install
# Optional WirePlumber override; upstream installs it unactivated.
install -Dpm0644 config/wireplumber/99-ersa-bluetooth.conf \
    %{buildroot}%{_datadir}/%{name}/99-ersa-bluetooth.conf

%check
%if %{with check}
%ctest
%endif

%post
%systemd_user_post ersa-bluetooth.service

%preun
%systemd_user_preun ersa-bluetooth.service

%postun
%systemd_user_postun_with_restart ersa-bluetooth.service

%files
%doc README.md docs/DBUS_API.md
%{_bindir}/ersa-bluetoothd
%{_bindir}/ersa-bluetoothctl
%{_userunitdir}/ersa-bluetooth.service
%{_datadir}/%{name}/

%changelog
* Wed Nov 04 2026 Ersa Compute Platform <ecp@ersa.local> - 0.1.0-1.git51858bc
- Initial RPM of ersa-bluetooth at commit 51858bc
