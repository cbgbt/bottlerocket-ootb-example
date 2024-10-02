%global _cross_first_party 1
%undefine _debugsource_packages

Name: %{_cross_os}ootb-release
Version: 0.0
Release: 0%{?dist}
Summary: Raspberry pi variants
License: Apache-2.0 OR MIT
URL: https://github.com/bottlerocket-os/bottlerocket

Requires: %{_cross_os}ootb-release(any)

%description
%{summary}.

%package ootb-k8s
Summary: The ootb-k8s variant
Requires: %{_cross_os}variant-family(ootb-k8s)

Provides: %{_cross_os}ootb-release(any)
Provides: %{_cross_os}ootb-release(ootb-k8s)
Conflicts: %{_cross_os}ootb-release(any)

Provides: %{_cross_os}variant-family(aws-k8s)
Provides: %{_cross_os}variant-runtime(k8s)
Provides: %{_cross_os}variant-platform(aws)

%description ootb-k8s
%{summary}.

%prep
%{nil}

%build
%{nil}

%install
%{nil}

%files
%{nil}

%files ootb-k8s
%{nil}
