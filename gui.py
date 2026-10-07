"""
gui.py

Phase 1 GUI for the CYOA Compendium Builder.

Features:

- Add TXT files
- Add folder of TXT files
- Remove selected files
- Optional cover image
- Anthology title
- Output PDF selection
- Build button

Designed for use with:
    models.py
    parser.py
    builder.py
"""

import os
import tkinter as tk

from tkinter import (
    filedialog,
    messagebox,
    ttk,
)

from parser import parse_story_files
from models import Anthology

# future import
# from builder import CompendiumBuilder


DEFAULT_TITLE = (
    "Collected Choose Your Own Adventures"
)


class CompendiumGUI:

    def __init__(self, root):

        self.root = root

        self.root.title(
            "CYOA Compendium Builder"
        )

        self.story_files = []

        self.cover_image = ""

        self._build_ui()

    # --------------------------------------------------
    # UI
    # --------------------------------------------------

    def _build_ui(self):

        outer = ttk.Frame(
            self.root,
            padding=10
        )

        outer.pack(
            fill="both",
            expand=True
        )

        ttk.Label(
            outer,
            text="Anthology Title"
        ).pack(
            anchor="w"
        )

        self.title_var = tk.StringVar(
            value=DEFAULT_TITLE
        )

        ttk.Entry(
            outer,
            textvariable=self.title_var,
            width=60
        ).pack(
            fill="x",
            pady=(0, 10)
        )

        # ------------------------------

        stories_frame = ttk.LabelFrame(
            outer,
            text="Stories"
        )

        stories_frame.pack(
            fill="both",
            expand=True,
            pady=5
        )

        self.story_list = tk.Listbox(
            stories_frame,
            height=15
        )

        self.story_list.pack(
            fill="both",
            expand=True,
            padx=5,
            pady=5
        )

        button_row = ttk.Frame(
            stories_frame
        )

        button_row.pack(
            fill="x"
        )

        ttk.Button(
            button_row,
            text="Add Files",
            command=self.add_files
        ).pack(
            side="left",
            padx=2
        )

        ttk.Button(
            button_row,
            text="Add Folder",
            command=self.add_folder
        ).pack(
            side="left",
            padx=2
        )

        ttk.Button(
            button_row,
            text="Remove Selected",
            command=self.remove_selected
        ).pack(
            side="left",
            padx=2
        )

        # ------------------------------

        cover_frame = ttk.LabelFrame(
            outer,
            text="Cover Image"
        )

        cover_frame.pack(
            fill="x",
            pady=5
        )

        self.cover_var = tk.StringVar()

        ttk.Entry(
            cover_frame,
            textvariable=self.cover_var
        ).pack(
            side="left",
            fill="x",
            expand=True,
            padx=5,
            pady=5
        )

        ttk.Button(
            cover_frame,
            text="Browse",
            command=self.select_cover
        ).pack(
            side="right",
            padx=5,
            pady=5
        )

        # ------------------------------

        output_frame = ttk.LabelFrame(
            outer,
            text="Output PDF"
        )

        output_frame.pack(
            fill="x",
            pady=5
        )

        self.output_var = tk.StringVar()

        ttk.Entry(
            output_frame,
            textvariable=self.output_var
        ).pack(
            side="left",
            fill="x",
            expand=True,
            padx=5,
            pady=5
        )

        ttk.Button(
            output_frame,
            text="Browse",
            command=self.select_output
        ).pack(
            side="right",
            padx=5,
            pady=5
        )

        # ------------------------------

        ttk.Button(
            outer,
            text="Generate Anthology",
            command=self.build_pdf
        ).pack(
            fill="x",
            pady=(10, 0)
        )

    # --------------------------------------------------
    # Files
    # --------------------------------------------------

    def add_files(self):

        files = filedialog.askopenfilenames(
            filetypes=[
                (
                    "Text Files",
                    "*.txt"
                )
            ]
        )

        if not files:
            return

        self.story_files.extend(files)

        self._refresh_story_list()

    def add_folder(self):

        folder = filedialog.askdirectory()

        if not folder:
            return

        txt_files = []

        for filename in os.listdir(folder):

            if filename.lower().endswith(
                ".txt"
            ):

                txt_files.append(
                    os.path.join(
                        folder,
                        filename
                    )
                )

        self.story_files.extend(
            txt_files
        )

        self._refresh_story_list()

    def remove_selected(self):

        selection = (
            self.story_list.curselection()
        )

        if not selection:
            return

        index = selection[0]

        del self.story_files[index]

        self._refresh_story_list()

    def _refresh_story_list(self):

        self.story_files = sorted(
            list(set(self.story_files)),
            key=lambda p:
                os.path.basename(
                    p
                ).lower()
        )

        self.story_list.delete(
            0,
            tk.END
        )

        for item in self.story_files:

            self.story_list.insert(
                tk.END,
                os.path.basename(
                    item
                )
            )

    # --------------------------------------------------
    # Cover
    # --------------------------------------------------

    def select_cover(self):

        filename = (
            filedialog.askopenfilename(
                filetypes=[
                    (
                        "Images",
                        "*.png *.jpg *.jpeg *.webp"
                    )
                ]
            )
        )

        if filename:

            self.cover_var.set(
                filename
            )

    # --------------------------------------------------
    # Output
    # --------------------------------------------------

    def select_output(self):

        filename = (
            filedialog.asksaveasfilename(
                defaultextension=".pdf"
            )
        )

        if filename:

            self.output_var.set(
                filename
            )

    # --------------------------------------------------
    # Build
    # --------------------------------------------------

    def build_pdf(self):

        if not self.story_files:

            messagebox.showwarning(
                "No Stories",
                "Please add at least one story."
            )

            return

        output_file = (
            self.output_var.get()
            .strip()
        )

        if not output_file:

            messagebox.showwarning(
                "No Output File",
                "Please choose an output PDF."
            )

            return

        anthology = Anthology(
            title=self.title_var.get()
            .strip()
        )

        anthology.cover_image = (
            self.cover_var.get()
            .strip()
        )

        stories, missing = (
            parse_story_files(
                self.story_files
            )
        )

        for story in stories:

            anthology.add_story(
                story
            )

        anthology.sort_by_filename()

        from builder import CompendiumBuilder

        builder = CompendiumBuilder()

        builder.build_pdf(
            anthology,
            output_file
        )

##        messagebox.showinfo(
##            "Phase 1",
##            (
##                "Anthology assembled.\n\n"
##                f"Stories: "
##                f"{anthology.total_story_count}\n"
##                f"Nodes: "
##                f"{anthology.total_node_count}\n\n"
##                "PDF build hook is ready "
##                "for builder.py integration."
##            )
##        )


def launch():

    root = tk.Tk()

    root.geometry(
        "800x650"
    )

    CompendiumGUI(
        root
    )

    root.mainloop()


if __name__ == "__main__":

    launch()
