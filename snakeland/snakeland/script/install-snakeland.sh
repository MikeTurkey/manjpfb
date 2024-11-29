#!/bin/sh
######################################################################
####################  SOFTWARE LICENSE   #############################
######################################################################
#
# SNAKELAND, Instant python script installer.
# Copyright (C) 2023-2024 Mike Turkey
# contact: voice[ATmark]miketurkey.com
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
# ADDITIONAL MACHINE LEARNING PROHIBITION CLAUSE
#
# In addition to the rights granted under the applicable license(GPL-3),
# you are expressly prohibited from using any form of machine learning,
# artificial intelligence, or similar technologies to analyze, process,
# or extract information from this software, or to create derivative
# works based on this software.
#
# This prohibition includes, but is not limited to, training machine
# learning models, neural networks, or any other automated systems using
# the code or output of this software.
#
# The purpose of this prohibition is to protect the integrity and
# intended use of this software. If you wish to use this software for
# machine learning or similar purposes, you must seek explicit written
# permission from the copyright holder.
#
# see also 
#     GPL-3 Licence, https://www.gnu.org/licenses/gpl-3.0.html.en
#     Mike Turkey.com, https://miketurkey.com
#

T=$(dirname "$0")
SCRDIR=$(cd "$T"; pwd)
SNAKELANDSH="$SCRDIR"/snakeland.sh
SNAKELANDPY="$SCRDIR"/snakeland.py
SNAKELANDMAN=$(cd "$SCRDIR"/../man; pwd)/snakeland.1
SNAKELANDMANGZ=$(cd "$SCRDIR"/../man; pwd)/snakeland.1.gz
TARGETDIR=/usr/local/libexec/snakeland/
TARGETMANDIR=/usr/local/share/man/man1/
CMDDIR=/usr/local/bin
CMDNAME=snakeland
install_cmd(){
    local CDIR CNAME DSTCMD CPATH
    CDIR="$1"
    CNAME="$2"
    DSTCMD="$3"
    if ! test -x "$DSTCMD"; then
	echo 'Error: Not found command.' " [$DSTCMD]" > /dev/stderr
	exit 1; fi
    CPATH="$(cd "$CDIR"; pwd)"/"$CNAME"
    printf '#!/bin/sh\n'              > "$CPATH"
    printf 'exec %s "$@"\n' "$DSTCMD" >> "$CPATH"
    chmod 755 "$CPATH" || exit 1
    return
}
check_rootuser(){
    local ARGSUSER TMP_USER
    ARGSUSER='root'
    TMP_USER=$(id -p | grep uid | awk '{print $2}')
    if test "$ARGSUSER" != "$TMP_USER"; then
        echo 'Error: Not root user.' " [uid: $TMP_USER]"
        exit 1
    fi
    return
}
check_rootuser
if ! test -d "$TARGETDIR"; then
    if ! mkdir -p "$TARGETDIR"; then
	echo 'Error: Can not make the directory.' " [$TARGETDIR]" > /dev/stderr
	exit 1; fi
fi
for F in "$SNAKELANDSH" "$SNAKELANDPY" "$SNAKELANDMAN" "$SNAKELANDMANGZ"; do
    if ! test -r "$F"; then
	echo 'Error: Not found source file.' " [$F]" > /dev/stderr
	exit 1; fi
done
if ! test -d "$TARGETMANDIR"; then
    if ! mkdir -p "$TARGETMANDIR"; then
	echo 'Error: Can not make man directory.' " [$TARGETMANDIR]"
	exit 1; fi
fi
cp -f "$SNAKELANDSH"   "$TARGETDIR" || exit 1
cp -f "$SNAKELANDPY"   "$TARGETDIR" || exit 1
case $(uname -s) in
     'Darwin')
	 cp -f "$SNAKELANDMAN"  "$TARGETMANDIR" || exit 1
	 ;;
     *)
	 cp -f "$SNAKELANDMANGZ"  "$TARGETMANDIR" || exit 1
	 ;;
esac
F=$(basename "$SNAKELANDSH")
TARGETCMD="$TARGETDIR"/"$F"
install_cmd "$CMDDIR" "$CMDNAME" "$TARGETCMD"
echo 'Success: snakeland has been installed.'
exit 0

