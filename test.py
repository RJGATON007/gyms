import tkinter as tk
from tkinter import ttk


def button_click(row, col):
    print(f"Button clicked in cell ({row}, {col})")


root=tk.Tk()

# Create a Treeview widget
tree=ttk.Treeview(root, columns=("Column 1", "Column 2"))
tree.pack()

# Add a button to a specific cell (e.g., row=1, column=0)
button=ttk.Button(tree, text="Click Me", command=lambda: button_click(1, 0))
tree.insert("", "end", values=("Button 1", "Button 2", button))

root.mainloop()
