import os
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

apps = [
    "7zFM",
    "Affinity Designer",
    "Affinity Photo",
    "AMD Ryzen Master",
    "Atom",
    "Audacity",
    "Blender",
    "Canon Import Utility",
    "Celestia",
    "Chrome",
    "Cisco VPN",
    "CPUZ",
    "Discord",
    "DOOM",
    "Emacs",
    "Excel",
    "Explorer",
    "Filezilla",
    "Firefox",
    "FurMark",
    "Geany",
    "Gimp",
    "Gitg",
    "Gnome Tweak Tools",
    "Google Keep",
    "Inkscape",
    "Internet Explorer 6",
    "ITunes",
    "Java 6",
    "Krita",
    "LibreOffice Calc",
    "LibreOffice Writer",
    "Mathematica",
    "Matlab",
    "MSYS2",
    "Mumble",
    "mySQLWorkbench",
    "Notepad",
    "Notepad++",
    "OBS Studio",
    "Outlook",
    "Oxygen",
    "Paint",
    "pgAdmin",
    "PowerPoint",
    "Prime95",
    "PuTTY",
    "Pycharm",
    "Python2.7",
    "Python3.6",
    "R Studio",
    "Rider",
    "RStudio",
    "Skype",
    "Steam",
    "Teamviewer",
    "Terminal",
    "Texmaker",
    "Thunderbird",
    "Tixati",
    "Transmission",
    "Visual Studio",
    "VLC Player",
    "WinAmp",
    "Word"
]

to_select = [54, 33, 6, 19, 21, 64, 26, 34, 12, 53]


class LongList:

    def __init__(self):
        # GTK initialization
        builder = Gtk.Builder()
        builder.add_from_file("longlist.glade")
        builder.connect_signals(self)
        # Collect view elements
        self.currentApp = builder.get_object("currentApp")
        listmodel = builder.get_object("applicationsStore")
        treeview = builder.get_object("applicationsView")
        window = builder.get_object("mainWindow")
        # Prepare other application state
        self.running = False
        # Add applications to the list model
        for a in apps:
            listmodel.append([a])
        # Render items in tree view
        col = Gtk.TreeViewColumn("Name", Gtk.CellRendererText(), text=0)
        treeview.append_column(col)
        # Display window
        window.show_all()

    def onSelectionChanged(self, selection):
        (model, iter) = selection.get_selected()
        if (
            self.running and
            iter != None and
            model[iter][0] == apps[to_select[0]]
        ):
            # Since the user selected it, remove from to_select
            del to_select[0]
            # Request the next selection
            self.show_next_element()

    def onButtonPressed(self, button):
        # Start evaluation
        self.running = True
        self.show_next_element()

    def onDeleteWindow(self, *args):
        Gtk.main_quit(*args)

    def show_next_element(self):
        if len(to_select) > 0:
            # Show the next application to select
            self.currentApp.set_text(apps[to_select[0]])
        else:
            # User has selected everything, finish evaluation
            self.running = False
            print("Done")


if __name__ == "__main__":
    LongList()
    Gtk.main()
