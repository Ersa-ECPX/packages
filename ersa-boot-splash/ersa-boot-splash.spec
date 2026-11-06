Name:           ersa-boot-splash
Version:        0.1.0
Release:        4
Summary:        Ersa Plymouth boot theme
License:        LicenseRef-Unknown
BuildArch:      noarch
Requires:       plymouth-plugin-script
Requires:       plymouth-plugin-label

Source0:        ersa.plymouth
Source1:        ersa.script
Source2:        ersa-logo.png
Source3:        ersa-logo.svg
Source4:        fill.png
Source5:        track.png
Source6:        ersa-logo@2x.png
Source7:        ersa-dark.plymouth
Source8:        ersa-dark.script
Source9:        ersa-dark-logo.png
Source10:       ersa-dark-logo@2x.png
Source11:       fill-dark.png
Source12:       track-dark.png

%description
The Ersa Plymouth themes, including their logo and progress bar assets: ersa (light, the default)
and ersa-dark (selected with plymouth.splash=ersa-dark on the kernel command line).

%prep

%build

%install
install -Dpm0644 %{SOURCE0} %{buildroot}%{_datadir}/plymouth/themes/ersa/ersa.plymouth
install -Dpm0644 %{SOURCE1} %{buildroot}%{_datadir}/plymouth/themes/ersa/ersa.script
install -Dpm0644 %{SOURCE2} %{buildroot}%{_datadir}/plymouth/themes/ersa/ersa-logo.png
install -Dpm0644 %{SOURCE3} %{buildroot}%{_datadir}/plymouth/themes/ersa/ersa-logo.svg
install -Dpm0644 %{SOURCE4} %{buildroot}%{_datadir}/plymouth/themes/ersa/fill.png
install -Dpm0644 %{SOURCE5} %{buildroot}%{_datadir}/plymouth/themes/ersa/track.png
install -Dpm0644 %{SOURCE6} %{buildroot}%{_datadir}/plymouth/themes/ersa/ersa-logo@2x.png
install -Dpm0644 %{SOURCE7} %{buildroot}%{_datadir}/plymouth/themes/ersa-dark/ersa-dark.plymouth
install -Dpm0644 %{SOURCE8} %{buildroot}%{_datadir}/plymouth/themes/ersa-dark/ersa-dark.script
install -Dpm0644 %{SOURCE9} %{buildroot}%{_datadir}/plymouth/themes/ersa-dark/ersa-dark-logo.png
install -Dpm0644 %{SOURCE10} %{buildroot}%{_datadir}/plymouth/themes/ersa-dark/ersa-dark-logo@2x.png
install -Dpm0644 %{SOURCE11} %{buildroot}%{_datadir}/plymouth/themes/ersa-dark/fill-dark.png
install -Dpm0644 %{SOURCE12} %{buildroot}%{_datadir}/plymouth/themes/ersa-dark/track-dark.png

%files
%dir %{_datadir}/plymouth/themes/ersa
%{_datadir}/plymouth/themes/ersa/ersa.plymouth
%{_datadir}/plymouth/themes/ersa/ersa.script
%{_datadir}/plymouth/themes/ersa/ersa-logo.png
%{_datadir}/plymouth/themes/ersa/ersa-logo.svg
%{_datadir}/plymouth/themes/ersa/fill.png
%{_datadir}/plymouth/themes/ersa/track.png
%{_datadir}/plymouth/themes/ersa/ersa-logo@2x.png
%dir %{_datadir}/plymouth/themes/ersa-dark
%{_datadir}/plymouth/themes/ersa-dark/ersa-dark.plymouth
%{_datadir}/plymouth/themes/ersa-dark/ersa-dark.script
%{_datadir}/plymouth/themes/ersa-dark/ersa-dark-logo.png
%{_datadir}/plymouth/themes/ersa-dark/ersa-dark-logo@2x.png
%{_datadir}/plymouth/themes/ersa-dark/fill-dark.png
%{_datadir}/plymouth/themes/ersa-dark/track-dark.png

%changelog
* Sat Nov 07 2026 Ersa Compute Platform <ecp@ersa.local> - 0.1.0-4
- Add the ersa-dark theme (dark background, light logo), selected with plymouth.splash=ersa-dark

* Wed Nov 04 2026 Ersa Compute Platform <ecp@ersa.local> - 0.1.0-3
- Render the logo PNGs from the branding SVG, add a 2x logo and HiDPI layout

* Wed Nov 04 2026 Ersa Compute Platform <ecp@ersa.local> - 0.1.0-2
- Show plymouth status messages below the progress bar

* Tue Nov 03 2026 Ersa Compute Platform <ecp@ersa.local> - 0.1.0-1
- Package the Ersa Plymouth theme assets
