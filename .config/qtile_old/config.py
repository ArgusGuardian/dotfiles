##########################
# title: qtile           #
# tags: config.py        #
# author: Alaa eddine    #
##########################

import os
import re
import socket
import subprocess
from typing import List
from libqtile import layout, bar, widget, hook
from libqtile.config import Click, Drag, Group, Key, Match, Screen, Rule
from libqtile.command import lazy
from libqtile.widget import Spacer
from qtile_extras import widget
from qtile_extras.widget.decorations import BorderDecoration
from qtile_extras.widget.decorations import RectDecoration

# Set the GTK theme
os.environ['GTK2_RC_FILES'] = "/home/alaa/.gtkrc-2.0"
os.environ['GTK_THEME'] = "Nordic-darker"

#mod4 or mod = super key
mod = "mod1"
mod1 = "alt"
mod2 = "control"
mod4="mod4"
home = os.path.expanduser('~')


@lazy.function
def window_to_prev_group(qtile):
    if qtile.currentWindow is not None:
        i = qtile.groups.index(qtile.currentGroup)
        qtile.currentWindow.togroup(qtile.groups[i - 1].name)

@lazy.function#
def window_to_next_group(qtile):
    if qtile.currentWindow is not None:
        i = qtile.groups.index(qtile.currentGroup)
        qtile.currentWindow.togroup(qtile.groups[i + 1].name)

keys = [

# SUPER + FUNCTION KEYS

    Key([mod], "m", lazy.window.toggle_fullscreen()),
    Key([mod], "q", lazy.window.kill()),


# SUPER + SHIFT KEYS

    Key([mod, "shift"], "r", lazy.restart()),


# QTILE LAYOUT KEYS
    Key([mod], "space", lazy.next_layout()),

# CHANGE FOCUS
    Key([mod], "Up", lazy.layout.up()),
    Key([mod], "Down", lazy.layout.down()),
    Key([mod], "j", lazy.layout.left()),
    Key([mod], "k", lazy.layout.right()),

# RESIZE UP, DOWN, LEFT, RIGHT
    Key([mod], "l",
        lazy.layout.grow_right(),
        lazy.layout.grow(),
        lazy.layout.increase_ratio(),
        lazy.layout.delete(),
        ),
    Key([mod], "h",
        lazy.layout.grow_left(),
        lazy.layout.shrink(),
        lazy.layout.decrease_ratio(),
        lazy.layout.add(),
        ),
    Key([mod, "control"], "Up",
        lazy.layout.grow_up(),
        lazy.layout.grow(),
        lazy.layout.decrease_nmaster(),
        ),
    Key([mod, "control"], "Down",
        lazy.layout.grow_down(),
        lazy.layout.shrink(),
        lazy.layout.increase_nmaster(),
        ),


# FLIP LAYOUT FOR MONADTALL/MONADWIDE
    Key([mod, "shift"], "f", lazy.layout.flip()),

# MOVE WINDOWS UP OR DOWN MONADTALL/MONADWIDE LAYOUT
    Key([mod, "shift"], "Up", lazy.layout.shuffle_up()),
    Key([mod, "shift"], "Down", lazy.layout.shuffle_down()),
    Key([mod, "shift"], "Left", lazy.layout.swap_left()),
    Key([mod, "shift"], "Right", lazy.layout.swap_right()),

# TOGGLE FLOATING LAYOUT
    Key([mod, "shift"], "space", lazy.window.toggle_floating()),

# SHUTDOWN QTILE
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),

# CHANGE KEYBOARD LAYOUT
    Key([mod4], "space",  lazy.widget["keyboardlayout"].next_keyboard()),

    ]

def window_to_previous_screen(qtile, switch_group=False, switch_screen=False):
    i = qtile.screens.index(qtile.current_screen)
    if i != 0:
        group = qtile.screens[i - 1].group.name
        qtile.current_window.togroup(group, switch_group=switch_group)
        if switch_screen == True:
            qtile.cmd_to_screen(i - 1)

def window_to_next_screen(qtile, switch_group=False, switch_screen=False):
    i = qtile.screens.index(qtile.current_screen)
    if i + 1 != len(qtile.screens):
        group = qtile.screens[i + 1].group.name
        qtile.current_window.togroup(group, switch_group=switch_group)
        if switch_screen == True:
            qtile.cmd_to_screen(i + 1)


groups = []

# FOR QWERTY KEYBOARDS
group_names = ["1", "2", "3", "4"]

group_labels = ["  ", " 󰅩 ", " 󰙯 ", " 󰅶 "]
#group_labels = ["web", "dev", "sys", "doc", "file", "vbox", "edit", "photos", "vid", "gfx",]

group_layouts = ["monadtall", "monadtall", "monadtall", "max"]

for i in range(len(group_names)):
    groups.append(
        Group(
            name=group_names[i],
            layout=group_layouts[i].lower(),
            label=group_labels[i],
        ))

for i in groups:
    keys.extend([

#CHANGE WORKSPACES
        Key([mod], i.name, lazy.group[i.name].toscreen()),
        Key([mod], "Tab", lazy.screen.next_group()),
        Key([mod, "shift" ], "Tab", lazy.screen.prev_group()),

# MOVE WINDOW TO SELECTED WORKSPACE 1-10 AND STAY ON WORKSPACE
        Key([mod, "control"], i.name, lazy.window.togroup(i.name)),
# MOVE WINDOW TO SELECTED WORKSPACE 1-10 AND FOLLOW MOVED WINDOW TO WORKSPACE
        Key([mod, "shift"], i.name, lazy.window.togroup(i.name) , lazy.group[i.name].toscreen()),
    ])


def init_layout_theme():
    return {"margin":10,
            "border_width":1,
            "border_focus": "#FF5F00",
            "border_normal": "#2E3440"
            }

layout_theme = init_layout_theme()


layouts = [
    layout.MonadTall(**layout_theme, new_client_position='top'),
    layout.Max()
]

# COLORS FOR THE BAR
def init_colors():
    return [["#D8DEE9", "#D8DEE9"], # color 0
            ["#2E3440", "#2E3440"], # color 1
            ["#4C566A", "#4C566A"], # color 2
            ["#A3BE8C", "#A3BE8C"], # color 3
            ["#EBCB8B", "#EBCB8B"], # color 4
            ["#5E81AC", "#5E81AC"], # color 5
            ["#BF616A", "#BF616A"], # color 6
            ["#81A1C1", "#81A1C1"], # color 7
            ["#FF9758", "#FF9758"], # color 8
            ["#FF5F00", "#FF5F00"]] # color 9


colors = init_colors()


# WIDGETS FOR THE BAR

def init_widgets_defaults():
    return dict(font="IosevkaTerm Nerd Font",
                fontsize = 16,
                padding = 2,
                background=colors[1])

widget_defaults = init_widgets_defaults()

def init_widgets_list():
    prompt = "{0}@{1}: ".format(os.environ["USER"], socket.gethostname())
    widgets_list = [
               widget.Sep(
                        linewidth = 1,
                        padding = 5,
                        foreground = colors[2],
                        background = colors[1]
                        ),
               widget.CurrentLayoutIcon(
                        padding = 4,
                        scale = 0.8,
                        ),
               widget.Sep(
                        linewidth = 1,
                        padding = 5,
                        foreground = colors[2],
                        background = colors[1]
                        ),
               widget.GroupBox(
                        font="IosevkaTerm Nerd Font Bold",
                        fontsize = 20,
                        margin_y = 2, # was 2
                        margin_x = 3, # was 3
                        padding_y = 2,
                        padding_x = 3,
                        borderwidth = 0,
                        disable_drag = True,
                        active = colors[8],
                        inactive = colors[2],
                        rounded = False,
                        highlight_method = "text",
                        this_current_screen_border = colors[9],
                        foreground = colors[2],
                        background = colors[1],
                        # decorations = [   # from here 
                        #    RectDecoration (
                        #        colour = colors[5],
                        #        padding_y = 5,
                        #        radius = 2,
                        #        filled = True
                        #    ),
                        # ], # to here was commented
                        ),
               widget.Sep(
                        linewidth = 1,
                        padding = 5,
                        background = colors[1],
                        foreground = colors[2],
                        ),
               widget.WindowName(
                        font="IosevkaTerm Nerd Font Bold",
                        fontsize = 17,
                        foreground = colors[0],
                        background = colors[1],
                        #decorations = [
                        #    RectDecoration (
                        #        colour = colors[5],
                        #        padding_y = 5,
                        #        radius = 2,
                        #        filled = True
                        #    ),
                        #    ],
                            ),
            #    widget.Sep(
            #             foreground = colors[2],
            #             background = colors[1],
            #             padding = 5,
            #             linewidth = 1
            #             ),
            #    widget.Net(
            #             foreground = colors[0],
            #             background = colors[1],
            #             font = 'IosevkaTerm Nerd Font Bold',
            #             fontsize = 16,
            #             format = '{down} ↓↑ {up}',
            #             interface = 'wlan0',
            #             decorations = [
            #                 RectDecoration (
            #                     colour = colors[1],
            #                     padding_y = 5,
            #                     radius = 2,
            #                     filled = True
            #                 ),
            #             ],
            #             ),
               widget.Sep(
                        linewidth = 1,
                        padding = 5,
                        foreground = colors[2],
                        background = colors[1]
                        ),
               widget.CPU(
                        background = colors[1],
                        foreground = colors[0],
                        font = "IosevkaTerm Nerd Font Bold",
                        fontsize = 16,
                        decorations = [
                            RectDecoration (
                                colour = colors[1],
                                padding_y = 5,
                                radius = 2,
                                filled = True
                            ),
                        ],
                        ),
               widget.Sep(
                        linewidth = 1,
                        padding = 5,
                        foreground = colors[2],
                        background = colors[1]
                        ),
               widget.Memory(
                        measure_mem = 'G',
                        foreground = colors[0],
                        background = colors[1],
                        font = "IosevkaTerm Nerd Font Bold",
                        fontsize = 16,
                        decorations = [
                            RectDecoration (
                                colour = colors[1],
                                padding_y = 5,
                                radius = 2,
                                filled = True
                                ),
                        ],
                        ),
            #    widget.Sep(
            #             linewidth = 1,
            #             padding = 5,
            #             foreground = colors[2],
            #             background = colors[1]
            #             ),
            #    widget.DF(
            #             visible_on_warn = False,
            #             background = colors[1],
            #             foreground = colors[0],
            #             font = "IosevkaTerm Nerd Font Bold",
            #             fontsize = 16,
            #             decorations = [
            #                 RectDecoration (
            #                     colour = colors[1],
            #                     padding_y = 5,
            #                     radius = 2,
            #                     filled = True
            #                 ),
            #             ],
            #             ),
               widget.Sep(
                        linewidth = 1,
                        padding = 5,
                        background = colors[1],
                        foreground = colors[2]
                        ),
               widget.KeyboardLayout(configured_keyboards=['us','ar']),         
               widget.Sep(
                        linewidth = 1,
                        padding = 5,
                        background = colors[1],
                        foreground = colors[2]
                        ),         
               widget.Clock(
                        foreground = colors[0],
                        background = colors[1],
                        font = "IosevkaTerm Nerd Font Bold",
                        fontsize = 16,
                        format = "%a %d %b %H:%M",
                        decorations = [
                            RectDecoration (
                                colour = colors[1],
                                padding_y = 5,
                                radius = 2,
                                filled = True
                            ),
                        ],
                        ),
               widget.Sep(
                        linewidth = 1,
                        padding = 5,
                        foreground = colors[2],
                        background = colors[1]
                        ),
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
                widget.Systray(
                        background = colors[1],
                        icon_size = 20,
                        padding = 4
                        ),
                # widget.Sep(
                #         linewidth = 1,
                #         padding = 5,
                #         foreground = colors[2],
                #         background = colors[1] 
                #         ),
                # widget.OpenWeather(
                #         app_key = "4cf3731a25d1d1f4e4a00207afd451a2",
                #         cityid = "4997193",
                #         format = '{main_temp}° {icon}',
                #         metric = False,
                #         font = "IosevkaTerm Nerd Font Bold",
                #         fontsize = 16,
                #         background = colors[1],
                #         foreground = colors[0],
                #         decorations = [
                #             RectDecoration (
                #                 colour = colors[1],
                #                 padding_y = 5,
                #                 radius = 2,
                #                 filled = True 
                #             ),
                #         ],
                #         ),
                widget.Sep(
                        linewidth = 1,
                        padding = 5,
                        background = colors[1],
                        foreground = colors[2]
                        ),
              ]
    return widgets_list

widgets_list = init_widgets_list()


def init_widgets_screen1():
    widgets_screen1 = init_widgets_list()
    return widgets_screen1


widgets_screen1 = init_widgets_screen1()


def init_screens():
    return [Screen(top=bar.Bar(widgets=init_widgets_screen1(), size=28, opacity=1.0))]
screens = init_screens()


# MOUSE CONFIGURATION
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size())
]

dgroups_key_binder = None
dgroups_app_rules = []


main = None

@hook.subscribe.startup_once
def start_once():
    home = os.path.expanduser('~')
    subprocess.call([home + '/.config/qtile/scripts/autostart.sh'])

@hook.subscribe.startup
def start_always():
    # Set the cursor to something sane in X
    subprocess.Popen(['xsetroot', '-cursor_name', 'left_ptr'])

@hook.subscribe.client_new
def set_floating(window):
    if (window.window.get_wm_transient_for()
            or window.window.get_wm_type() in floating_types):
        window.floating = True

floating_types = ["notification", "toolbar", "splash", "dialog"]


follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(float_rules=[
    # Run the utility of `xprop` to see the wm class and name of an X client.
    *layout.Floating.default_float_rules,
    Match(wm_class='dialog'),
    Match(wm_class='download'),
    Match(wm_class='error'),
    Match(wm_class='file_progress'),
    Match(wm_class='notification'),
    Match(wm_class='splash'),
    Match(wm_class='toolbar'),
    Match(wm_class='Arandr'),
    Match(wm_class='feh'),

], fullscreen_border_width = 0, border_width = 0)
auto_fullscreen = True

focus_on_window_activation = "focus" # or smart

wmname = "LG3D"
