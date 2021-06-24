#!/usr/bin/python3

#Phosh_look GPL3
#Copyright (C) 2019-2021 David Hamner
#Copyright (C) 2020 Tobias Frisch (Based on Phonic)

#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.

#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.

#You should have received a copy of the GNU General Public License
#along with this program. If not, see <http://www.gnu.org/licenses/>.
import os
import operator
import re
import subprocess
import threading
import time
import shutil

from gi import require_version
require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib
from gi.repository.GdkPixbuf import Pixbuf, InterpType

script_path = os.path.dirname(os.path.realpath(__file__))

#########################DEFINE Globals##########################
selected_file = None


#########################DEFINE Functions########################
def load_ui_parts(dropdown):
    with open(script_path + "/ui_parts.txt") as ui_fh:
        ui_parts = ui_fh.readlines()
        for ui_part in ui_parts:
            dropdown.append_text(ui_part)

def load_preset_themes(dropdown):
    global themes
    global theme_order
    css_path = "/home/purism/.config/gtk-3.0"

    path = script_path + "/themes"
    themes = {}
    for root, directories, files in os.walk(path, topdown=False):
        for name in directories:
            themes[name] = os.path.join(root, name)
    
    for theme in themes.keys():
        dropdown.append_text(theme)
    
    theme_order = list(themes.keys())
    #set active
    if os.path.islink(css_path):
        link_path = os.readlink(css_path)
        print(link_path)
        name = link_path.split("/")[-1]
        index = theme_order.index(name)
        dropdown.set_active(index)
    else:
        index = theme_order.index("defualt")
        dropdown.set_active(index)
    
    #dropdown.append_text("custom")
#########################DEFINE Handlers#########################

def on_destroy(phosh_look_window):
    
    Gtk.main_quit()


def apply_and_restart(apply_button):
    global preset_theme
    global theme_order
    global script_path
    
    selected_theme_index = preset_theme.get_active()
    selected_theme = theme_order[selected_theme_index]
    link_source = f"{script_path}/themes/{selected_theme}"
    link_target = "/home/purism/.config/gtk-3.0"
    backup_dir = "/home/purism/.config/gtk-3.0_backup"
    gtk_theme_file = open(f"{link_source}/gtk_theme")
    gtk_theme = gtk_theme_file.readlines()[0].strip()
    print(gtk_theme)
    
    #clean up old stuff
    if os.path.islink(link_target):
        os.remove(link_target)
    elif os.path.isdir(link_target):
        if os.path.isdir(backup_dir):
            shutil.rmtree(backup_dir)
        shutil.move(link_target, backup_dir)
        print(f"Moved GTK folder to {backup_dir}")

    
    #make new link
    os.symlink(link_source, link_target)
    print(selected_theme)
    
    #set gtk theme
    os.system(f"gsettings set org.gnome.desktop.interface gtk-theme '{gtk_theme}'")
    
    #restart UI
    os.system("sudo systemctl restart phosh")

##########################INIT Handlers##########################
handlers = {
    "on_apply_activate": apply_and_restart,
    "on_destroy": on_destroy,
}


###########################INIT Window###########################
builder = Gtk.Builder()
builder.add_from_file(script_path + '/phosh_look.glade')
builder.connect_signals(handlers)

phosh_look_window = builder.get_object('phosh_look_window')
files_store = builder.get_object('files_store')

#page_stack = builder.get_object('page_stack')
main_page = builder.get_object('main_page')
preset_theme = builder.get_object('preset_theme')
selected_ui_element = builder.get_object('selected_ui_element')
#load_ui_parts(selected_ui_element) #Not used yet
load_preset_themes(preset_theme)
#settings_page = builder.get_object('settings_page')
#files_page = builder.get_object('files_page')

#title_label = builder.get_object('title_label')
#chapter_progress = builder.get_object('chapter_progress')
#audiobook_progress = builder.get_object('audiobook_progress')

phosh_look_window.show_all()
Gtk.main()

