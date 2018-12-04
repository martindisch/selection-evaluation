import time
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
apps_short = [
    "Audacity",
    "Discord",
    "Firefox",
    "FurMark",
    "Gimp",
    "Internet Explorer 6",
    "Matlab",
    "Paint",
    "PowerPoint",
    "Skype",
    "Steam",
    "Terminal",
    "Thunderbird",
    "Word"
]
to_select = [
    "Steam",
    "Matlab",
    "Blender",
    "FurMark",
    "Gimp",
    "Word",
    "Internet Explorer 6",
    "MSYS2",
    "Discord",
    "Skype"
]

class ListEval:

    def __init__(self):
        # GTK initialization
        builder = Gtk.Builder()
        builder.add_from_file("listeval.glade")
        builder.connect_signals(self)
        # Collect view elements
        self.currentApp = builder.get_object("currentApp")
        self.subjectAge = builder.get_object("subjectAge")
        self.selectionStack = builder.get_object("selectionStack")
        listmodel = builder.get_object("applicationsStore")
        listmodel_short = builder.get_object("applicationsStoreShort")
        treeview = builder.get_object("applicationsView")
        treeview_short = builder.get_object("applicationsViewShort")
        window = builder.get_object("mainWindow")
        # Prepare other application state
        self.running = False
        self.gender = "male"
        # Add applications to the list model
        for a in apps:
            listmodel.append([a])
        for a in apps_short:
            listmodel_short.append([a])
        # Render items in tree view
        col = Gtk.TreeViewColumn("Name", Gtk.CellRendererText(), text=0)
        treeview.append_column(col)
        col_short = Gtk.TreeViewColumn("Name", Gtk.CellRendererText(), text=0)
        treeview_short.append_column(col_short)
        # Display window
        window.show_all()

    def onSelectionChanged(self, selection):
        (model, iter) = selection.get_selected()
        if (
            self.running and
            iter != None and
            model[iter][0] == self.to_select[0]
        ):
            # Since the user selected it, remove from self.to_select
            del self.to_select[0]
            # Request the next selection
            self.show_next_element()

    def onButtonPressed(self, button):
        # Make copy of selection array
        self.to_select = to_select[:]
        self.intermediate_times = []
        # Remember which mode we're in (short or long list)
        self.stack = self.selectionStack.get_visible_child_name()
        # Start evaluation by showing the first item
        self.show_next_element()

    def onButtonToggled(self, button):
        self.gender = button.get_label()

    def onDeleteWindow(self, *args):
        Gtk.main_quit(*args)

    def show_next_element(self):
        if self.running:
            # Remember how long it took the user to select this item
            self.intermediate_times.append(time.time() - self.current_start)
        else:
            # We're showing the first application, start counting
            self.running = True
            self.start = time.time()

        # Return to the original list mode if it was changed
        if self.selectionStack.get_visible_child_name() != self.stack:
            self.selectionStack.set_visible_child_name(self.stack)

        if len(self.to_select) > 0:
            # Show the next application to select
            self.currentApp.set_text(self.to_select[0])
            self.current_start = time.time()
        else:
            # User has selected everything, finish evaluation
            self.running = False
            self.write_result()

    def write_result(self):
        with open("{}.txt".format(str(int(self.start))), "w") as f:
            f.write("Subject:\n")
            f.write("{}, {}".format(self.gender, self.subjectAge.get_text()))
            f.write("\n\n")
            f.write("Times for selection of individual items [s]:\n")
            f.write("\n".join([str(x) for x in self.intermediate_times]))
            f.write("\n\n")
            f.write("Total time [s]:\n")
            f.write(str(sum(self.intermediate_times)))
            f.write("\n")


if __name__ == "__main__":
    ListEval()
    Gtk.main()
