Summary:	IP protocols logger
Summary(pl):	Program loguj�cy informacje na temat protoko��w IP
Name:		ippl
Version:	1.99.5
Release:	7
License:	GPL
Vendor:		Hugo Haas & Etienne Bernard <ippl@via.ecp.fr>
Group:		Networking
Group(de):	Netzwerkwesen
Group(es):	Red
Group(pl):	Sieciowe
Group(pt_BR):	Rede
Source0:	http://www.via.ecp.fr/~hugo/ippl/archive/dev/%{name}-%{version}.tar.gz
Source1:	%{name}d.init
Source2:	%{name}.logrotate
Source3:	%{name}.conf
URL:		http://www.via.ecp.fr/~hugo/ippl/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	bison
BuildRequires:	flex
PreReq:		/sbin/chkconfig
PreReq:		rc-scripts
Requires:	logrotate
Requires:	psmisc >= 20.1
Obsoletes:	iplog
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir	/etc

%description
IP protocols logger - logs TCP, UDP and ICMP.

%description -l pl
Program loguj�cy informacje na temat protoko��w IP - TCP, UDP oraz
ICMP.

%prep
%setup -q

%build
aclocal
autoconf
%configure \
	--enable-cache-debug

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/{etc/{logrotate.d,rc.d/init.d},var/log/{archiv/ippl,ippl}} \
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
