#Module-Specific definitions
%define apache_version 2.4.0
%define mod_name mod_auth_remote
%define load_order 182

Summary:	DSO module for the apache Web server
Name:		apache-%{mod_name}
Version:	0.2
Release:	2
Group:		System/Servers
License:	Apache License
URL:		http://saju.pillai.googlepages.com/mod_auth_remote
Source0:	https://raw.github.com/saju/mod_auth_remote/master/src/mod_auth_remote.c
Requires(pre): rpm-helper
Requires(postun): rpm-helper
Requires:	apache >= %{apache_version}
BuildRequires:  apache-devel >= %{apache_version}
Epoch:		1

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

%build
apxs -c %{mod_name}.c

%install

install -d %{buildroot}%{_libdir}/apache
install -d %{buildroot}%{_sysconfdir}/httpd/modules.d

install -m0755 .libs/*.so %{buildroot}%{_libdir}/apache/

cat > %{buildroot}%{_sysconfdir}/httpd/modules.d/%{load_order}_%{mod_name}.conf << EOF
LoadModule auth_remote_module %{_libdir}/apache/%{mod_name}.so
EOF

%post
/bin/systemctl daemon-reload >/dev/null 2>&1 || :

%postun
if [ "$1" = "0" ]; then
    /bin/systemctl daemon-reload >/dev/null 2>&1 || :
fi

%files
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/modules.d/*.conf
%attr(0755,root,root) %{_libdir}/apache/*.so
