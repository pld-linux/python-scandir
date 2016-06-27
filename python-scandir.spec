#
# Conditional build:
%bcond_without	doc	# don't build doc
%bcond_without	tests	# do not perform "make test"
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

%define 	module		scandir
%define 	egg_name	scandir
Summary:	A better directory iterator and faster os.walk() for Python
Name:		python-%{module}
Version:	1.2
Release:	1
License:	BSD
Group:		Libraries/Python
Source0:	https://github.com/benhoyt/scandir/archive/v%{version}/%{module}-%{version}.tar.gz
# Source0-md5:	aaf700930492f9595eb15bbb0b0c9695
URL:		https://github.com/benhoyt/scandir
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with python2}
BuildRequires:	python-modules
BuildRequires:	python-setuptools
%endif
%if %{with python3}
BuildRequires:	python3-modules
BuildRequires:	python3-setuptools
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
scandir() is a directory iteration function like os.listdir(), except
that instead of returning a list of bare filenames, it yields DirEntry
objects that include file type and stat information along with the
name. Using scandir() increases the speed of os.walk() by 2-20 times
(depending on the platform and file system) by avoiding unnecessary
calls to os.stat() in most cases. scandir is included in the Python
3.5+ standard library.

%package -n python3-%{module}
Summary:	A better directory iterator and faster os.walk() for Python
Group:		Libraries/Python

%description -n python3-%{module}
scandir() is a directory iteration function like os.listdir(), except
that instead of returning a list of bare filenames, it yields DirEntry
objects that include file type and stat information along with the
name. Using scandir() increases the speed of os.walk() by 2-20 times
(depending on the platform and file system) by avoiding unnecessary
calls to os.stat() in most cases. scandir is included in the Python
3.5+ standard library.

%prep
%setup -q -n %{module}-%{version}

%build
%if %{with python2}
%py_build

%if %{with tests}
rm -rf test/testdir
# Tests fail if unicode is not supported
LC_ALL=en_US.utf8 \
%{__python} test/run_tests.py
%endif

%endif

%if %{with python3}
%py3_build

%if %{with tests}
rm -rf test/testdir
# Tests fail if unicode is not supported
LC_ALL=en_US.utf8 \
%{__python3} test/run_tests.py
%endif

%endif

%install
rm -rf $RPM_BUILD_ROOT
%if %{with python2}
%py_install
%py_postclean
%endif

%if %{with python3}
%py3_install
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc README* LICENSE*
%{py_sitedir}/%{module}.py[co]
%attr(755,root,root) %{py_sitedir}/_%{module}.so
%{py_sitedir}/%{egg_name}-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-%{module}
%defattr(644,root,root,755)
%doc README* LICENSE*
%{py3_sitedir}/%{module}.py
%{py3_sitedir}/__pycache__/%{module}.*.pyc
%attr(755,root,root) %{py3_sitedir}/_%{module}.*.so
%{py3_sitedir}/%{egg_name}-%{version}-py*.egg-info
%endif
