%{!?beta:%global beta 0}
%{!?test:%global test 1}
%ifarch riscv64
# Fail to pass tests on riscv64
%{!?llvmjit:%global llvmjit 0}
%else
%{!?llvmjit:%global llvmjit 1}
%endif
%{!?external_libpq:%global external_libpq 0}
%{!?upgrade:%global upgrade 0}
%{!?plpython:%global plpython 0}
%{!?plpython3:%global plpython3 1}
%{!?pltcl:%global pltcl 1}
%{!?plperl:%global plperl 1}
%{!?ssl:%global ssl 1}
%{!?icu:%global icu 1}
%{!?kerberos:%global kerberos 1}
%{!?ldap:%global ldap 1}
%{!?nls:%global nls 1}
%{!?uuid:%global uuid 1}
%{!?xml:%global xml 1}
%{!?pam:%global pam 1}
%{!?sdt:%global sdt 1}
%{!?selinux:%global selinux 1}
%{!?runselftest:%global runselftest 1}

%global _default_patch_flags --no-backup-if-mismatch

%global macrosdir %(d=%{_rpmconfigdir}/macros.d; [ -d $d ] || d=%{_sysconfdir}/rpm; echo $d)

Summary: PostgreSQL client programs
Name: postgresql
%global majorversion 13
Version: %{majorversion}.3
Release: 5

# The PostgreSQL license is very similar to other MIT licenses, but the OSI
# recognizes it as an independent license, so we do as well.
License: PostgreSQL
Url: http://www.postgresql.org/

%global prevmajorversion 12
%global prevversion %{prevmajorversion}.7
%global prev_prefix %{_libdir}/pgsql/postgresql-%{prevmajorversion}
%global precise_version %{?epoch:%epoch:}%version-%release

%global setup_version 8.5

%global service_name postgresql.service

Source0: https://ftp.postgresql.org/pub/source/v%{version}/postgresql-%{version}.tar.bz2
Source1: postgresql-%{version}-US.pdf
Source2: generate-pdf.sh
Source3: https://ftp.postgresql.org/pub/source/v%{prevversion}/postgresql-%{prevversion}.tar.bz2
Source4: Makefile.regress
Source9: postgresql.tmpfiles.d
Source10: postgresql.pam
Source11: postgresql-bashprofile


# git: https://github.com/devexp-db/postgresql-setup
Source12: https://github.com/devexp-db/postgresql-setup/releases/download/v%{setup_version}/postgresql-setup-%{setup_version}.tar.gz

# Those here are just to enforce packagers check that the tarball was downloaded
# correctly.  Also, this allows us check that packagers-only tarballs do not
# differ with publicly released ones.
Source16: https://ftp.postgresql.org/pub/source/v%{version}/postgresql-%{version}.tar.bz2.sha256
Source17: https://ftp.postgresql.org/pub/source/v%{prevversion}/postgresql-%{prevversion}.tar.bz2.sha256

# Comments for these patches are in the patch files.
Patch1: rpm-pgsql.patch
Patch2: postgresql-logging.patch
Patch5: postgresql-var-run-socket.patch
Patch6: postgresql-man.patch
Patch8: postgresql-external-libpq.patch
Patch9: postgresql-server-pg_config.patch
Patch10: postgresql-no-libecpg.patch
Patch11: postgresql-datalayout-mismatch-on-s390.patch
Patch12: CVE-2021-23214.patch
Patch13: CVE-2021-23222.patch

BuildRequires: gcc
BuildRequires: perl(ExtUtils::MakeMaker) glibc-devel bison flex gawk
BuildRequires: perl(ExtUtils::Embed), perl-devel
BuildRequires: perl-generators
BuildRequires: readline-devel zlib-devel
BuildRequires: systemd systemd-devel util-linux
BuildRequires: multilib-rpm-config
%if %external_libpq
BuildRequires: libpq-devel >= %version
%endif
BuildRequires: docbook-style-xsl

# postgresql-setup build requires
BuildRequires: m4 elinks docbook-utils help2man

%if %plpython
BuildRequires: python2-devel
%endif

%if %plpython3
BuildRequires: python3-devel
%endif

%if %pltcl
BuildRequires: tcl-devel
%endif

%if %ssl
BuildRequires: openssl-devel
%endif

%if %kerberos
BuildRequires: krb5-devel
%endif

%if %ldap
BuildRequires: openldap-devel
%endif

%if %nls
BuildRequires: gettext >= 0.10.35
%endif

%if %uuid
BuildRequires: uuid-devel
%endif

%if %xml
BuildRequires: libxml2-devel libxslt-devel
%endif

%if %pam
BuildRequires: pam-devel
%endif

%if %sdt
BuildRequires: systemtap-sdt-devel
%endif

%if %selinux
BuildRequires: libselinux-devel
%endif

%if %icu
BuildRequires:  libicu-devel
%endif

%global __provides_exclude_from %{_libdir}/pgsql

%description
PostgreSQL is an advanced Object-Relational database management system (DBMS).
The base postgresql package contains the client programs that you'll need to
access a PostgreSQL DBMS server, as well as HTML documentation for the whole
system.  These client programs can be located on the same machine as the
PostgreSQL server, or on a remote machine that accesses a PostgreSQL server
over a network connection.  The PostgreSQL server can be found in the
postgresql-server sub-package.


%package server
Summary: The programs needed to create and run a PostgreSQL server
Requires: %{name}%{?_isa} = %precise_version
Requires(pre): /usr/sbin/useradd
Requires: systemd
%{?systemd_requires}
Provides: %{name}-server(:MODULE_COMPAT_%{majorversion})
Provides: bundled(postgresql-setup) = %setup_version

%description server
PostgreSQL is an advanced Object-Relational database management system (DBMS).
The postgresql-server package contains the programs needed to create
and run a PostgreSQL server, which will in turn allow you to create
and maintain PostgreSQL databases.


%package docs
Summary: Extra documentation for PostgreSQL
Requires: %{name}%{?_isa} = %precise_version
Provides: %{name}-doc = %precise_version

%description docs
The postgresql-docs package contains some additional documentation for
PostgreSQL.  Currently, this includes the main documentation in PDF format
and source files for the PostgreSQL tutorial.


%package contrib
Summary: Extension modules distributed with PostgreSQL
Requires: %{name}%{?_isa} = %precise_version

%description contrib
The postgresql-contrib package contains various extension modules that are
included in the PostgreSQL distribution.


%package server-devel
Summary: PostgreSQL development header files and libraries
%if %icu
Requires:       libicu-devel
%endif
%if %kerberos
Requires:       krb5-devel
%endif

%description server-devel
The postgresql-server-devel package contains the header files and configuration
needed to compile PostgreSQL server extension.

%package test-rpm-macros
Summary: Convenience RPM macros for build-time testing against PostgreSQL server
Requires: %{name}-server = %precise_version
BuildArch: noarch

%description test-rpm-macros
This package is meant to be added as BuildRequires: dependency of other packages
that want to run build-time testsuite against running PostgreSQL server.


%package static
Summary: Statically linked PostgreSQL libraries
Requires: %{name}-server-devel%{?_isa} = %precise_version

%description static
Statically linked PostgreSQL libraries that do not have dynamically linked
counterparts.


%if %upgrade
%package upgrade
Summary: Support for upgrading from the previous major release of PostgreSQL
Requires: %{name}-server%{?_isa} = %precise_version
Provides: bundled(postgresql-server) = %prevversion

%description upgrade
The postgresql-upgrade package contains the pg_upgrade utility and supporting
files needed for upgrading a PostgreSQL database from the previous major
version of PostgreSQL.


%package upgrade-devel
Summary: Support for build of extensions required for upgrade process
Requires: %{name}-upgrade%{?_isa} = %precise_version

%description upgrade-devel
The postgresql-devel package contains the header files and libraries
needed to compile C or C++ applications which are necessary in upgrade
process.
%endif


%if %plperl
%package plperl
Summary: The Perl procedural language for PostgreSQL
Requires: %{name}-server%{?_isa} = %precise_version
Requires: perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
%if %runselftest
BuildRequires: perl(Opcode)
BuildRequires: perl(Data::Dumper)
%endif

%description plperl
The postgresql-plperl package contains the PL/Perl procedural language,
which is an extension to the PostgreSQL database server.
Install this if you want to write database functions in Perl.
%endif


%if %plpython
%package plpython
Summary: The Python2 procedural language for PostgreSQL
Requires: %{name}-server%{?_isa} = %precise_version
Provides: %{name}-plpython2 = %precise_version

%description plpython
The postgresql-plpython package contains the PL/Python procedural language,
which is an extension to the PostgreSQL database server.
Install this if you want to write database functions in Python 2.
%endif


%if %plpython3
%package plpython3
Summary: The Python3 procedural language for PostgreSQL
Requires: %{name}-server%{?_isa} = %precise_version

%description plpython3
The postgresql-plpython3 package contains the PL/Python3 procedural language,
which is an extension to the PostgreSQL database server.
Install this if you want to write database functions in Python 3.
%endif


%if %pltcl
%package pltcl
Summary: The Tcl procedural language for PostgreSQL
Requires: %{name}-server%{?_isa} = %precise_version

%description pltcl
The postgresql-pltcl package contains the PL/Tcl procedural language,
which is an extension to the PostgreSQL database server.
Install this if you want to write database functions in Tcl.
%endif


%if %test
%package test
Summary: The test suite distributed with PostgreSQL
Requires: %{name}-server%{?_isa} = %precise_version
Requires: %{name}-server-devel%{?_isa} = %precise_version

%description test
The postgresql-test package contains files needed for various tests for the
PostgreSQL database management system, including regression tests and
benchmarks.
%endif

%if %llvmjit
%package llvmjit
Summary:        Just-in-time compilation support for PostgreSQL
Requires:       %{name}-server%{?_isa} = %{version}-%{release}
Requires:       llvm => 5.0
Provides:       postgresql-llvmjit >= %{version}-%{release}
BuildRequires:  llvm-devel >= 5.0 clang-devel >= 5.0

%description llvmjit
The postgresql-llvmjit package contains support for
just-in-time compiling parts of PostgreSQL queries. Using LLVM it
compiles e.g. expressions and tuple deforming into native code, with the
goal of accelerating analytics queries.
%endif

%prep
(
  cd "$(dirname "%{SOURCE0}")"
  sha256sum -c %{SOURCE16}
%if %upgrade
  sha256sum -c %{SOURCE17}
%endif
)
%setup -q -a 12 -n postgresql-%{version}
%patch1 -p1
%patch2 -p1
%patch5 -p1
%patch6 -p1
%if %external_libpq
%patch8 -p1
%else
%patch10 -p1
%endif
%patch9 -p1
%patch11 -p1
%patch12 -p1
%patch13 -p1

# We used to run autoconf here, but there's no longer any real need to,
# since Postgres ships with a reasonably modern configure script.

cp -p %{SOURCE1} .

%if ! %external_libpq
%global private_soname private%{majorversion}
find . -type f -name Makefile -exec sed -i -e "s/SO_MAJOR_VERSION=\s\?\([0-9]\+\)/SO_MAJOR_VERSION= %{private_soname}-\1/" {} \;
%endif

%if %upgrade
tar xfj %{SOURCE3}

# libpq from this upgrade-only build is dropped and the libpq from the main
# version is used. Use the same major hack therefore.
%if ! %external_libpq
find . -type f -name Makefile -exec sed -i -e "s/SO_MAJOR_VERSION=\s\?\([0-9]\+\)/SO_MAJOR_VERSION= %{private_soname}-\1/" {} \;
%endif

# apply once SOURCE3 is extracted
%endif

# remove .gitignore files to ensure none get into the RPMs (bug #642210)
find . -type f -name .gitignore | xargs rm


%build
# fail quickly and obviously if user tries to build as root
%if %runselftest
        if [ x"`id -u`" = x0 ]; then
                echo "postgresql's regression tests fail if run as root."
                echo "If you really need to build the RPM as root, use"
                echo "--define='runselftest 0' to skip the regression tests."
                exit 1
        fi
%endif

# Building postgresql-setup

cd postgresql-setup-%{setup_version}
export pgsetup_cv_os_family=redhat
%configure \
    pgdocdir=%{_pkgdocdir} \
    PGVERSION=%{version} \
    PGMAJORVERSION=%{majorversion} \
    NAME_DEFAULT_PREV_SERVICE=postgresql

make %{?_smp_mflags}
unset pgsetup_cv_os_family
cd ..

# Fiddling with CFLAGS.

CFLAGS="${CFLAGS:-%optflags}"
# Strip out -ffast-math from CFLAGS....
CFLAGS=`echo $CFLAGS|xargs -n 1|grep -v ffast-math|xargs -n 100`
export CFLAGS

# plpython requires separate configure/build runs to build against python 2
# versus python 3.  Our strategy is to do the python 3 run first, then make
# distclean and do it again for the "normal" build.  Note that the installed
# Makefile.global will reflect the python 2 build, which seems appropriate
# since that's still considered the default plpython version.
common_configure_options='
        --disable-rpath
%ifarch riscv64
        --disable-spinlocks
%endif
%if %beta
        --enable-debug
        --enable-cassert
%endif
%if %plperl
        --with-perl
%endif
%if %pltcl
        --with-tcl
        --with-tclconfig=%_libdir
%endif
%if %ldap
        --with-ldap
%endif
%if %ssl
        --with-openssl
%endif
%if %pam
        --with-pam
%endif
%if %kerberos
        --with-gssapi
%endif
%if %uuid
        --with-ossp-uuid
%endif
%if %xml
        --with-libxml
        --with-libxslt
%endif
%if %nls
        --enable-nls
%endif
%if %sdt
        --enable-dtrace
%endif
%if %selinux
        --with-selinux
%endif
        --with-system-tzdata=%_datadir/zoneinfo
        --datadir=%_datadir/pgsql
        --with-systemd
%if %icu
        --with-icu
%endif
%if %llvmjit
        --with-llvm
%endif
'

%if %plpython3

export PYTHON=/usr/bin/python3

# These configure options must match main build
%configure $common_configure_options \
        --with-python

# Fortunately we don't need to build much except plpython itself.
%global python_subdirs       \\\
        src/pl/plpython          \\\
        contrib/hstore_plpython  \\\
        contrib/jsonb_plpython   \\\
        contrib/ltree_plpython

for dir in %python_subdirs; do
        %make_build -C "$dir" all
done

# save built form in a directory that "make distclean" won't touch
for dir in %python_subdirs; do
        rm -rf "${dir}3" # shouldn't exist, unless --short-circuit
        cp -a "$dir" "${dir}3"
done

# must also save this version of Makefile.global for later
cp src/Makefile.global src/Makefile.global.python3

make distclean

%endif # %%plpython3

PYTHON=/usr/bin/python2

# Normal (python2) build begins here
%configure $common_configure_options \
%if %plpython
        --with-python
%endif

unset PYTHON

%make_build world

# Have to hack makefile to put correct path into tutorial scripts
sed "s|C=\`pwd\`;|C=%{_libdir}/pgsql/tutorial;|" < src/tutorial/Makefile > src/tutorial/GNUmakefile
make %{?_smp_mflags} -C src/tutorial NO_PGXS=1 all
rm -f src/tutorial/GNUmakefile

# The object files shouldn't be copied to rpm bz#1187514
rm -f src/tutorial/*.o

# run_testsuite WHERE
# -------------------
# Run 'make check' in WHERE path.  When that command fails, return the logs
# given by PostgreSQL build system and set 'test_failure=1'.  This function
# never exits directly nor stops rpmbuild where `set -e` is enabled.
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

%if %runselftest
        run_testsuite "src/test/regress"
        make clean -C "src/test/regress"
        run_testsuite "src/pl"
%if %plpython3
        # must install Makefile.global that selects python3
        mv src/Makefile.global src/Makefile.global.save
        cp src/Makefile.global.python3 src/Makefile.global
        touch -r src/Makefile.global.save src/Makefile.global

        for dir in %python_subdirs; do
                # because "make check" does "make install" on the whole tree,
                # we must temporarily install *plpython3 dir as *plpython,
                # since that is the subdirectory src/pl/Makefile knows about
                mv "$dir" "${dir}2"
                mv "${dir}3" "$dir"
        done

        for dir in %python_subdirs; do
                run_testsuite "$dir"
        done

        for dir in %python_subdirs; do
                # and clean up our mess
                mv "$dir" "${dir}3"
                mv "${dir}2" "${dir}"
        done

        mv -f src/Makefile.global.save src/Makefile.global
%endif
        run_testsuite "contrib"
%endif

# "assert(ALL_TESTS_OK)"
test "$test_failure" -eq 0

%if %test
        # undo the "make clean" above
        make all -C src/test/regress
%endif

%if %upgrade
        pushd postgresql-%{prevversion}

        # The upgrade build can be pretty stripped-down, but make sure that
        # any options that affect on-disk file layout match the previous
        # major release!

        # The set of built server modules here should ideally create superset
        # of modules we used to ship in %%prevversion (in the installation
        # the user will upgrade from), including *-contrib or *-pl*
        # subpackages.  This increases chances that the upgrade from
        # %%prevversion will work smoothly.

upgrade_configure ()
{
        # Note we intentionally do not use %%configure here, because we *don't* want
        # its ideas about installation paths.

        # The -fno-aggressive-loop-optimizations is hack for #993532
        PYTHON="${PYTHON-/usr/bin/python2}" \
        CFLAGS="$CFLAGS -fno-aggressive-loop-optimizations" ./configure \
                --build=%{_build} \
                --host=%{_host} \
                --prefix=%prev_prefix \
                --disable-rpath \
%ifarch riscv64
                --disable-spinlocks \
%endif
%if %beta
                --enable-debug \
                --enable-cassert \
%endif
%if %icu
                --with-icu \
%endif
%if %plperl
                --with-perl \
%endif
%if %pltcl
                --with-tcl \
%endif
                --with-tclconfig=%_libdir \
                --with-system-tzdata=/usr/share/zoneinfo \
                "$@"
}

%if %plpython3
        export PYTHON=/usr/bin/python3
        upgrade_configure --with-python
        for dir in %python_subdirs; do
                # Previous version doesn't necessarily have this.
                test -d "$dir" || continue
                %make_build -C "$dir" all

                # save aside the only one file which we are interested here
                cp "$dir"/*plpython3.so ./
        done
        unset PYTHON
        make distclean
%endif

        upgrade_configure \
%if %plpython
                --with-python
%endif

        make %{?_smp_mflags} all
        make -C contrib %{?_smp_mflags} all
        popd
%endif # %%upgrade


%install
cd postgresql-setup-%{setup_version}
make install DESTDIR=$RPM_BUILD_ROOT
cd ..

# For some reason, having '%%doc %%{_pkgdocdir}/README.rpm-dist' in %%files
# causes FTBFS (at least on RHEL6), see rhbz#1250006.
mv $RPM_BUILD_ROOT/%{_pkgdocdir}/README.rpm-dist ./

cat > $RPM_BUILD_ROOT%{_sysconfdir}/postgresql-setup/upgrade/postgresql.conf <<EOF
id              postgresql
major           %{prevmajorversion}
data_default    %{_localstatedir}/pgsql/data
package         postgresql-upgrade
engine          %{_libdir}/pgsql/postgresql-%{prevmajorversion}/bin
description     "Upgrade data from system PostgreSQL version (PostgreSQL %{prevmajorversion})"
redhat_sockets_hack no
EOF

make DESTDIR=$RPM_BUILD_ROOT install-world

# We ship pg_config through libpq-devel
mv $RPM_BUILD_ROOT/%_mandir/man1/pg_{,server_}config.1

%if %plpython3
        mv src/Makefile.global src/Makefile.global.save
        cp src/Makefile.global.python3 src/Makefile.global
        touch -r src/Makefile.global.save src/Makefile.global
        for dir in %python_subdirs; do
                %make_install -C "${dir}3"
        done
        mv -f src/Makefile.global.save src/Makefile.global
%endif

# make sure these directories exist even if we suppressed all contrib modules
install -d -m 755 $RPM_BUILD_ROOT%{_datadir}/pgsql/contrib
install -d -m 755 $RPM_BUILD_ROOT%{_datadir}/pgsql/extension

# multilib header hack
for header in \
        %{_includedir}/pgsql/server/pg_config.h \
        %{_includedir}/pgsql/server/pg_config_ext.h
do
%multilib_fix_c_header --file "$header"
done

install -d -m 755 $RPM_BUILD_ROOT%{_libdir}/pgsql/tutorial
cp -p src/tutorial/* $RPM_BUILD_ROOT%{_libdir}/pgsql/tutorial

%if %pam
install -d $RPM_BUILD_ROOT/etc/pam.d
install -m 644 %{SOURCE10} $RPM_BUILD_ROOT/etc/pam.d/postgresql
%endif

# Create the directory for sockets.
install -d -m 755 $RPM_BUILD_ROOT%{?_localstatedir}/run/postgresql

# ... and make a tmpfiles script to recreate it at reboot.
mkdir -p $RPM_BUILD_ROOT%{_tmpfilesdir}
install -m 0644 %{SOURCE9} $RPM_BUILD_ROOT%{_tmpfilesdir}/postgresql.conf

# PGDATA needs removal of group and world permissions due to pg_pwd hole.
install -d -m 700 $RPM_BUILD_ROOT%{?_localstatedir}/lib/pgsql/data

# backups of data go here...
install -d -m 700 $RPM_BUILD_ROOT%{?_localstatedir}/lib/pgsql/backups

# postgres' .bash_profile
install -m 644 %{SOURCE11} $RPM_BUILD_ROOT%{?_localstatedir}/lib/pgsql/.bash_profile

rm $RPM_BUILD_ROOT/%{_datadir}/man/man1/ecpg.1

%if %upgrade
        pushd postgresql-%{prevversion}
        make DESTDIR=$RPM_BUILD_ROOT install
        make -C contrib DESTDIR=$RPM_BUILD_ROOT install
%if %plpython3
        for file in *plpython3.so; do
                install -m 755 "$file" \
                        $RPM_BUILD_ROOT/%_libdir/pgsql/postgresql-%prevmajorversion/lib
        done
%endif
        popd

        # remove stuff we don't actually need for upgrade purposes
        pushd $RPM_BUILD_ROOT%{_libdir}/pgsql/postgresql-%{prevmajorversion}
        rm bin/clusterdb
        rm bin/createdb
        rm bin/createuser
        rm bin/dropdb
        rm bin/dropuser
        rm bin/ecpg
        rm bin/initdb
        rm bin/pg_basebackup
        rm bin/pg_dump
        rm bin/pg_dumpall
        rm bin/pg_restore
        rm bin/pgbench
        rm bin/psql
        rm bin/reindexdb
        rm bin/vacuumdb
        rm -rf share/doc
        rm -rf share/man
        rm -rf share/tsearch_data
        rm lib/*.a
        # Drop libpq.  This might need some tweaks once there's
        # soname bump between %%prevversion and %%version.
        rm lib/libpq.so*
        # Drop libraries.
        rm lib/lib{ecpg,ecpg_compat,pgtypes}.so*
        rm share/*.bki
        rm share/*description
        rm share/*.sample
        rm share/*.sql
        rm share/*.txt
        rm share/extension/*.sql
        rm share/extension/*.control
        popd
        cat <<EOF > $RPM_BUILD_ROOT%macrosdir/macros.%name-upgrade
%%postgresql_upgrade_prefix %prev_prefix
EOF
%endif


%if %test
        # tests. There are many files included here that are unnecessary,
        # but include them anyway for completeness.  We replace the original
        # Makefiles, however.
        mkdir -p $RPM_BUILD_ROOT%{_libdir}/pgsql/test
        cp -a src/test/regress $RPM_BUILD_ROOT%{_libdir}/pgsql/test
        # pg_regress binary should be only in one subpackage,
        # there will be a symlink from -test to -devel
        rm -f $RPM_BUILD_ROOT%{_libdir}/pgsql/test/regress/pg_regress
        ln -sf ../../pgxs/src/test/regress/pg_regress $RPM_BUILD_ROOT%{_libdir}/pgsql/test/regress/pg_regress
        pushd  $RPM_BUILD_ROOT%{_libdir}/pgsql/test/regress
        rm -f GNUmakefile Makefile *.o
        chmod 0755 pg_regress regress.so
        popd
        sed 's|@bindir@|%{_bindir}|g' \
                < %{SOURCE4} \
                > $RPM_BUILD_ROOT%{_libdir}/pgsql/test/regress/Makefile
        chmod 0644 $RPM_BUILD_ROOT%{_libdir}/pgsql/test/regress/Makefile
%endif

rm -rf doc/html # HACK! allow 'rpmbuild -bi --short-circuit'
mv $RPM_BUILD_ROOT%{_docdir}/pgsql/html doc
rm -rf $RPM_BUILD_ROOT%{_docdir}/pgsql

# remove files not to be packaged
rm $RPM_BUILD_ROOT%{_libdir}/libpgfeutils.a

%if !%plperl
rm -f $RPM_BUILD_ROOT%{_bindir}/pgsql/hstore_plperl.so
%endif

%if !%plpython
rm -f $RPM_BUILD_ROOT%{_bindir}/pgsql/hstore_plpython2.so
rm -f $RPM_BUILD_ROOT%{_datadir}/pgsql/extension/*_plpythonu*
rm -f $RPM_BUILD_ROOT%{_datadir}/pgsql/extension/*_plpython2u*
%endif

%if %nls
find_lang_bins ()
{
        lstfile=$1 ; shift
        cp /dev/null "$lstfile"
        for binary; do
                %find_lang "$binary"-%{majorversion}
                cat "$binary"-%{majorversion}.lang >>"$lstfile"
        done
}
find_lang_bins devel.lst pg_server_config
find_lang_bins server.lst \
        initdb pg_basebackup pg_controldata pg_ctl pg_resetwal pg_rewind plpgsql \
        postgres pg_checksums pg_verifybackup
find_lang_bins contrib.lst \
        pg_archivecleanup pg_test_fsync pg_test_timing pg_waldump
find_lang_bins main.lst \
        pg_dump pg_upgrade pgscripts psql \
%if ! %external_libpq
libpq%{private_soname}-5
%endif
%if %plperl
find_lang_bins plperl.lst plperl
%endif
%if %plpython
find_lang_bins plpython.lst plpython
%endif
%if %plpython3
# plpython3 shares message files with plpython
find_lang_bins plpython3.lst plpython
%endif
%if %pltcl
find_lang_bins pltcl.lst pltcl
%endif
%endif

%pre server
/usr/sbin/groupadd -g 26 -o -r postgres >/dev/null 2>&1 || :
/usr/sbin/useradd -M -N -g postgres -o -r -d /var/lib/pgsql -s /bin/bash \
        -c "PostgreSQL Server" -u 26 postgres >/dev/null 2>&1 || :

%post server
%systemd_post %service_name


%preun server
%systemd_preun %service_name


%postun server
%systemd_postun_with_restart %service_name


%check
%if %runselftest
make -C postgresql-setup-%{setup_version} check
%endif

# FILES sections.
%files -f main.lst
%doc doc/KNOWN_BUGS doc/MISSING_FEATURES doc/TODO
%doc COPYRIGHT README HISTORY
%doc README.rpm-dist
%{_bindir}/clusterdb
%{_bindir}/createdb
%{_bindir}/createuser
%{_bindir}/dropdb
%{_bindir}/dropuser
%{_bindir}/pg_dump
%{_bindir}/pg_dumpall
%{_bindir}/pg_isready
%{_bindir}/pg_restore
%{_bindir}/pg_upgrade
%{_bindir}/psql
%{_bindir}/reindexdb
%{_bindir}/vacuumdb
%{_mandir}/man1/clusterdb.*
%{_mandir}/man1/createdb.*
%{_mandir}/man1/createuser.*
%{_mandir}/man1/dropdb.*
%{_mandir}/man1/dropuser.*
%{_mandir}/man1/pg_dump.*
%{_mandir}/man1/pg_dumpall.*
%{_mandir}/man1/pg_isready.*
%{_mandir}/man1/pg_restore.*
%{_mandir}/man1/pg_upgrade.*
%{_mandir}/man1/psql.*
%{_mandir}/man1/reindexdb.*
%{_mandir}/man1/vacuumdb.*
%{_mandir}/man7/*
%if %llvmjit
# Install bitcode directory along with the main package,
# so that extensions can use this dir.
%dir %{_libdir}/pgsql/bitcode
%endif
%if ! %external_libpq
%{_libdir}/libpq.so.*
%endif

%files docs
%doc *-US.pdf
%doc doc/html
%{_libdir}/pgsql/tutorial/


%files contrib -f contrib.lst
%doc contrib/spi/*.example
%{_bindir}/oid2name
%{_bindir}/pg_archivecleanup
%{_bindir}/pg_standby
%{_bindir}/pg_test_fsync
%{_bindir}/pg_test_timing
%{_bindir}/pg_waldump
%{_bindir}/pgbench
%{_bindir}/vacuumlo
%{_datadir}/pgsql/extension/adminpack*
%{_datadir}/pgsql/extension/amcheck*
%{_datadir}/pgsql/extension/autoinc*
%{_datadir}/pgsql/extension/bloom*
%{_datadir}/pgsql/extension/btree_gin*
%{_datadir}/pgsql/extension/btree_gist*
%{_datadir}/pgsql/extension/citext*
%{_datadir}/pgsql/extension/cube*
%{_datadir}/pgsql/extension/dblink*
%{_datadir}/pgsql/extension/dict_int*
%{_datadir}/pgsql/extension/dict_xsyn*
%{_datadir}/pgsql/extension/earthdistance*
%{_datadir}/pgsql/extension/file_fdw*
%{_datadir}/pgsql/extension/fuzzystrmatch*
%{_datadir}/pgsql/extension/hstore*
%{_datadir}/pgsql/extension/insert_username*
%{_datadir}/pgsql/extension/intagg*
%{_datadir}/pgsql/extension/intarray*
%{_datadir}/pgsql/extension/isn*
%if %{plperl}
%{_datadir}/pgsql/extension/jsonb_plperl*
%endif
%if %{plpython}
%{_datadir}/pgsql/extension/jsonb_plpythonu*
%{_datadir}/pgsql/extension/jsonb_plpython2u*
%endif
%if %{plpython3}
%{_datadir}/pgsql/extension/jsonb_plpython3u*
%endif
%{_datadir}/pgsql/extension/lo*
%{_datadir}/pgsql/extension/ltree*
%{_datadir}/pgsql/extension/moddatetime*
%{_datadir}/pgsql/extension/pageinspect*
%{_datadir}/pgsql/extension/pg_buffercache*
%{_datadir}/pgsql/extension/pg_freespacemap*
%{_datadir}/pgsql/extension/pg_prewarm*
%{_datadir}/pgsql/extension/pg_stat_statements*
%{_datadir}/pgsql/extension/pg_trgm*
%{_datadir}/pgsql/extension/pg_visibility*
%{_datadir}/pgsql/extension/pgcrypto*
%{_datadir}/pgsql/extension/pgrowlocks*
%{_datadir}/pgsql/extension/pgstattuple*
%{_datadir}/pgsql/extension/postgres_fdw*
%{_datadir}/pgsql/extension/refint*
%{_datadir}/pgsql/extension/seg*
%{_datadir}/pgsql/extension/tablefunc*
%{_datadir}/pgsql/extension/tcn*
%{_datadir}/pgsql/extension/tsm_system_rows*
%{_datadir}/pgsql/extension/tsm_system_time*
%{_datadir}/pgsql/extension/unaccent*
%{_libdir}/pgsql/_int.so
%{_libdir}/pgsql/adminpack.so
%{_libdir}/pgsql/amcheck.so
%{_libdir}/pgsql/auth_delay.so
%{_libdir}/pgsql/auto_explain.so
%{_libdir}/pgsql/autoinc.so
%{_libdir}/pgsql/bloom.so
%{_libdir}/pgsql/btree_gin.so
%{_libdir}/pgsql/btree_gist.so
%{_libdir}/pgsql/citext.so
%{_libdir}/pgsql/cube.so
%{_libdir}/pgsql/dblink.so
%{_libdir}/pgsql/dict_int.so
%{_libdir}/pgsql/dict_xsyn.so
%{_libdir}/pgsql/earthdistance.so
%{_libdir}/pgsql/file_fdw.so
%{_libdir}/pgsql/fuzzystrmatch.so
%{_libdir}/pgsql/hstore.so
%if %plperl
%{_libdir}/pgsql/hstore_plperl.so
%endif
%if %plpython
%{_libdir}/pgsql/hstore_plpython2.so
%endif
%if %plpython3
%{_libdir}/pgsql/hstore_plpython3.so
%endif
%{_libdir}/pgsql/insert_username.so
%{_libdir}/pgsql/isn.so
%if %plperl
%{_libdir}/pgsql/jsonb_plperl.so
%endif
%if %plpython
%{_libdir}/pgsql/jsonb_plpython2.so
%endif
%if %plpython3
%{_libdir}/pgsql/jsonb_plpython3.so
%endif
%{_libdir}/pgsql/lo.so
%{_libdir}/pgsql/ltree.so
%if %plpython
%{_libdir}/pgsql/ltree_plpython2.so
%endif
%if %plpython3
%{_libdir}/pgsql/ltree_plpython3.so
%endif
%{_libdir}/pgsql/moddatetime.so
%{_libdir}/pgsql/pageinspect.so
%{_libdir}/pgsql/passwordcheck.so
%{_libdir}/pgsql/pg_buffercache.so
%{_libdir}/pgsql/pg_freespacemap.so
%{_libdir}/pgsql/pg_stat_statements.so
%{_libdir}/pgsql/pg_trgm.so
%{_libdir}/pgsql/pg_visibility.so
%{_libdir}/pgsql/pgcrypto.so
%{_libdir}/pgsql/pgrowlocks.so
%{_libdir}/pgsql/pgstattuple.so
%{_libdir}/pgsql/postgres_fdw.so
%{_libdir}/pgsql/refint.so
%{_libdir}/pgsql/seg.so
%{_libdir}/pgsql/tablefunc.so
%{_libdir}/pgsql/tcn.so
%{_libdir}/pgsql/test_decoding.so
%{_libdir}/pgsql/tsm_system_rows.so
%{_libdir}/pgsql/tsm_system_time.so
%{_libdir}/pgsql/unaccent.so
%{_mandir}/man1/oid2name.*
%{_mandir}/man1/pg_archivecleanup.*
%{_mandir}/man1/pg_recvlogical.*
%{_mandir}/man1/pg_standby.*
%{_mandir}/man1/pg_test_fsync.*
%{_mandir}/man1/pg_test_timing.*
%{_mandir}/man1/pg_waldump.*
%{_mandir}/man1/pgbench.*
%{_mandir}/man1/vacuumlo.*
%{_mandir}/man3/dblink*
%if %selinux
%{_datadir}/pgsql/contrib/sepgsql.sql
%{_libdir}/pgsql/sepgsql.so
%endif
%if %ssl
%{_datadir}/pgsql/extension/sslinfo*
%{_libdir}/pgsql/sslinfo.so
%endif
%if %uuid
%{_datadir}/pgsql/extension/uuid-ossp*
%{_libdir}/pgsql/uuid-ossp.so
%endif
%if %xml
%{_datadir}/pgsql/extension/xml2*
%{_libdir}/pgsql/pgxml.so
%endif

%files server -f server.lst
%{_bindir}/initdb
%{_bindir}/pg_basebackup
%{_bindir}/pg_controldata
%{_bindir}/pg_ctl
%{_bindir}/pg_receivewal
%{_bindir}/pg_recvlogical
%{_bindir}/pg_resetwal
%{_bindir}/pg_rewind
%{_bindir}/pg_checksums
%{_bindir}/pg_verifybackup
%{_bindir}/postgres
%{_bindir}/postgresql-setup
%{_bindir}/postgresql-upgrade
%{_bindir}/postmaster
%dir %{_datadir}/pgsql
%{_datadir}/pgsql/*.sample
%dir %{_datadir}/pgsql/contrib
%dir %{_datadir}/pgsql/extension
%{_datadir}/pgsql/extension/plpgsql*
%{_datadir}/pgsql/information_schema.sql
%{_datadir}/pgsql/postgres.bki
%{_datadir}/pgsql/snowball_create.sql
%{_datadir}/pgsql/sql_features.txt
%{_datadir}/pgsql/system_views.sql
%{_datadir}/pgsql/timezonesets/
%{_datadir}/pgsql/tsearch_data/
%dir %{_datadir}/postgresql-setup
%{_datadir}/postgresql-setup/library.sh
%dir %{_libdir}/pgsql
%{_libdir}/pgsql/*_and_*.so
%{_libdir}/pgsql/dict_snowball.so
%{_libdir}/pgsql/euc2004_sjis2004.so
%{_libdir}/pgsql/libpqwalreceiver.so
%{_libdir}/pgsql/pg_prewarm.so
%{_libdir}/pgsql/pgoutput.so
%{_libdir}/pgsql/plpgsql.so
%dir %{_libexecdir}/initscripts/legacy-actions/postgresql
%{_libexecdir}/initscripts/legacy-actions/postgresql/*
%{_libexecdir}/postgresql-check-db-dir
%dir %{_sysconfdir}/postgresql-setup
%dir %{_sysconfdir}/postgresql-setup/upgrade
%config %{_sysconfdir}/postgresql-setup/upgrade/*.conf
%{_mandir}/man1/initdb.*
%{_mandir}/man1/pg_basebackup.*
%{_mandir}/man1/pg_controldata.*
%{_mandir}/man1/pg_ctl.*
%{_mandir}/man1/pg_receivewal.*
%{_mandir}/man1/pg_resetwal.*
%{_mandir}/man1/pg_rewind.*
%{_mandir}/man1/pg_checksums.*
%{_mandir}/man1/pg_verifybackup.*
%{_mandir}/man1/postgres.*
%{_mandir}/man1/postgresql-new-systemd-unit.*
%{_mandir}/man1/postgresql-setup.*
%{_mandir}/man1/postgresql-upgrade.*
%{_mandir}/man1/postmaster.*
%{_sbindir}/postgresql-new-systemd-unit
%{_tmpfilesdir}/postgresql.conf
%{_unitdir}/*postgresql*.service
%attr(700,postgres,postgres) %dir %{?_localstatedir}/lib/pgsql
%attr(644,postgres,postgres) %config(noreplace) %{?_localstatedir}/lib/pgsql/.bash_profile
%attr(700,postgres,postgres) %dir %{?_localstatedir}/lib/pgsql/backups
%attr(700,postgres,postgres) %dir %{?_localstatedir}/lib/pgsql/data
%attr(755,postgres,postgres) %dir %{?_localstatedir}/run/postgresql
%if %pam
%config(noreplace) /etc/pam.d/postgresql
%endif


%files server-devel -f devel.lst
%{_bindir}/pg_server_config
%dir %{_datadir}/pgsql
%{_datadir}/pgsql/errcodes.txt
%dir %{_includedir}/pgsql
%{_includedir}/pgsql/server
%{_libdir}/pgsql/pgxs/
%{_includedir}/*
%{_libdir}/{pgsql/pgxs/,pkgconfig/*.pc}
%{_libdir}/{libecpg,libecpg_compat,libpgtypes,libpq}.so*
%{_libdir}/libpq.a
%{_mandir}/man1/pg_server_config.*
%{_mandir}/man3/SPI_*
%{macrosdir}/macros.%name


%files test-rpm-macros
%{_datadir}/postgresql-setup/postgresql_pkg_tests.sh
%{macrosdir}/macros.%name-test


%files static
%{_libdir}/libpgcommon.a
%{_libdir}/libpgport.a
%{_libdir}/libpgcommon_shlib.a
%{_libdir}/libpgport_shlib.a


%if %upgrade
%files upgrade
%{_libdir}/pgsql/postgresql-%{prevmajorversion}/bin
%exclude %{_libdir}/pgsql/postgresql-%{prevmajorversion}/bin/pg_config
%{_libdir}/pgsql/postgresql-%{prevmajorversion}/lib
%exclude %{_libdir}/pgsql/postgresql-%{prevmajorversion}/lib/pgxs
%exclude %{_libdir}/pgsql/postgresql-%{prevmajorversion}/lib/pkgconfig
%{_libdir}/pgsql/postgresql-%{prevmajorversion}/share


%files upgrade-devel
%{_libdir}/pgsql/postgresql-%{prevmajorversion}/bin/pg_config
%{_libdir}/pgsql/postgresql-%{prevmajorversion}/include
%{_libdir}/pgsql/postgresql-%{prevmajorversion}/lib/pkgconfig
%{_libdir}/pgsql/postgresql-%{prevmajorversion}/lib/pgxs
%{macrosdir}/macros.%name-upgrade
%endif

%if %llvmjit
%files llvmjit
%defattr(-,root,root)
%{_libdir}/pgsql/bitcode/*
%{_libdir}/pgsql/llvmjit.so
%{_libdir}/pgsql/llvmjit_types.bc
%endif

%if %plperl
%files plperl -f plperl.lst
%{_datadir}/pgsql/extension/bool_plperl*
%{_datadir}/pgsql/extension/plperl*
%{_libdir}/pgsql/bool_plperl.so
%{_libdir}/pgsql/plperl.so
%endif


%if %pltcl
%files pltcl -f pltcl.lst
%{_datadir}/pgsql/extension/pltcl*
%{_libdir}/pgsql/pltcl.so
%endif


%if %plpython
%files plpython -f plpython.lst
%{_datadir}/pgsql/extension/plpython2*
%{_datadir}/pgsql/extension/plpythonu*
%{_libdir}/pgsql/plpython2.so
%endif


%if %plpython3
%files plpython3 -f plpython3.lst
%{_datadir}/pgsql/extension/plpython3*
%{_libdir}/pgsql/plpython3.so
%endif


%if %test
%files test
%attr(-,postgres,postgres) %{_libdir}/pgsql/test
%endif


%changelog
* Fri Mar 11 2022 wangkai <wangkai385@huawei.com> - 13.3-5
- Fix CVE-2021-23214 CVE-2021-23222

* Tue Jan 18 2022 lvxiaoqian<xiaoqian@nj.iscas.ac.cn> - 13.3-4
- Disable spinlocks on RISC-V 64-bit (riscv64)
- Disable LLVM/Clang for riscv64 (fails tests)

* Tue Aug 3 2021 bzhaoop<bzhaojyathousandy@gmail.com> - 13.3-3
- Add the missed libpq.so file into postgresql-server-devel package.

* Mon Jun 28 2021 bzhaoop<bzhaojyathousandy@gmail.com> - 13.3-2
- Figure out the dependency by postgresql-odbc, refactor the package to fix

* Thu Jun 17 2021 bzhaoop<bzhaojyathousandy@gmail.com> - 13.3-1
- Package init for new version 13.3

* Fri Feb 26 2021 wangyue <wangyue92@huawei.com> - 10.5-19
- Fix CVE-2021-20229

* Tue Dec 8 2020 wangxiao <wangxiao65@huawei.com> - 10.5-18
- Fix CVE-2020-25694 CVE-2020-25695 CVE-2020-25696

* Thu Sep 10 2020 yanglongkang <yanglongkang@huawei.com> - 10.5-17
- Fix CVE-2020-14349 CVE-2020-14350

* Fri Jun 19 2020 cuibaobao <cuibaobao1@huawei.com> - 10.5-16
- Type: enhancement
- DESC: delete all about residual parse_upgrade_setup in postgresql-setup

* Wed May 6 2020 cuibaobao <cuibaobao1@huawei.com> - 10.5-15
- Type:cve
- ID:CVE-2020-1720
- SUG: NA
- DESC: fix CVE-2020-1720

* Tue Apr 08 2020 daiqianwen <daiqianwen@huawei.com> - 10.5-14
- Type: enhancement
- DESC: add postgresql-test-rpm-macros

* Tue Apr 07 2020 daiqianwen <daiqianwen@huawei.com> - 10.5-13
- Type: enhancement
- DESC: delete unseless tarball

* Tue Mar 10 2020 steven <steven_ygui@163.com> - 10.5-12
- Type: enhancement
- DESC: remove python2

* Mon Mar 10 2020 yanzhihua <yanzhihua4@huawei.com> - 10.5-11
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

