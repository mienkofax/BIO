import gi
gi.require_version('Gtk', '3.0')
from gi.repository import GdkPixbuf, GLib


class PixBufUtil:
    """Pomocna trieda pre pracu s pix buffrom."""

    @staticmethod
    def create_empty_pixbuf(width, height, mode='RGB'):
        """Vytvorenie prazdneho pix bufferu na zaklade zadanych velkosti a modu."""

        if mode == 'RGB':
            alpha = False
        elif mode == 'RGBA':
            alpha = True

        return GdkPixbuf.Pixbuf.new(GdkPixbuf.Colorspace.RGB, alpha, 8, width, height)

    @staticmethod
    def pil_to_pixbuf(img):
        """Vytvorenie pix buffera zo zadaneho obrazka."""

        if img.mode == 'L':
            img = img.convert('RGB')

        data = GLib.Bytes.new(img.tobytes())
        w, h = img.size

        if img.mode == 'RGB':
            alpha = False
            color_size = 3
        elif img.mode == 'RGBA':
            alpha = True
            color_size = 4
        else:
            raise SyntaxError('image mod %s is not supported' % img.mode)

        colorspace = GdkPixbuf.Colorspace.RGB
        return GdkPixbuf.Pixbuf.new_from_bytes(data, colorspace, alpha, 8, w, h, w * color_size)
