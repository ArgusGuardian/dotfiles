#gruvbox config
from typing import List  # noqa: F401
import os
import subprocess
from os import path

from libqtile import bar, layout, widget, hook, qtile
from libqtile.config import Click, Drag, Group, ScratchPad, DropDown, Key, Match, Screen
from libqtile.lazy import lazy
from settings.path import qtile_path
from qtile_extras import widget

import colors

# Set the GTK theme
os.environ['GTK2_RC_FILES'] = "/home/alaa/.gtkrc-2.0"
os.environ['GTK_THEME'] = "Nordic-darker"


mod = "mod1"
mod1 = "mod4"
#terminal = "kitty"

colors, backgroundColor, foregroundColor, workspaceColor, chordColor = colors.nord()

keys = [
# Open terminal
    #Key([mod], "Return", lazy.spawn(terminal)),
# Qtile System Actions
    Key([mod, "control"], "r", lazy.restart()),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "m", lazy.window.toggle_fullscreen()),

# Active Window Actions
    # Key([mod], "m", lazy.window.toggle_fullscreen()),
    Key([mod], "q", lazy.window.kill()),
    Key([mod, "control"], "h",
        lazy.layout.grow_right(),
        lazy.layout.grow(),
        lazy.layout.increase_ratio(),
        lazy.layout.delete()
        ),
    Key([mod, "control"], "Right",
        lazy.layout.grow_right(),
        lazy.layout.grow(),
        lazy.layout.increase_ratio(),
        lazy.layout.delete()
        ),
    Key([mod, "control"], "l",
        lazy.layout.grow_left(),
        lazy.layout.shrink(),
        lazy.layout.decrease_ratio(),
        lazy.layout.add()
        ),
    Key([mod, "control"], "Left",
        lazy.layout.grow_left(),
        lazy.layout.shrink(),
        lazy.layout.decrease_ratio(),
        lazy.layout.add()
        ),
    Key([mod, "control"], "k",
        lazy.layout.grow_up(),
        lazy.layout.grow(),
        lazy.layout.decrease_nmaster()
        ),
    Key([mod, "control"], "Up",
        lazy.layout.grow_up(),
        lazy.layout.grow(),
        lazy.layout.decrease_nmaster()
        ),
    Key([mod, "control"], "j",
        lazy.layout.grow_down(),
        lazy.layout.shrink(),
        lazy.layout.increase_nmaster()
        ),
    Key([mod, "control"], "Down",
        lazy.layout.grow_down(),
        lazy.layout.shrink(),
        lazy.layout.increase_nmaster()
        ),

# Window Focus (Arrows and Vim keys)
    Key([mod], "Up", lazy.layout.up()),
    Key([mod], "Down", lazy.layout.down()),
    Key([mod], "Left", lazy.layout.left()),
    Key([mod], "Right", lazy.layout.right()),
    Key([mod], "k", lazy.layout.up()),
    Key([mod], "j", lazy.layout.down()),
    Key([mod], "h", lazy.layout.left()),
    Key([mod], "l", lazy.layout.right()),

# Qtile Layout Actions
    Key([mod], "r", lazy.layout.reset()),
    Key([mod], "Tab", lazy.next_layout()),
    Key([mod, "shift"], "f", lazy.layout.flip()),
    Key([mod, "shift"], "space", lazy.window.toggle_floating()),

# Move windows around MonadTall/MonadWide Layouts
    Key([mod, "shift"], "Up", lazy.layout.shuffle_up()),
    Key([mod, "shift"], "Down", lazy.layout.shuffle_down()),
    Key([mod, "shift"], "Left", lazy.layout.swap_left()),
    Key([mod, "shift"], "Right", lazy.layout.swap_right()),
# Change keyboard layout
	Key([mod1],"space", lazy.widget["keyboardlayout"].next_keyboard()),

 # Add this line to toggle between max and monadtall layout
    Key([mod], "space", lazy.next_layout(), desc="Toggle between max and monadtall layout"),
]
# Create labels for groups and assign them a default layout.
groups = []


group_names = ["1", "2", "3", "4", "5"]

group_labels = [" ", "󰨞 ", " ", " ", "󰓇 "]
#group_labels = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"]

group_layouts = ["monadtall", "monadtall", "monadtall", "monadtall", "max"]

# Add group names, labels, and default layouts to the groups object.
for i in range(len(group_names)):
    groups.append(
        Group(
            name=group_names[i],
            layout=group_layouts[i].lower(),
            label=group_labels[i],
        ))

# Add group specific keybindings
for i in groups:
    keys.extend([
        Key([mod], i.name, lazy.group[i.name].toscreen(), desc="Mod + number to move to that group."),
        Key(["mod1"], "Tab", lazy.screen.next_group(), desc="Move to next group."),
        Key(["mod1", "shift"], "Tab", lazy.screen.prev_group(), desc="Move to previous group."),
# MOVE WINDOW TO SELECTED WORKSPACE 1-10 AND STAY ON WORKSPACE
        Key([mod, "control"], i.name, lazy.window.togroup(i.name)),
# MOVE WINDOW TO SELECTED WORKSPACE 1-10 AND FOLLOW MOVED WINDOW TO WORKSPACE
        Key([mod, "shift"], i.name, lazy.window.togroup(i.name) , lazy.group[i.name].toscreen()),
    ])

# Define scratchpads
groups.append(ScratchPad("scratchpad", [
    DropDown("term", "kitty --class=scratch", width=0.8, height=0.8, x=0.1, y=0.1, opacity=0.9),
    DropDown("ranger", "kitty --class=ranger -e ranger", width=0.8, height=0.8, x=0.1, y=0.1, opacity=0.9),
    DropDown("news", "kitty --class=news -e newsboat", width=0.8, height=0.8, x=0.1, y=0.1, opacity=0.9),
    DropDown("catfish","catfish", width = 0.4, height=0.7, x=0.3, y=0.1,opacity=0.9 ),
    #DropDown("xdm","xdm-app", width = 0.3, height=0.7, x=0.4, y=0.1,opacity=0.9 ),
    #DropDown("notion", "brave-browser --app=https://notion.com", width = 0.4, height = 0.7, x = 0.3, y = 0.1, opacity = 0.9),
]))

# Scratchpad keybindings
keys.extend([
    Key([mod], "t", lazy.group['scratchpad'].dropdown_toggle('term')),
    Key([mod], "f", lazy.group['scratchpad'].dropdown_toggle('ranger')),
    Key([mod], "n", lazy.group['scratchpad'].dropdown_toggle('news')),
    Key([mod], "s", lazy.group['scratchpad'].dropdown_toggle('catfish')),
    #Key([mod], "x", lazy.group['scratchpad'].dropdown_toggle('xdm')),
    #Key([mod], "m", lazy.group['scratchpad'].dropdown_toggle('notion')),
])


# Define layouts and layout themes
layout_theme = {
        "margin":10,
        "border_width": 1,
        "border_focus": colors[2],
        "border_normal": backgroundColor
    }

layouts = [
    layout.MonadTall(**layout_theme),
    #layout.MonadWide(**layout_theme),
    layout.Floating(**layout_theme),
    #layout.RatioTile(**layout_theme),
    layout.Max(**layout_theme)
]

# Mouse callback functions
def launch_menu():
    qtile.cmd_spawn("rofi -show drun -show-icons")


# Define Widgets
widget_defaults = dict(
    font="IosevkaTerm Nerd Font",
    fontsize = 16,
    padding = 2,
    background=backgroundColor
)

def init_widgets_list(monitor_num):
    widgets_list = [
        widget.CurrentLayoutIcon(scale = 0.8, foreground = colors[4], background = colors[4]),
        widget.GroupBox(
            font="IosevkaTerm Nerd Font Bold",
            fontsize = 20,
            margin_y = 2,
            margin_x = 4,
            padding_y = 6,
            padding_x = 6,
            borderwidth = 2,
            disable_drag = True,
            active = colors[4],
            inactive = foregroundColor,
            hide_unused = False,
            rounded = False,
            highlight_method = "line",
            highlight_color = [backgroundColor, backgroundColor],
            this_current_screen_border = colors[5],
            this_screen_border = colors[7],
            other_screen_border = colors[6],
            other_current_screen_border = colors[6],
            urgent_alert_method = "line",
            urgent_border = colors[9],
            urgent_text = colors[1],
            foreground = foregroundColor,
            background = backgroundColor,
            use_mouse_wheel = False
        ),
        widget.Sep(linewidth = 1, padding = 10, foreground = colors[5],background = backgroundColor),
        #widget.TaskList(
         #   icon_size = 15,
          #  font = "IosevkaTerm Nerd Font Bold",
           # foreground = colors[0],
            #background = colors[2],
            #borderwidth = 0,
            #border = colors[6],
            #margin = 0,
            #padding = 8,
            #highlight_method = "block",
            #title_width_method = "uniform",
            #urgent_alert_method = "border",
            #urgent_border = colors[1],
            #rounded = False,
            #txt_floating = "🗗 ",
            #txt_maximized = "🗖 ",
            #txt_minimized = "🗕 ",
        #),
        widget.WindowName(
			font = "IosevkaTerm Nerd Font Bold",
			font_size = 17,
			foreground = foregroundColor,
			background = backgroundColor,
        ),
        widget.Sep(linewidth = 1, padding = 10, foreground = colors[0],background = colors[0]),
        widget.Sep(linewidth = 1, padding = 10, foreground = colors[0],background = backgroundColor),
        widget.Net(
            format='{down} ↓↑{up}',
            font = "IosevkaTerm Nerd Font Bold",
            foreground = foregroundColor,
            padding = 5,),
        widget.Sep(linewidth = 1, padding = 10, foreground = colors[5],background = colors[0]),
        widget.CPU(
            font = "IosevkaTerm Nerd Font Bold",
            update_interval = 1.0,
            foreground = foregroundColor,
            padding = 5,
            format = '{freq_current}/{load_percent}%',
        ),
        widget.TextBox(text = " 󰻠 ", fontsize = 16, font = "IosevkaTerm Nerd Font Bold", foreground = colors[7]),
        widget.Sep(linewidth = 1, padding = 10, foreground = colors[5],background = colors[0]),
        widget.Memory(
            font = "IosevkaTerm Nerd Font Bold",
            foreground = foregroundColor,
            format = '{MemPercent}%',
            measure_mem='G',
            padding = 5,
        ),
        widget.TextBox(text = " 󰍛 ", fontsize = 16, font = "IosevkaTerm Nerd Font Bold", foreground = colors[3]),
        widget.Sep(linewidth = 1, padding = 10, foreground = colors[5],background = colors[0]),
        widget.KeyboardLayout(
			configured_keyboards=['us','ar'],
			font = "IosevkaTerm Nerd Font Bold",
            foreground = foregroundColor, 
        ),
        widget.TextBox(text = "  ", fontsize = 16, font = "IosevkaTerm Nerd Font Bold", foreground = colors[6]),
        widget.Sep(linewidth = 1, padding = 10, foreground = colors[5],background = colors[0]),
        widget.Clock(format='%a %d %b  %H:%M', font = "IosevkaTerm Nerd Font Bold", padding = 10, foreground = foregroundColor),
        widget.TextBox(text = " ", fontsize = 16, font = "IosevkaTerm Nerd Font Bold", foreground = colors[10]),
        widget.Sep(linewidth = 1, padding = 10, foreground = colors[5],background = colors[0]),
        widget.UPowerWidget(
                        border_colour = '#d8dee9',
                        border_critical_colour = '#bf616a',
                        border_charge_colour = '#81a1c1',
                        fill_charge = '#a3be8c',
                        fill_low = '#ebcb8b',
                        fill_critical = '#bf616a',
                        fill_normal = '#d8dee9',
                        percentage_low = 0.4,
                        percentage_critical = 0.2,
                        font = "IosevkaTerm Nerd Font"
        ),
        widget.Systray(background = backgroundColor, icon_size = 20, padding = 4),
    ]

    return widgets_list

widgets_list = init_widgets_list("1")

screens = [
    Screen(top=bar.Bar(widgets=widgets_list, size=28, background=backgroundColor, margin=0, opacity=0.8),),
    ]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]

#@hook.subscribe.startup_once
#def autostart():
#home = os.path.expanduser('~/.config/qtile/scripts/autostart.sh')
#subprocess.run([home])

@hook.subscribe.startup_once
def start_once():
    home = os.path.expanduser('~')
    subprocess.call([home + '/.config/qtile/scripts/autostart.sh'])

dgroups_key_binder = None
dgroups_app_rules = []  # type: List
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(float_rules=[
    *layout.Floating.default_float_rules,
    Match(wm_class='confirmreset'),  # gitk
    Match(wm_class='makebranch'),  # gitk
    Match(wm_class='maketag'),  # gitk
    Match(wm_class='ssh-askpass'),  # ssh-askpass
    Match(title='branchdialog'),  # gitk
    Match(title='pinentry'),  # GPG key password entry
    Match(wm_class='xdm-app'),
], fullscreen_border_width = 0, border_width = 0)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

auto_minimize = True
wmname = "Qtile 0.21.0"
