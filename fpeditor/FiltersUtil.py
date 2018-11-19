from PIL import Image


class FiltersUtil:
    @staticmethod
    def grayscale(img):
        """Prevod obrazku do odtieni sivej."""

        data = list(img.getdata())
        data_m = []

        for pixel in data:
            gray = (pixel[0] + pixel[1] + pixel[2]) // 3
            data_m.append((gray, gray, gray))

        img_grayscale = Image.new(img.mode, img.size)
        img_grayscale.putdata(data_m)

        return img_grayscale

    @staticmethod
    def black_white(img, treshold=128):
        """Prevod obrazku do ciernobieleho rezimu."""

        data = list(img.getdata())
        data_m = []

        for pixel in data:
            gray = (pixel[0] + pixel[1] + pixel[2]) // 3
            gray = 0 if gray < treshold else 255
            data_m.append((gray, gray, gray))

        img_black_white = Image.new(img.mode, img.size)
        img_black_white.putdata(data_m)

        return img_black_white
