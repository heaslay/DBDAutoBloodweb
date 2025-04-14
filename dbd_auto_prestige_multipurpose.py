import pyautogui as py
import time
import cv2
import numpy as np
import os
import requests
import tkinter as tk
from tkinter import messagebox
import webbrowser
import sys
import time

__version__ = "v1.0.1"
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

def check_for_updates():
    """ Check for new GitHub releases after the script completes its task. """
    repo_url = "https://api.github.com/repos/heaslay/DBDAutoBloodweb/releases/latest"
    
    try:
        response = requests.get(repo_url)

        """if response.status_code == 404:
            # Handle the case where no releases are found
            root = tk.Tk()
            root.withdraw()  # Hide the root window
            messagebox.showinfo("No Updates Available", "There are no releases available at this time.")
            return""" #Might no longer be needed - there are releases on Github now.
        
        # Raise other potential errors (e.g., 500 server errors)
        response.raise_for_status()

        latest_release = response.json()

        # Extract the latest version and URL
        latest_version = latest_release.get("tag_name", "Unknown")
        release_url = latest_release.get("html_url", "")

        # Compare the current version with the latest version
        if latest_version != __version__:
            # Create a popup with options to Update or Cancel
            root = tk.Tk()
            root.withdraw()  # Hide the root window

            result = messagebox.askquestion(
                "Update Available",
                f"A new version ({latest_version}) is available!\nWould you like to update?",
                icon='info'
            )

            if result == 'yes':
                # Open the release page in the web browser
                webbrowser.open(release_url)
            else:
                # If the user clicks 'Cancel', exit silently
                return
        else:
            # If the current version is the latest, exit silently
            return
    except requests.RequestException as e:
        # Handle other errors (network issues, etc.)
        root = tk.Tk()
        root.withdraw()  # Hide the root window
        messagebox.showerror("Update Check Failed", "Could not check for updates. Please try again later.")

def resource_path(relative_path):
    """ Get the absolute path to the resource, works for both development and PyInstaller """
    try:
        base_path = sys._MEIPASS  # PyInstaller temporary folder
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def multi_scale_search(image, template, scales):
    """Search for the template at different scales to detect the correct UI scale."""
    for scale in scales:
        resized_template = cv2.resize(template, None, fx=scale, fy=scale)
        result = cv2.matchTemplate(image, resized_template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(result)
        if max_val > 0.8:  # Assuming 0.8 as the matching threshold
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
    else:
        print("Failed to detect UI scale.")

def execute_autoprestige():
    for _ in range(9):
        clicker.automate_auto_bloodweb()
        time.sleep(5.5)

    # Image search and node purchase (for offerings)
    for _ in range(21):
        execute_test_image_search()
        time.sleep(6.5)
    for _ in range(21):
        execute_test_image_search()
        time.sleep(7.5)

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
    clicker.automate_auto_bloodweb()

def test_image_search(image_path, offeringFound, offeringName):
    try:
        image = cv2.imread(resource_path(image_path))
        image_height, image_width = image.shape[:2]

        screenshot_np = py.screenshot().convert("RGB")
        screenshot_cv2 = cv2.cvtColor(np.array(screenshot_np), cv2.COLOR_RGB2BGR)
        resized_template = cv2.resize(image, None, fx=detected_ui_scale, fy=detected_ui_scale)
        result = cv2.matchTemplate(screenshot_cv2, resized_template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(result)

        if max_val > 0.75:
            center_x = max_loc[0] + image_width // 2
            center_y = max_loc[1] + image_height // 2
            py.moveTo(center_x, center_y)
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
    #start_time = time.time() - debug, testing for time (section start)
    print("Please switch to the Dead By Daylight application within 5 seconds.")
    time.sleep(5)
    detect_ui_scale('images/auto_purchase_node_withBG.png')
    clicker = Clicker(auto_purchase_coords)
    execute_autoprestige()
    check_for_updates()
    #end_time = time.time()
    #total_time = end_time - start_time
    #minutes, seconds = divmod(total_time, 60)
    #print(f"Execution finished in {int(minutes)} minutes and {seconds:.2f} seconds.") - debug, testing for time (section end)