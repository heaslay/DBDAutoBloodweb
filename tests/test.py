import cv2
import numpy as np

# Load the screenshot and the offering template
screenshot_path = 'images/ibovd_screenshot 0.7.png'  # Replace with your local path
template_path = 'images/ibovd 0.7.png'  # Replace with your local path

screenshot_img = cv2.imread(screenshot_path)
template_img = cv2.imread(template_path)

# Convert both images to grayscale
gray_screenshot = cv2.cvtColor(screenshot_img, cv2.COLOR_BGR2GRAY)
gray_template = cv2.cvtColor(template_img, cv2.COLOR_BGR2GRAY)

# Perform template matching
result = cv2.matchTemplate(gray_screenshot, gray_template, cv2.TM_CCOEFF_NORMED)
_, max_val, _, max_loc = cv2.minMaxLoc(result)

# Set a confidence threshold (adjust if needed)
confidence_threshold = 0.75

# Check if the template is found
if max_val >= confidence_threshold:
    print(f"Offering found! Confidence: {max_val}")
    # Draw a rectangle around the detected area
    template_h, template_w = gray_template.shape[:2]
    top_left = max_loc
    bottom_right = (top_left[0] + template_w, top_left[1] + template_h)
    cv2.rectangle(screenshot_img, top_left, bottom_right, (0, 255, 0), 2)
else:
    print(f"Offering not found. Max confidence: {max_val}")
