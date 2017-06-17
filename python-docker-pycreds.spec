# Created by pyp2rpm-1.1.2 and rewrote manually afterwards
%global pypi_name docker-pycreds
%if 0%{?fedora}
%bcond_without python3
%else
%bcond_with python3
%endif
# the test suite is diabled b/c it needs docker-credential-secretservice binary
# and we don't have that now (Sep 2016) in Fedora
%bcond_with tests

Name:           python-%{pypi_name}
Version:        0.2.1
Release:        4%{?dist}
Summary:        Python bindings for the docker credentials store API

License:        ASL 2.0
URL:            https://github.com/shin-/dockerpy-creds/
Source0:        https://files.pythonhosted.org/packages/source/d/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  python2-devel
BuildRequires:  python-setuptools
BuildRequires:  python2-six

%if %{with tests}
BuildRequires:  pytest
%endif # tests

%if %{with python3}
BuildRequires:  python3-devel
BuildRequires:  python3-six
%if %{with tests}
BuildRequires:  python3-pytest
%endif # tests
%endif # python3


%description
Python bindings for the docker credentials store API


%package -n python2-%{pypi_name}
Summary:        Python bindings for the docker credentials store API
%{?python_provide:%python_provide python2-%{pypi_name}}

Requires:  python2-six

%description -n python2-%{pypi_name}
Python bindings for the docker credentials store API


%if %{with python3}
%package -n python3-%{pypi_name}
Summary:        Python bindings for the docker credentials store API
%{?python_provide:%python_provide python3-%{pypi_name}}

Requires:  python3-six

%description -n python3-%{pypi_name}
Python bindings for the docker credentials store API

%endif # python3


%prep
%autosetup -n %{pypi_name}-%{version}


%build
%py2_build
%if %{with python3}
%py3_build
%endif # python3


%install
# Must do the subpackages' install first because the scripts in /usr/bin are
# overwritten with every setup.py install (and we want the python2 version
# to be the default for now).
%py2_install
%if %{with python3}
%py3_install
%endif # python3


# we are not using setup.py test here b/c the project pins to specific versions
%check
# sanity test
%{__python2} -c "import dockerpycreds"
%if %{with tests}
PYTHONPATH="${PWD}" py.test-%{python2_version} -vv tests/
%endif # tests

%if %{with python3}
%{__python3} -c "import dockerpycreds"
%if %{with tests}
PYTHONPATH="${PWD}" py.test-%{python3_version} -vv tests/
%endif # tests
%endif # python3


%files -n python2-%{pypi_name}
%doc README.md
%license LICENSE
%{python2_sitelib}/dockerpycreds
%{python2_sitelib}/docker_pycreds-%{version}-py?.?.egg-info

%if %{with python3}
%files -n python3-%{pypi_name}
%doc README.md
%license LICENSE
%{python3_sitelib}/dockerpycreds
%{python3_sitelib}/docker_pycreds-%{version}-py?.?.egg-info
%endif # python3


%changelog
* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 0.2.1-3
- Rebuild for Python 3.6

* Wed Oct 05 2016 Tomas Tomecek <ttomecek@redhat.com> - 0.2.1-2
- rebuilt

* Mon Sep 26 2016 Tomas Tomecek <ttomecek@redhat.com> - 0.2.1-1
- Initial package.
