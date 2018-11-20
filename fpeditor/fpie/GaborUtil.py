import numpy as np

from fpeditor.fpie.Utils import Utils


class GaborUtil:
    @staticmethod
    def gaborKernel(size, angle, frequency):
        """
        Create a Gabor kernel given a size, angle and frequency.

        Code is taken from https://github.com/rtshadow/biometrics.git
        """

        angle += np.pi * 0.5
        cos = np.cos(angle)
        sin = -np.sin(angle)

        yangle = lambda x, y: x * cos + y * sin
        xangle = lambda x, y: -x * sin + y * cos

        xsigma = ysigma = 4

        return Utils.kernel_from_function(size, lambda x, y:
        np.exp(-(
                (xangle(x, y) ** 2) / (xsigma ** 2) +
                (yangle(x, y) ** 2) / (ysigma ** 2)) / 2) *
        np.cos(2 * np.pi * frequency * xangle(x, y)))

    @staticmethod
    def gaborFilter(image, orientations, frequencies, w=32):
        result = np.empty(image.shape)

        height, width = image.shape
        for y in range(0, height - w, w):
            for x in range(0, width - w, w):
                orientation = orientations[y+w//2, x+w//2]
                frequency = Utils.average_frequency(frequencies[y:y + w, x:x + w])

                if frequency < 0.0:
                    result[y:y+w, x:x+w] = image[y:y+w, x:x+w]
                    continue

                kernel = GaborUtil.gaborKernel(16, orientation, frequency)
                result[y:y+w, x:x+w] = Utils.convolve(image, kernel, (y, x), (w, w))

        return Utils.normalize(result)

    @staticmethod
    def gaborFilterSubdivide(image, orientations, frequencies, rect=None):
        if rect:
            y, x, h, w = rect
        else:
            y, x = 0, 0
            h, w = image.shape

        result = np.empty((h, w))

        orientation, deviation = Utils.average_orientation(
            orientations[y:y+h, x:x+w], deviation=True)

        if (deviation < 0.2 and h < 50 and w < 50) or h < 6 or w < 6:
            frequency = Utils.average_frequency(frequencies[y:y + h, x:x + w])

            if frequency < 0.0:
                result = image[y:y+h, x:x+w]
            else:
                kernel = GaborUtil.gaborKernel(16, orientation, frequency)
                result = Utils.convolve(image, kernel, (y, x), (h, w))

        else:
            if h > w:
                hh = h // 2

                result[0:hh, 0:w] = \
                    GaborUtil.gaborFilterSubdivide(image, orientations, frequencies, (y, x, hh, w))

                result[hh:h, 0:w] = \
                    GaborUtil.gaborFilterSubdivide(image, orientations, frequencies, (y + hh, x, h - hh, w))
            else:
                hw = w // 2

                result[0:h, 0:hw] = \
                    GaborUtil.gaborFilterSubdivide(image, orientations, frequencies, (y, x, h, hw))

                result[0:h, hw:w] = \
                    GaborUtil.gaborFilterSubdivide(image, orientations, frequencies, (y, x + hw, h, w - hw))

        if w > 20 and h > 20:
            result = Utils.normalize(result)

        return result
