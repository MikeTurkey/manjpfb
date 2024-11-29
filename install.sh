#!/bin/sh

# manjpfb, FreeBSD Japanese-man Pager.
# Copyright (C) 2024 Mike Turkey
# contact: voice[ATmark]miketurkey.com
# license: GPLv3 License

T=$(dirname "$0")
SCRDIR=$(cd "$T"; pwd)
CONF="$SCRDIR"/snakeland-manjpfb.conf
INSTALLSNAKE="$SCRDIR"/snakeland/install.sh

### Function ###
check_rootuser(){
    local ARGSUSER TMP_USER
    ARGSUSER='root'
    case "$(uname -s)" in
	'Darwin' | 'FreeBSD')
	    TMP_USER=$(id -p | grep uid | awk '{print $2}')
	    ;;
	'Linux')
	    TMP_USER=$(id -u -n)
	    ;;
	*)
	    TMP_USER=$(id -p | grep uid | awk '{print $2}')
	    ;;
    esac
	    
    if [ "$ARGSUSER" != "$TMP_USER" ]; then
        echo 'Error: Not root user.' " [uid: $TMP_USER]"
        exit 1
    fi
    return
}

### Main ###
check_rootuser

for F in "$CONF" "$INSTALLSNAKE"; do
    if ! test -r "$F"; then
	echo 'Error: Not found the file.' " [$F]" > /dev/stderr; exit 1; fi
done

if ! snakeland --version > /dev/null 2>&1; then
    "$INSTALLSNAKE" || exit 1
fi

snakeland install "$CONF"  || exit 1
exit 0
