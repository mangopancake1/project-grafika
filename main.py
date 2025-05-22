import tkinter as tk
from ui import ShapeAppUI

def main():
    root = tk.Tk()
    root.title("Aplikasi Transformasi Objek 2D & 3D")
    app = ShapeAppUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
