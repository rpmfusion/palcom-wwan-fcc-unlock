%bcond build 0

%if %{without build}
%global __strip /bin/true
%endif
%global debug_package %{nil}

Name:		palcom-wwan-fcc-unlock
Version:	3.1.1
Release:	1%{?dist}
Summary:	FCC unlocking service for Palcom modems

License:	BSD-3-Clause
URL:		https://github.com/palcomwireless/linux_pkgs
Source0:	%{url}/archive/%{version}/%{name}-%{version}.tar.gz
ExclusiveArch:	x86_64

%if %{with build}
BuildRequires: cmake gcc g++ glib2-devel
BuildRequires: openssl-libs libmbim-devel
%endif
BuildRequires: chrpath
Requires: ModemManager dmidecode usbutils openssl
Requires: policycoreutils

%description
FCC unlocking service for Palcom modems to be used by ModemManager.
For the detail capable WWAN modules, please refer the GitHub project.


%prep
%setup -q -n linux_pkgs-%{version}


%if %{with build}
%build
%cmake -DCMAKE_POSITION_INDEPENDENT_CODE=ON \
	--no-warn-unused-cli
%cmake_build
%endif


%install
sh deb_extra/install >/dev/null 2>&1
mkdir -p %{buildroot}%{_sbindir}
cp build/release/dpkg/opt/pwl/pwl-unlock/pwl_unlock %{buildroot}%{_sbindir}
chrpath --delete %{buildroot}%{_sbindir}/*
chmod a+x %{buildroot}%{_sbindir}/*
mkdir -p %{buildroot}%{_libdir}/ModemManager/fcc-unlock.d
cp build/release/dpkg/opt/pwl/pwl-unlock/fcc-unlock.d/* %{buildroot}%{_libdir}/ModemManager/fcc-unlock.d
sed -i 's@/opt/pwl/pwl-unlock/pwl_unlock@pwl_unlock@g' %{buildroot}%{_libdir}/ModemManager/fcc-unlock.d/*
chmod a+x %{buildroot}%{_libdir}/ModemManager/fcc-unlock.d/*
mkdir -p %{buildroot}%{_datadir}/selinux/packages
cp deb_extra/modemmanager_fccunlock.cil %{buildroot}%{_datadir}/selinux/packages


%post
%selinux_modules_install %{_datadir}/selinux/packages/modemmanager_fccunlock.cil


%postun
if [ $1 -eq 0 ]; then
	%selinux_modules_uninstall modemmanager_fccunlock
fi


%files
%{_sbindir}/pwl_unlock
%dir %{_libdir}/ModemManager/fcc-unlock.d
%{_libdir}/ModemManager/fcc-unlock.d/413c:8217
%{_libdir}/ModemManager/fcc-unlock.d/413c:8218
%{_libdir}/ModemManager/fcc-unlock.d/413c:8219
%{_datadir}/selinux/packages/modemmanager_fccunlock.cil


%changelog
* Fri Jun 14 2024 Jose Ignacio Tornos Martinez <jtornosm@redhat.com> - 3.1.1-1
- Initial version of the package
