# Gesture configuration
MIN_DETECTION_CONFIDENCE = 0.75
MIN_TRACKING_CONFIDENCE = 0.70
MAX_HANDS = 1

# Distance-to-brightness mapping
MIN_DISTANCE = 30    # pixels — closed pinch
MAX_DISTANCE = 250   # pixels — fully open

# Brightness range
MIN_BRIGHTNESS = 0
MAX_BRIGHTNESS = 100

# Smoothing factor (0 = no smoothing, 1 = no change)
SMOOTHING_ALPHA = 0.3
BRIGHTNESS_DELTA_THRESHOLD = 3  # Only update if change > 3%

# Display
FRAME_WIDTH = 640
FRAME_HEIGHT = 480