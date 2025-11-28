# main.py
# Main entry point for the GreenWave Conference System

import tkinter as tk
from view.gui import GreenWaveGUI

def main():
    root = tk.Tk()
    app = GreenWaveGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
