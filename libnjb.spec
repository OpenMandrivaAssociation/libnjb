%define name	libnjb
%define version	2.2.6

%define major		5
%define libname 	%mklibname njb %{major}
%define develname	%mklibname njb -d

Name: 	 	%{name}
Summary:	A software library for talking to the Creative Nomad Jukeboxes and Dell DJs
Version: 	%{version}
Release: 	%mkrel 8

Source0:	http://prdownloads.sourceforge.net/libnjb/%{name}-%{version}.tar.bz2
Patch0:		libnjb-2.2.6-optimize-udev-rule.patch
Patch1:		libnjb-2.2.6-libnjb.fdi-cvs-revision-1.3.patch
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
%patch0 -p1 -b .udev_opt~
%patch1 -p1 -b .fdi_rev1.3~

%build
%configure2_5x
%make

%install
rm -rf %{buildroot} installed-docs
%makeinstall pkgdocdir=`pwd`/installed-docs
#gw TODO fix device ownership
install -m644 nomad.rules -D %{buildroot}%{_sysconfdir}/udev/rules.d/60-libnjb.rules
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
%config(noreplace) %{_sysconfdir}/udev/rules.d/60-libnjb.rules
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
%attr(644,root,root) %{_libdir}/%{name}.la
%{_libdir}/pkgconfig/%{name}.pc

