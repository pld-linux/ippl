Summary:	IP protocols logger
Summary(pl):	Program loguj±cy informacje na temat protoko³ów IP
Name:		ippl
Version:	1.0
Release:	1d
Copyright:	GPL
Group:		Networking
Group(pl):	Sieciowe
Source:		http://www.via.ecp.fr/~hugo/ippl/archive/%{name}-%{version}.tar.gz
Patch:		%{name}-egcs.patch
URL:		http://www.via.ecp.fr/~hugo/ippl/
Vendor:		Hugo Haas & Etienne Bernard <ippl@via.ecp.fr>
Buildroot:	/var/tmp/buildroot-%{name}-%{version}

%description
IP protocols logger - logs TCP, UDP and ICMP

%description -l pl
Program loguj±cy informacje na temat protoko³ów IP - TCP, UDP oraz ICMP

%prep
%setup -q
%patch -p1

%build
make TARGETDIR=/usr CFLAGS+="$RPM_OPT_FLAGS"

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/{etc/rc.d/init.d,usr/{sbin,man/man{5,8}},var/log}
install -s Source/ippl $RPM_BUILD_ROOT/usr/sbin
install ippl.conf $RPM_BUILD_ROOT/etc
install Docs/*.5  $RPM_BUILD_ROOT/usr/man/man5/
install Docs/*.8  $RPM_BUILD_ROOT/usr/man/man8/

gzip -9nf         $RPM_BUILD_ROOT/usr/man/man*/*
touch $RPM_BUILD_ROOT/var/log/ippl.log

cat  << EOF > $RPM_BUILD_ROOT/etc/rc.d/init.d/ippld
#!/bin/bash
#
# chkconfig: 2345 50 50
# description: IP protocols logger - logs TCP, UDP and ICMP.
#
# processname: ippl
# pidfile: /var/run/ippl.pid
# config: /etc/ippl.conf
#
# Source function library.
. /etc/rc.d/init.d/functions

# Source networking configuration.
. /etc/sysconfig/network

# Check that networking is up.
[ "\${NETWORKING}" = "no" ] && exit 0
# See how we were called.
case "\$1" in
  start)
        show "Starting IP protocols logger daemon: "
        daemon ippl
        touch /var/lock/subsys/ippl
        ;;
  stop)
        show "Stopping IP protocols logger daemon: "
	busy
        if killall -q ippl; then
	deltext;ok; else deltext; fail
        fi
	rm -f /var/lock/subsys/ippl
        ;;
  status)
        status ippl
        ;;
  restart)
        \$0 stop
	\$0 /etc/rc.d/init.d/ippl start
        ;;
  *)
        echo "Usage: \$0 {start|stop|status|restart}"
        exit 1
esac

exit 0
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add ippld

%preun
if [ $0 = 1]; then
    /sbin/chkconfig --del ippld
fi
%files
%defattr(644,root,root,755)

%attr(755,root,root) /usr/sbin/ippl
%attr(600,root,root) /etc/ippl.conf
%attr(700,root,root) %config /etc/rc.d/init.d/ippld
%attr(644,root,man)  /usr/man/man[58]/*

%changelog
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
