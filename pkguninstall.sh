#!/bin/sh

if [ $EUID -ne 0 ]; then
	echo "This script must be run as root"
	exit 1
fi

if [ $# != 1 ]; then
	echo " Usage: $0 regex"
	echo " Use 'pkgutil --pkgs' to list all installed packages."
	exit 1
fi

packages=`pkgutil --pkgs="$1"`

function try_remove_directory
{
	if [ ! "`ls -A $1`" ]; then
    		rmdir "$1"
		try_remove_directory `dirname "$1"`
	fi
}

function remove_file
{
	if [ -f "$1" ]; then
		rm -f $1
		try_remove_directory `dirname "$1"`
	fi 
}

function uninstall_package
{
	location=`pkgutil --pkg-info "$1" | grep "^location: " | cut -c11-` 
	
	echo "I'll be removing the following files:"
	echo

	for f in `pkgutil --files "$1"`; do
		echo "$location/$f"
	done

	echo	
	read -p "Proceed? This cannot be undone. (y/N) " -n 1 -r
	
	case "$REPLY" in
		'') return;;
		'y'|'Y') ;;
		*) echo; return;;
	esac
	
	for f in `pkgutil --files "$1"`; do
		remove_file "$location/$f"
	done
	
	pkgutil --forget "$1"
}

for p in $packages; do
	read -p "Uninstall $p ? (y/N) " -n 1 -r

	case "$REPLY" in
		'') ;;
		'y'|'Y') echo; uninstall_package $p;;
		*) echo;;
	esac
done
