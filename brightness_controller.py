import threading
import screen_brightness_control as sbc
from config import SMOOTHING_ALPHA, BRIGHTNESS_DELTA_THRESHOLD


class BrightnessController:
    def __init__(self):
        self._current = sbc.get_brightness(display=0)[0]
        self._target = self._current
        self._lock = threading.Lock()                    
        self._running = True                              

        self._thread = threading.Thread(                  
            target=self._update_loop, daemon=True)
        self._thread.start()

    def set_target(self, value: float):
        clamped = max(0, min(100, int(value)))
        with self._lock:                                  
            self._target = clamped

    def _update_loop(self):                             
        import time
        while self._running:
            with self._lock:
                target = self._target
                current = self._current

            smoothed = SMOOTHING_ALPHA * target + (1 - SMOOTHING_ALPHA) * current

            if abs(smoothed - current) > BRIGHTNESS_DELTA_THRESHOLD:
                try:
                    sbc.set_brightness(int(smoothed), display=0)
                    with self._lock:
                        self._current = smoothed
                except Exception:
                    pass

            time.sleep(0.05)

    def stop(self):                                      
        self._running = False