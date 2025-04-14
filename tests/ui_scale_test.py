import cv2
import pyautogui
import numpy as np
import time

# Store the detected scale globally
detected_ui_scale = None

def multi_scale_search(image, template, scales):
    """Search for the template at different scales to detect the correct UI scale."""
    for scale in scales:
        resized_template = cv2.resize(template, None, fx=scale, fy=scale)
        result = cv2.matchTemplate(image, resized_template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(result)
        
        if max_val > 0.8:  # Assuming 0.8 as the matching threshold
            return max_loc, scale
    return None, None

def detect_ui_scale_and_move(template_path):
    """Detect the UI scale by searching for the auto-purchase node and move the mouse to that node."""
    global detected_ui_scale

    # Take a screenshot
    screen = pyautogui.screenshot()
    screen_np = np.array(screen)
    screen_cv2 = cv2.cvtColor(screen_np, cv2.COLOR_RGB2BGR)

    # Load the auto-purchase node template
    template = cv2.imread(template_path)

    # Perform a multi-scale search to detect the correct UI scale
    scales = [0.7, 0.75, 0.8, 0.85, 0.9, 0.95, 1.0]  # Full list of scales
    loc, scale = multi_scale_search(screen_cv2, template, scales)

    if loc:
        detected_ui_scale = scale  # Store the detected scale
        template_height, template_width = cv2.resize(template, None, fx=scale, fy=scale).shape[:2]
        center_x = loc[0] + int(template_width // 2)
        center_y = loc[1] + int(template_height // 2)

        # Move the mouse pointer to the detected location
        pyautogui.moveTo(center_x, center_y)
        print(f"UI scale detected: {scale}. Mouse moved to the auto-purchase node at ({center_x}, {center_y})")
    else:
        print("Failed to detect UI scale or auto-purchase node.")

# Add a 5-second delay before execution
print("Please switch to the Dead By Daylight application within 5 seconds.")
time.sleep(5)

# Example workflow: Detect UI scale and move the pointer
detect_ui_scale_and_move('images/auto_purchase_node_withBG.png')
