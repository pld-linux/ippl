Summary:	IP protocols logger
Summary(es.UTF-8):	Analizador de paquetes IP
Summary(pl.UTF-8):	Program logujący informacje na temat protokołów IP
Summary(pt_BR.UTF-8):	Analisador de pacotes IP
Name:		ippl
Version:	1.99.5
Release:	11
License:	GPL
Group:		Networking
Source0:	http://pltplp.net/ippl/archive/dev/%{name}-%{version}.tar.gz
# Source0-md5:	68349a916ed5fa20b43d1712ca70fbbf
Source1:	%{name}d.init
Source2:	%{name}.logrotate
Source3:	%{name}.conf
Patch0:		%{name}-format-security.patch
URL:		http://pltplp.net/ippl/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	libpcap-devel
BuildRequires:	rpmbuild(macros) >= 1.268
Requires(post,preun):	/sbin/chkconfig
Requires:	logrotate >= 3.7-4
Requires:	psmisc >= 20.1
Requires:	rc-scripts
Obsoletes:	iplog
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
IP protocols logger - logs TCP, UDP and ICMP.

%description -l es.UTF-8
Analizador de paquetes IP.

%description -l pl.UTF-8
Program logujący informacje na temat protokołów IP - TCP, UDP oraz
ICMP.

%description -l pt_BR.UTF-8
O IPPL registra pacotes IP enviados à um sistema.

%prep
%setup -q
%patch0 -p1

%build
%{__aclocal}
%{__autoconf}
%configure \
	--enable-cache-debug

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/etc/{logrotate.d,rc.d/init.d},/var/log/{archive/ippl,ippl}} \
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
%attr(750,root,root) %dir /var/log/archive/ippl
%attr(640,root,root) %ghost /var/log/ippl/*
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/ippl.conf
%{_mandir}/man[58]/*
