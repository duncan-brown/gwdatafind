%define name    gwdatafind
%define version 1.0.0
%define release 1

Name:      %{name}
Version:   %{version}
Release:   %{release}%{?dist}
Summary:   The client library for the LIGO Data Replicator (LDR) service

License:   GPLv3
Url:       https://pypi.org/project/%{name}/
Source0:   https://pypi.io/packages/source/g/%{name}/%{name}-%{version}.tar.gz

Vendor:    Duncan Macleod <duncan.macleod@ligo.org>

BuildArch: noarch
BuildRequires: rpm-build
BuildRequires: python-rpm-macros
BuildRequires: python-setuptools
BuildRequires: python2-six
BuildRequires: pyOpenSSL
BuildRequires: lal-python
BuildRequires: python2-ligo-segments
BuildRequires: python2-pytest
BuildRequires: python2-mock

%description
The DataFind service allows users to query for the location of
Gravitational-Wave Frame (GWF) files containing data from the current
gravitational-wave detectors.

# -- python2-gwdatafind

%package -n python2-%{name}
Summary:  %{summary}
Requires: python-six
Requires: pyOpenSSL
Requires: lal-python
Requires: python2-ligo-segments
%{?python_provide:%python_provide python2-%{name}}
%description -n python2-%{name}
The DataFind service allows users to query for the location of
Gravitational-Wave Frame (GWF) files containing data from the current
gravitational-wave detectors.

# -- build steps

%prep
%autosetup -n %{name}-%{version}

%build
%py2_build

%check
%{__python2} -m pytest --pyargs %{name}

%install
%py2_install

%clean
rm -rf $RPM_BUILD_ROOT

%files -n python2-%{name}
%license LICENSE
%doc README.md
%{_bindir}/gw_data_find
%{python2_sitelib}/*

# -- changelog

%changelog
* Mon Jul 26 2018 Duncan Macleod <duncan.macleod@ligo.org>
- 1.0.0 first build
