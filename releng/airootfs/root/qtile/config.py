from typing import List  # noqa: F401
from libqtile import bar, layout, widget, hook, qtile
from libqtile.config import Click, Drag, Group, Key, Screen, KeyChord
from libqtile.lazy import lazy
import os, subprocess

mod = 'mod4'
term = 'termite'

keys = [
    ### Window controls
    # Switch between windows in current stack pane
    Key([mod], 'j', lazy.layout.down()),
    Key([mod], 'k', lazy.layout.up()),
    # Move windows up or down in current stack
    Key([mod, 'control'], 'j', lazy.layout.shuffle_down()),
    Key([mod, 'control'], 'k', lazy.layout.shuffle_up()),
    # Switch window focus to other pane(s) of stack
    Key([mod], 'space', lazy.layout.next()),
    # Swap panes
    Key(['control', 'shift'], 'space', lazy.layout.shuffle_up()),
    # Grow and shrink
    Key(['control', 'shift'], 'p', lazy.layout.grow()),
    Key(['control', 'shift'], 'm', lazy.layout.shrink()),

    ### System
    Key([mod], 'Return', lazy.spawn(term)),
    Key([mod], 'Tab', lazy.next_layout()),
    Key([mod, 'shift'], 'q', lazy.window.kill()),
    Key([mod, 'control'], 'r', lazy.restart()),
    Key([mod, 'control'], 'e', lazy.spawn('~./scripts/power_menu.sh')),
    Key([mod], 'r', lazy.spawncmd()),
    Key([mod], 'd', lazy.spawn('dmenu_run -fn "Monospace Bold 14" -p "Run: "')),
    Key([mod], 'g', lazy.spawn('gammy')),
    Key(['control'], 'space', lazy.spawn('rofi -show combi')),
    Key(['control'], 's', lazy.spawn('steam')),

    ### My Applications
    Key([mod], 'w', lazy.spawn('qutebrowser')),
    Key(['control'], 'f', lazy.spawn('librewolf')),
    Key(['control'], 'b', lazy.spawn('brave')),
    Key([mod, 'shift'], 'f', lazy.spawn(term + ' -e ranger')),
    Key(['control'], 'm', lazy.spawn(term + ' -e ncmpcpp')),

    ### Function Keys
    Key([], 'F2', lazy.spawn('xbacklight -inc -10')),
    Key([], 'F3', lazy.spawn('xbacklight -inc +10')),
    Key([], 'F4', lazy.spawn('./scripts/search.sh')),
    # Key([], 'F5', lazy.spawn('i3exit blurlock')), currently don't have lock screen
    Key([], 'F6', lazy.spawn('pactl set-sink-mute 0 toggle'),
                  lazy.spawn('pactl set-sink-mute 1 toggle'),
                  lazy.spawn('pactl set-sink-mute 2 toggle')),
    Key([], 'F7', lazy.spawn('pactl set-sink-volume 0 -5%'),
                  lazy.spawn('pactl set-sink-volume 1 -5%'),
                  lazy.spawn('pactl set-sink-volume 2 -5%')),
    Key([], 'F8', lazy.spawn('pactl set-sink-volume 0 +5%'),
                  lazy.spawn('pactl set-sink-volume 1 +5%'),
                  lazy.spawn('pactl set-sink-volume 2 +5%')),
    Key([], 'F9', lazy.spawn(term + ' -e ncmpcpp')),
    Key([], 'F10', lazy.spawn('mpc prev')),
    Key([], 'F11', lazy.spawn('mpc toggle')),
    Key([], 'F12', lazy.spawn('mpc next')),


]

### Color scheme
colors = [
        'ee4266',   #focused window color
        '0f4c5c',   #background color
        '540d6e',   #inactove workspaces
        '3bceac',   #active workspaces
        '0ead69',   #activer font
        'ff70a6',   #even widgets font
        'e9ff70',   #odd widgets font
         ]

### Groups
grps = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'IIX', 'IX']
groups = [Group(i) for i in grps]
grplist = []
for i in range(len(groups) + 1):
    grplist.append(i)
grplist.remove(0)

for i, j in zip(grplist, groups):
    keys.extend([
        # switch to group
        Key([mod], str(i), lazy.group[j.name].toscreen()),
        # moves window without changing focus
        Key([mod, 'shift'], str(i), lazy.window.togroup(j.name)),
        # moves window and changes focus
        Key(['mod1', 'shift'], str(i), lazy.window.togroup(j.name, switch_group = True)),
                ])

### Layouts

#Theme
theme = {
        'border_width': 3,
        'margin': 8,
        'border_focus': colors[0],
        'border_normal': '140100'
        }

# Layouts
layouts = [
    # layout.Bsp(),
    # layout.Col:set numbermns(),
    # layout.Matrix(),
    layout.MonadTall(**theme),
    layout.MonadWide(**theme),
    # layout.RatioTile(),
    # layout.Tile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    layout.Zoomy(**theme),
    layout.Max(**theme)

]

widget_defaults = dict(
    font='Monospace Bold',
    fontsize=14,
    padding=3,
    background = colors[1],
)
extension_defaults = widget_defaults.copy()

screens = [
    Screen(
        top=bar.Bar(
            [
                widget.Image(
                    filename = '~/.config/qtile/icons/arch.png'
                            ),
                widget.CurrentLayout(
                                    foreground = colors[5],
                                    ),
                widget.GroupBox(
                              rounded = True,
                              active = colors[3],
                              inactive = colors[2],
                              highlight_color = colors[1],
                              highlight_method = 'line',
                              hide_unused = True,
                              this_current_screen_border = colors[6],
                               ),
                widget.Prompt(),
                widget.WindowName(
                                foreground = colors[6],
                                 ),
                widget.TextBox(
                                text = 'Vol: ',
                                foreground = colors[5],
                                mouse_callbacks = {'Button3': lambda: qtile.cmd_spawn('pavucontrol')}
                              ),
                widget.PulseVolume(
                                foreground = colors[5],
                                  ),
                widget.Battery(
                                foreground = colors[6],
                                format = '{percent:2.0%} {watt:.2f} W',
                                mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn('xfce4-power-manager-settings'),
                                                   'Button2': lambda: qtile.cmd_spawn('xfce4-power-manager')
                                                   },
                              ),

                widget.Systray(),
                widget.Clock(
                    format='%a %H:%M:%S %d/%m/%Y',
                    foreground = colors[5],
                            ),
                widget.TextBox(
                    text = 'Simone',
                    foreground = colors[6],
                    mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn('./scripts/power_menu.sh')}
                                ),
            ],
            24,
        ),
        bottom = bar.Bar([
            widget.Image(
                filename = '~/.config/qtile/icons/hard-drive.png',
                        ),
            widget.DF(
                warn_space = 1000,
                warn_color = colors[5],
                format = '({uf}{m}|{r:.0f}%)',
                     ),
            widget.Image(
                filename = '~/.config/qtile/icons/turntable.png',
                        ),
            widget.DF(
                warn_space = 1000,
                warn_color = colors[6],
                format = '({uf}{m}|{r:.0f}%)',
                partition = '/backup',
                     ),
            widget.DF(
                warn_space = 1000,
                warn_color = colors[5],
                format = '({uf}{m}|{r:.0f}%)',
                partition = '/home/simone/storage',
                     ),

            widget.Spacer(),
            widget.Spacer(),
            widget.NvidiaSensors(
                foreground = colors[6],
                ),
            widget.Image(
                filename = '~/.config/qtile/icons/computer-chip-8.png',
                        ),
            widget.ThermalSensor(
                    foreground = colors[5],
                    tag_sensor = 'Core 0',
                    #mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn(term + ' -e sensors')},
                ),
            widget.CPU(
                foreground = colors[5],
                mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn(term + ' -e htop')},
                      ),
            widget.Image(
                filename = '~/.config/qtile/icons/computer-ram.png',
                        ),
            widget.Memory(
                foreground = colors[6],
                format = '{MemUsed:.0f} M',
                mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn(term + ' -e htop')},
                         ),
            widget.Sep(
                foreground = colors[1],
                linewidth = 3,
                      ),
            widget.Image(
                filename = '~/.config/qtile/icons/network-arrow-sync.png',
                        ),
            widget.Net(
                foreground = colors[5],
                format = 'd:{down} u:{up}',
                mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn(term + ' -e nmtui')},
                      ),

            ],
            24,
            ),
    ),
    Screen(
        top=bar.Bar(
            [
                widget.Image(
                    filename = '~/.config/qtile/icons/arch.png'
                            ),
                widget.CurrentLayout(
                                    foreground = colors[5],
                                    ),
                widget.GroupBox(
                              rounded = True,
                              active = colors[3],
                              inactive = colors[2],
                              highlight_color = colors[1],
                              highlight_method = 'line',
                              hide_unused = True,
                              this_current_screen_border = colors[6],
                               ),

                widget.Prompt(),
                widget.WindowName(
                                foreground = colors[6],
                                 ),
                widget.TextBox(
                                text = 'Vol: ',
                                foreground = colors[5],
                                mouse_callbacks = {'Button3': lambda: qtile.cmd_spawn('pavucontrol')}
                              ),
                widget.PulseVolume(
                                foreground = colors[5],
                                  ),
                widget.Battery(
                                foreground = colors[6],
                                format = '{percent:2.0%} {watt:.2f} W',
                                mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn('xfce4-power-manager-settings'),
                                                   'Button2': lambda: qtile.cmd_spawn('xfce4-power-manager')
                                                   },
                              ),

                widget.Clock(
                    format='%a %H:%M:%S %d/%m/%Y',
                    foreground = colors[5],
                            ),
                widget.TextBox(
                    text = 'Simone',
                    foreground = colors[6],
                    mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn('./scripts/power_menu.sh')},
                                ),
            ],
            24,
        ),
        bottom = bar.Bar([
            widget.Image(
                filename = '~/.config/qtile/icons/hard-drive.png',
                        ),
            widget.DF(
                warn_space = 1000,
                warn_color = colors[5],
                format = '({uf}{m}|{r:.0f}%)',
                     ),
            widget.Image(
                filename = '~/.config/qtile/icons/turntable.png',
                        ),
            widget.DF(
                warn_space = 1000,
                warn_color = colors[6],
                format = '({uf}{m}|{r:.0f}%)',
                partition = '/backup',
                     ),
            widget.DF(
                warn_space = 1000,
                warn_color = colors[5],
                format = '({uf}{m}|{r:.0f}%)',
                partition = '/home/simone/storage',
                     ),

            widget.Spacer(),
            widget.Spacer(),
            widget.NvidiaSensors(
                foreground = colors[6],
                format = '{temp}°C {perf}',
                ),
            widget.Image(
                filename = '~/.config/qtile/icons/computer-chip-8.png',
                        ),
            widget.ThermalSensor(
                    foreground = colors[5],
                    tag_sensor = 'Core 0',
                    ),
            widget.CPU(
                foreground = colors[5],
                mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn(term + ' -e htop')},
                      ),
            widget.Image(
                filename = '~/.config/qtile/icons/computer-ram.png',
                        ),
            widget.Memory(
                foreground = colors[6],
                format = '{MemUsed:.0f} M',
                mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn(term + ' -e htop')},
                         ),
            widget.Sep(
                foreground = colors[1],
                linewidth = 3,
                      ),
            widget.Image(
                filename = '~/.config/qtile/icons/network-arrow-sync.png',
                        ),
            widget.Net(
                foreground = colors[5],
                format = 'd:{down} u:{up}',
                      ),

            ],
            24,
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
dgroups_app_rules = []  # type: List
main = None  # WARNING: this is deprecated and will be removed soon
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(float_rules=[
    # Run the utility of `xprop` to see the wm class and name of an X client.
    {'wmclass': 'confirm'},
    {'wmclass': 'dialog'},
    {'wmclass': 'download'},
    {'wmclass': 'error'},
    {'wmclass': 'file_progress'},
    {'wmclass': 'notification'},
    {'wmclass': 'splash'},
    {'wmclass': 'toolbar'},
    {'wmclass': 'confirmreset'},  # gitk
    {'wmclass': 'makebranch'},  # gitk
    {'wmclass': 'maketag'},  # gitk
    {'wname': 'branchdialog'},  # gitk
    {'wname': 'pinentry'},  # GPG key password entry
    {'wmclass': 'ssh-askpass'},  # ssh-askpass
])
auto_fullscreen = True
focus_on_window_activation = "smart"

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"

@hook.subscribe.startup_once
def autostart():
    home = os.path.expanduser('~')
    subprocess.call([home + '/.config/qtile/autostart.sh'])
