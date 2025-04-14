import requests
import tkinter as tk
from tkinter import messagebox
import webbrowser

if(True):
        result = messagebox.askquestion(
                "Update Available",
                f"A new version is available!\nWould you like to update?",
                icon='info'
            )
        if result == 'yes':
            pass
        else:
            pass