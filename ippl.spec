Summary:	IP protocols logger
Summary(pl):	Program loguj±cy informacje na temat protoko³ów IP
Name:		ippl
Version:	1.5.3
Release:	3
Copyright:	GPL
Vendor:		Hugo Haas & Etienne Bernard <ippl@via.ecp.fr>
Group:		Networking
Group(pl):	Sieciowe
Source0:	http://www.via.ecp.fr/~hugo/ippl/archive/dev/%{name}-%{version}.tar.gz
Source1:	ippld.init
Source2:	ippl.logrotate
URL:		http://www.via.ecp.fr/~hugo/ippl/
Prereq:		/sbin/chkconfig
Requires:	rc-scripts
Requires:	logrotate
Buildroot:	/tmp/%{name}-%{version}-root

%define		_sysconfdir /etc

%description
IP protocols logger - logs TCP, UDP and ICMP.

%description -l pl
Program loguj±cy informacje na temat protoko³ów IP - TCP, UDP oraz ICMP.

%prep
%setup -q

%build
%configure \
	--enable-cache-debug

make LDFLAGS="-s"

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/{etc/{logrotate.d,rc.d/init.d},var/log} \
	$RPM_BUILD_ROOT{%{_sbindir},%{_mandir}/man{5,8}}
install Source/ippl $RPM_BUILD_ROOT%{_sbindir}

install ippl.conf $RPM_BUILD_ROOT/etc
install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/ippl
install %{SOURCE2} $RPM_BUILD_ROOT/etc/logrotate.d/ippl

install Docs/*.5  $RPM_BUILD_ROOT%{_mandir}/man5/
install Docs/*.8  $RPM_BUILD_ROOT%{_mandir}/man8/

gzip -9nf $RPM_BUILD_ROOT%{_mandir}/man*/*

touch $RPM_BUILD_ROOT/var/log/ippl.log

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add ippl
if test -r /var/run/ippl.pid; then
	/etc/rc.d/init.d/ippl restart >&2
else
	echo "Run \"/etc/rc.d/init.d/ippl start\" to start ippld daemon."
fi
touch /var/log/ippl.log
chmod 600 /var/log/ippl.log

%preun
if [ "$0" = "1" ]; then
	/sbin/chkconfig --del ippl
	/etc/rc.d/init.d/ippl stop >&2
fi

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/ippl
%attr(600,root,root) %config(noreplace) /etc/ippl.conf
%attr(754,root,root) /etc/rc.d/init.d/ippl
%attr(600,root,root) %config /etc/logrotate.d/ippl
%{_mandir}/man[58]/*
%attr(600,root,root) %ghost /var/log/ippl.log
