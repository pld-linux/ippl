Summary:	IP protocols logger
Summary(es):	Analizador de paquetes IP
Summary(pl):	Program loguj±cy informacje na temat protoko³ów IP
Summary(pt_BR):	Analisador de pacotes IP
Name:		ippl
Version:	1.99.5
Release:	9
License:	GPL
Vendor:		Hugo Haas & Etienne Bernard <ippl@via.ecp.fr>
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
PreReq:		rc-scripts
Requires(post,preun):	/sbin/chkconfig
Requires:	logrotate
Requires:	psmisc >= 20.1
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
if [ -f /var/lock/subsys/ippl ]; then
	/etc/rc.d/init.d/ippl restart >&2
else
	echo "Run \"/etc/rc.d/init.d/ippl start\" to start ippld daemon."
fi

%preun
if [ "$0" = "1" ]; then
	if [ -f /var/lock/subsys/ippl ]; then
		/etc/rc.d/init.d/ippl stop >&2
	fi
	/sbin/chkconfig --del ippl
fi

%files
%defattr(644,root,root,755)
%attr(640,root,root) /etc/logrotate.d/ippl
%attr(754,root,root) /etc/rc.d/init.d/ippl
%attr(755,root,root) %{_sbindir}/ippl
%attr(750,root,root) %dir /var/log/ippl
%attr(750,root,root) %dir /var/log/archiv/ippl
%attr(640,root,root) %ghost /var/log/ippl/*
%attr(640,root,root) %config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/ippl.conf
%{_mandir}/man[58]/*
