#
# Please submit bugfixes or comments via http://www.trinitydesktop.org/
#

# TDE variables
%define tde_epoch 2
%if "%{?tde_version}" == ""
%define tde_version 14.1.5
%endif
%define tde_pkg kshowmail
%define tde_prefix /opt/trinity
%define tde_bindir %{tde_prefix}/bin
%define tde_datadir %{tde_prefix}/share
%define tde_docdir %{tde_datadir}/doc
%define tde_includedir %{tde_prefix}/include
%define tde_libdir %{tde_prefix}/%{_lib}
%define tde_mandir %{tde_datadir}/man
%define tde_tdeappdir %{tde_datadir}/applications/tde
%define tde_tdedocdir %{tde_docdir}/tde
%define tde_tdeincludedir %{tde_includedir}/tde
%define tde_tdelibdir %{tde_libdir}/trinity

%if 0%{?mdkversion}
%undefine __brp_remove_la_files
%define dont_remove_libtool_files 1
%define _disable_rebuild_configure 1
%endif

# fixes error: Empty %files file …/debugsourcefiles.list
%define _debugsource_template %{nil}

%define tarball_name %{tde_pkg}-trinity
%global toolchain %(readlink /usr/bin/cc)


Name:		trinity-%{tde_pkg}
Epoch:		%{tde_epoch}
Version:	3.3.1
Release:	%{?tde_version}_%{?!preversion:1}%{?preversion:0_%{preversion}}%{?dist}
Summary:	Look messages into your mail server
Group:		Applications/Internet
URL:		http://sourceforge.net/projects/kshowmail/

%if 0%{?suse_version}
License:	GPL-2.0+
%else
License:	GPLv2+
%endif

#Vendor:		Trinity Desktop
#Packager:	Francois Andriot <francois.andriot@free.fr>

Prefix:		%{tde_prefix}

Source0:		https://mirror.ppa.trinitydesktop.org/trinity/releases/R%{tde_version}/main/applications/internet/%{tarball_name}-%{tde_version}%{?preversion:~%{preversion}}.tar.xz

BuildRequires:  cmake make
BuildRequires:	trinity-tdelibs-devel >= %{tde_version}
BuildRequires:	trinity-tdebase-devel >= %{tde_version}
BuildRequires:	desktop-file-utils
BuildRequires:	trinity-tdepim-devel >= %{tde_version}

BuildRequires:	trinity-tde-cmake >= %{tde_version}
%if "%{?toolchain}" != "clang"
BuildRequires:	gcc-c++
%endif
BuildRequires:	pkgconfig
BuildRequires:	fdupes

# SUSE desktop files utility
%if 0%{?suse_version}
BuildRequires:	update-desktop-files
%endif

%if 0%{?opensuse_bs} && 0%{?suse_version}
# for xdg-menu script
BuildRequires:	brp-check-trinity
%endif

# ACL support
BuildRequires:  pkgconfig(libacl)

# IDN support
BuildRequires:	pkgconfig(libidn)

# OPENSSL support
BuildRequires:  pkgconfig(openssl)

BuildRequires:  pkgconfig(xrender)
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(ice)
BuildRequires:  pkgconfig(sm)


%description
Very simply kshowmail is a program that allows you to look in on your mail server,
see what is waiting, decide if it is legitimate, and delete it right off of the server if it is not.
All without dragging any messages into your computer.

##########

%if 0%{?suse_version} && 0%{?opensuse_bs} == 0
%debug_package
%endif

##########

%prep
%autosetup -n %{tarball_name}-%{tde_version}%{?preversion:~%{preversion}}


%build
unset QTDIR QTINC QTLIB
export PATH="%{tde_bindir}:${PATH}"
export PKG_CONFIG_PATH="%{tde_libdir}/pkgconfig"

if ! rpm -E %%cmake|grep -e 'cd build\|cd ${CMAKE_BUILD_DIR:-build}'; then
  %__mkdir_p build
  cd build
fi

%cmake \
  -DCMAKE_BUILD_TYPE="RelWithDebInfo" \
  -DCMAKE_C_FLAGS="${RPM_OPT_FLAGS}" \
  -DCMAKE_CXX_FLAGS="${RPM_OPT_FLAGS}" \
  -DCMAKE_SKIP_RPATH=OFF \
  -DCMAKE_SKIP_INSTALL_RPATH=OFF \
  -DCMAKE_INSTALL_RPATH="%{tde_libdir}" \
  -DCMAKE_VERBOSE_MAKEFILE=ON \
  -DWITH_GCC_VISIBILITY=OFF \
  \
  -DCMAKE_INCLUDE_PATH="%{tde_tdeincludedir}" \
  -DCMAKE_INSTALL_PREFIX="%{tde_prefix}" \
  -DSHARE_INSTALL_PREFIX="%{tde_datadir}" \
  -DLIB_INSTALL_DIR="%{tde_libdir}" \
  \
  -DWITH_ALL_OPTIONS=ON \
  -DWITH_GCC_VISIBILITY=ON \
  \
  -DBUILD_ALL=ON \
  -DBUILD_DOC=ON \
  -DBUILD_TRANSLATIONS=ON \
  ..

%__make %{?_smp_mflags} || %__make


%install
%__make install DESTDIR=$RPM_BUILD_ROOT -C build

%find_lang %{tde_pkg}

# Install missing icons
install -D -m 644 "pics/cr16-app-kshowmail.png" "$RPM_BUILD_ROOT%{tde_datadir}/icons/hicolor/16x16/apps/kshowmail.png"
install -D -m 644 "pics/kshowmail.png"          "$RPM_BUILD_ROOT%{tde_datadir}/icons/hicolor/48x48/apps/kshowmail.png"

# Updates applications categories for openSUSE
%if 0%{?suse_version}
%suse_update_desktop_file kshowmail Network Email
%endif


%files -f %{tde_pkg}.lang
%defattr(-,root,root,-)
%doc AUTHORS COPYING README.md ChangeLog
%{tde_bindir}/kshowmail
%{tde_tdelibdir}/kcm_kshowmailconfigaccounts.la
%{tde_tdelibdir}/kcm_kshowmailconfigaccounts.so
%{tde_tdelibdir}/kcm_kshowmailconfigactions.la
%{tde_tdelibdir}/kcm_kshowmailconfigactions.so
%{tde_tdelibdir}/kcm_kshowmailconfigdisplay.la
%{tde_tdelibdir}/kcm_kshowmailconfigdisplay.so
%{tde_tdelibdir}/kcm_kshowmailconfigfilter.la
%{tde_tdelibdir}/kcm_kshowmailconfigfilter.so
%{tde_tdelibdir}/kcm_kshowmailconfiggeneral.la
%{tde_tdelibdir}/kcm_kshowmailconfiggeneral.so
%{tde_tdelibdir}/kcm_kshowmailconfiglog.la
%{tde_tdelibdir}/kcm_kshowmailconfiglog.so
%{tde_tdelibdir}/kcm_kshowmailconfigspamcheck.la
%{tde_tdelibdir}/kcm_kshowmailconfigspamcheck.so
%{tde_tdeappdir}/kshowmail.desktop
%{tde_datadir}/apps/kshowmail/
%{tde_datadir}/icons/crystalsvg/16x16/apps/kshowmail.png
%{tde_datadir}/icons/hicolor/*/apps/kshowmail.png
%{tde_datadir}/services/kshowmailconfigaccounts.desktop
%{tde_datadir}/services/kshowmailconfigactions.desktop
%{tde_datadir}/services/kshowmailconfigdisplay.desktop
%{tde_datadir}/services/kshowmailconfigfilter.desktop
%{tde_datadir}/services/kshowmailconfiggeneral.desktop
%{tde_datadir}/services/kshowmailconfiglog.desktop
%{tde_datadir}/services/kshowmailconfigspamcheck.desktop
%lang(cs) %{tde_tdedocdir}/HTML/cs/kshowmail/
%lang(de) %{tde_tdedocdir}/HTML/de/kshowmail/
%lang(en) %{tde_tdedocdir}/HTML/en/kshowmail/
%lang(es) %{tde_tdedocdir}/HTML/es/kshowmail/
%lang(fr) %{tde_tdedocdir}/HTML/fr/kshowmail/
%lang(hu) %{tde_tdedocdir}/HTML/hu/kshowmail/
%lang(it) %{tde_tdedocdir}/HTML/it/kshowmail/
%lang(ru) %{tde_tdedocdir}/HTML/ru/kshowmail/
%lang(sv) %{tde_tdedocdir}/HTML/sv/kshowmail/
%{tde_mandir}/man1/kshowmail.*

