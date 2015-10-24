#
# Conditional build:
%bcond_without	static_libs	# don't build static libraries
#
Summary:	High-quality glyph rendering library using OpenGL ES2 shaders
Summary(pl.UTF-8):	Biblioteka wysokiej jakości renderowania glifów przy użyciu shaderów OpenGL ES2
Name:		glyphy
Version:	0.2.0
%define	snap	20151002
%define	gitref	71390c5baccbe2bcba19171d1e31732a49c35fa3
%define	rel	1
Release:	0.%{snap}.%{rel}
License:	Apache v2.0
Group:		Libraries
Source0:	https://github.com/behdad/glyphy/archive/%{gitref}/%{name}-%{snap}.tar.gz
# Source0-md5:	295ee71482abf9b3c4798d6955bc0b6a
Patch0:		%{name}-default-font.patch
URL:		http://glyphy.org/
BuildRequires:	OpenGL-devel
BuildRequires:	OpenGL-glut-devel
BuildRequires:	autoconf >= 2.64
BuildRequires:	automake >= 1:1.11.1
BuildRequires:	freetype-devel >= 2
BuildRequires:	glew-devel
BuildRequires:	libtool >= 2:2.2
BuildRequires:	pkgconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
GLyphy is a signed-distance-field (SDF) text renderer using OpenGL ES2
shading language.

%description -l pl.UTF-8
GLyphy to biblioteka renderująca tekst metodą SDF (signed distance
field) przy użyciu języka cieniującego OpenGL ES2.

%package devel
Summary:	Header files for GLyphy library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki GLyphy
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	freetype-devel >= 2

%description devel
Header files for GLyphy library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki GLyphy.

%package static
Summary:	Static GLyphy library
Summary(pl.UTF-8):	Statyczna biblioteka GLyphy
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static GLyphy library.

%description static -l pl.UTF-8
Statyczna biblioteka GLyphy.

%prep
%setup -q -n %{name}-%{gitref}
%patch0 -p1

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	DEFAULT_FONT="%{_fontsdir}/TTF/DejaVuSans.ttf" \
	--disable-silent-rules \
	%{?with_static_libs:--enable-static}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libglyphy.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS COPYING NEWS README.md
%attr(755,root,root) %{_libdir}/libglyphy.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libglyphy.so.0
%{_datadir}/glyphy

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libglyphy.so
%{_includedir}/glyphy
%{_pkgconfigdir}/glyphy.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libglyphy.a
%endif
