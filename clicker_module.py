import pyautogui as py
import time
import cv2
import numpy as np

class Clicker:
    def __init__(self, target_png):
        self.target_png = target_png
        py.FAILSAFE = True

    def automate_auto_bloodweb(self):
        try:
            # position = py.locateCenterOnScreen(self.target_png, confidence=.35)
            # need to install OpenCV for confidence to work
            py.mouseDown(690, 575)
            time.sleep(1)
            py.mouseUp()
        except:
            print('Error: Cannot find auto purchase node.')

    def test_image_search(self, image_path):
        try:
            # Read the image
            image = cv2.imread(image_path)
            image_height, image_width = image.shape[:2]

            # Take a screenshot
            screenshot_np = py.screenshot().convert("RGB")
            screenshot_cv2 = cv2.cvtColor(np.array(screenshot_np), cv2.COLOR_RGB2BGR)

            # Match the template
            result = cv2.matchTemplate(screenshot_cv2, image, cv2.TM_CCOEFF_NORMED)
            _, _, _, max_loc = cv2.minMaxLoc(result)

            # Specify a threshold for matching
            threshold = 0.8

            if result[max_loc[1], max_loc[0]] >= threshold:
                # Calculate the center coordinates
                center_x = max_loc[0] + image_width // 2
                center_y = max_loc[1] + image_height // 2

                # Move the mouse to the center coordinates
                print(f"Image found at coordinates: ({center_x}, {center_y})")
                py.moveTo(center_x, center_y)
            else:
                print("Image not found on the screen.")
        except Exception as e:
            print(f"Error during image search: {e}")

    def execute_autobuy(self):
        print("Ctrl+1 pressed! Auto purchase bloodweb once.")
        self.automate_auto_bloodweb()

    def execute_autoprestige(self):
        print("Ctrl+2 pressed! Auto prestige once.")
        for _ in range(10):
            self.automate_auto_bloodweb()
            time.sleep(5)
        for _ in range(20):
            self.automate_auto_bloodweb()
            time.sleep(6)
        for _ in range(21):
            self.automate_auto_bloodweb()
            time.sleep(7)

    def execute_test_image_search(self):
        print("Ctrl+9 pressed! Testing image search for auto_purchase_node.png...")
        self.test_image_search('images/bloody_party_streamers.png')