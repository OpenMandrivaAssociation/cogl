%define major 		11
%define pangomajor	0
%define gir_major	1.0

%define libname		%mklibname %{name} %{major}
%define pangoname	%mklibname %{name}-pango %{pangomajor}
%define develname 	%mklibname -d %{name}
%define develpango 	%mklibname -d %{name}-pango
%define girname 	%mklibname %{name}-gir %{gir_major}
%define girpango	%mklibname %{name}-pango-gir %{gir_major}

Summary:	A library for using 3D graphics hardware to draw pretty pictures
Name:		cogl
Version:	1.12.0
Release:	1
Group:		System/Libraries
License:	LGPLv2+
URL:		http://www.clutter-project.org/
Source0:	ftp://ftp.gnome.org/pub/GNOME/sources/cogl/1.12/%{name}-%{version}.tar.xz

BuildRequires:  pkgconfig(gl)
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(xext)
BuildRequires:  pkgconfig(xfixes) >= 3
BuildRequires:  pkgconfig(xdamage)
BuildRequires:  pkgconfig(xcomposite) >= 0.4
BuildRequires:  pkgconfig(gobject-2.0) >= 2.28.0
BuildRequires:  pkgconfig(gmodule-no-export-2.0)
BuildRequires:  pkgconfig(gdk-pixbuf-2.0)
BuildRequires:  pkgconfig(cairo) >= 1.10
BuildRequires:  pkgconfig(pangocairo) >= 1.20
BuildRequires:  pkgconfig(gobject-introspection-1.0)

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

%description -n %{libname}
This package contains the shared library for %{name}.

%package -n %{pangoname}
Summary:	A library for using 3D graphics hardware to draw pretty pictures
Group:		System/Libraries

%description -n %{pangoname}
This package contains the shared library for %{name}-pango.

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

%package -n %{develname}
Summary:	%{name} development environment
Group:		Development/C 
Provides:	%{name}-devel = %{version}-%{release}
Requires:	%{libname} = %{version}-%{release}
Requires:	%{girname} = %{version}-%{release}

%description -n %{develname}
Header files and libraries for building and developing apps with %{name}.

%package -n %{develpango}
Summary:	%{name}-pango development environment
Group:		Development/C 
Requires:	%{pangoname} = %{version}-%{release}
Requires:	%{girpango} = %{version}-%{release}

%description -n %{develpango}
Header files and libraries for building and developing apps with %{name}-pango.

%prep
%setup -q
#%apply_patches

%build
CFLAGS="$RPM_OPT_FLAGS -fPIC"
%configure2_5x \
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

#Remove libtool archives.
find %{buildroot} -name "*.la" -delete

%find_lang %{name}

%files -n %{libname}
%{_libdir}/libcogl.so.%{major}*

%files -n %{pangoname}
%{_libdir}/libcogl-pango.so.%{pangomajor}*

%files -n %{girname}
%{_libdir}/girepository-1.0/Cogl-%{gir_major}.typelib

%files -n %{girpango}
%{_libdir}/girepository-1.0/CoglPango-%{gir_major}.typelib

%files -n %{develname}
%doc NEWS README ChangeLog
%{_includedir}/%{name}/%{name}
%{_libdir}/libcogl.so
%{_libdir}/pkgconfig/cogl-1.0.pc
%{_libdir}/pkgconfig/cogl-gl-1.0.pc
%{_libdir}/pkgconfig/cogl-2.0-experimental.pc
%{_datadir}/gir-1.0/Cogl-%{gir_major}.gir

%files -n %{develpango}
%{_includedir}/%{name}/%{name}-pango
%{_libdir}/libcogl-pango.so
%{_libdir}/pkgconfig/cogl-pango*.pc
%{_datadir}/gir-1.0/CoglPango-%{gir_major}.gir

%changelog
* Fri Sep 28 2012 Arkady L. Shane <ashejn@rosalab.ru> 1.12.0-1
- update to 1.12.0
