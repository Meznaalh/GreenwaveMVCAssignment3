# main.py
# --------------------------------------------------
# This file is the MAIN ENTRY POINT of the
# GreenWave Conference Ticketing System.
# It is responsible for launching the GUI window.
# --------------------------------------------------

import tkinter as tk                 # Import tkinter to create the main window
from view.gui import GreenWaveGUI    # Import the GUI class from the view layer (MVC)

def main():
    """
    This function initializes and starts the
    GreenWave Conference graphical user interface.
    """
    
    root = tk.Tk()                   # Create the main application window
    app = GreenWaveGUI(root)         # Create an instance of the GUI class
    root.mainloop()                  # Start the Tkinter event loop (keeps window running)

# --------------------------------------------------
# Program execution starts here
# --------------------------------------------------
if __name__ == "__main__":
    main()                           # Call the main function to launch the system
