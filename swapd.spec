Summary:	Dynamic swapping manager for Linux
Summary(pl):	Program zarz±dzaj±cy dynamicznym swapowaniem dla Linuksa
Name:		swapd
Version:	0.2
Release:	4
License:	GPL v2+
Group:		Daemons
Source0:	ftp://ftp.linux.hr/pub/swapd/%{name}-%{version}.tar.gz
# Source0-md5:	5ae232ee69130426b595ba90c81eca4e
Source1:	%{name}.init
URL:		http://cvs.linux.hr/swapd/
Patch0:		%{name}-gcc33.patch
Patch1:		%{name}-confdir.patch
BuildRequires:	autoconf
PreReq:		rc-scripts
Requires(post,preun):	/sbin/chkconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define _swapfilesdir   %{_localstatedir}/lib/%{name}

%description
swapd is a dynamic swapping manager for Linux. It provides the system
with as much swap space (virtual memory) as is required at a
particular time by dynamically creating swap files. This is more
convinient than using fixed swap files and/or partitions because they
(a) are unused most of the time and are just taking up disk space; and
(b) provide a limited amount of virtual memory.

%description -l pl
swapd to program zarz±dzaj±cy dynamicznym swapowaniem dla Linuksa.
Dostarcza systemowi tak± objêto¶æ swapu (pamiêci wirtualnej), jaka
jest w danej chwili potrzebna, poprzez dynamiczne tworzenie plików
swap. Jest to bardziej wygodne ni¿ u¿ywanie sta³ych plików i/lub
partycji swap, poniewa¿ (a) s± one nie u¿ywane przez wiêkszo¶æ czasu i
tylko zajmuj± miejsce; oraz (b) daj± ograniczon± ilo¶æ pamiêci
wirtualnej.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
%{__autoconf}
%configure

%{__make} \
	CFLAGS="%{rpmcflags} -Wall -I."

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT{%{_sbindir},%{_mandir}/man8,%{_sysconfdir}/%{name}}
install -d $RPM_BUILD_ROOT{%{_sysconfdir}/rc.d/init.d,%{_swapfilesdir}}

install swapd $RPM_BUILD_ROOT%{_sbindir}
gzip -dc swapd.8.gz | sed -e "s@/usr/local/etc@%{_sysconfdir}@" > \
	$RPM_BUILD_ROOT%{_mandir}/man8/%{name}.8
cat %{name}.conf \
	|sed -e "s@^swapdir[ tab]\+/swap@swapdir %{_swapfilesdir}@">%{name}.conf2
install %{name}.conf2 $RPM_BUILD_ROOT%{_sysconfdir}/%{name}.conf
install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add %{name}
if [ -f /var/lock/subsys/swapd ]; then
	/etc/rc.d/init.d/%{name} restart 1>&2
else
	echo "Run \"/etc/rc.d/init.d/%{name} start\" to start swap daemon."
fi

%preun
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/swapd ]; then
		/etc/rc.d/init.d/%{name} stop 1>&2
	fi
	/sbin/chkconfig --del %{name}
fi

%files
%defattr(644,root,root,755)
# INSTALL may be useful (contains configuration instructions)
%doc CHANGELOG INSTALL README
%attr(755,root,root) %{_sbindir}/*
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/%{name}.conf
%{_mandir}/man8/*
%attr(754,root,root) /etc/rc.d/init.d/%{name}
%attr(755,root,root) %dir %{_swapfilesdir}
