%define name    gwdatafind
%define version 1.0.4
%define release 2

Name:      %{name}
Version:   %{version}
Release:   %{release}%{?dist}
Summary:   The client library for the LIGO Data Replicator (LDR) service

Group:     Development/Libraries
License:   GPL-3.0-or-later
Url:       https://gwdatafind.readthedocs.io/
Source0:   https://pypi.io/packages/source/g/%{name}/%{name}-%{version}.tar.gz
Packager:  Duncan Macleod <duncan.macleod@ligo.org>

BuildArch: noarch

# build dependencies
BuildRequires: rpm-build
BuildRequires: python-rpm-macros
BuildRequires: python-srpm-macros
BuildRequires: python2-rpm-macros
BuildRequires: python3-rpm-macros
BuildRequires: epel-rpm-macros
BuildRequires: python2-setuptools
BuildRequires: python%{python3_pkgversion}-setuptools
BuildRequires: help2man

# testing dependencies (python3x only)
BuildRequires: python%{python3_pkgversion}-six
BuildRequires: python%{python3_pkgversion}-pyOpenSSL
BuildRequires: python%{python3_pkgversion}-ligo-segments
BuildRequires: python%{python3_pkgversion}-pytest >= 2.8.0

%description
The DataFind service allows users to query for the location of
Gravitational-Wave Frame (GWF) files containing data from the current
gravitational-wave detectors. This package provides the python interface
libraries.

# -- python2-gwdatafind

%package -n python2-%{name}
Summary:  Python %{python2_version} library for the LIGO Data Replicator (LDR) service
Requires: python-six
Requires: pyOpenSSL
Requires: python2-ligo-segments
Conflicts: glue < 1.61.0
%{?python_provide:%python_provide python2-%{name}}
%description -n python2-%{name}
The DataFind service allows users to query for the location of
Gravitational-Wave Frame (GWF) files containing data from the current
gravitational-wave detectors. This package provides the
Python %{python2_version} interface libraries.

# -- python3x-gwdatafind

%package -n python%{python3_pkgversion}-%{name}
Summary:  Python %{python3_version} library for the LIGO Data Replicator (LDR) service
Requires: python%{python3_pkgversion}-six
Requires: python%{python3_pkgversion}-pyOpenSSL
Requires: python%{python3_pkgversion}-ligo-segments
%{?python_provide:%python_provide python%{python3_pkgversion}-%{name}}
%description -n python%{python3_pkgversion}-%{name}
The DataFind service allows users to query for the location of
Gravitational-Wave Frame (GWF) files containing data from the current
gravitational-wave detectors. This package provides the
Python %{python3_version} interface libraries.

# -- build steps

%prep
%autosetup -n %{name}-%{version}

%build
%py2_build
%py3_build

%check
%{__python3} -m pytest --pyargs %{name}

%install
%py3_install
# install py2 last so that /usr/bin/gw_data_find comes from that
%py2_install
# make man page for gw_data_find
mkdir -vp %{buildroot}%{_mandir}/man1
env PYTHONPATH="%{buildroot}%{python2_sitelib}" \
help2man \
    --source %{name} \
    --version-string %{version} \
    --section 1 --no-info --no-discard-stderr \
    --output %{buildroot}%{_mandir}/man1/gw_data_find.1 \
    %{buildroot}%{_bindir}/gw_data_find

%clean
rm -rf $RPM_BUILD_ROOT

%files -n python2-%{name}
%license LICENSE
%doc README.md
%{_bindir}/gw_data_find
%{python2_sitelib}/*
%{_mandir}/man1/gw_data_find.1*

%files -n python%{python3_pkgversion}-%{name}
%license LICENSE
%doc README.md
%{python3_sitelib}/*

# -- changelog

%changelog
* Fri Jul 12 2019 Duncan Macleod <duncan.macleod@ligo.org> 1.0.4-2
- fixed incorrect installation of /usr/bin/gw_data_find
- use python-srpm-macros to provide python3 versions

* Fri Jan 11 2019 Duncan Macleod <duncan.macleod@ligo.org> 1.0.4-1
- include command-line client, requires matching glue release

* Fri Jan 04 2019 Duncan Macleod <duncan.macleod@ligo.org> 1.0.3-1
- added python3 packages

* Tue Aug 14 2018 Duncan Macleod <duncan.macleod@ligo.org> 1.0.2-1
- bug-fix release

* Tue Aug 14 2018 Duncan Macleod <duncan.macleod@ligo.org> 1.0.1-1
- bug-fix release

* Mon Jul 30 2018 Duncan Macleod <duncan.macleod@ligo.org> 1.0.0-1
- first build
