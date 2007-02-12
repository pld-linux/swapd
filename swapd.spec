Summary:	Dynamic swapping manager for Linux
Summary(pl.UTF-8):   Program zarządzający dynamicznym swapowaniem dla Linuksa
Name:		swapd
Version:	1.0.3
Release:	0.1
License:	GPL
Group:		Daemons
Source0:	http://www.rkeene.org/files/oss/swapd/source/%{name}-%{version}.tar.gz
# Source0-md5:	cb9ec64a5abd4535b95ec59311114ade
Source1:	%{name}.init
URL:		http://www.rkeene.org/oss/swapd/
BuildRequires:	autoconf
BuildRequires:	rpmbuild(macros) >= 1.268
Requires(post,preun):	/sbin/chkconfig
Requires:	rc-scripts
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define	_swapfilesdir	%{_localstatedir}/lib/%{name}

%description
swapd is a dynamic swapping manager for Linux. It provides the system
with as much swap space (virtual memory) as is required at a
particular time by dynamically creating swap files. This is more
convinient than using fixed swap files and/or partitions because they
  (a) are unused most of the time and are just taking up disk space,
  (b) provide a limited amount of virtual memory.

%description -l pl.UTF-8
swapd to program zarządzający dynamicznym swapowaniem dla Linuksa.
Dostarcza systemowi taką objętość swapu (pamięci wirtualnej), jaka
jest w danej chwili potrzebna, poprzez dynamiczne tworzenie plików
swap. Jest to bardziej wygodne niż używanie stałych plików i/lub
partycji swap, ponieważ:
  (a) są one nie używane przez większość czasu i tylko zajmują miejsce,
  (b) dają ograniczoną ilość pamięci wirtualnej.

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
	$RPM_BUILD_ROOT{/etc/rc.d/init.d,%{_swapfilesdir}}

install %{name} $RPM_BUILD_ROOT%{_sbindir}
install %{name}.8 $RPM_BUILD_ROOT%{_mandir}/man8
install %{name}.conf $RPM_BUILD_ROOT%{_sysconfdir}
install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add %{name}
%service %{name} restart "swap daemon"

%preun
if [ "$1" = "0" ]; then
	%service %{name} stop
	/sbin/chkconfig --del %{name}
fi

%files
%defattr(644,root,root,755)
%doc LICENSE README
%attr(755,root,root) %{_sbindir}/*
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}.conf
%attr(754,root,root) /etc/rc.d/init.d/%{name}
%attr(755,root,root) %dir %{_swapfilesdir}
%{_mandir}/man8/*
