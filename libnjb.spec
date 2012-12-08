
%define major		5
%define libname 	%mklibname njb %{major}
%define develname	%mklibname njb -d

Name: 	 	libnjb
Summary:	A software library for talking to the Creative Nomad Jukeboxes and Dell DJs
Version: 	2.2.7
Release: 	1

Source0:	%{name}-%{version}.tar.gz
Patch0:		libnjb-2.2.6-optimize-udev-rule.patch
URL:		http://sourceforge.net/projects/libnjb/
License:	BSD
Group:		System/Libraries
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot

BuildRequires:  libusb-devel
BuildRequires:  doxygen

%description
Provides a user-level API (C library) for communicating with the
Creative Nomad JukeBox MP3 player under Linux and *BSD, as well
as simple command-line utilities to demonstrate the API functions.
This library works in user space.

%package -n 	%{libname}
Summary:        Dynamic libraries from %{name}
Group:          System/Libraries
Provides:	daemon
Obsoletes:	daemon = %{version}-%{release}

%description -n %{libname}
Provides a user-level API (C library) for communicating with the
Creative Nomad JukeBox MP3 player under Linux and *BSD, as well
as simple command-line utilities to demonstrate the API functions.
This library works in user space.
This libraries from %{name}.

%package -n 	%{develname}
Summary: 	Header files and static libraries from %name
Group: 		Development/C
Requires: 	%{libname} = %{version}
Provides:	%{name}-devel = %{version}-%{release} 
Obsoletes:	%{mklibname njb 5 -d}

%description -n %{develname}
Libraries and includes files for developing programs based on %name.

%prep
%setup -q
#%patch0 -p1 -b .udev_opt~

%build
%configure2_5x
%make

%install
rm -rf %{buildroot} installed-docs
%makeinstall pkgdocdir=`pwd`/installed-docs
#gw TODO fix device ownership
#install -m644 nomad.rules -D %{buildroot}%{_sysconfdir}/udev/rules.d/60-libnjb.rules
install -m644 libnjb.fdi -D %{buildroot}%{_datadir}/hal/fdi/information/10freedesktop/10-usb-music-players-libnjb.fdi

%clean
rm -rf $RPM_BUILD_ROOT

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif
%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

%files
%defattr(-,root,root)
%doc AUTHORS ChangeLog FAQ HACKING  README LICENSE
%{_bindir}/*
#%config(noreplace) %{_sysconfdir}/udev/rules.d/60-libnjb.rules
%{_datadir}/hal/fdi/information/10freedesktop/10-usb-music-players-libnjb.fdi

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/libnjb.so.%{major}*

%files -n %{develname}
%defattr(-,root,root)
%doc installed-docs/*
%{_includedir}/%{name}.h
%{_libdir}/%{name}.so
%{_libdir}/%{name}.a
%{_libdir}/pkgconfig/%{name}.pc



%changelog
* Thu Aug 30 2012 Vladimir Testov <vladimir.testov@rosalab.ru> 2.2.7-1
- update to 2.2.7

* Mon May 02 2011 Oden Eriksson <oeriksson@mandriva.com> 2.2.6-9mdv2011.0
+ Revision: 661504
- mass rebuild

* Sun Nov 28 2010 Oden Eriksson <oeriksson@mandriva.com> 2.2.6-8mdv2011.0
+ Revision: 602582
- rebuild

* Wed Nov 25 2009 Per Øyvind Karlsen <peroyvind@mandriva.org> 2.2.6-7mdv2010.1
+ Revision: 469930
- backport libnjb.fdi from CVS (P1):
  	o Add keys that signify WAV support on all devices.
  	o Update hal fdi file to output info.vendor info.product, as
  	 hal-supplied values for these are often incorrect.
- fix bogus summary
- use more recent hal .fdi file that comes with libnjb
- fix ordering of udev rule
- optimize udev rule (P0 from cvs)

* Thu Oct 08 2009 Götz Waschk <waschk@mandriva.org> 2.2.6-5mdv2010.0
+ Revision: 456083
- rebuild for new libusb.la location

* Wed Sep 02 2009 Christophe Fergeau <cfergeau@mandriva.com> 2.2.6-4mdv2010.0
+ Revision: 425630
- rebuild

* Tue Jun 17 2008 Thierry Vignaud <tv@mandriva.org> 2.2.6-3mdv2009.0
+ Revision: 222938
- rebuild

  + Pixel <pixel@mandriva.com>
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

* Tue Mar 04 2008 Oden Eriksson <oeriksson@mandriva.com> 2.2.6-2mdv2008.1
+ Revision: 178978
- rebuild

  + Thierry Vignaud <tv@mandriva.org>
    - fix no-buildroot-tag

* Thu Sep 06 2007 Emmanuel Andry <eandry@mandriva.org> 2.2.6-1mdv2008.0
+ Revision: 81157
- New version

* Thu Jul 26 2007 Adam Williamson <awilliamson@mandriva.org> 2.2.5-5mdv2008.0
+ Revision: 55730
- rebuild for 2008
- new devel policy
- drop all the hotplug stuff (hotplug is not used any more)


* Tue Sep 19 2006 Per Øyvind Karlsen <pkarlsen@mandriva.com> 2.2.5-5mdv2007.0
- rebuild

* Thu Aug 31 2006 Götz Waschk <waschk@mandriva.org> 2.2.5-4mdv2007.0
- enable hotplugging

* Wed Aug 23 2006 Emmanuel Andry <eandry@mandriva.org> 2.2.5-3mdv2007.0
- rebuild

* Wed Mar 01 2006 Götz Waschk <waschk@mandriva.org> 2.2.5-2mdk
- fix license
- fix doc listing
- fix buildrequires

* Mon Feb 27 2006 Götz Waschk <waschk@mandriva.org> 2.2.5-1mdk
- spec fixes
- source URL
- new version

* Wed Dec 07 2005 Götz Waschk <waschk@mandriva.org> 2.2.4-1mdk
- New release 2.2.4

* Fri Oct 28 2005 Nicolas Lécureuil <neoclust@mandriva.org> 2.2-2mdk
- Fix BuildRequires

* Thu Jul 07 2005 Per Øyvind Karlsen <pkarlsen@mandriva.com> 2.2-1mdk
- 2.2
- bump major

* Thu Jun 16 2005 Per Øyvind Karlsen <pkarlsen@mandriva.com> 2.1.2-1mdk
- 2.1.2
- new major

* Wed Nov 10 2004 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 1.2-1mdk
- 1.2

* Sat Jun 05 2004 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 1.1-1mdk
- initial mdk release

