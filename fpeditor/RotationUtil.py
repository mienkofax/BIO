from PIL import Image


class RotationUtil:
    """Pomocna trieda pre pracu s rotaciou obrazkov."""

    @staticmethod
    def rotate(img, angle):
        """Otocie obrazku o zadanu velkost uhla."""

        return img.rotate(angle, expand=True)

    @staticmethod
    def horizontal_mirror(img):
        """Horizontalne otocenie obrazka."""

        return img.transpose(Image.FLIP_TOP_BOTTOM)

    @staticmethod
    def vertical_mirror(img):
        """Vertikalne otocenie obrazka."""

        return img.transpose(Image.FLIP_LEFT_RIGHT)
