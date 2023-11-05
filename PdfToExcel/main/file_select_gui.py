import tkinter as tk
from datetime import datetime
from tkinter import filedialog


class FileSelectGUI:
    FRAME_WIDTH = 450
    FRAME_HEIGHT = 400
    DISTANCE_FROM_TOP = 100
    DISTANCE_FROM_LEFT = 400
    RESIZABLE_X = False
    RESIZABLE_Y = False

    RESULT_FILE_PREFIX = "extracted_pdfs-"
    DATE_TIME_FORMAT = "%d_%b_%Y-%H_%M_%S"


    def __init__(self):
        root = tk.Tk()
        self.root_frame = root
        self.file_paths_to_extract = set()

        # Configure window properties
        self.root_frame.title("Extract PDF to Excel")
        self.root_frame.geometry(f"{self.FRAME_WIDTH}x{self.FRAME_HEIGHT}+{self.DISTANCE_FROM_LEFT}+{self.DISTANCE_FROM_TOP}")
        self.root_frame.resizable(self.RESIZABLE_X, self.RESIZABLE_Y)

        # Create listbox to display file paths
        self.listbox = tk.Listbox(self.root_frame, width=70, height=14, font=8, xscrollcommand=True, yscrollcommand=True)
        self.listbox.pack(pady=10)

        # Create frame for buttons
        self.button_frame = tk.Frame(self.root_frame)
        self.button_frame.pack()

        # Create "Browse" button
        self.browse_button = tk.Button(self.button_frame, text="Select Files", command=self.browse_files, width=10)
        self.browse_button.pack(side=tk.LEFT, padx=5, pady=5)

        # Create "Save" button
        self.extract_button = tk.Button(self.button_frame, text="Extract", command=self.extract_paths, width=10)
        self.extract_button.pack(side=tk.LEFT, padx=5, pady=5)

        root.mainloop()

    def browse_files(self):
        # open dialog to select files that allows to select only pdf files
        selected_files = set(filedialog.askopenfilenames(filetypes=[("PDF files", "*.pdf")]))
        for file_path in selected_files:
            file_name = file_path.strip().split('/')[-1]
            self.listbox.insert(tk.END, file_name)
            self.file_paths_to_extract.add(file_path)

    def extract_paths(self):
        if not self.file_paths_to_extract:
            return

        self.extracted_file_name_with_path = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx")],
            initialfile=self.get_file_name()
        )

        if not self.extracted_file_name_with_path:
            return

        self.root_frame.quit()


    def get_file_name(self):
        current_date_time = datetime.now()
        formatted_date_time = current_date_time.strftime(self.DATE_TIME_FORMAT)
        return self.RESULT_FILE_PREFIX + formatted_date_time + ".xlsx"



# if __name__ == "__main__":
#     app = FileSelectGUI()
#
#     # After the GUI is closed, you can access the selected file paths
#     selected_paths = app.file_paths_to_extract
#     print(" File save to: " + app.file_with_path)
#     print("Selected paths:")
#     for path in selected_paths:
#         print(path)
