Summary:	IP protocols logger
Summary(pl):	Program loguj±cy informacje na temat protoko³ów IP
Name:		ippl
Version:	1.4.6
Release:	1
Copyright:	GPL
Vendor:		Hugo Haas & Etienne Bernard <ippl@via.ecp.fr>
Group:		Networking
Group(pl):	Sieciowe
Source0:	http://www.via.ecp.fr/~hugo/ippl/archive/%{name}-%{version}.tar.gz
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
LDFLAGS="-s"; export LDFLAGS
%configure \
	--enable-cache-debug
make

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/{etc/{logrotate.d,rc.d/init.d},usr/{sbin,man/man{5,8}},var/log}
install Source/ippl $RPM_BUILD_ROOT%{_sbindir}

install ippl.conf $RPM_BUILD_ROOT/etc
install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/ippl
install %{SOURCE2} $RPM_BUILD_ROOT/etc/logrotate.d/ippl

install Docs/*.5  $RPM_BUILD_ROOT%{_mandir}/man5/
install Docs/*.8  $RPM_BUILD_ROOT%{_mandir}/man8/

gzip -9nf         $RPM_BUILD_ROOT%{_mandir}/man*/*
touch $RPM_BUILD_ROOT/var/log/ippl.log

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add ippl
if test -r /var/run/ippl.pid; then
	/etc/rc.d/init.d/ippl stop >&2
	/etc/rc.d/init.d/ippl start >&2
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
%attr(755,root,root) %{_sbindir}/ippl
%attr(600,root,root) %config(noreplace) /etc/ippl.conf
%attr(754,root,root) /etc/rc.d/init.d/ippl
%attr(600,root,root) %config /etc/logrotate.d/ippl
%attr(644,root,root) %{_mandir}/man[58]/*
%ghost /var/log/ippl.log

%changelog
* Mon Apr 19 1999 Tomasz K³oczko <kloczek@rudy.mif.pg.gda.pl>
  [1.4.5-1]
- recompiles on new rpm.

* Wed Mar  3 1999 Tomasz K³oczko <kloczek@rudy.mif.pg.gda.pl>
  [1.2-1]
- rc script to separated Source,
- added logrotate config file (added also "Requires: logrotate") - for
  configurations with uncommented logging into file,
- added %config(noreplace) to /etc/ippl.conf,
- added "Requires: rc-scripts",
- LDFLAGS="-s" to make parameters instead stripping on install (faster),
- added "Prereq: /sbin/chkconfig",
- added /var/log/ippl.log as %ghost,
- removed %config from /etc/rc.d/init.d/ippld script,
- changed permission on /etc/rc.d/init.d/ippld to 754,
- %post, %postun scripts rewrited to allow restart automatically service on
  upgrade and stopping on remove package,
- added handling reload parameter to rc scriptc,
- removed man group from man pages.

* Tue Mar 02 1999 Arkadiusz Mi¶kiewicz <misiek@misiek.eu.org>
- new upstream release

* Sat Feb 20 1999 Arkadiusz Mi¶kiewicz <misiek@misiek.eu.org>
  [1.0-1d]
- new upstream release

* Wed Feb 03 1999 Arkadiusz Mi¶kiewicz <misiek@misiek.eu.org>
  [0.8-1d]
- new upstream release

* Wed Dec 23 1998 Arkadiusz Mi¶kiewicz <misiek@misiek.eu.org>
  [0.6-1d]
- new upstream release

* Thu Oct 02 1998 Arkadiusz Mi¶kiewicz <misiek@misiek.eu.org>
  [0.5-1d]
- initial RPM release
