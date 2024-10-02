%global _cross_first_party 1
%undefine _debugsource_packages

%global cargo_clean %{__cargo_cross_env} %{__cargo} clean

%global _cross_defaultsdir %{_cross_datadir}/storewolf

Name: %{_cross_os}settings-defaults
Version: 0.0
Release: 0%{?dist}
Summary: Settings defaults
License: Apache-2.0 OR MIT
URL: https://github.com/bottlerocket-os/bottlerocket
BuildRequires: %{_cross_os}glibc-devel
Requires: %{_cross_os}settings-defaults(any)

%description
%{summary}.

%package ootb-k8s
Summary: Settings defaults for the ootb-k8s variant
Requires: %{_cross_os}variant-family(ootb-k8s)
Provides: %{_cross_os}settings-defaults(any)
Provides: %{_cross_os}settings-defaults(ootb-k8s)
Conflicts: %{_cross_os}settings-defaults(any)

%description ootb-k8s
%{summary}.

%prep
%setup -T -c
%cargo_prep

%build
declare -a projects
for defaults in \
  ootb-k8s \
  ;
do
  projects+=( "-p" "settings-defaults-$(echo "${defaults}" | sed -e 's,\.,_,g')" )
done

# Output is written to an unpredictable directory name, so clean it up first to
# avoid reusing any cached artifacts.
%cargo_clean --manifest-path %{_builddir}/sources/Cargo.toml \
  "${projects[@]}" \
  %{nil}

%cargo_build --manifest-path %{_builddir}/sources/Cargo.toml \
  "${projects[@]}" \
  %{nil}

%install
install -d %{buildroot}%{_cross_defaultsdir}
install -d %{buildroot}%{_cross_tmpfilesdir}

for defaults in \
  ootb-k8s \
  ;
do
  crate="$(echo "${defaults}" | sed -e 's,\.,_,g')"
  for f in $(find "${HOME}/.cache" -name "settings-defaults-${crate}.toml") ; do
    install -p -m 0644 "${f}" "%{buildroot}%{_cross_defaultsdir}/${defaults}.toml"
  done
  echo \
    "L+ /etc/storewolf/defaults.toml - - - - %{_cross_defaultsdir}/${defaults}.toml" > \
    "%{buildroot}%{_cross_tmpfilesdir}/storewolf-defaults-${defaults}.conf"
done

%files
%dir %{_cross_defaultsdir}

%files ootb-k8s
%{_cross_defaultsdir}/ootb-k8s.toml
%{_cross_tmpfilesdir}/storewolf-defaults-ootb-k8s.conf
