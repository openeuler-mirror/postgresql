%global _default_patch_flags --no-backup-if-mismatch
%global __provides_exclude_from %{_libdir}/pgsql
%global macrosdir %(d=%{_rpmconfigdir}/macros.d; [ -d $d ] || d=%{_sysconfdir}/rpm; echo $d)

Name:          postgresql
Version:       10.5
Release:       11
Summary:       PostgreSQL client programs
License:       PostgreSQL
URL:           http://www.postgresql.org/
Source0:       https://ftp.postgresql.org/pub/source/v%{version}/postgresql-%{version}.tar.bz2
Source1:       https://ftp.postgresql.org/pub/source/v9.6.10/postgresql-9.6.10.tar.bz2
Source2:       https://github.com/devexp-db/postgresql-setup/releases/download/v8.2/postgresql-setup-8.2.tar.gz
Source3:       https://ftp.postgresql.org/pub/source/v%{version}/postgresql-%{version}.tar.bz2.sha256
Source4:       https://ftp.postgresql.org/pub/source/v9.6.10/postgresql-9.6.10.tar.bz2.sha256
Source5:       postgresql.tmpfiles.d
Source6:       postgresql-bashprofile

Patch0000:     0000-postgresql-var-run-socket.patch
Patch0001:     0000-rpm-pgsql.patch

Patch6000:     6000-CVE-2019-10164-1.patch
Patch6001:     6001-CVE-2019-10164-2.patch
Patch6002:     CVE-2019-10208.patch
Patch6003:     CVE-2018-16850.patch
Patch6004:     CVE-2019-10130.patch

BuildRequires: gcc perl(ExtUtils::MakeMaker) glibc-devel bison flex gawk perl(ExtUtils::Embed)
BuildRequires: perl-devel perl-generators readline-devel zlib-devel systemd systemd-devel
BuildRequires: util-linux m4 elinks docbook-utils help2man python2-devel
BuildRequires: python3-devel tcl-devel openssl-devel krb5-devel openldap-devel gettext >= 0.10.35
BuildRequires: uuid-devel libxml2-devel libxslt-devel pam-devel systemtap-sdt-devel libselinux-devel
Requires:      %{name}-libs = %{version}-%{release}

%package libs
Summary: The shared libraries required for any PostgreSQL clients
Requires(post): glibc
Requires(postun): glibc

%description libs
The postgresql-libs package provides the essential shared libraries for any
PostgreSQL client program or interface. You will need to install this package
to use any other PostgreSQL package or any clients that need to connect to a
PostgreSQL server.

%description
PostgreSQL is an advanced Object-Relational database management system (DBMS)
that supports almost all SQL constructs (including transactions, subselects
and user-defined types and functions). The postgresql package includes the client
programs and libraries that you'll need to access a PostgreSQL DBMS server.

%package server
Summary:       A package helps to create and run a PostgreSQL server
Requires:      %{name} = %{version}-%{release} %{name}-libs = %{version}-%{release} systemd
Requires(pre): shadow
%{?systemd_requires}
Provides:      %{name}-server(:MODULE_COMPAT_10)
Provides:       bundled(postgresql-setup) = 8.2

%description server
The postgresql-server package includes the programs needed to create and run
a PostgreSQL server, which will in turn allow you to create and maintain
PostgreSQL databases.

%package help
Summary:        Help documentation for PostgreSQL
Requires:       %{name} = %{version}-%{release}
Provides:       %{name}-doc = %{version}-%{release} %{name}-docs = %{version}-%{release}
Obsoletes:      %{name}-docs < %{version}-%{release}

%description help
Man pages and other related help documents for PostgreSQL.

%package contrib
Summary:        Include the contrib tree distributed with PostgreSQL tarball
Requires:       %{name} = %{version}-%{release} %{name}-libs = %{version}-%{release}

%description contrib
The postgresql-contrib package includes the contrib tree distributed
with the PostgreSQL tarball. Selected contrib modules are prebuilt.

%package devel
Summary:        Development files for postgresql
Requires:       %{name}-libs = %{version}-%{release} %{name}-server = %{version}-%{release}
Provides:       libpq-devel = %{version}-%{release} libecpg-devel = %{version}-%{release}
Provides:       postgresql-server-devel = %{version}-%{release}

%package test-rpm-macros
Summary:        Convenience RPM macros for build-time testing against PostgreSQL server
Requires:       %{name}-server = %{version}-%{release}

%description test-rpm-macros
This package is meant to be added as BuildRequires: dependency of other packages
that want to run build-time testsuite against running PostgreSQL server.


%package static
Summary:        Statically linked PostgreSQL libraries
Requires:       %{name}-devel = %{version}-%{release}

%description static
Statically linked PostgreSQL libraries that do not have dynamically linked
counterparts.

%description devel
This package provides Libraries and header files for postgresql.

%package upgrade
Summary:       Support needed for upgrading a PostgreSQL database
Requires:      %{name}-server = %{version}-%{release} %{name}-libs = %{version}-%{release}
Provides:      bundled(postgresql-libs) = 9.6.10

%description upgrade
This package provides the pg_upgrade utility and supporting files needed
for upgrading a PostgreSQL database from the previous major version of
PostgreSQL.

%package upgrade-devel
Summary:       Support for build of extensions required for upgrade process
Requires:      %{name}-upgrade = %{version}-%{release}

%description upgrade-devel
This package provides the development files needed to compile C or C++
applications which are necessary in upgrade process.

%package plperl
Summary:       The Perl procedural language for PostgreSQL
Requires:      %{name}-server = %{version}-%{release}
Requires:      perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
BuildRequires: perl(Data::Dumper)

%description plperl
This package contains the PL/Perl procedural language, which is an extension
to the PostgreSQL database server.Install this if you want to write database
functions in Perl.

%package plpython
Summary:       The Python2 procedural language for PostgreSQL
Requires:      %{name}-server = %{version}-%{release}
Provides:      %{name}-plpython2 = %{version}-%{release}

%description plpython
This package contains the PL/Python procedural language, which is an extension
to the PostgreSQL database server.It is used when you want to write database
functions in Python2.


%package plpython3
Summary:       The Python3 procedural language for PostgreSQL
Requires:      %{name}-server = %{version}-%{release}

%description plpython3
This package contains the PL/Python procedural language, which is an extension
to the PostgreSQL database server.It is used when you want to write database
functions in Python3.


%package pltcl
Summary:       The Tcl procedural language for PostgreSQL
Requires:      %{name}-server = %{version}-%{release}

%description pltcl
This package provides the PL/Tcl procedural language, which is an extension
to the PostgreSQL database server.

%package test
Summary:  The test suite distributed with PostgreSQL
Requires: %{name}-server = %{version}-%{release} %{name}-devel = %{version}-%{release}

%description test
The postgresql-test package contains files needed for various tests for the
PostgreSQL database management system, including regression tests and benchmarks.

%prep
(
  cd "$(dirname "%{SOURCE0}")"
  sha256sum -c %{SOURCE3}
  sha256sum -c %{SOURCE4}
)
%setup -q -a 2
%patch0000 -p1
%patch0001 -p1
%patch6000 -p1
%patch6001 -p1
%patch6002 -p1
%patch6003 -p1
%patch6004 -p1

tar xfj %{SOURCE1}
find . -type f -name .gitignore | xargs rm

%build
if [ x"`id -u`" = x0 ]; then
        echo "postgresql's regression tests fail if run as root."
        echo "If you really need to build the RPM as root, use"
        echo "--define='runselftest 0' to skip the regression tests."
        exit 1
fi

pushd postgresql-setup-8.2

%configure pgdocdir=%{_pkgdocdir} PGVERSION=%{version} pgsetup_cv_os_family=redhat \
    PGMAJORVERSION=10  NAME_DEFAULT_PREV_SERVICE=postgresql

%make_build
popd

CFLAGS="${CFLAGS:-%optflags}"
CFLAGS=`echo $CFLAGS|xargs -n 1|grep -v ffast-math|xargs -n 100`
export CFLAGS

common_configure_options='
	--disable-rpath --with-perl --with-tcl --with-tclconfig=%_libdir
	--with-ldap --with-openssl --with-pam --with-gssapi --with-ossp-uuid
	--with-libxml --with-libxslt --enable-nls --enable-dtrace
	--with-selinux --with-system-tzdata=%_datadir/zoneinfo
	--datadir=%_datadir/pgsql --with-systemd
'

export PYTHON=/usr/bin/python3

%configure $common_configure_options --with-python

%make_build -C src/pl/plpython all
cp -a src/pl/plpython src/pl/plpython3

cp src/Makefile.global src/Makefile.global.python3

make distclean

PYTHON=/usr/bin/python2

%configure $common_configure_options --with-python

unset PYTHON

%make_build world

sed "s|C=\`pwd\`;|C=%{_libdir}/pgsql/tutorial;|" < src/tutorial/Makefile > src/tutorial/GNUmakefile
%make_build -C src/tutorial NO_PGXS=1 all

rm -f src/tutorial/GNUmakefile src/tutorial/*.o

run_testsuite()
{
	make -k -C "$1" MAX_CONNECTIONS=5 check && return 0 || test_failure=1
	(
		set +x
		echo "=== trying to find all regression.diffs files in build directory ==="
		find "$1" -name 'regression.diffs' | \
		while read line; do
			echo "=== make failure: $line ==="
			cat "$line"
		done
	)
}

test_failure=0

run_testsuite "src/test/regress"
make clean -C "src/test/regress"
run_testsuite "src/pl"
mv src/Makefile.global src/Makefile.global.save
cp src/Makefile.global.python3 src/Makefile.global
touch -r src/Makefile.global.save src/Makefile.global
mv src/pl/plpython src/pl/plpython2
mv src/pl/plpython3 src/pl/plpython

run_testsuite "src/pl/plpython"

mv src/pl/plpython src/pl/plpython3
mv src/pl/plpython2 src/pl/plpython
mv -f src/Makefile.global.save src/Makefile.global
run_testsuite "contrib"

test "$test_failure" -eq 0
make all -C src/test/regress

pushd postgresql-9.6.10

upgrade_configure ()
{
        PYTHON="${PYTHON-/usr/bin/python2}" \
        CFLAGS="$CFLAGS -fno-aggressive-loop-optimizations" ./configure \
                --build=%{_build} --host=%{_host} --prefix=%{_libdir}/pgsql/postgresql-9.6 \
                --disable-rpath --with-perl --with-tcl --with-tclconfig=%_libdir \
                --with-system-tzdata=/usr/share/zoneinfo "$@"
}

export PYTHON=/usr/bin/python3
upgrade_configure --with-python
%make_build -C src/pl/plpython all
cp src/pl/plpython/plpython3.so ./
unset PYTHON
make distclean

upgrade_configure --with-python
%make_build all
%make_build -C contrib all
popd


%install
pushd postgresql-setup-8.2
%make_install
popd

mv $RPM_BUILD_ROOT/%{_pkgdocdir}/README.rpm-dist ./

cat > $RPM_BUILD_ROOT%{_sysconfdir}/postgresql-setup/upgrade/postgresql.conf <<EOF
id              postgresql
major           9.6
data_default    %{_localstatedir}/pgsql/data
package         postgresql-upgrade
engine          %{_libdir}/pgsql/postgresql-9.6/bin
description     "Upgrade data from system PostgreSQL version (PostgreSQL 9.6)"
redhat_sockets_hack no
EOF

make DESTDIR=$RPM_BUILD_ROOT install-world

mv src/Makefile.global src/Makefile.global.save
cp src/Makefile.global.python3 src/Makefile.global
touch -r src/Makefile.global.save src/Makefile.global
pushd src/pl/plpython3
%make_install
popd
mv -f src/Makefile.global.save src/Makefile.global

install -d -m 755 $RPM_BUILD_ROOT%{_datadir}/pgsql/contrib
install -d -m 755 $RPM_BUILD_ROOT%{_datadir}/pgsql/extension

install -d -m 755 $RPM_BUILD_ROOT%{_libdir}/pgsql/tutorial
cp -p src/tutorial/* $RPM_BUILD_ROOT%{_libdir}/pgsql/tutorial

install -d  $RPM_BUILD_ROOT%{_tmpfilesdir}
install -d -m 755 $RPM_BUILD_ROOT%{?_localstatedir}/run/postgresql
install -m 0644 %{SOURCE5} $RPM_BUILD_ROOT%{_tmpfilesdir}/postgresql.conf

install -d -m 700 $RPM_BUILD_ROOT%{?_localstatedir}/lib/pgsql/data
install -d -m 700 $RPM_BUILD_ROOT%{?_localstatedir}/lib/pgsql/backups
install -m 0644 %{SOURCE6} $RPM_BUILD_ROOT%{?_localstatedir}/lib/pgsql/.bash_profile

pushd postgresql-9.6.10
%make_install
%make_install -C contrib
install -m 755 plpython3.so $RPM_BUILD_ROOT/%_libdir/pgsql/postgresql-9.6/lib
popd

pushd $RPM_BUILD_ROOT%{_libdir}/pgsql/postgresql-9.6
rm bin/{clusterdb,createdb,createlang,createuser,dropdb,droplang,dropuser,ecpg}
rm bin/{initdb,pg_basebackup,pg_dump,pg_dumpall,pg_restore,pgbench,psql,reindexdb,vacuumdb}
rm -rf share/{doc,man,tsearch_data}
rm lib/*.a
rm lib/libpq.so*
rm lib/lib{ecpg,ecpg_compat,pgtypes}.so*
rm share/{*.bki,*description,*.sample,*.sql,*.txt}
rm share/extension/{*.sql,*.control}
popd
cat <<EOF > $RPM_BUILD_ROOT%macrosdir/macros.%name-upgrade
%%postgresql_upgrade_prefix %{_libdir}/pgsql/postgresql-9.6
EOF


install -d $RPM_BUILD_ROOT%{_libdir}/pgsql/test
cp -a src/test/regress $RPM_BUILD_ROOT%{_libdir}/pgsql/test
ln -sf ../../pgxs/src/test/regress/pg_regress $RPM_BUILD_ROOT%{_libdir}/pgsql/test/regress/pg_regress
pushd  $RPM_BUILD_ROOT%{_libdir}/pgsql/test/regress
rm -f GNUmakefile Makefile *.o
chmod 0755 pg_regress regress.so
popd

rm -rf doc/html
mv $RPM_BUILD_ROOT%{_docdir}/pgsql/html doc

find_lang_bins ()
{
        lstfile=$1 ; shift
        cp /dev/null "$lstfile"
        for binary; do
                %find_lang "$binary"-10
                cat "$binary"-10.lang >>"$lstfile"
        done
}

find_lang_bins devel.lst ecpg pg_config
find_lang_bins libs.lst ecpglib6 libpq5
find_lang_bins server.lst initdb pg_basebackup pg_controldata pg_ctl pg_resetwal pg_rewind plpgsql postgres
find_lang_bins contrib.lst pg_archivecleanup pg_test_fsync pg_test_timing pg_waldump
find_lang_bins main.lst pg_dump pg_upgrade pgscripts psql
find_lang_bins plperl.lst plperl
find_lang_bins plpython.lst plpython
find_lang_bins plpython3.lst plpython
find_lang_bins pltcl.lst pltcl


%post libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig


%pre server
/usr/sbin/groupadd -g 26 -o -r postgres >/dev/null 2>&1 || :
/usr/sbin/useradd -M -N -g postgres -o -r -d /var/lib/pgsql -s /bin/bash \
        -c "PostgreSQL Server" -u 26 postgres >/dev/null 2>&1 || :

%post server
%systemd_post postgresql.service


%preun server
%systemd_preun postgresql.service


%postun server
%systemd_postun_with_restart postgresql.service


%check
make -C postgresql-setup-8.2 check


%clean


%files -f main.lst
%doc COPYRIGHT README
%{_bindir}/{clusterdb,createdb,createuser,dropdb,dropuser,pg_dump,pg_dumpall}
%{_bindir}/{pg_isready,pg_restore,pg_upgrade,psql,reindexdb,vacuumdb}
%exclude %{_docdir}/pgsql
%exclude %{_libdir}/pgsql/test/regress/pg_regress
%exclude %{_libdir}/lib{ecpg,pq,ecpg_compat,pgfeutils,pgtypes}.a

%files libs -f libs.lst
%doc COPYRIGHT
%dir %{_libdir}/pgsql
%{_libdir}/libecpg.so.*
%{_libdir}/libecpg_compat.so.*
%{_libdir}/libpgtypes.so.*
%{_libdir}/libpq.so.*


%files help
%doc doc/html doc/KNOWN_BUGS doc/MISSING_FEATURES doc/TODO
%doc HISTORY doc/bug.template README.rpm-dist
%{_libdir}/pgsql/tutorial/
%{_mandir}/man1/*
%{_mandir}/man3/*
%{_mandir}/man7/*


%files contrib -f contrib.lst
%doc contrib/spi/*.example
%{_bindir}/{oid2name,pg_archivecleanup,pg_standby,pg_test_fsync,pg_test_timing,pg_waldump,pgbench,vacuumlo}
%{_datadir}/pgsql/extension/{adminpack*,amcheck*,autoinc*,bloom*,btree_gin*,btree_gist*,chkpass*}
%{_datadir}/pgsql/extension/{citext*,cube*,dblink*,dict_int*,dict_xsyn*,earthdistance*,file_fdw*,fuzzystrmatch*}
%{_datadir}/pgsql/extension/{hstore*,insert_username*,intagg*,intarray*,isn*,lo*,ltree*,moddatetime*}
%{_datadir}/pgsql/extension/{pageinspect*,pg_buffercache*,pg_freespacemap*,pg_prewarm*,pg_stat_statements*}
%{_datadir}/pgsql/extension/{pg_trgm*,pg_visibility*,pgcrypto*,pgrowlocks*,pgstattuple*,postgres_fdw*}
%{_datadir}/pgsql/extension/{refint*,seg*,tablefunc*,tcn*,timetravel*,tsm_system_rows*,tsm_system_time*}
%{_datadir}/pgsql/extension/{unaccent*,sslinfo*,uuid-ossp*,xml2*}
%{_datadir}/pgsql/contrib/sepgsql.sql
%{_libdir}/pgsql/{_int,adminpack,amcheck,auth_delay,auto_explain,autoinc,bloom,btree_gin,btree_gist}.so
%{_libdir}/pgsql/{chkpass,citext,cube,dblink,dict_int,dict_xsyn,earthdistance,file_fdw,fuzzystrmatch}.so
%{_libdir}/pgsql/{hstore,hstore_plperl,hstore_plpython2,insert_username,isn,lo,ltree,ltree_plpython2}.so
%{_libdir}/pgsql/{moddatetime,pageinspect,passwordcheck,pg_buffercache,pg_freespacemap,pg_stat_statements}.so
%{_libdir}/pgsql/{pg_trgm,pg_visibility,pgcrypto,pgrowlocks,pgstattuple,postgres_fdw,refint}.so
%{_libdir}/pgsql/{seg,tablefunc,tcn,test_decoding,timetravel,tsm_system_rows,tsm_system_time,unaccent}.so
%{_libdir}/pgsql/{sepgsql,sslinfo,uuid-ossp,pgxml}.so


%files server -f server.lst
%{_bindir}/{initdb,pg_basebackup,pg_controldata,pg_ctl,pg_receivewal,pg_recvlogical}
%{_bindir}/{pg_resetwal,pg_rewind,postgres,postgresql-setup,postmaster}
%{_datadir}/pgsql/{conversion_create.sql,*.sample,extension/plpgsql*,information_schema.sql}
%{_datadir}/pgsql/postgres.{bki,description,shdescription}
%{_datadir}/pgsql/{snowball_create.sql,sql_features.txt,system_views.sql,timezonesets/,tsearch_data/}
%{_datadir}/postgresql-setup/library.sh
%{_tmpfilesdir}/postgresql.conf
%{_libdir}/pgsql/{*_and_*,dict_snowball,euc2004_sjis2004,libpqwalreceiver,pg_prewarm,pgoutput,plpgsql}.so
%{_libexecdir}/initscripts/legacy-actions/postgresql/*
%{_libexecdir}/postgresql-check-db-dir
%{_sbindir}/postgresql-new-systemd-unit
%{_unitdir}/*postgresql*.service
%dir %{_datadir}/pgsql/{extension,contrib}
%dir %{_datadir}/postgresql-setup
%dir %{_libexecdir}/initscripts/legacy-actions/postgresql
%dir %{_sysconfdir}/postgresql-setup/upgrade
%attr(700,postgres,postgres) %dir %{?_localstatedir}/lib/pgsql
%attr(700,postgres,postgres) %dir %{?_localstatedir}/lib/pgsql/backups
%attr(700,postgres,postgres) %dir %{?_localstatedir}/lib/pgsql/data
%attr(755,postgres,postgres) %dir %{?_localstatedir}/run/postgresql
%attr(700,postgres,postgres) %config(noreplace) %{?_localstatedir}/lib/pgsql/.bash_profile
%config %{_sysconfdir}/postgresql-setup/upgrade/*.conf


%files devel -f devel.lst
%{_includedir}/*
%{_bindir}/{ecpg,pg_config}
%{_libdir}/{pgsql/pgxs/,pkgconfig/*.pc}
%{_libdir}/{libecpg,libecpg_compat,libpgtypes,libpq}.so
%{macrosdir}/macros.%name

%files static
%{_libdir}/libpgcommon.a
%{_libdir}/libpgport.a

%files test-rpm-macros
%{_datadir}/postgresql-setup/postgresql_pkg_tests.sh
%{macrosdir}/macros.%name-test


%files upgrade
%{_libdir}/pgsql/postgresql-9.6/{bin,lib,share}
%exclude %{_libdir}/pgsql/postgresql-9.6/bin/pg_config
%exclude %{_libdir}/pgsql/postgresql-9.6/lib/{pgxs,pkgconfig}


%files upgrade-devel
%{_libdir}/pgsql/postgresql-9.6/{include,bin/pg_config}
%{_libdir}/pgsql/postgresql-9.6/lib/{pkgconfig,pgxs}
%{macrosdir}/macros.%name-upgrade


%files plperl -f plperl.lst
%{_datadir}/pgsql/extension/plperl*
%{_libdir}/pgsql/plperl.so


%files pltcl -f pltcl.lst
%{_datadir}/pgsql/extension/pltcl*
%{_libdir}/pgsql/pltcl.so


%files plpython -f plpython.lst
%{_datadir}/pgsql/extension/{plpython2*,plpythonu*}
%{_libdir}/pgsql/plpython2.so


%files plpython3 -f plpython3.lst
%{_datadir}/pgsql/extension/plpython3*
%{_libdir}/pgsql/plpython3.so

%files test
%attr(-,postgres,postgres) %{_libdir}/pgsql/test

%changelog
* Mon Mar 10 2020 yanzhihua <yanzhihua4@huawei.com> 10.5-11
- Type: bug fix
- ID: #I1AHMH
- SUG: NA
- DESC: fix issue #I1AHMH

* Mon Feb 3 2020 chenli <chenli147@huawei.com> 10.5-10
- Type:cve
- ID:CVE-2019-10130
- SUG: NA
- DESC: fix CVE-2019-10130

* Tue Jan 14 2020 openEuler Buildteam <buildteam@openeuler.org> - 10.5-9
- Type:enhancement
- ID:NA
- SUG:restart
- DESC: remove useless files

* Mon Jan 13 2020 yanzhihua <yanzhihua4@huawei.com> - 10.5-8
- Type: enhancement
- ID: NA
- SUG: NA
- DESC: modify buildrequire

* Tue Dec 24 2019 fengbing <fengbing7@huawei.com> - 10.5-7
- Type:cves
- ID:CVE-2019-10208 CVE-2018-16850
- SUG:restart
- DESC: fix CVE-2019-10208 CVE-2018-16850

* Fri Nov 15 2019 yanzhihua<yanzhihua4@huawei.com> - 10.5-6
- Package init
