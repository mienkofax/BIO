import gi
import wsq
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio, GdkPixbuf, Gdk
from os import path
from PIL import Image

from fpeditor.DialogUtil import DialogUtil
from fpeditor.ZoomUtil import ZoomUtil
from fpeditor.PixBufUtil import PixBufUtil
from fpeditor.ImgEditor import ImgEditor


class ApplicationWindow(Gtk.ApplicationWindow):
    """Hlavne okno, kde sa zobrazuju a vykonavaju vsetky operacie."""

    def __init__(self, app):
        # settings
        settings = Gtk.Settings.get_default()
        settings.set_property("gtk-application-prefer-dark-theme", True)

        # variables
        self.__program_name = 'Fingerprint Editor'
        self.__supported_formats = ('png', 'wsq')
        self.__logo_filename = 'assets/logo.png'
        self.__image_widget = None
        self.__last_pixbuf = None
        self.__opened_filename = None
        self.__active_image_widget = False
        self.__zoom_level = 100  # default zoom level after open image
        self.__width = 0
        self.__height = 0
        self.__tmp_filename = '/tmp/wsq_to_png.png'

        Gtk.Window.__init__(self, title=self.__program_name, application=app)
        self.set_default_size(950, 550)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.__gtk_style('assets/custom.css')
        self.set_icon(self.__load_logo())

        # create components
        self.__header_bar = self.__create_header_bar()
        self.__header_bar.pack_end(self.__create_menu())
        self.__header_bar.pack_start(self.__create_header_bar_tools())
        self.set_titlebar(self.__header_bar)

        # main box
        main_box = Gtk.Box()
        main_box.add(self.__init_img_widget())
        self.add(main_box)

        self.__editor = None

        self.show_all()

    def __gtk_style(self, css_file):
        """Nacitanie CSS vlastnosti zo suboru a nastavenie do aplikacie."""

        base_path = path.dirname(path.abspath(__file__)) + '/'
        css_file = base_path + css_file

        with open(css_file, 'rb') as f:
            css = f.read()

        style_provider = Gtk.CssProvider()
        style_provider.load_from_data(css)

        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            style_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

    def __create_header_bar_tools(self):
        """Vytvoreni nastrojov v hlavicke pre pracu s obrazkom."""

        box = Gtk.Toolbar()
        box.set_name('tool')
        box.set_icon_size = Gtk.IconSize.DND
        box.set_property('icon-size', Gtk.IconSize.LARGE_TOOLBAR)

        # open
        btn_open = Gtk.ToolButton()
        btn_open.set_name('headerbar-btn')
        btn_open.set_icon_name('document-open')
        btn_open.set_property('tooltip-text', 'Open file')
        btn_open.connect('clicked', self.__open_file_callback)

        # close
        btn_close = Gtk.ToolButton()
        btn_close.set_name('headerbar-btn')
        btn_close.set_icon_name('window-close')
        btn_close.set_property('tooltip-text', 'Close file')
        btn_close.connect('clicked', self.__close_file_callback)
        btn_close.set_sensitive(False)
        self.__btn_close = btn_close

        # save
        btn_save = Gtk.ToolButton()
        btn_save.set_name('headerbar-btn')
        btn_save.set_icon_name('document-save')
        btn_save.set_property('tooltip-text', 'Save file')
        btn_save.connect('clicked', self.__save_callback)
        btn_save.set_sensitive(False)
        self.__btn_save = btn_save

        # save as
        btn_save_as = Gtk.ToolButton()
        btn_save_as.set_name('headerbar-btn')
        btn_save_as.set_icon_name('document-save-as')
        btn_save_as.set_property('tooltip-text', "Save file as ")
        btn_save_as.connect('clicked', self.__save_as_callback)
        btn_save_as.set_sensitive(False)
        self.__btn_save_as = btn_save_as

        # zoom in
        btn_zoom_in = Gtk.ToolButton()
        btn_zoom_in.set_name('headerbar-btn')
        btn_zoom_in.set_icon_name('zoom-in')
        btn_zoom_in.set_property('tooltip-text', 'Zoom in')
        btn_zoom_in.connect('clicked', self.__zoom_in_callback)
        btn_zoom_in.set_sensitive(False)
        self.__btn_zoom_in = btn_zoom_in

        # zoom original
        btn_zoom_original = Gtk.ToolButton()
        btn_zoom_original.set_name('headerbar-btn')
        btn_zoom_original.set_icon_name('zoom-original')
        btn_zoom_original.set_property('tooltip-text', 'Zoom original')
        btn_zoom_original.connect('clicked', self.__zoom_original_callback)
        btn_zoom_original.set_sensitive(False)
        self.__btn_zoom_original = btn_zoom_original

        # zoom fit best
        btn_zoom_fit_best = Gtk.ToolButton()
        btn_zoom_fit_best.set_name('headerbar-btn')
        btn_zoom_fit_best.set_icon_name('zoom-fit-best')
        btn_zoom_fit_best.set_property('tooltip-text', 'Zoom fit best')
        btn_zoom_fit_best.connect('clicked', self.__zoom_fit_best_callback)
        btn_zoom_fit_best.set_sensitive(False)
        self.__btn_zoom_fit_best = btn_zoom_fit_best

        # zoom out
        btn_zoom_out = Gtk.ToolButton()
        btn_zoom_out.set_name('headerbar-btn')
        btn_zoom_out.set_icon_name('zoom-out')
        btn_zoom_out.set_property('tooltip-text', 'Zoom out')
        btn_zoom_out.connect('clicked', self.__zoom_out_callback)
        btn_zoom_out.set_sensitive(False)
        self.__btn_zoom_out = btn_zoom_out

        # undo
        btn_undo = Gtk.ToolButton()
        btn_undo.set_name('headerbar-btn')
        btn_undo.set_icon_name('edit-undo')
        btn_undo.set_property('tooltip-text', 'Undo')
        btn_undo.set_sensitive(False)
        self.__btn_undo = btn_undo

        # redo
        btn_redo = Gtk.ToolButton()
        btn_redo.set_name('headerbar-btn')
        btn_redo.set_icon_name('edit-redo')
        btn_redo.set_property('tooltip-text', 'Redo')
        btn_redo.set_sensitive(False)
        self.__btn_redo = btn_redo

        box.insert(btn_open, 0)
        box.insert(btn_save, 1)
        box.insert(btn_save_as, 2)
        box.insert(btn_zoom_in, 3)
        box.insert(btn_zoom_original, 4)
        box.insert(btn_zoom_fit_best, 5)
        box.insert(btn_zoom_out, 6)
        box.insert(btn_close, 7)
        box.insert(btn_undo, 8)
        box.insert(btn_redo, 9)

        return box

    def __create_menu(self):
        """Vytvorenie jednoducheho menu pre dalsie zakladne operacie."""

        menu_button = Gtk.MenuButton()
        menu_button.set_name('headerbar-btn')
        menu_button.set_image(Gtk.Image.new_from_icon_name('open-menu-symbolic', Gtk.IconSize.MENU))

        model_menu = Gio.Menu()

        # sub menu for Rotate image
        model_menu_sub_operations = Gio.Menu()
        model_menu_sub_operations.append('Rotate -90°', 'win.rotate-left')
        model_menu_sub_operations.append('Rotate +90°', 'win.rotate-right')
        model_menu_sub_operations.append('Horizontal mirror', 'win.horizontal-mirror')
        model_menu_sub_operations.append('Vertical mirror', 'win.vertical-mirror')
        model_menu.append_submenu('Rotate image', model_menu_sub_operations)

        # rotate -90
        rotate_left_action = Gio.SimpleAction.new('rotate-left', None)
        rotate_left_action.connect('activate', self.__apply_rotate_action, 'rotate-left')
        self.add_action(rotate_left_action)

        # rotate +90
        rotate_right_action = Gio.SimpleAction.new('rotate-right', None)
        rotate_right_action.connect('activate', self.__apply_rotate_action, 'rotate-right')
        self.add_action(rotate_right_action)

        # horizontal mirror
        horizontal_mirror = Gio.SimpleAction.new('horizontal-mirror', None)
        horizontal_mirror.connect('activate', self.__apply_rotate_action, 'horizontal-mirror')
        self.add_action(horizontal_mirror)

        # vertical mirror
        vertical_mirror = Gio.SimpleAction.new('vertical-mirror', None)
        vertical_mirror.connect('activate', self.__apply_rotate_action, 'vertical-mirror')
        self.add_action(vertical_mirror)

        # horizontal mirror
        horizontal_mirror = Gio.SimpleAction.new('horizontal-mirror', None)
        horizontal_mirror.connect('activate', self.__apply_rotate_action, 'horizontal-mirror')
        self.add_action(horizontal_mirror)

        # sub menu for Filters
        model_menu_sub_filters = Gio.Menu()
        model_menu_sub_filters.append('Back & White', 'win.black-white')
        model_menu_sub_filters.append('Grayscale', 'win.grayscale')
        model_menu.append_submenu('Filters', model_menu_sub_filters)

        # black & white
        black_white = Gio.SimpleAction.new('black-white', None)
        black_white.connect('activate', self.__apply_filter_dialog_action, 'black-white',
                            ('Black & White', 0, 255))
        self.add_action(black_white)

        # grayscale
        grayscale = Gio.SimpleAction.new('grayscale', None)
        grayscale.connect('activate', self.__apply_filter_action, 'grayscale')
        self.add_action(grayscale)

        # sub menu for biometrics library
        model_menu_sub_biometrics = Gio.Menu()
        model_menu_sub_biometrics.append('Gabor filter', 'win.gabor-filter')
        model_menu_sub_biometrics.append('Thinning (skeletonization)', 'win.skeletonization-filter')
        model_menu.append_submenu('Biometrics library', model_menu_sub_biometrics)

        # Gabor filter
        gabor_filter = Gio.SimpleAction.new('gabor-filter', None)
        gabor_filter.connect('activate', self.__gabor_filter_action,
                             ('Block size', 1, 64))
        self.add_action(gabor_filter)

        # thinning (skeletonization)
        skeletonization_filter = Gio.SimpleAction.new('skeletonization-filter', None)
        skeletonization_filter.connect('activate', self.__skeletonization_filter_action)
        self.add_action(skeletonization_filter)

        # about
        model_menu.append('About', 'win.about')
        about_action = Gio.SimpleAction.new('about', None)
        about_action.connect('activate', self.__about_action)
        self.add_action(about_action)

        menu_button.set_menu_model(model_menu)
        return menu_button

    def __create_header_bar(self):
        """Vytvorenie header baru, do ktoreho mozu byt vlozene nastroje a menu."""

        hb = Gtk.HeaderBar()
        hb.set_show_close_button(True)
        hb.props.title = self.__program_name

        return hb

    def __init_img_widget(self):
        """Vytvorenie skrolovacieho okna s framom, ktory obsahuje obrazok po otvoreni.

        Skrolovacie okno umoznuje odchytit scroll-event a tak priblizovat obrazok.
        """

        self.__image_widget = Gtk.Image()

        event_box = Gtk.EventBox()
        event_box.add(self.__image_widget)

        frame = Gtk.Frame(hexpand=True, vexpand=True)
        frame.set_name('frame-img')
        frame.set_halign(Gtk.Align.CENTER)
        frame.set_valign(Gtk.Align.CENTER)
        frame.add(event_box)

        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.connect('scroll-event', self.__scroll_zoom_callback)
        scrolled_window.add(frame)

        return scrolled_window

    def update_image(self, img):
        """Aktualizacia obrazka vo widgete a spravne zobrazenie undo/redo tlacidiel."""

        pixbuf = PixBufUtil.pil_to_pixbuf(img)
        self.__image_widget.set_from_pixbuf(pixbuf)

        self.__last_pixbuf = pixbuf
        self.__width = img.width
        self.__height = img.height

        self.set_undo_redo_sensitive()

        self.show()

    def set_undo_redo_sensitive(self):
        """Zobrazenie undo/redo tlacidiel, len vtedy, ked je mozne dane tlacidla pouzit."""

        if self.__editor.number_of_images() < 1:
            self.__btn_undo.set_sensitive(False)
            self.__btn_redo.set_sensitive(False)
        else:
            self.__btn_undo.set_sensitive(True)
            self.__btn_redo.set_sensitive(True)

        if self.__editor.actual_image_index() == 0:
            self.__btn_undo.set_sensitive(False)

        if self.__editor.actual_image_index() >= self.__editor.number_of_images() - 1:
            self.__btn_redo.set_sensitive(False)

    def __load_image(self, img, filename, wsq_filename=None):
        """Nacitanie obrazku do pixbufferu a jeho zobrazenie vo widgete.

        Nacitany obrazok sa prevedie do pixbufferu, ulozia sa jeho rozmery. Ulozenie rozmerov
        musi byt pred volanim metod, ktore pracuju s priblizenim. Tieto metody pouzivaju
        tieto rozmery. Nasledne po rozmeroch sa vypocita najlepsie priblizenie obrazka, ale
        len v pripade, ze je vacsi ako okno, ak je mensi nic sa nedeje.
        Metoda __change_image_scale(), musi byt volana az po nastaveni pixbufferu do triednej
        premennej.
        """

        self.__editor = ImgEditor(self, img, filename, wsq_filename)

        self.__btn_undo.connect('clicked', self.__undo_callback)
        self.__btn_redo.connect('clicked', self.__redo_callback)
        self.set_undo_redo_sensitive()

        self.update_image(img)

        self.__zoom_level = self.__best_zoom_level()
        self.__change_image_scale()

        self.__active_image_widget = True
        self.__opened_filename = filename

        self.__btn_close.set_sensitive(True)
        self.__btn_save.set_sensitive(True)
        self.__btn_save_as.set_sensitive(True)
        self.__btn_zoom_in.set_sensitive(True)
        self.__btn_zoom_original.set_sensitive(True)
        self.__btn_zoom_fit_best.set_sensitive(True)
        self.__btn_zoom_out.set_sensitive(True)

        self.__set_window_subtitle()

        self.show_all()

    def __open_file_callback(self, _):
        """Otvorenie noveho obrazka a jeho nacitanie po overeni zakladnych parametrov.

        Pri praci s wsq suborom sa tento subor najpr prevedie na png a nasledne sa este upravi
        zo stupne sedej na RGB.
        """

        if self.__active_image_widget:
            DialogUtil.message(self, 'warning', 'Any img is opened',
                               'First close old image')
            return

        filename = DialogUtil.open_file_dialog(self)
        if filename is None:
            return

        suffix = path.splitext(filename)[-1][1:].lower()
        if suffix not in self.__supported_formats:
            DialogUtil.message(self, 'warning', 'Unknown format',
                               'File format: `%s` is not supported.' % suffix)
            return

        if suffix == 'wsq':
            wsq.wsq_to_png(filename, self.__tmp_filename)

            # convert gray to RGB
            im = Image.open(self.__tmp_filename).convert('RGB')
            im.save(self.__tmp_filename)
            im.close()

            img = Image.open(self.__tmp_filename)

            self.__load_image(img, self.__tmp_filename, filename)
            return

        img = Image.open(filename)
        self.__load_image(img, filename)

    def __close_file_callback(self, _):
        """Skrytie widgetu s obrazkom a deaktivovanie tlacidla na zatvorenie suboru.

        Skrytie widgetu s obrazkom (__image_widget), musi byt az po zavolani
        funkcie show_all().
        """

        self.__btn_close.set_sensitive(False)
        self.__btn_save.set_sensitive(False)
        self.__btn_save_as.set_sensitive(False)
        self.__btn_zoom_in.set_sensitive(False)
        self.__btn_zoom_original.set_sensitive(False)
        self.__btn_zoom_fit_best.set_sensitive(False)
        self.__btn_zoom_out.set_sensitive(False)

        self.__active_image_widget = False
        self.__clear_window_subtitle()

        self.__editor.close()
        self.__editor = None
        self.__btn_undo.set_sensitive(False)
        self.__btn_redo.set_sensitive(False)

        self.show_all()
        self.__image_widget.hide()

    def __scroll_zoom_callback(self, _, event):
        """Detekcia smeru skrolovania, vypocet novej urovne priblizenia a uprava obrazku."""

        if not (event.state & Gdk.ModifierType.CONTROL_MASK):
            return

        zoom = 0
        is_smooth, dx, dy = Gdk.Event.get_scroll_deltas(event)

        if is_smooth:
            if dy > 0:
                zoom = -1
            elif dy < 0:
                zoom = 1
        elif event.direction == Gdk.ScrollDirection.UP:
            zoom = 1
        elif event.direction == Gdk.ScrollDirection.DOWN:
            zoom = -1

        self.__zoom_level = ZoomUtil.compute_new_value(self.__zoom_level, zoom)
        self.__change_image_scale()

    def __zoom_in_callback(self, _):
        """Priblizenie o 10 %."""

        self.__zoom_level = ZoomUtil.compute_new_value(self.__zoom_level, 1)
        self.__change_image_scale()

    def __zoom_original_callback(self, _):
        """Nastavenie priblizenia na 100 %."""

        self.__zoom_level = 100
        self.__change_image_scale()

    def __zoom_fit_best_callback(self, _):
        """Priblizenie, aby bol obrazok viditelny v celkom okne."""

        self.__zoom_level = self.__best_zoom_level()
        self.__change_image_scale()

    def __zoom_out_callback(self, _):
        """Oddialenie priblizenia o 10 %."""

        self.__zoom_level = ZoomUtil.compute_new_value(self.__zoom_level, -1)
        self.__change_image_scale()

    def __undo_callback(self, _):
        """Krok spat."""

        self.__editor.undo()

    def __redo_callback(self, _):
        """Krok vpred."""

        self.__editor.redo()

    def __save_callback(self, _):
        """Ulozenie obrazka."""

        self.__editor.save()

    def __save_as_callback(self, _):
        """Ulozenie obrazka ako novy subor."""

        self.__editor.save_as()
        self.__set_window_subtitle()

    def __about_action(self, _, __):
        """Zobrazenie informacii o obrazku."""

        dialog = Gtk.AboutDialog(transient_for=self)
        dialog.set_logo(self.__load_logo())
        dialog.set_program_name(self.__program_name)
        dialog.set_version('0.11')
        dialog.set_website('https://github.com/mienkofax/bio')
        dialog.set_authors(['Klára Nečasová', 'Václav Ševčík', 'Peter Tisovčík'])

        dialog.run()
        dialog.destroy()

    def __apply_rotate_action(self, _, __, name):
        """Aplikovanie operacie no otocenie obrazka, pripadne zrkadlenie."""

        self.__editor.apply_rotation(name)

    def __apply_filter_dialog_action(self, _, __, name, params):
        """Vytvorenie dialogoveho okna a nasledne aplikovanie filtra so zadanymi hodnotami."""

        dialog = DialogUtil.dialog_with_param(self, *params)
        values = dialog.get_values()

        self.__editor.apply_filter(name, values)

    def __apply_filter_action(self, _, __, name, params=None):
        """Aplikovanie filtra so zadanymi parametrami."""

        self.__editor.apply_filter(name, params)

    def __gabor_filter_action(self, _, __, params=None):
        dialog = DialogUtil.dialog_with_param(self, *params)
        values = dialog.get_values()

        if values is None:
            self.__editor.gabor_filter()
        else:
            self.__editor.gabor_filter(values)

    def __skeletonization_filter_action(self, _, __):
        self.__editor.skeletonization_filter()

    def __load_logo(self):
        """Nacitanie loga do pixbufferu z adresara, kde sa spusta aplikacia."""

        base_path = path.dirname(path.abspath(__file__)) + '/'
        return GdkPixbuf.Pixbuf.new_from_file(base_path + self.__logo_filename)

    def __set_window_subtitle(self):
        """Nastavenie podnazvu okna na cestu k suboru a velkost priblizenia."""

        if self.__editor is None:
            return

        file = path.basename(self.__editor.filename())
        subtitle = '[{}] - {}%'.format(file, self.__zoom_level)
        self.__header_bar.props.subtitle = subtitle

    def __clear_window_subtitle(self):
        """Vymazanie podnazvu okna."""

        self.__header_bar.props.subtitle = None

    def __best_zoom_level(self):
        """Vypocitanie uroven priblizenia, aby nebolo potrebne s obrazkom skrolovat."""

        win = self.get_allocation()
        return ZoomUtil.best_level(self.__width, self.__height, win.width, win.height)

    def __change_image_scale(self):
        """Vypocet urovne priblizenia na zaklade velkosti obrazku a urovne priblizenia."""

        w = self.__width
        h = self.__height
        zoom_level = self.__zoom_level

        pixbuf = self.__last_pixbuf
        if self.__zoom_level != 100:
            w *= zoom_level / 100
            h *= zoom_level / 100

        pixbuf = pixbuf.scale_simple(w, h, GdkPixbuf.InterpType.BILINEAR)
        self.__image_widget.set_from_pixbuf(pixbuf)
        self.__set_window_subtitle()
