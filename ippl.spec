Summary:	IP protocols logger
Summary(pl):	Program loguj±cy informacje na temat protoko³ów IP
Name:		ippl
Version:	1.99.5
Release:	4
License:	GPL
Vendor:		Hugo Haas & Etienne Bernard <ippl@via.ecp.fr>
Group:		Networking
Group(de):	Netzwerkwesen
Group(pl):	Sieciowe
Source0:	http://www.via.ecp.fr/~hugo/ippl/archive/dev/%{name}-%{version}.tar.gz
Source1:	%{name}d.init
Source2:	%{name}.logrotate
Source3:	%{name}.conf
URL:		http://www.via.ecp.fr/~hugo/ippl/
Prereq:		/sbin/chkconfig
Prereq:		rc-scripts
Requires:	logrotate
BuildRequires:	flex
BuildRequires:	bison
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir /etc

%description
IP protocols logger - logs TCP, UDP and ICMP.

%description -l pl
Program loguj±cy informacje na temat protoko³ów IP - TCP, UDP oraz
ICMP.

%prep
%setup -q

%build
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

install docs/*.5  $RPM_BUILD_ROOT%{_mandir}/man5/
install docs/*.8  $RPM_BUILD_ROOT%{_mandir}/man8/

touch $RPM_BUILD_ROOT/var/log/ippl/{tcp,udp,icmp}.log

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add ippl
if [ -f /var/lock/subsys/ippl ]; then
	/etc/rc.d/init.d/ippl restart >&2
else
	echo "Run \"/etc/rc.d/init.d/ippl start\" to start ippld daemon."
fi
touch /var/log/ippl/{icmp,tcp,udp}.log
chmod 640 /var/log/ippl/*

%preun
if [ "$0" = "1" ]; then
	if [ -f /var/lock/subsys/ippl ]; then
		/etc/rc.d/init.d/ippl stop >&2
	fi
	/sbin/chkconfig --del ippl
fi

%files
%defattr(644,root,root,755)
%attr(750,root,root) %dir /var/log/ippl
%attr(750,root,root) %dir /var/log/archiv/ippl
%attr(755,root,root) %{_sbindir}/ippl
%attr(754,root,root) /etc/rc.d/init.d/ippl
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/ippl.conf
%attr(640,root,root) %config /etc/logrotate.d/ippl
%attr(640,root,root) %ghost /var/log/ippl/*
%{_mandir}/man[58]/*
