# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from libqtile.config import Key, Screen, Group, Drag, Click
from libqtile.command import lazy
from libqtile import layout, bar, widget

mod = "mod4"
terminal = "gnome-terminal"
webbrowser = 'firefox'

keys = [
    # Switch between windows in current stack pane
    Key(
        [mod], "Down",
        lazy.layout.down()
    ),
    Key(
        [mod], "Up",
        lazy.layout.up()
    ),
    Key(
        [mod], "Left",
        lazy.layout.left()
    ),
    Key(
        [mod], "Right",
        lazy.layout.right()
    ),

    # Move windows up or down in current stack
    Key(
        [mod, "shift"], "Down",
        lazy.layout.shuffle_down()
    ),
    Key(
        [mod, "shift"], "Up",
        lazy.layout.shuffle_up()
    ),
    Key(
        [mod, "shift"], "Left",
        lazy.layout.swap_left()
    ),
    Key(
        [mod, "shift"], "Right",
        lazy.layout.swap_right()
    ),



    # Swap panes of split stack
    Key(
        [mod, "shift"], "space",
        lazy.layout.rotate()
    ),

    # Layout modification
    Key([mod], 'space', lazy.window.toggle_floating()),

    # Spawn a terminal
    Key([mod], "Return", lazy.spawn(terminal)),

    # Toggle fullscreen
    Key([mod], 'f', lazy.window.toggle_fullscreen()),

    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout()),

    Key([mod, 'shift'], "q", lazy.window.kill()),
    Key([mod, "shift"], "r", lazy.restart()),
    Key([mod, "shift"], "k", lazy.shutdown()),

    # Start dmenu to launch application
    # TODO: migrate to jmenu
    Key([mod], 'd', lazy.spawn('dmenu_run')),
]

autostart = {'1': terminal, '2': webbrowser}
groups = [Group(i, spawn=autostart.get(i)) for i in "123456789"]

for i in groups:
    grp = i.name
    key = "F%s" % i.name

    keys.append(
        Key([mod], key, lazy.group[grp].toscreen())
    )
    keys.append(
        Key([mod, "shift"], key, lazy.window.togroup(grp))
    )

layouts = [
#    layout.TreeTab(),
    layout.xmonad.MonadTall(ratio=0.50),
    layout.Matrix(),
]

flat_theme = {"bg_dark": ["#606060", "#000000"],
              "bg_light": ["#707070", "#303030"],
              "font_color": ["#ffffff", "#cacaca"],

              # groupbox
              "gb_selected": ["#7BA1BA", "#215578"],
              "gb_urgent": ["#ff0000", "#820202"]
              }

theme = flat_theme

widget_defaults = dict(background=theme["bg_light"],
                       opacity=0.9,
                       border_color="#6f6f6f",
                       fontshadow="#000000",
                       foreground=theme["font_color"],
                       fontsize=13,
                       font="Anonymous Pro",
)

screens = [
    Screen(
        top=bar.Bar(
            [
                widget.GroupBox(),
                widget.TextBox(text="", name="info"),
                widget.TextBox(text=u"◥", fontsize=40, padding=-1,
                               font="Arial",
                               foreground=theme["bg_dark"]),
                widget.MemoryGraph(width=42, line_width=2,
                                   graph_color='#22BB44',
                                   fill_color=['#11FF11', "#002200"],
                                   border_width=1,
                                   background=theme["bg_dark"],
                ),
                widget.TextBox(text=u" ", background=theme["bg_dark"]),
                widget.TextBox(text=u"◣", fontsize=40, padding=-1,
                   font="Arial",
                   foreground=theme["bg_dark"]),
                widget.Volume(update_interval=0.2, emoji=True),
                widget.Systray(icon_size=14),
                widget.Clock(format='%Y-%m-%d %a %I:%M %p'),
            ],
            24, opacity=0.9
        ),
    ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
        start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
        start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]

dgroups_key_binder = None
dgroups_app_rules = []
main = None
follow_mouse_focus = False
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating()
auto_fullscreen = True
focus_on_window_activation = "smart"

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, github issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
