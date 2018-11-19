import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio, GdkPixbuf, Gdk
import sys

from fpeditor.ApplicationWindow import ApplicationWindow


class Application(Gtk.Application):
    def __init__(self):
        Gtk.Application.__init__(self,
                                 application_id='eu.mienkofax',
                                 flags=Gio.ApplicationFlags.HANDLES_OPEN)

        self.window = None

    def do_activate(self):
        if not self.window:
            self.window = ApplicationWindow(self)


def main():
    app = Application()
    app.run(sys.argv)


if __name__ == '__main__':
    main()
