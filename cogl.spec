%define url_ver %(echo %{version}|cut -d. -f1,2)

%define major 		20
%define pangomajor	20
%define gir_major	1.0
%define gir2_major	2.0

%define libname		%mklibname %{name} %{major}
%define pangoname	%mklibname %{name}-pango %{pangomajor}
%define devname 	%mklibname -d %{name}
%define devpango 	%mklibname -d %{name}-pango
%define devpath		%mklibname -d %{name}-path
%define girname 	%mklibname %{name}-gir %{gir_major}
%define girpango	%mklibname %{name}-pango-gir %{gir_major}
%define gir2name         %mklibname %{name}-gir %{gir2_major}
%define gir2pango        %mklibname %{name}-pango-gir %{gir2_major}
%define pathname	%mklibname %{name}-path %{major}

Summary:	A library for using 3D graphics hardware to draw pretty pictures
Name:		cogl
Version:	 1.20.0
Release:	2
Group:		System/Libraries
License:	LGPLv2+
Url:		http://www.clutter-project.org/
Source0:	ftp://ftp.gnome.org/pub/GNOME/sources/cogl/%{url_ver}/%{name}-%{version}.tar.xz

BuildRequires:  pkgconfig(cairo) >= 1.10
BuildRequires:  pkgconfig(gdk-pixbuf-2.0)
BuildRequires:  pkgconfig(gl)
BuildRequires:  pkgconfig(gobject-2.0) >= 2.28.0
BuildRequires:  pkgconfig(gobject-introspection-1.0)
BuildRequires:  pkgconfig(gmodule-no-export-2.0)
BuildRequires:  pkgconfig(pangocairo) >= 1.20
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(xext)
BuildRequires:  pkgconfig(xrandr)
BuildRequires:  pkgconfig(xfixes) >= 3
BuildRequires:  pkgconfig(xdamage)
BuildRequires:  pkgconfig(xcomposite) >= 0.4

%description
Cogl is a small open source library for using 3D graphics hardware to draw
pretty pictures. The API departs from the flat state machine style of
OpenGL and is designed to make it easy to write orthogonal components that
can render without stepping on each others toes.

As well aiming for a nice API, we think having a single library as opposed
to an API specification like OpenGL has a few advantages too; like being
able to paper over the inconsistencies/bugs of different OpenGL
implementations in a centralized place, not to mention the myriad of OpenGL
extensions. It also means we are in a better position to provide utility
APIs that help software developers since they only need to be implemented
once and there is no risk of inconsistency between implementations.

Having other backends, besides OpenGL, such as drm, Gallium or D3D are
options we are interested in for the future.

%package i18n
Summary:	Translations for %{name}
Group:		System/Internationalization
Obsoletes:	%{name} < 1.9.2

%description i18n
This contains the translation data for %{name}.

%files i18n -f %{name}.lang

%package -n %{libname}
Summary:	A library for using 3D graphics hardware to draw pretty pictures
Group:		System/Libraries
Suggests:	%{name}-i18n

%description -n %{libname}
This package contains the shared library for %{name}.

%package -n %{pangoname}
Summary:	A library for using 3D graphics hardware to draw pretty pictures
Group:		System/Libraries

%description -n %{pangoname}
This package contains the shared library for %{name}-pango.

%package -n %{pathname}
Summary:        A library for using 3D graphics hardware to draw pretty pictures
Group:          System/Libraries

%description -n %{pathname}
This package contains the shared library for %{name}-path.


%package -n %{girname}
Summary:	GObject Introspection interface description for %{name}
Group:		System/Libraries

%description -n %{girname}
GObject Introspection interface description for %{name}.

%package -n %{girpango}
Summary:	GObject Introspection interface description for %{name}-pango
Group:		System/Libraries

%description -n %{girpango}
GObject Introspection interface description for %{name}-pango.

%package -n %{gir2name}
Summary:        GObject Introspection interface description for %{name}
Group:          System/Libraries

%description -n %{gir2name}
GObject Introspection interface description for %{name}.

%package -n %{gir2pango}
Summary:        GObject Introspection interface description for %{name}-pango
Group:          System/Libraries

%description -n %{gir2pango}
GObject Introspection interface description for %{name}-pango.


%package -n %{devname}
Summary:	%{name} development environment
Group:		Development/C
Provides:	%{name}-devel = %{version}-%{release}
Requires:	%{libname} = %{version}-%{release}
Requires:	%{girname} = %{version}-%{release}
Requires:       %{gir2name} = %{version}-%{release}
Requires:	%{pathname} = %{version}-%{release}

%description -n %{devname}
Header files and libraries for building and developing apps with %{name}.

%package -n %{devpango}
Summary:	%{name}-pango development environment
Group:		Development/C
Requires:	%{pangoname} = %{version}-%{release}
Requires:	%{girpango} = %{version}-%{release}
Requires:       %{gir2pango} = %{version}-%{release}

%description -n %{devpango}
Header files and libraries for building and developing apps with %{name}-pango.

%package -n %{devpath}
Summary:        %{name}-path development environment
Group:          Development/C
Requires:       %{pathname} = %{version}-%{release}

%description -n %{devpath}
Header files and libraries for building and developing apps with %{name}-path.

%prep
%setup -q
%apply_patches

%build
export G_IR_SCANNER_DISABLE_CACHE=yes

CFLAGS="$RPM_OPT_FLAGS -fPIC"
%configure \
	--enable-cairo=yes \
	--enable-gdk-pixbuf=yes \
	--enable-cogl-pango=yes \
	--enable-glx=yes \
	--enable-gtk-doc=no \
	--enable-introspection=yes \
	--enable-examples-install=no

%make

%install
%makeinstall_std

#Remove examples
rm -rf %{buildroot}%{_datadir}/%{name}/examples-data/

%find_lang %{name}

%files -n %{libname}
%{_libdir}/libcogl.so.%{major}*

%files -n %{pangoname}
%{_libdir}/libcogl-pango.so.%{pangomajor}*

%files -n %{pathname}
%{_libdir}/libcogl-path.so.%{major}*

%files -n %{girname}
%{_libdir}/girepository-1.0/Cogl-%{gir_major}.typelib

%files -n %{gir2name}
%{_libdir}/girepository-1.0/Cogl-%{gir2_major}.typelib

%files -n %{girpango}
%{_libdir}/girepository-1.0/CoglPango-%{gir_major}.typelib

%files -n %{gir2pango}
%{_libdir}/girepository-1.0/CoglPango-%{gir2_major}.typelib

%files -n %{devname}
%doc NEWS README ChangeLog
%{_includedir}/%{name}/%{name}
%{_libdir}/libcogl.so
%{_libdir}/pkgconfig/cogl-1.0.pc
%{_libdir}/pkgconfig/cogl-gl-1.0.pc
%{_libdir}/pkgconfig/cogl-2.0-experimental.pc
%{_datadir}/gir-1.0/Cogl-%{gir_major}.gir
%{_datadir}/gir-1.0/Cogl-%{gir2_major}.gir

%files -n %{devpango}
%{_includedir}/%{name}/%{name}-pango
%{_libdir}/libcogl-pango.so
%{_libdir}/pkgconfig/cogl-pango*.pc
%{_datadir}/gir-1.0/CoglPango-%{gir_major}.gir
%{_datadir}/gir-1.0/CoglPango-%{gir2_major}.gir

%files -n %{devpath}
%{_includedir}/%{name}/%{name}-path
%{_libdir}/libcogl-path.so
%{_libdir}/pkgconfig/cogl-path*.pc

