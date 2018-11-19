class ZoomUtil:
    """Pomocna trieda pre pocitanie zoomu obrazku."""

    @staticmethod
    def best_level(img_w, img_h, win_w, win_h, margin=20):
        """Vypocet najlepsieho priblizenia na zaklade velkosti okna a obrazku."""

        start_zoom = 100

        win_w -= win_w * margin / 100
        win_h -= win_h * margin / 100

        # If the image is higher than the window
        if img_w > win_w or img_h > win_h:
            ratio_w = img_w / win_w
            ratio_h = img_h / win_h
            ratio = round(max((ratio_w, ratio_h)), 1)

            start_zoom = int(round(start_zoom / ratio))

        return start_zoom

    @staticmethod
    def compute_new_value(zoom_level, value, zoom_min=10, zoom_max=300):
        """Vypocet novej hodnoty zoomu, na zaklade aktualneho priblizenia v obrazku."""

        zoom_level += value * 10
        zoom_level = round(zoom_level / 10) * 10  # round to the nearest decade

        if zoom_level < zoom_min:
            zoom_level = zoom_min
        elif zoom_level > zoom_max:
            zoom_level = zoom_max

        return zoom_level
