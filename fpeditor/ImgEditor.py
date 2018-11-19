from os import path
from fpeditor.RotationUtil import RotationUtil
from fpeditor.ImgObj import ImgObj
from fpeditor.DialogUtil import DialogUtil


class ImgEditor:
    """Editor obrazkov, ktory zabezpecuje editaciu obrazku a pracu s obrazkom.

    Trieda poskytuje moznosti pre upravu obrazku a uchovava si informacie o zmene,
    na zaklade ktorych je mozne potom vykonavat krok spat a vpred. Dalej umoznuje
    Ulozenie obrazka do povodneho suboru, pripadne do noveho suboru.
    """
    MAX_HISTORY_ITEMS = 100

    def __init__(self, win, img, filename):
        self.__win = win
        self.__image = ImgObj(img, filename)
        self.__filename = filename

    def filename(self):
        """Cesta k aktualne otvorenemu obrazku."""

        return self.__filename

    def number_of_images(self):
        """Pocet obrazkov, ulozenych v ImgObj."""

        return self.__image.size()

    def actual_image_index(self):
        """Index aktualne zobrazovaneho obrazku v zozname obrazkov."""

        return self.__image.actual_index()

    def apply_filter(self, name):
        """Aplikovanie filtra na zobrazeny obrazok.

        Kazdy filter je aplikovany samostatne a je mozne urobit krok spat po jeho aplikovani.
        """

        img = self.__image.current_img()

        if name == 'rotate-right':
            img = RotationUtil.rotate(img, -90)
        elif name == 'rotate-left':
            img = RotationUtil.rotate(img, +90)
        elif name == 'horizontal-mirror':
            img = RotationUtil.horizontal_mirror(img)
        elif name == 'vertical-mirror':
            img = RotationUtil.vertical_mirror(img)
        else:
            raise NameError('unknown filter name: %s' % name)

        self.do_change(img)

        return img

    def do_change(self, img):
        """Vykonanie aktualizacie obrazku po nejakej zmene."""

        self.__win.update_image(img)
        self.__image.clear()
        self.__image.append_img(img)
        self.__image.increment()

        self.__win.set_undo_redo_sensitive()

    def undo(self):
        """Krok spat."""

        if self.__image.size() > 1 and self.__image.actual_index() > 0:
            self.__image.decrement()
            self.__win.update_image(self.__image.current_img())

    def redo(self):
        """Krok vpred."""

        if self.__image.size() > 1:
            if self.__image.actual_index() + 1 < self.__image.size():
                self.__image.increment()
                self.__win.update_image(self.__image.current_img())

    def save(self):
        """Ulozenie obrazku do povodneho suboru."""

        if path.isfile(self.__filename):
            img = self.__image.current_img()
            img.save(self.__filename)

    def save_as(self):
        """Ulozenie obrazku do noveho suboru."""

        filename = DialogUtil.save_as_dialog(self.__win, self.__filename)
        if filename is None:
            return

        suffix = path.splitext(filename)[-1][1:].lower()
        if suffix == 'wsq':
            #wsq save
            pass
        else:
            img = self.__image.current_img()
            img.save(filename)
            self.__filename = filename

    def close(self):
        """Zatvorenie vsetkych obrazkov, ktore sa nachadzaju v zozname obrazkov."""

        self.__image.close_all_img()
