# The build process looks for at least one package to provide a migrations directory.
# This package provides a stub so that the build will proceed.

%global _cross_first_party 1
%undefine _debugsource_packages

Name: %{_cross_os}migrations
Version: 0.0
Release: 0%{?dist}
Summary: Settings migrations
License: Apache-2.0 OR MIT
URL: https://github.com/cbgbt/bottlerocket-ootb-example

# Ideally this would be the package name, but for now the build system expects to find a package
# named "bottlerocket-migrations"
Provides: %{_cross_os}settings-migrations

%description
%{summary}

%prep
%{nil}

%build
%{nil}

%install
install -d %{buildroot}%{_cross_datadir}/migrations

%files
%dir %{_cross_datadir}/migrations
