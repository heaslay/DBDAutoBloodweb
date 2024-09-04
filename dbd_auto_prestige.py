import pyautogui as py
import time
import cv2
import numpy as np
import os

class Clicker:
    def __init__(self, target_png):
        self.target_png = resource_path(target_png)
        py.FAILSAFE = True

    def automate_auto_bloodweb(self):
        try:
            py.moveTo(x=690, y=575)
            time.sleep(0.2)
            py.mouseDown()
            time.sleep(0.2)
            py.mouseUp()
            py.moveTo(1000, 150)
        except:
            pass 

def resource_path(relative_path):
    """ Get the absolute path to the resource, works for both development and PyInstaller """
    try:
        base_path = sys._MEIPASS  # PyInstaller temporary folder
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def execute_autoprestige():
    clicker = Clicker('images/auto_purchase_node.png')
    for _ in range(9):
        clicker.automate_auto_bloodweb()
        time.sleep(5)

    # Image search and node purchase (for offerings)
    for _ in range(21):
        execute_test_image_search()
        time.sleep(6)
    for _ in range(21):
        execute_test_image_search()
        time.sleep(7)

def execute_test_image_search():
    offeringFound = True
    offeringName = "Bloody Party Streamers"
    while offeringFound:
        offeringFound = test_image_search('images/bloody_party_streamers.png', offeringFound, offeringName)

    # Test for "Escape! Cake"
    offeringFound = True
    offeringName = "Escape! Cake"
    while offeringFound:
        offeringFound = test_image_search('images/escape_cake.png', offeringFound, offeringName)

    # Test for "Survivor Pudding"
    offeringFound = True
    offeringName = "Survivor Pudding"
    while offeringFound:
        offeringFound = test_image_search('images/survivor_pudding.png', offeringFound, offeringName)
    
    # No offerings available. Proceed with pressing auto node.
    Clicker.automate_auto_bloodweb()

def test_image_search(image_path, offeringFound, offeringName):
    try:
        image = cv2.imread(resource_path(image_path))
        image_height, image_width = image.shape[:2]

        screenshot_np = py.screenshot().convert("RGB")
        screenshot_cv2 = cv2.cvtColor(np.array(screenshot_np), cv2.COLOR_RGB2BGR)

        result = cv2.matchTemplate(screenshot_cv2, image, cv2.TM_CCOEFF_NORMED)
        _, _, _, max_loc = cv2.minMaxLoc(result)

        threshold = 0.8

        if result[max_loc[1], max_loc[0]] >= threshold:
            center_x = max_loc[0] + image_width // 2
            center_y = max_loc[1] + image_height // 2
            py.moveTo(x=center_x, y=center_y)
            time.sleep(0.2)
            py.mouseDown(center_x, center_y)
            time.sleep(1.5)
            py.mouseUp()
            py.moveTo(1000, 150)
        else:
            offeringFound = False
    except:
        pass  # Error handling if needed
    return offeringFound

if __name__ == '__main__':
    print("Please switch to the Dead By Daylight application within 5 seconds.")
    time.sleep(5)
    execute_autoprestige()
