%define name	libnjb
%define version	2.2.6

%define major		5
%define libname 	%mklibname njb %{major}
%define develname	%mklibname njb -d

Name: 	 	%{name}
Summary: 	Lightweight C library which eases the writing of UNIX daemons
Version: 	%{version}
Release: 	%mkrel 5

Source0:	http://prdownloads.sourceforge.net/libnjb/%{name}-%{version}.tar.bz2
Source1:	http://banshee-project.org/files/misc/20-njb.fdi.bz2
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

%build
%configure2_5x
%make

%install
rm -rf $RPM_BUILD_ROOT installed-docs
%makeinstall pkgdocdir=`pwd`/installed-docs
#gw TODO fix device ownership
install -D -m 644 nomad.rules %buildroot%_sysconfdir/udev/rules.d/nomad.rules
mkdir -p %buildroot%_datadir/hal/information/20thirdparty/
# gw TODO fix resmgr config in hal according to
# http://banshee-project.org/Releases/0.10.10
bzcat %SOURCE1 > %buildroot%_datadir/hal/information/20thirdparty/20-njb.fdi

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
%config(noreplace) %_sysconfdir/udev/rules.d/nomad.rules
%_datadir/hal/information/20thirdparty/20-njb.fdi

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

