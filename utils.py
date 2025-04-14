import cv2
import pyautogui as py
import numpy as np
import sys
import os
import time
import requests
import tkinter as tk
from tkinter import messagebox
import webbrowser

# Global variables
detected_ui_scale = None
auto_purchase_coords = None

class Clicker:
    def __init__(self, auto_purchase_coords):
        self.auto_purchase_coords = auto_purchase_coords
        py.FAILSAFE = True

    def automate_auto_bloodweb(self):
        """Move to the detected auto-purchase node coordinates and perform the action."""
        if self.auto_purchase_coords:
            try:
                py.moveTo(self.auto_purchase_coords)
                time.sleep(0.2)
                py.mouseDown()
                time.sleep(0.2)
                py.mouseUp()
                py.moveTo(1000, 150)
            except:
                pass
        else:
            print("Error: Auto-purchase node coordinates not set.")

def check_for_updates(current_version):
    """ Check for new GitHub releases after the script completes its task. """
    repo_url = "https://api.github.com/repos/heaslay/DBDAutoBloodweb/releases/latest"
    
    try:
        response = requests.get(repo_url)
        response.raise_for_status()

        latest_release = response.json()
        latest_version = latest_release.get("tag_name", "Unknown")
        release_url = latest_release.get("html_url", "")

        if latest_version != current_version:
            root = tk.Tk()
            root.withdraw()

            result = messagebox.askquestion(
                "Update Available",
                f"A new version ({latest_version}) is available!\nWould you like to update?",
                icon='info'
            )

            if result == 'yes':
                webbrowser.open(release_url)
            else:
                return
        else:
            return
    except requests.RequestException as e:
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror("Update Check Failed", "Could not check for updates. Please try again later.")

def resource_path(relative_path):
    """ Get the absolute path to the resource, works for both development and PyInstaller """
    try:
        base_path = sys._MEIPASS  # PyInstaller temporary folder
    except Exception:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)

def multi_scale_search(image, template, scales):
    """Search for the template at different scales to detect the correct UI scale."""
    for scale in scales:
        resized_template = cv2.resize(template, None, fx=scale, fy=scale)
        result = cv2.matchTemplate(image, resized_template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(result)
        if max_val > 0.8:  # Adjust threshold if necessary
            return max_loc, scale
    return None, None

def detect_ui_scale(template_path):
    """Detect the UI scale by searching for the auto-purchase node."""
    global detected_ui_scale, auto_purchase_coords

    # Take a screenshot
    screen = py.screenshot()
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
        auto_purchase_coords = (center_x, center_y)  # Store the coordinates of the node
        print(f"UI scale detected: {scale}. Auto-purchase node at ({center_x}, {center_y})")
        return detected_ui_scale, auto_purchase_coords
    else:
        print("Failed to detect UI scale.")
        return None, None

def test_image_search(image_path, detected_ui_scale):
    """Search for the offering image using the detected UI scale."""
    # Take a screenshot of the game
    screen = py.screenshot()
    screen_np = np.array(screen)
    gray_screen = cv2.cvtColor(screen_np, cv2.COLOR_RGB2GRAY)

    # Load the offering template
    template = cv2.imread(image_path)

    # Resize the template using the detected scale
    resized_template = cv2.resize(template, None, fx=detected_ui_scale, fy=detected_ui_scale)
    gray_template = cv2.cvtColor(resized_template, cv2.COLOR_BGR2GRAY)

    # Perform template matching at the known scale
    result = cv2.matchTemplate(gray_screen, gray_template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(result)

    if max_val > 0.75:
        template_height, template_width = resized_template.shape[:2]
        center_x = max_loc[0] + int(template_width // 2)
        center_y = max_loc[1] + int(template_height // 2)
        py.moveTo(center_x, center_y)
        time.sleep(0.2)
        py.mouseDown(center_x, center_y)
        time.sleep(1.5)
        py.mouseUp()
        py.moveTo(1000, 150)
        offeringName1 = image_path.split('.')[0] #debug
        offeringName = offeringName1.split('/')[1] #debug
        print(f'Found {offeringName}. Confidence: {max_val}') #debug
        return True
    else:
        return False

def execute_autoprestige(clicker):
    """Perform the auto-prestige functionality."""
    for _ in range(9):
        clicker.automate_auto_bloodweb()
        time.sleep(5.5)

    for _ in range(21):
        execute_test_image_search(clicker)
        time.sleep(6.5)

    for _ in range(21):
        execute_test_image_search(clicker)
        time.sleep(7.5)

def execute_full_auto(clicker):
    """Perform full auto prestiging."""
    for _ in range(9):
        clicker.automate_auto_bloodweb()
        time.sleep(5.5)

    for _ in range(21):
        clicker.automate_auto_bloodweb()
        time.sleep(6.5)

    for _ in range(21):
        clicker.automate_auto_bloodweb()
        time.sleep(7.5)

def execute_test_image_search(clicker):
    """Run the image search process for various offerings."""
    offerings = ['ibovd2.png', 'bloody_party_streamers.png', 'bound_envelope.png', 
                 'escape_cake2.png', 'survivor_pudding.png', 'sealed_envelope.png', 'hollow_shell2.png']
    for offering in offerings:
        offeringFound = True
        while offeringFound:
            image_path = resource_path(os.path.join('images', offering))
            offeringFound = test_image_search(image_path, detected_ui_scale)
    clicker.automate_auto_bloodweb()
