Summary:	IP protocols logger
Summary(pl):	Program loguj±cy informacje na temat protoko³ów IP
Name:		ippl
Version:	0.8
Release:	1d
Copyright:	GPL
Group:		Networking
Group(pl):	Sieciowe
Source:		http://master.debian.org/~hugo/ippl/%{name}-%{version}.tar.gz
Buildroot:	/var/tmp/buildroot-%{name}-%{version}

%description
IP protocols logger - logs TCP and ICMP

%description -l pl
Program loguj±cy informacje na temat protoko³ów IP - TCP oraz ICMP

%prep
%setup -q

%build
make TARGETDIR=/usr CFLAGS+="$RPM_OPT_FLAGS"

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/{etc/rc.d/init.d,usr/sbin,var/log}
install -s Source/ippl $RPM_BUILD_ROOT/usr/sbin
install ippl.conf $RPM_BUILD_ROOT/etc

touch $RPM_BUILD_ROOT/var/log/ippl.log

bzip2 -9 CREDITS HISTORY 

cat  << EOF > $RPM_BUILD_ROOT/etc/rc.d/init.d/ippld
#!/bin/bash
#
# chkconfig: 2345 50 50
# description: IP protocols logger - logs TCP and ICMP.
#
# processname: ippl
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
%doc CREDITS.bz2 HISTORY.bz2 

%attr(755,root,root) /usr/sbin/ippl
%attr(600,root,root) /etc/ippl.conf
%attr(700,root,root) %config /etc/rc.d/init.d/ippld
%attr(600,root,root) /var/log/ippl.log

%changelog
* Wed Feb 03 1999 Arkadiusz Mi¶kiewicz <misiek@misiek.eu.org>
  [0.8-1d]
- new upstream release

* Wed Dec 23 1998 Arkadiusz Mi¶kiewicz <misiek@misiek.eu.org>
  [0.6-1d]
- new upstream release

* Thu Oct 02 1998 Arkadiusz Mi¶kiewicz <misiek@misiek.eu.org>
  [0.5-1d]
- initial RPM release
