import screen_brightness_control as sbc


class BrightnessController:
    def __init__(self):
        self._current = sbc.get_brightness(display=0)[0]
        self._target = self._current

    def set_target(self, value: float):
        clamped = max(0, min(100, int(value)))
        self._target = clamped
        sbc.set_brightness(clamped, display=0)            