import wsq
from PIL import Image

from os import path
from fpeditor.RotationUtil import RotationUtil
from fpeditor.ImgObj import ImgObj
from fpeditor.DialogUtil import DialogUtil
from fpeditor.FiltersUtil import FiltersUtil
from fpeditor.BiometricsLib import BiometricsLib


class ImgEditor:
    """Editor obrazkov, ktory zabezpecuje editaciu obrazku a pracu s obrazkom.

    Trieda poskytuje moznosti pre upravu obrazku a uchovava si informacie o zmene,
    na zaklade ktorych je mozne potom vykonavat krok spat a vpred. Dalej umoznuje
    Ulozenie obrazka do povodneho suboru, pripadne do noveho suboru.
    """
    MAX_HISTORY_ITEMS = 100

    def __init__(self, win, img, filename, wsq_filename):
        self.__win = win
        self.__image = ImgObj(img, filename)
        self.__filename = filename
        self.__wsq_filename = wsq_filename

    def filename(self):
        """Cesta k aktualne otvorenemu obrazku."""

        return self.__filename

    def number_of_images(self):
        """Pocet obrazkov, ulozenych v ImgObj."""

        return self.__image.size()

    def actual_image_index(self):
        """Index aktualne zobrazovaneho obrazku v zozname obrazkov."""

        return self.__image.actual_index()

    def apply_rotation(self, name):
        """Aplikovanie rotacie na zobrazeny obrazok.

        Kazda rotacia je aplikovatelna samostatne a je mozne urobit krok spat
        po jej aplikovani.
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
            raise NameError('unknown rotation name: %s' % name)

        self.do_change(img)

        return img

    def apply_filter(self, name, value=None):
        """Aplikovanie pozadovaneho filtra."""

        img = self.__image.current_img()

        if name == 'black-white':
            img = FiltersUtil.black_white(img, value)
        elif name == 'grayscale':
            img = FiltersUtil.grayscale(img)
        else:
            raise NameError('unknown filter name: %s' % name)

        self.do_change(img)

        return img

    def gabor_filter(self, block_size):
        img = self.__image.current_img()
        self.do_change(BiometricsLib.gabor_filter(img, block_size))

        return img

    def skeletonization_filter(self):
        img = self.__image.current_img()
        self.do_change(BiometricsLib.skeletonization_filter(img))

        return img

    def singular_points(self):
        img = self.__image.current_img()
        self.do_change(BiometricsLib.singular_points(img))

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
        """Ulozenie obrazku do povodneho suboru.

        Pri ukladani wsq suboru sa najpr ulozi pouzivany subor do png, nasledne sa upravi
        rezim s RGB do gray a potom sa prevedie naspat do wsq formatu.
        """

        img = self.__image.current_img()
        if path.isfile(self.__filename) and self.__wsq_filename is None:
            img.save(self.__filename)

        if self.__wsq_filename is not None:
            img.save(self.__filename)
            # convert RGB to gray
            Image.open(self.__filename).convert('L').save(self.__filename)
            wsq.png_to_wsq(self.__filename, self.__wsq_filename)

    def save_as(self):
        """Ulozenie obrazku do noveho suboru."""

        if self.__wsq_filename is not None:
            filename = DialogUtil.save_as_dialog(self.__win, self.__wsq_filename)
        else:
            filename = DialogUtil.save_as_dialog(self.__win, self.__filename)
        if filename is None:
            return

        suffix = path.splitext(filename)[-1][1:].lower()
        img = self.__image.current_img()

        if suffix == 'wsq':
            img.save(self.__filename)
            # convert RGB to gray
            Image.open(self.__filename).convert('L').save(self.__filename)
            wsq.png_to_wsq(self.__filename, filename)
            pass
        else:
            img.save(filename)
            self.__filename = filename

    def close(self):
        """Zatvorenie vsetkych obrazkov, ktore sa nachadzaju v zozname obrazkov."""

        self.__image.close_all_img()
