import tkinter as tk                     # Import the tkinter library to create the GUI window
from view.gui import GreenWaveGUI       # Import the main GUI class from the view folder

def main():
    """
    This is the main entry point of the program.
    It creates the main window and launches the GUI.
    """

    root = tk.Tk()                       # Create the main application window
    app = GreenWaveGUI(root)             # Create an object of the GUI class and attach it to the window
    root.mainloop()                      # Start the event loop to keep the window running

# This condition ensures that main() runs only when this file is executed directly,
# and not when it is imported into another file.
if __name__ == "__main__":
    main()                              # Call the main function to start the program
