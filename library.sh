die()     { echo >&2 $"FATAL: $@" ; exit 1 ; }
error()   { echo >&2 $"ERROR: $@" ; }
error_q() { echo >&2 $"       $@" ; }
warn()    { echo >&2 $"WARNING: $@" ; }
warn_q()  { echo >&2 $"         $@" ; }
info()    { echo >&2 $" * $@" ; }
info_q()  { echo >&2 $"   $@" ; }
debug()   { test "$option_debug" != "1" || echo >&2 $"DEBUG: $@";  }


set_var()
{
    eval "$1=\"$2\""
}


root_prereq()
{
    test -z "$PGSETUP_TEST" || return 0
    test "$(id -u)" -eq 0 || die "$0 requires root access for this action"
}


read_config_file()
{
    local key="" val=""

    test -r "$1" || die "can't read file '$1'"

    for i in $2; do
        eval "unset __pg_conf_$i"
    done

    # No easy (and secure) way to read configuration files from bash script,
    # sorry.
    while read key val; do
        [[ $key =~ ^[a-zA-Z_][a-zA-Z0-9_]*$ ]] || return 1

        case " $2 " in
        *" $key "*)
            ;;
        *)
            warn "config file '$1':  unknown key '$key'"
            continue
            ;;
        esac

        # Strip double quotes
        case "$val" in
        \"*\")
            val=${val##\"}
            val=${val%%\"}
            ;;
        esac

        # Make it reasonably safe.  Keep dolar-sign escaped.
        eval "__pg_conf_$key=\$val"

    done < <(grep -v -e "^$" -e "^#" < "$1")
}


