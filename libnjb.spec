%define major	5
%define libname	%mklibname njb %{major}
%define devname	%mklibname njb -d

Summary:	A software library for talking to the Creative Nomad Jukeboxes and Dell DJs
Name: 	 	libnjb
Version: 	2.2.7
Release: 	3
License:	BSD
Group:		System/Libraries
Url:		http://sourceforge.net/projects/libnjb/
Source0:	%{name}-%{version}.tar.gz
Patch0:		libnjb-2.2.6-optimize-udev-rule.patch

BuildRequires:  doxygen
BuildRequires:  pkgconfig(libusb)

%description
Provides a user-level API (C library) for communicating with the
Creative Nomad JukeBox MP3 player under Linux and *BSD, as well
as simple command-line utilities to demonstrate the API functions.
This library works in user space.

%package -n 	%{libname}
Summary:        Dynamic libraries from %{name}
Group:          System/Libraries
%rename		daemon

%description -n %{libname}
Provides a user-level API (C library) for communicating with the
Creative Nomad JukeBox MP3 player under Linux and *BSD, as well
as simple command-line utilities to demonstrate the API functions.
This library works in user space.
This libraries from %{name}.

%package -n 	%{devname}
Summary: 	Header files and static libraries from %{name}
Group: 		Development/C
Requires: 	%{libname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release} 
Obsoletes:	%{mklibname njb 5 -d}

%description -n %{devname}
Libraries and includes files for developing programs based on %{name}.

%prep
%setup -q
#%patch0 -p1 -b .udev_opt~

%build
%configure2_5x --disable-static
%make

%install
%makeinstall pkgdocdir=`pwd`/installed-docs
#gw TODO fix device ownership
#install -m644 nomad.rules -D %{buildroot}%{_sysconfdir}/udev/rules.d/60-libnjb.rules
install -m644 libnjb.fdi -D %{buildroot}%{_datadir}/hal/fdi/information/10freedesktop/10-usb-music-players-libnjb.fdi

%files
%doc AUTHORS ChangeLog FAQ HACKING README LICENSE
%{_bindir}/*
#config(noreplace) %{_sysconfdir}/udev/rules.d/60-libnjb.rules
%{_datadir}/hal/fdi/information/10freedesktop/10-usb-music-players-libnjb.fdi

%files -n %{libname}
%{_libdir}/libnjb.so.%{major}*

%files -n %{devname}
%doc installed-docs/*
%{_includedir}/%{name}.h
%{_libdir}/%{name}.so
%{_libdir}/pkgconfig/%{name}.pc

