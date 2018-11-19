import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class CustomDialog(Gtk.Dialog):
    """Obalenie dialogoveho okna, ktore zobrazuje zakladne prvky."""

    def __init__(self, parent, title):
        Gtk.Dialog.__init__(self, transient_for=parent)

        # settings
        self.set_title(title)
        self.set_modal(True)
        self.set_resizable(False)
        self.set_size_request(300, -1)
        self.set_border_width(10)

        # variables
        self.values = []
        self.dialog_box = self.get_content_area()
        self.dialog_box.set_spacing(6)

    def get_values(self):
        if not self.values:
            return None
        elif len(self.values) == 1:
            return self.values[0]
        else:
            return self.values

    def launch(self):
        self.show_all()
        self.run()
        self.destroy()

    def close(self, _):
        self.destroy()
