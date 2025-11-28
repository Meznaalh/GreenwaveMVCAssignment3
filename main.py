# main.py
# Main entry point for the GreenWave Conference Ticketing System

import tkinter as tk
from view.gui import GreenWaveGUI

def main():
    """Starts the GreenWave Conference GUI application"""
    root = tk.Tk()
    app = GreenWaveGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
