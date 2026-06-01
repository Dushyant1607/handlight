import screen_brightness_control as sbc
from config import SMOOTHING_ALPHA, BRIGHTNESS_DELTA_THRESHOLD  


class BrightnessController:
    def __init__(self):
        self._current = sbc.get_brightness(display=0)[0]
        self._target = self._current

    def set_target(self, value: float):
        clamped = max(0, min(100, int(value)))
        self._target = clamped

        smoothed = SMOOTHING_ALPHA * clamped + (1 - SMOOTHING_ALPHA) * self._current

        if abs(smoothed - self._current) > BRIGHTNESS_DELTA_THRESHOLD:
            sbc.set_brightness(int(smoothed), display=0)
            self._current = smoothed