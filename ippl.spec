Summary:	IP protocols logger
Summary(es):	Analizador de paquetes IP
Summary(pl):	Program loguj±cy informacje na temat protoko³ów IP
Summary(pt_BR):	Analisador de pacotes IP
Name:		ippl
Version:	1.99.5
Release:	10
License:	GPL
Group:		Networking
Source0:	http://pltplp.net/ippl/archive/dev/%{name}-%{version}.tar.gz
# Source0-md5:	68349a916ed5fa20b43d1712ca70fbbf
Source1:	%{name}d.init
Source2:	%{name}.logrotate
Source3:	%{name}.conf
URL:		http://pltplp.net/ippl/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	libpcap-devel
BuildRequires:	rpmbuild(macros) >= 1.268
Requires(post,preun):	/sbin/chkconfig
Requires:	logrotate
Requires:	psmisc >= 20.1
Requires:	rc-scripts
Obsoletes:	iplog
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
IP protocols logger - logs TCP, UDP and ICMP.

%description -l es
Analizador de paquetes IP.

%description -l pl
Program loguj±cy informacje na temat protoko³ów IP - TCP, UDP oraz
ICMP.

%description -l pt_BR
O IPPL registra pacotes IP enviados à um sistema.

%prep
%setup -q

%build
%{__aclocal}
%{__autoconf}
%configure \
	--enable-cache-debug

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/etc/{logrotate.d,rc.d/init.d},/var/log/{archiv/ippl,ippl}} \
	$RPM_BUILD_ROOT{%{_sbindir},%{_mandir}/man{5,8}}

install source/ippl $RPM_BUILD_ROOT%{_sbindir}

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/ippl
install %{SOURCE2} $RPM_BUILD_ROOT/etc/logrotate.d/ippl
install %{SOURCE3} $RPM_BUILD_ROOT%{_sysconfdir}/ippl.conf

install docs/*.5 $RPM_BUILD_ROOT%{_mandir}/man5
install docs/*.8 $RPM_BUILD_ROOT%{_mandir}/man8

> $RPM_BUILD_ROOT/var/log/ippl/tcp.log
> $RPM_BUILD_ROOT/var/log/ippl/udp.log
> $RPM_BUILD_ROOT/var/log/ippl/icmp.log

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add ippl
%service ippl restart "ippld daemon"

%preun
if [ "$0" = "1" ]; then
	%service ippl sto
	/sbin/chkconfig --del ippl
fi

%files
%defattr(644,root,root,755)
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/logrotate.d/ippl
%attr(754,root,root) /etc/rc.d/init.d/ippl
%attr(755,root,root) %{_sbindir}/ippl
%attr(750,root,root) %dir /var/log/ippl
%attr(750,root,root) %dir /var/log/archiv/ippl
%attr(640,root,root) %ghost /var/log/ippl/*
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/ippl.conf
%{_mandir}/man[58]/*
