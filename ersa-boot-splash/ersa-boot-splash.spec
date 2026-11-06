Name:           ersa-boot-splash
Version:        0.1.0
Release:        3
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

%description
The Ersa Plymouth theme, including its logo and progress bar assets.

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

%files
%dir %{_datadir}/plymouth/themes/ersa
%{_datadir}/plymouth/themes/ersa/ersa.plymouth
%{_datadir}/plymouth/themes/ersa/ersa.script
%{_datadir}/plymouth/themes/ersa/ersa-logo.png
%{_datadir}/plymouth/themes/ersa/ersa-logo.svg
%{_datadir}/plymouth/themes/ersa/fill.png
%{_datadir}/plymouth/themes/ersa/track.png
%{_datadir}/plymouth/themes/ersa/ersa-logo@2x.png

%changelog
* Wed Nov 04 2026 Ersa Compute Platform <ecp@ersa.local> - 0.1.0-3
- Render the logo PNGs from the branding SVG, add a 2x logo and HiDPI layout

* Wed Nov 04 2026 Ersa Compute Platform <ecp@ersa.local> - 0.1.0-2
- Show plymouth status messages below the progress bar

* Tue Nov 03 2026 Ersa Compute Platform <ecp@ersa.local> - 0.1.0-1
- Package the Ersa Plymouth theme assets
