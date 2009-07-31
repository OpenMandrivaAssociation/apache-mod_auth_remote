#Module-Specific definitions
%define apache_version 2.2.4
%define mod_name mod_auth_remote
%define mod_conf 82_%{mod_name}.conf
%define mod_so %{mod_name}.so

Summary:	DSO module for the apache Web server
Name:		apache-%{mod_name}
Version:	0.2
Release:	%mkrel 0.2
Group:		System/Servers
License:	Apache License
URL:		http://saju.pillai.googlepages.com/mod_auth_remote
Source0:	http://github.com/saju/mod_auth_remote/raw/dd48860bdca8366df1d93cd5df66a128278b6104/src/mod_auth_remote.c
Source1:	%{mod_conf}
Requires(pre): rpm-helper
Requires(postun): rpm-helper
Requires(pre):  apache-conf >= %{apache_version}
Requires(pre):  apache >= %{apache_version}
Requires:	apache-conf >= %{apache_version}
Requires:	apache >= %{apache_version}
BuildRequires:  apache-devel >= %{apache_version}
Epoch:		1
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
This module is a very simple, lightweight method of setting up a single signon
system across multiple web-applicaitions hosted on different servers.

The actual authentication & authorization system is deployed on a single server
instead of each individual server. All other servers are built with
mod_auth_remote enabled. When a request comes in, mod_auth_remote obtains the
client username & password from the client via basic authentication scheme.

It then builds a HTTP header with authorization header built from the client's
userid:passwd. mod_auth_remote then makes a HEAD request to the authentication
server. On reciept of a 2XX response, the client is validated; for all other
responses the client is not validated.

%prep

%setup -q -T -c -n %{mod_name}-%{version}

cp %{SOURCE0} %{mod_name}.c
cp %{SOURCE1} %{mod_conf}

%build
%{_sbindir}/apxs -c %{mod_name}.c

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

install -d %{buildroot}%{_libdir}/apache-extramodules
install -d %{buildroot}%{_sysconfdir}/httpd/modules.d

install -m0755 .libs/*.so %{buildroot}%{_libdir}/apache-extramodules/
install -m0644 %{mod_conf} %{buildroot}%{_sysconfdir}/httpd/modules.d/%{mod_conf}

%post
if [ -f %{_var}/lock/subsys/httpd ]; then
    %{_initrddir}/httpd restart 1>&2;
fi

%postun
if [ "$1" = "0" ]; then
    if [ -f %{_var}/lock/subsys/httpd ]; then
        %{_initrddir}/httpd restart 1>&2
    fi
fi

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files
%defattr(-,root,root)
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/modules.d/%{mod_conf}
%attr(0755,root,root) %{_libdir}/apache-extramodules/%{mod_so}
