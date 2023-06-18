import tkinter as tk
from tkinter import filedialog


class FileSelectGUI:
    WINDOW_WIDTH = 700
    WINDOW_HEIGHT = 400
    DISTANCE_FROM_TOP = 100
    DISTANCE_FROM_LEFT = 320
    RESIZABLE_X = False
    RESIZABLE_Y = False

    def __init__(self, root):
        self.root_frame = root
        self.saved_file_paths = set()

        # Configure window properties
        self.root_frame.title("Extract PDF to Excel")
        self.root_frame.geometry(
            f"{self.WINDOW_WIDTH}x{self.WINDOW_HEIGHT}+{self.DISTANCE_FROM_LEFT}+{self.DISTANCE_FROM_TOP}")
        self.root_frame.resizable(self.RESIZABLE_X, self.RESIZABLE_Y)

        # Create listbox to display file paths
        self.listbox = tk.Listbox(self.root_frame, width=70, height=14, font=8, xscrollcommand=True,
                                  yscrollcommand=True)
        self.listbox.pack(pady=10)

        # Create frame for buttons
        self.button_frame = tk.Frame(self.root_frame)
        self.button_frame.pack()

        # Create "Browse" button
        self.browse_button = tk.Button(self.button_frame, text="Select Files", command=self.browse_files, width=10)
        self.browse_button.pack(side=tk.LEFT, padx=5, pady=5)

        # Create "Save" button
        self.save_button = tk.Button(self.button_frame, text="Extract", command=self.save_paths, width=10)
        self.save_button.pack(side=tk.LEFT, padx=5, pady=5)

    def browse_files(self):
        selected_files = set(filedialog.askopenfilenames())
        for file_path in selected_files:
            if file_path not in self.saved_file_paths:
                self.listbox.insert(tk.END, file_path)
                self.saved_file_paths.add(file_path)

    def save_paths(self):
        # TODO
        self.root_frame.quit()


if __name__ == "__main__":
    root = tk.Tk()
    app = FileSelectGUI(root)
    root.mainloop()

    # After the GUI is closed, you can access the selected file paths
    selected_paths = app.saved_file_paths
    print("Selected paths:")
    for path in selected_paths:
        print(path)
