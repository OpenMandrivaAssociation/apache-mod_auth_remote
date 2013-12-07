#Module-Specific definitions
%define apache_version 2.2.4
%define mod_name mod_auth_remote
%define mod_conf 82_%{mod_name}.conf
%define mod_so %{mod_name}.so

Summary:	DSO module for the apache Web server
Name:		apache-%{mod_name}
Version:	0.2
Release:	0.13
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
%{_bindir}/apxs -c %{mod_name}.c

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


%changelog
* Sat May 14 2011 Oden Eriksson <oeriksson@mandriva.com> 1:0.2-0.7mdv2011.0
+ Revision: 674423
- rebuild

* Mon May 02 2011 Oden Eriksson <oeriksson@mandriva.com> 1:0.2-0.6
+ Revision: 662771
- mass rebuild

* Sun Oct 24 2010 Oden Eriksson <oeriksson@mandriva.com> 1:0.2-0.5mdv2011.0
+ Revision: 588277
- rebuild

* Mon Mar 08 2010 Oden Eriksson <oeriksson@mandriva.com> 1:0.2-0.4mdv2010.1
+ Revision: 515832
- rebuilt for apache-2.2.15

* Wed Sep 30 2009 Oden Eriksson <oeriksson@mandriva.com> 1:0.2-0.3mdv2010.0
+ Revision: 451696
- rebuild

* Fri Jul 31 2009 Oden Eriksson <oeriksson@mandriva.com> 1:0.2-0.2mdv2010.0
+ Revision: 405127
- rebuild

* Sun Mar 22 2009 Oden Eriksson <oeriksson@mandriva.com> 1:0.2-0.1mdv2009.1
+ Revision: 360422
- 0.2 (beta)

* Wed Jan 07 2009 Oden Eriksson <oeriksson@mandriva.com> 1:0.1-18mdv2009.1
+ Revision: 326480
- rebuild

* Mon Jul 14 2008 Oden Eriksson <oeriksson@mandriva.com> 1:0.1-17mdv2009.0
+ Revision: 235637
- rebuild

* Thu Jun 05 2008 Oden Eriksson <oeriksson@mandriva.com> 1:0.1-16mdv2009.0
+ Revision: 215287
- rebuild

* Fri Mar 07 2008 Oden Eriksson <oeriksson@mandriva.com> 1:0.1-15mdv2008.1
+ Revision: 181436
- rebuild

* Mon Feb 18 2008 Thierry Vignaud <tv@mandriva.org> 1:0.1-14mdv2008.1
+ Revision: 170709
- rebuild
- fix "foobar is blabla" summary (=> "blabla") so that it looks nice in rpmdrake

* Fri Jan 11 2008 Thierry Vignaud <tv@mandriva.org> 1:0.1-13mdv2008.1
+ Revision: 148460
- rebuild
- kill re-definition of %%buildroot on Pixel's request

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

* Sat Sep 08 2007 Oden Eriksson <oeriksson@mandriva.com> 1:0.1-12mdv2008.0
+ Revision: 82357
- rebuild

* Thu Aug 16 2007 Oden Eriksson <oeriksson@mandriva.com> 1:0.1-11mdv2008.0
+ Revision: 64317
- use the new %%serverbuild macro

* Wed Jun 13 2007 Oden Eriksson <oeriksson@mandriva.com> 1:0.1-10mdv2008.0
+ Revision: 38409
- rebuild


* Sat Mar 10 2007 Oden Eriksson <oeriksson@mandriva.com> 0.1-9mdv2007.1
+ Revision: 140579
- rebuild

* Tue Feb 27 2007 Oden Eriksson <oeriksson@mandriva.com> 1:0.1-8mdv2007.1
+ Revision: 126607
- general cleanups

* Sat Feb 10 2007 Oden Eriksson <oeriksson@mandriva.com> 1:0.1-7mdv2007.1
+ Revision: 118723
- bump release
- do mdvsys sync...

* Sat Feb 10 2007 Oden Eriksson <oeriksson@mandriva.com> 1:0.1-6mdv2007.1
+ Revision: 118714
- fix url

* Thu Nov 09 2006 Oden Eriksson <oeriksson@mandriva.com> 1:0.1-5mdv2007.1
+ Revision: 79234
- Import apache-mod_auth_remote

* Sun Jul 30 2006 Oden Eriksson <oeriksson@mandriva.com> 1:0.1-5mdv2007.0
- rebuild

* Thu Dec 15 2005 Oden Eriksson <oeriksson@mandriva.com> 0.1-4mdk
- rebuilt against apache-2.2.0
- added P1 to fix warnings (pterjan)
- added P2 to conform with apr1

* Sun Oct 30 2005 Oden Eriksson <oeriksson@mandriva.com> 0.1-3mdk
- rebuilt to provide a -debug package too

* Mon Oct 17 2005 Oden Eriksson <oeriksson@mandriva.com> 1:0.1-2mdk
- rebuilt against correct apr-0.9.7

* Sat Oct 15 2005 Oden Eriksson <oeriksson@mandriva.com> 1:0.1-1mdk
- rebuilt for apache-2.0.55

* Sat Jul 30 2005 Oden Eriksson <oeriksson@mandriva.com> 2.0.54_0.1-3mdk
- added another work around for a rpm bug

* Sat Jul 30 2005 Oden Eriksson <oeriksson@mandriva.com> 2.0.54_0.1-2mdk
- added a work around for a rpm bug, "Requires(foo,bar)" don't work

* Fri May 27 2005 Oden Eriksson <oeriksson@mandriva.com> 2.0.54_0.1-1mdk
- rename the package
- use the %%mkrel macro
- the conf.d directory is renamed to modules.d
- use new rpm-4.4.x pre,post magic

* Sun Feb 27 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 2.0.53_0.1-5mdk
- fix %%post and %%postun to prevent double restarts

* Wed Feb 16 2005 Stefan van der Eijk <stefan@eijk.nu> 2.0.53_0.1-4mdk
- fix bug #6574

* Wed Feb 16 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 2.0.53_0.1-3mdk
- fix deps

* Tue Feb 15 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 2.0.53_0.1-2mdk
- spec file cleanups, remove the ADVX-build stuff

* Tue Feb 08 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 2.0.53_0.1-1mdk
- rebuilt for apache 2.0.53

* Wed Sep 29 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 2.0.52_0.1-1mdk
- built for apache 2.0.52

* Fri Sep 17 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 2.0.51_0.1-1mdk
- built for apache 2.0.51

* Wed Aug 11 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 2.0.50_0.1-3mdk
- rebuilt

* Tue Jul 13 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 2.0.50_0.1-2mdk
- remove redundant provides

* Thu Jul 01 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 2.0.50_0.1-1mdk
- built for apache 2.0.50

* Sat Jun 12 2004 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.49_0.1-1mdk
- built for apache 2.0.49
- used a sligthly newer source
- v1.0 was wrong, should have been v0.1, fixed now
- fixed P0

