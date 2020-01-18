%if 0%{?el6}%{?el7}
    # python3 and python version related macros
    # required to build python3- subpackage
    # are not available in el6 and el7
    %bcond_with python3
    %{!?__python2: %global __python2 %{__python}}
    %{!?python2_sitelib: %global python2_sitelib %{python_sitelib}}
    %{!?py2_build: %global py2_build %{__python2} setup.py build --executable="%{__python2} -s" %{?*}}
    %{!?py2_install: %global py2_install %{__python2} setup.py install --skip-build --root %{buildroot} %{?*}}
%else
    %bcond_without python3
%endif

%global distname requests-oauthlib
%global modname requests_oauthlib

Name:               python-requests-oauthlib
Version:            0.8.0
Release:            5%{?dist}
Summary:            OAuthlib authentication support for Requests.

Group:              Development/Libraries
License:            ISC
URL:                http://pypi.python.org/pypi/requests-oauthlib
Source0:            https://github.com/requests/requests-oauthlib/archive/v%{version}.tar.gz

BuildArch:          noarch

%description
This project provides first-class OAuth library support for python-request.

%package -n python2-%{distname}
%if 0%{?python_provide:1}
%python_provide python2-%{distname}
%else
Provides: python-%{distname} = %{?epoch:%{epoch}:}%{version}-%{release}
%endif

Summary:            OAuthlib authentication support for Requests.
Group:              Development/Libraries

BuildRequires:      python2-devel
BuildRequires:      python2-setuptools

BuildRequires:      python2-oauthlib >= 0.6.2
BuildRequires:      python-requests >= 2.0.0

BuildRequires:      python-mock

Requires:           python2-oauthlib
Requires:           python-requests >= 2.0.0

%description -n python2-%{distname}
This project provides first-class OAuth library support for python-request.

%if 0%{?with_python3}
%package -n python3-%{distname}
%{?python_provide:%python_provide python3-%{distname}}
Summary:            OAuthlib authentication support for Requests.
Group:              Development/Libraries

BuildRequires:      python3-devel
BuildRequires:      python3-setuptools

BuildRequires:      python3-oauthlib >= 0.6.2
BuildRequires:      python3-requests >= 2.0.0

BuildRequires:      python3-mock

Requires:           python3-oauthlib
Requires:           python3-requests

%description -n python3-%{distname}
This project provides first-class OAuth library support for python-request.
%endif

%prep
%autosetup -n %{distname}-%{version}

# Remove bundled egg-info in case it exists
rm -rf %{distname}.egg-info


%build
%py2_build
%if 0%{?with_python3}
%py3_build
%endif

%install
%py2_install
%if 0%{?with_python3}
%py3_install
%endif

# Upstream doesn't actually ship the tests with the tarball.
# https://github.com/requests/requests-oauthlib/pull/91
#%%check
#%%{__python2} setup.py test

%files -n python2-%{distname}
%doc README.rst HISTORY.rst requirements.txt AUTHORS.rst
%license LICENSE
%{python2_sitelib}/%{modname}/
%{python2_sitelib}/%{modname}-%{version}*

%if 0%{?with_python3}
%files -n python3-%{distname}
%doc README.rst HISTORY.rst requirements.txt AUTHORS.rst
%license LICENSE
%{python3_sitelib}/%{modname}/
%{python3_sitelib}/%{modname}-%{version}*
%endif

%changelog
* Tue Apr 11 2017 John Dennis <jdennis@redhat.com> - 0.8.0-5
- BuildRequires had python-requests but the Requires was still referencing
  python2-requests which is not yet provided in RHEL 7.4.,
  also add the missing version dependency on python-requests.
  Resolves: rhbz#1401783

* Fri Apr  7 2017 John Dennis <jdennis@redhat.com> - 0.8.0-4
- fix with_python3 conditional test
  Resolves: rhbz#1401783

* Thu Apr  6 2017 John Dennis <jdennis@redhat.com> - 0.8.0-3
- fix python provides
  fix with_python3
  Resolves: rhbz#1401783

* Tue Apr  4 2017 John Dennis <jdennis@redhat.com> - 0.8.0-2
- Add Provides for unversioned python
  Resolves: rhbz#1401783

* Fri Mar 17 2017 John Dennis <jdennis@redhat.com> - 0.8.0-1
- Initial import for RHEL-7
  Resolves: rhbz#1401783

