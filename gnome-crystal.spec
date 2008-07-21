%define name 	gnome-crystal
%define version 0.6.5
%define release %mkrel 2

Summary: 	GNOME crystal structure visualization
Name: 		%{name}
Version: 	%{version}
Release: 	%{release}
Source0: 	%{name}-%{version}.tar.bz2
Patch0:		gnome-crystal-0.6.5-hooks.patch
URL: 		http://www.nongnu.org/gcrystal/
License: 	GPL
Group: 		Sciences/Chemistry
BuildRoot: 	%{_tmppath}/%{name}-buildroot
BuildRequires:	gcu-devel libglade2.0-devel libgnomeprintui-devel libgnomeui2-devel
BuildRequires:	jpeg-devel gettext pkgconfig png-devel ImageMagick
Requires(post):	scrollkeeper GConf2 shared-mime-info desktop-file-utils
Requires(preun): scrollkeeper GConf2 shared-mime-info desktop-file-utils
Provides:	gcrystal
Obsoletes:	gcrystal

%description
GCrystal is a light, GNOME2-incorporated model visualizer for crystal
structures.

%prep
%setup -q
%patch0

%build
%configure2_5x
perl -p -i -e 's/install-data-local//g' Makefile
%make

%install
%makeinstall_std
rm -fr $RPM_BUILD_ROOT/var/lib/scrollkeeper
%find_lang gnome-crystal

# menu
mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications/
cat << EOF > %buildroot%{_datadir}/applications/mandriva-%{name}.desktop
[Desktop Entry]
Type=Application
Exec=gcrystal
Categories=Science;Chemistry;
Name=GCrystal
Icon=%name
Comment=GNOME crystal structure tool
EOF

#icons
mkdir -p $RPM_BUILD_ROOT/%_liconsdir
cp gcrystal48.png $RPM_BUILD_ROOT/%_liconsdir/%name.png
mkdir -p $RPM_BUILD_ROOT/%_iconsdir
cp gcrystal32.png $RPM_BUILD_ROOT/%_iconsdir/%name.png
mkdir -p $RPM_BUILD_ROOT/%_miconsdir
convert -size 16x16 gcrystal32.png $RPM_BUILD_ROOT/%_miconsdir/%name.png

%clean
rm -rf $RPM_BUILD_ROOT

%post
%if %mdkversion < 200900
%post_install_gconf_schemas sound-juicer
%{update_menus}
%update_scrollkeeper
%endif
update-mime-database %_datadir/mime > /dev/null
update-desktop-database %_datadir/applications > /dev/null

%preun
%preun_uninstall_gconf_schemas sound-juicer
update-mime-database %_datadir/mime > /dev/null
update-desktop-database %_datadir/applications > /dev/null

%if %mdkversion < 200900
%postun
%clean_menus
%clean_scrollkeeper
%endif

%files -f gnome-crystal.lang
%defattr(-,root,root)
%doc AUTHORS ChangeLog COPYING NEWS README
%_bindir/gcrystal
%{_datadir}/applications/mandriva-%name.desktop
%_sysconfdir/gconf/schemas/gcrystal.schemas
%_datadir/gnome-2.0/ui/gcrystal.xml
%_datadir/gnome/help/gnome-crystal
%_datadir/omf/gnome-crystal/gnome-crystal-C.omf
%_libdir/bonobo/servers/*
%_datadir/applications/*
%_datadir/gcrystal
%_datadir/%name
#%_datadir/gnome/ui/%name.xml
#%_datadir/pixmaps/*.png
%{_datadir}/icons/*/*/*/*.png
%_datadir/mime/packages/*
%_miconsdir/%name.png
%_iconsdir/%name.png
%_liconsdir/%name.png

