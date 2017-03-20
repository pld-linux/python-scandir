#
# Conditional build:
%bcond_without	doc	# don't build doc
%bcond_without	tests	# do not perform "make test"
%bcond_without	python2 # CPython 2.x module
%bcond_with	python3 # CPython 3.x module, build for Python3<3.5

%define 	module		scandir
%define 	egg_name	scandir
Summary:	A better directory iterator and faster os.walk() for Python 2
Summary(pl.UTF-8):	Lepszy iterator po katalogach i szybsze os.walk() dla Pythona 2
Name:		python-%{module}
Version:	1.5
Release:	1
License:	BSD
Group:		Libraries/Python
#Source0Download: https://github.com/benhoyt/scandir/releases
Source0:	https://github.com/benhoyt/scandir/archive/v%{version}/%{module}-%{version}.tar.gz
# Source0-md5:	798407545833aa7011c1ee34b580e902
URL:		https://github.com/benhoyt/scandir
%if %{with tests} && %(locale -a | grep -q '^C\.UTF-8$'; echo $?)
BuildRequires:	glibc-localedb-all
%endif
%if %{with python2}
BuildRequires:	python-modules >= 1:2.6
BuildRequires:	python-setuptools
%endif
%if %{with python3}
BuildRequires:	python3-modules >= 1:3.2
BuildRequires:	python3-setuptools
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
Requires:	python-modules >= 1:2.6
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
scandir() is a directory iteration function like os.listdir(), except
that instead of returning a list of bare filenames, it yields DirEntry
objects that include file type and stat information along with the
name. Using scandir() increases the speed of os.walk() by 2-20 times
(depending on the platform and file system) by avoiding unnecessary
calls to os.stat() in most cases. scandir is included in the Python
3.5+ standard library.

%description -l pl.UTF-8
scandir() to funkcja iterująca po katalogu podobna do os.listdir(),
ale zamiast zwracania listy samych nazw plików, przekazująca przez
yield obiekty DirEntry, zawierające poza nazwą typ pliku oraz
informacje stat. Użycie scandir() przyspiesza os.walk() 2-20 razy (w
zależności od platformy i systemu plików), zapobiegając w większości
przypadków niepotrzebnym wywołaniom os.stat(). scandir jest zawarte w
bibliotece standardowej Pythona 3.5+.

%package -n python3-%{module}
Summary:	A better directory iterator and faster os.walk() for Python 3 < 3.5
Summary(pl.UTF-8):	Lepszy iterator po katalogach i szybsze os.walk() dla Pythona 3 < 3.5
Group:		Libraries/Python
Requires:	python3-modules >= 1:3.2

%description -n python3-%{module}
scandir() is a directory iteration function like os.listdir(), except
that instead of returning a list of bare filenames, it yields DirEntry
objects that include file type and stat information along with the
name. Using scandir() increases the speed of os.walk() by 2-20 times
(depending on the platform and file system) by avoiding unnecessary
calls to os.stat() in most cases. scandir is included in the Python
3.5+ standard library.

%description -n python3-%{module} -l pl.UTF-8
scandir() to funkcja iterująca po katalogu podobna do os.listdir(),
ale zamiast zwracania listy samych nazw plików, przekazująca przez
yield obiekty DirEntry, zawierające poza nazwą typ pliku oraz
informacje stat. Użycie scandir() przyspiesza os.walk() 2-20 razy (w
zależności od platformy i systemu plików), zapobiegając w większości
przypadków niepotrzebnym wywołaniom os.stat(). scandir jest zawarte w
bibliotece standardowej Pythona 3.5+.

%prep
%setup -q -n %{module}-%{version}

%build
%if %{with python2}
%py_build

%if %{with tests}
rm -rf test/testdir
# Tests fail if unicode is not supported
LC_ALL=C.UTF-8 \
%{__python} test/run_tests.py
%endif

%endif

%if %{with python3}
%py3_build

%if %{with tests}
rm -rf test/testdir
# Tests fail if unicode is not supported
LC_ALL=C.UTF-8 \
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
%doc LICENSE.txt README.rst
%{py_sitedir}/scandir.py[co]
%attr(755,root,root) %{py_sitedir}/_scandir.so
%{py_sitedir}/%{egg_name}-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-%{module}
%defattr(644,root,root,755)
%doc LICENSE.txt README.rst
%{py3_sitedir}/scandir.py
%{py3_sitedir}/__pycache__/scandir.cpython-*.pyc
%attr(755,root,root) %{py3_sitedir}/_scandir.cpython-*.so
%{py3_sitedir}/%{egg_name}-%{version}-py*.egg-info
%endif
