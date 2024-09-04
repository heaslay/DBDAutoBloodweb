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

__version__ = "v1.0.1"

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

def check_for_updates():
    """ Check for new GitHub releases after the script completes its task. """
    repo_url = "https://api.github.com/repos/heaslay/DBDAutoBloodweb/releases/latest"
    
    try:
        response = requests.get(repo_url)

        if response.status_code == 404:
            # Handle the case where no releases are found
            root = tk.Tk()
            root.withdraw()  # Hide the root window
            messagebox.showinfo("No Updates Available", "There are no releases available at this time.")
            return
        
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
    clicker = Clicker('images/auto_purchase_node.png')
    print("Please switch to the Dead By Daylight application within 5 seconds.")
    time.sleep(5)
    execute_autoprestige()
    check_for_updates()