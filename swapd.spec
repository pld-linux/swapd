Summary:	Dynamic swapping manager for Linux
Summary(pl):	Program zarz±dzaj±cy dynamicznym swapowaniem dla Linuksa
Name:		swapd
Version:	1.0.1
Release:	0.1
License:	GPL
Group:		Daemons
Source0:	http://www.rkeene.org/files/oss/swapd/source/%{name}-%{version}.tar.gz
# Source0-md5:	b53414b5317706ebc7b3b514342c6c43
Source1:	%{name}.init
URL:		http://www.rkeene.org/oss/swapd/
BuildRequires:	autoconf
PreReq:		rc-scripts
Requires(post,preun):	/sbin/chkconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define	_swapfilesdir	%{_localstatedir}/lib/%{name}

%description
swapd is a dynamic swapping manager for Linux. It provides the system
with as much swap space (virtual memory) as is required at a
particular time by dynamically creating swap files. This is more
convinient than using fixed swap files and/or partitions because they
  (a) are unused most of the time and are just taking up disk space,
  (b) provide a limited amount of virtual memory.

%description -l pl
swapd to program zarz±dzaj±cy dynamicznym swapowaniem dla Linuksa.
Dostarcza systemowi tak± objêto¶æ swapu (pamiêci wirtualnej), jaka
jest w danej chwili potrzebna, poprzez dynamiczne tworzenie plików
swap. Jest to bardziej wygodne ni¿ u¿ywanie sta³ych plików i/lub
partycji swap, poniewa¿:
  (a) s± one nie u¿ywane przez wiêkszo¶æ czasu i tylko zajmuj± miejsce,
  (b) daj± ograniczon± ilo¶æ pamiêci wirtualnej.

%prep
%setup -q

%build
%{__autoconf}
%configure
%{__make} \
	CFLAGS="%{rpmcflags} -Wall -I."

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sbindir},%{_mandir}/man8,%{_sysconfdir}/%{name}} \
	$RPM_BUILD_ROOT{%{_sysconfdir}/rc.d/init.d,%{_swapfilesdir}}

install %{name} $RPM_BUILD_ROOT%{_sbindir}
install %{name}.8 $RPM_BUILD_ROOT%{_mandir}/man8/
install %{name}.conf $RPM_BUILD_ROOT%{_sysconfdir}/
install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add %{name}
if [ -f /var/lock/subsys/%{name} ]; then
	/etc/rc.d/init.d/%{name} restart 1>&2
else
	echo "Run \"/etc/rc.d/init.d/%{name} start\" to start swap daemon."
fi

%preun
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/%{name} ]; then
		/etc/rc.d/init.d/%{name} stop 1>&2
	fi
	/sbin/chkconfig --del %{name}
fi

%files
%defattr(644,root,root,755)
%doc LICENSE README
%attr(755,root,root) %{_sbindir}/*
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/%{name}.conf
%attr(754,root,root) /etc/rc.d/init.d/%{name}
%attr(755,root,root) %dir %{_swapfilesdir}
%{_mandir}/man8/*
