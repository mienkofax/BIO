import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from fpeditor.CustomDialog import CustomDialog


class DialogUtil:
    """Pomocna trieda pre pracu s dialogovimi oknami."""

    @staticmethod
    def supported_format_filter(dialog):
        """Filter s podporovanymi koncovkami suborov."""

        filter_text = Gtk.FileFilter()
        filter_text.set_name("WSQ")
        filter_text.add_mime_type("application/octet-stream")
        dialog.add_filter(filter_text)

        filter_text = Gtk.FileFilter()
        filter_text.set_name("PNG")
        filter_text.add_mime_type("image/png")
        dialog.add_filter(filter_text)

        filter_any = Gtk.FileFilter()
        filter_any.set_name("Any files")
        filter_any.add_pattern("*")
        dialog.add_filter(filter_any)

        return dialog

    @staticmethod
    def message(parent, dialog_type, title, text):
        """Zjednodusene vytvaranie dialogovych sprav na zaklade jej typu, nazvu a textu."""

        btn_type = Gtk.ButtonsType.OK

        if dialog_type == 'info':
            dialog_type = Gtk.MessageType.INFO
        elif dialog_type == 'warning':
            dialog_type = Gtk.MessageType.WARNING
        elif dialog_type == 'error':
            dialog_type = Gtk.MessageType.ERROR
        elif dialog_type == 'question':
            dialog_type = Gtk.MessageType.QUESTION
            btn_type = Gtk.ButtonsType.YES_NO
        else:
            raise SyntaxError('unknown dialog type: %s' % dialog_type)

        dialog = Gtk.MessageDialog(parent, 0, dialog_type, btn_type, title)
        dialog.format_secondary_text(text)

        response = dialog.run()
        dialog.destroy()

        return response

    @staticmethod
    def open_file_dialog(parent):
        """Dialog pre otvorenie okna."""

        dialog = Gtk.FileChooserDialog("Please choose a file", parent,
                                       Gtk.FileChooserAction.OPEN,
                                       (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                                        Gtk.STOCK_OPEN, Gtk.ResponseType.OK))

        dialog = DialogUtil.supported_format_filter(dialog)
        response = dialog.run()

        if response != Gtk.ResponseType.OK:
            dialog.destroy()
            return None

        filename = dialog.get_filename()
        dialog.destroy()

        return filename

    @staticmethod
    def save_as_dialog(parent, save_as_filename):
        """Dialog pre ulozenie suboru."""

        dialog = Gtk.FileChooserDialog("Save File", parent, Gtk.FileChooserAction.SAVE,
                                       (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                                        Gtk.STOCK_SAVE, Gtk.ResponseType.OK))

        dialog.set_current_name(save_as_filename)
        response = dialog.run()
        if response != Gtk.ResponseType.OK:
            dialog.destroy()
            return None

        filename = dialog.get_filename()
        dialog.destroy()

        return filename

    @staticmethod
    def dialog_with_param(parent, title, limit_min, limit_max, default_value=None):
        def on_apply_clicked(_, scale, dialog):
            dialog.values.append(int(scale.get_value()))
            dialog.destroy()

        dialog = CustomDialog(parent, title)

        if default_value is None:
            default_value = (limit_min + limit_max) / 2

        scale = Gtk.Scale.new_with_range(Gtk.Orientation.HORIZONTAL, limit_min, limit_max, 20)
        scale.set_value(default_value)
        scale.set_hexpand(True)
        scale.set_valign(Gtk.Align.START)

        btn_cancel = Gtk.Button.new_with_label('Cancel')
        btn_cancel.connect('clicked', dialog.close)

        btn_apply = Gtk.Button.new_with_label('Apply')
        btn_apply.connect('clicked', on_apply_clicked, scale, dialog)
        btn_apply.get_style_context().add_class(Gtk.STYLE_CLASS_SUGGESTED_ACTION)

        btn_box = Gtk.Box(spacing=6)
        btn_box.pack_start(btn_cancel, True, True, 0)
        btn_box.pack_end(btn_apply, True, True, 0)

        dialog.dialog_box.add(scale)
        dialog.dialog_box.add(btn_box)
        dialog.launch()

        return dialog
