class ImgObj:
    """Trieda uchovavajuca informacie o obrazkoch spolu s historiou."""

    def __init__(self, img, filename):
        self.__images = [img]
        self.__filename = filename

        self.__actual_index = 0

    def append_img(self, img):
        """Pridanie obrazku do objektu."""

        self.__images.append(img)

    def current_img(self):
        """Vratenie obrazka na aktualnom indexe."""

        return self.__images[self.__actual_index]

    def increment(self):
        """Zvacsenie aktualneho indexu o jedna."""

        self.__actual_index += 1

    def decrement(self):
        """Zmensenie aktualneho indexu o jedna."""

        self.__actual_index -= 1

    def size(self):
        """Celkovy pocet obrazkov v zozname."""

        return len(self.__images)

    def actual_index(self):
        """Aktualny index v zozname."""

        return self.__actual_index

    def clear(self):
        """Vycistenie zoznamu od nepotrebnych obrazkov, pouzite pri redo."""

        self.__images = self.__images[:self.__actual_index + 1]

    def close_all_img(self):
        """Zatvorenie obrazkov, pri ukonceni aplikacie."""

        for img in self.__images:
            img.close()
