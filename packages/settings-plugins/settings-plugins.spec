%global _cross_first_party 1
%undefine _debugsource_packages

# Do not prefer shared linking, since the libstd we use at build time
# may not match the one installed on the final image.
%global __global_rustflags_shared %__global_rustflags

%global _cross_pluginsdir %{_cross_libdir}/settings-plugins

Name: %{_cross_os}settings-plugins
Version: 0.0
Release: 0%{?dist}
Summary: Settings plugins
License: Apache-2.0 OR MIT
URL: https://github.com/bottlerocket-os/bottlerocket
BuildRequires: %{_cross_os}glibc-devel
Requires: %{_cross_os}glibc-devel
Requires: %{_cross_os}settings-plugin(any)

%description
%{summary}.

%package ootb-k8s
Summary: Settings plugin for the ootb-k8s variants
Requires: %{_cross_os}variant-family(ootb-k8s)
Provides: %{_cross_os}settings-plugin(any)
Provides: %{_cross_os}settings-plugin(ootb-k8s)
Conflicts: %{_cross_os}settings-plugin(any)

%description ootb-k8s
%{summary}.

%prep
%setup -T -c
%cargo_prep

%build
cat %{_builddir}/sources/Cargo.toml
%cargo_build --manifest-path %{_builddir}/sources/Cargo.toml \
  -p settings-plugin-ootb-k8s \
  %{nil}

%install
install -d %{buildroot}%{_cross_pluginsdir}
install -d %{buildroot}%{_cross_factorydir}%{_cross_sysconfdir}/ld.so.conf.d
install -d %{buildroot}%{_cross_tmpfilesdir}

for plugin in \
  ootb-k8s \
  ;
do
  install -d "%{buildroot}%{_cross_pluginsdir}/${plugin}"
  plugin_so="libsettings_$(echo "${plugin}" | sed -e 's,-,_,g' -e 's,\.,_,g').so"
  install -p -m 0755 \
    "${HOME}/.cache/%{__cargo_target}/release/${plugin_so}" \
    "%{buildroot}%{_cross_pluginsdir}/${plugin}/libsettings.so"
  echo \
    "%{_cross_pluginsdir}/${plugin}" > \
    "%{buildroot}%{_cross_factorydir}%{_cross_sysconfdir}/ld.so.conf.d/${plugin}.conf"
  echo \
    "C /etc/ld.so.conf.d/${plugin}.conf" > \
    "%{buildroot}%{_cross_tmpfilesdir}/settings-plugin-${plugin}.conf"
done

%files
%dir %{_cross_pluginsdir}

%files ootb-k8s
%{_cross_pluginsdir}/ootb-k8s/libsettings.so
%{_cross_factorydir}%{_cross_sysconfdir}/ld.so.conf.d/ootb-k8s.conf
%{_cross_tmpfilesdir}/settings-plugin-ootb-k8s.conf
