%define name    gwdatafind
%define version 1.0.3
%define release 1

Name:      %{name}
Version:   %{version}
Release:   %{release}%{?dist}
Summary:   The client library for the LIGO Data Replicator (LDR) service

Group:     Development/Libraries
License:   GPLv3
Url:       https://gwdatafind.readthedocs.io/
Source0:   https://pypi.io/packages/source/g/%{name}/%{name}-%{version}.tar.gz
Packager:  Duncan Macleod <duncan.macleod@ligo.org>

BuildArch: noarch

# build dependencies
BuildRequires: rpm-build
BuildRequires: python-rpm-macros
BuildRequires: python2-rpm-macros
BuildRequires: python3-rpm-macros
BuildRequires: python2-setuptools
BuildRequires: python%{python3_version_nodots}-setuptools

# testing dependencies (python3x only)
BuildRequires: python%{python3_version_nodots}-six
BuildRequires: python%{python3_version_nodots}-pyOpenSSL
BuildRequires: python%{python3_version_nodots}-ligo-segments
BuildRequires: python%{python3_version_nodots}-pytest >= 2.8.0

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
%{?python_provide:%python_provide python2-%{name}}
%description -n python2-%{name}
The DataFind service allows users to query for the location of
Gravitational-Wave Frame (GWF) files containing data from the current
gravitational-wave detectors. This package provides the
Python %{python2_version} interface libraries.

# -- python3x-gwdatafind

%package -n python%{python3_version_nodots}-%{name}
Summary:  Python %{python3_version} library for the LIGO Data Replicator (LDR) service
Requires: python%{python3_version_nodots}-six
Requires: python%{python3_version_nodots}-pyOpenSSL
Requires: python%{python3_version_nodots}-ligo-segments
%{?python_provide:%python_provide python%{python3_version_nodots}-%{name}}
%description -n python%{python3_version_nodots}-%{name}
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
%py2_install
%py3_install

%clean
rm -rf $RPM_BUILD_ROOT

%files -n python2-%{name}
%license LICENSE
%doc README.md
%{python2_sitelib}/*

%files -n python%{python3_version_nodots}-%{name}
%license LICENSE
%doc README.md
%{python3_sitelib}/*

# -- changelog

%changelog
* Fri Jan 04 2019 Duncan Macleod <duncan.macleod@ligo.org> 1.0.3-1
- added python3 packages

* Tue Aug 14 2018 Duncan Macleod <duncan.macleod@ligo.org> 1.0.2-1
- bug-fix release

* Tue Aug 14 2018 Duncan Macleod <duncan.macleod@ligo.org> 1.0.1-1
- bug-fix release

* Mon Jul 30 2018 Duncan Macleod <duncan.macleod@ligo.org> 1.0.0-1
- first build
