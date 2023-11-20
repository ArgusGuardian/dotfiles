#!/bin/bash

function run {
	if ! pgrep -x $(basename $1 | head -c 15) 1>/dev/null; then
		$@ &
	fi
}

# Wallpaper #
run variety &
#nitrogen --restore
wal -R &

# SXHKD #
run sxhkd -c ~/.config/qtile/sxhkd/sxhkdrc &

# Utility Applications #
run nm-applet &
run xfce4-power-manager &
numlockx on &
#blueman-applet &
#blueberry-tray &
picom --config $HOME/.config/qtile/scripts/picom.conf &
/usr/lib/polkit-1/polkitd %
/usr/libexec/xfce-polkit &
#/usr/lib/polkit-gnome/polkit-gnome-authentication-agent-1 &
/usr/lib/xfce4/notifyd/xfce4-notifyd &
/usr/bin/dunst &
#xdm-app &
light-locker &
# clipboard startup
xfce4-clipman &

# User Applications #
# run volumeicon &
# start the synching on local network
#syncthing &
