import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from platform import system
import re

class CustomTextEditorMenu:
    def __init__(self, parent):
        font_styles = ("calibri", 12)

        menu_bar = tk.Menu(parent.master, font=font_styles)
        parent.master.config(menu=menu_bar)

        file_menu = tk.Menu(menu_bar, font=font_styles, tearoff=0)
        file_menu.add_command(label="New Document", accelerator="Command+N", command=parent.new_document)
        file_menu.add_command(label="Open Document", accelerator="Command+O", command=parent.open_document)
        file_menu.add_command(label="Save", accelerator="Command+S", command=parent.save)
        file_menu.add_command(label="Save As", accelerator="Command+Shift+S", command=parent.save_as)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=parent.exit_application)

        edit_menu = tk.Menu(menu_bar, font=font_styles, tearoff=0)
        edit_menu.add_command(label="Undo", accelerator="Command+Z", command=parent.undo)
        edit_menu.add_command(label="Redo", accelerator="Command+Y", command=parent.redo)
        edit_menu.add_separator()
        edit_menu.add_command(label="Find", accelerator="Command+F", command=parent.find)
        edit_menu.add_command(label="Replace", accelerator="Command+R", command=parent.replace)
        edit_menu.add_separator()
        edit_menu.add_command(label="Bold", accelerator="Command+B", command=parent.toggle_bold)
        edit_menu.add_command(label="Italic", accelerator="Command+I", command=parent.toggle_italic)
        edit_menu.add_command(label="Underline", accelerator="Command+U", command=parent.toggle_underline)

        about_menu = tk.Menu(menu_bar, font=font_styles, tearoff=0)
        about_menu.add_command(label="Release Notes", command=self.show_release_notes)
        about_menu.add_separator()
        about_menu.add_command(label="About", command=self.show_about_message)

        menu_bar.add_cascade(label="File", menu=file_menu)
        menu_bar.add_cascade(label="Edit", menu=edit_menu)
        menu_bar.add_cascade(label="About", menu=about_menu)

    def show_about_message(self):
        title = "About Custom Text Editor"
        message = "A simple Python Text Editor"
        messagebox.showinfo(title, message)

    def show_release_notes(self):
        title = "Release Notes"
        message = "Version 2.0 - Text Editor"
        messagebox.showinfo(title, message)

class CustomTextEditorStatusBar:
    def __init__(self, parent):
        font_styles = ("calibri", 12)
        self.status_var = tk.StringVar()
        self.status_var.set("Custom Text Editor - Version 2.0")

        self.word_count_var = tk.StringVar()
        self.word_count_var.set("Word Count: 0")

        status_label = tk.Label(parent.text_area, textvariable=self.status_var, fg="black", bg="lightgrey", anchor='sw', font=font_styles)
        status_label.pack(side=tk.BOTTOM, fill=tk.BOTH)

        word_count_label = tk.Label(parent.text_area, textvariable=self.word_count_var, fg="black", bg="lightgrey", anchor='se', font=font_styles)
        word_count_label.pack(side=tk.BOTTOM, fill=tk.BOTH)

    def update_status(self, *args):
        if isinstance(args[0], bool):
            self.status_var.set("Your Document Has Been Saved!")
        else:
            self.status_var.set("Custom Text Editor - Version 2.0")
        # Update word count
        words = re.findall(r'\w+', parent_editor.text_area.get(1.0, tk.END))
        self.word_count_var.set(f"Word Count: {len(words)}")

class CustomTextEditor:
    def __init__(self, master):
        master.title("Untitled - Custom Text Editor")
        master.geometry("1200x700")
        font_styles = ("calibri", 18)

        self.master = master
        self.file_name = None
        self.text_changed = False

        self.text_area = tk.Text(master, font=font_styles, undo=True, wrap="word")
        self.scroll_bar = tk.Scrollbar(master, command=self.text_area.yview)
        self.text_area.configure(yscrollcommand=self.scroll_bar.set)
        self.text_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scroll_bar.pack(side=tk.RIGHT, fill=tk.Y)

        self.menu = CustomTextEditorMenu(self)
        self.status_bar = CustomTextEditorStatusBar(self)

        self.bind_shortcuts()
        self.set_window_title()

        # Binding for undo and redo
        self.text_area.bind('<Command-z>', self.undo)
        self.text_area.bind('<Command-y>', self.redo)
        # Binding for find and replace
        self.text_area.bind('<Command-f>', self.find)
        self.text_area.bind('<Command-r>', self.replace)
        # Binding for text formatting
        self.text_area.tag_configure("bold", font=(font_styles[0], font_styles[1], "bold"))
        self.text_area.tag_configure("italic", font=(font_styles[0], font_styles[1], "italic"))
        self.text_area.tag_configure("underline", underline=True)
        self.text_area.bind('<Command-b>', self.toggle_bold)
        self.text_area.bind('<Command-i>', self.toggle_italic)
        self.text_area.bind('<Command-u>', self.toggle_underline)
        # Binding for font size change
        if system() == "Darwin":
            self.text_area.bind('<Command-=>', self.increase_font_size)
        else:
            self.text_area.bind('<Command-plus>', self.increase_font_size)
        self.text_area.bind('<Command-minus>', self.decrease_font_size)

        # Binding for detecting text changes
        self.text_area.bind("<KeyRelease>", self.text_modified)
        self.text_area.bind("<KeyRelease>", self.update_word_count)

    def set_window_title(self, name=None):
        if name:
            self.master.title(name + " - Custom Text Editor")
        else:
            self.master.title("Untitled - Custom Text Editor")

    def new_document(self, *args):
        if self.text_changed:
            confirmation = messagebox.askyesnocancel("Unsaved Changes", "Do you want to save the changes?")
            if confirmation is None:
                return
            elif confirmation:
                self.save()
        self.text_area.delete(1.0, tk.END)
        self.file_name = None
        self.text_changed = False
        self.set_window_title()

    def open_document(self, *args):
        if self.text_changed:
            confirmation = messagebox.askyesnocancel("Unsaved Changes", "Do you want to save the changes?")
            if confirmation is None:
                return
            elif confirmation:
                self.save()
        self.file_name = filedialog.askopenfilename(
            defaultextension=".txt",
            filetypes=[("All Files", "*.*"),
                       ("Text Files", "*.txt"),
                       ("Python Scripts", "*.py"),
                       ("Markdown Documents", "*.md"),
                       ("JavaScript Files", "*.js"),
                       ("HTML Documents", "*.html"),
                       ("CSS Documents", "*.css")])
        if self.file_name:
            self.text_area.delete(1.0, tk.END)
            with open(self.file_name, "r") as file:
                self.text_area.insert(1.0, file.read())
            self.set_window_title(self.file_name)
            self.text_changed = False

    def save(self, *args):
        if self.file_name:
            try:
                text_area_content = self.text_area.get(1.0, tk.END)
                with open(self.file_name, "w") as file:
                    file.write(text_area_content)
                self.text_changed = False
                self.status_bar.update_status(True)
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred while saving the document: {e}")
        else:
            self.save_as()

    def save_as(self, *args):
        try:
            new_file = filedialog.asksaveasfilename(
                initialfile="Untitled.txt",
                defaultextension=".txt",
                filetypes=[("All Files", "*.*"),
                           ("Text Files", "*.txt"),
                           ("Python Scripts", "*.py"),
                           ("Markdown Documents", "*.md"),
                           ("JavaScript Files", "*.js"),
                           ("HTML Documents", "*.html"),
                           ("CSS Documents", "*.css")])
            if not new_file:
                return
            text_area_content = self.text_area.get(1.0, tk.END)
            with open(new_file, "w") as file:
                file.write(text_area_content)
            self.file_name = new_file
            self.set_window_title(self.file_name)
            self.text_changed = False
            self.status_bar.update_status(True)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while saving the document: {e}")

    def text_modified(self, *args):
        self.text_changed = True

    def undo(self, *args):
        try:
            self.text_area.event_generate("<<Undo>>")
        except tk.TclError:
            pass

    def redo(self, *args):
        try:
            self.text_area.event_generate("<<Redo>>")
        except tk.TclError:
            pass

    def find(self, *args):
        find_str = simpledialog.askstring("Find", "Enter text to find:")
        if find_str:
            start_pos = self.text_area.search(find_str, "1.0", tk.END)
            if start_pos:
                end_pos = f"{start_pos}+{len(find_str)}c"
                self.text_area.tag_remove(tk.SEL, "1.0", tk.END)
                self.text_area.tag_add(tk.SEL, start_pos, end_pos)
                self.text_area.mark_set(tk.INSERT, start_pos)
                self.text_area.see(tk.INSERT)

    def replace(self, *args):
        find_str = simpledialog.askstring("Find", "Enter text to find:")
        if find_str:
            replace_str = simpledialog.askstring("Replace", f"Replace '{find_str}' with:")
            if replace_str:
                start_pos = self.text_area.search(find_str, "1.0", tk.END)
                while start_pos:
                    end_pos = f"{start_pos}+{len(find_str)}c"
                    self.text_area.delete(start_pos, end_pos)
                    self.text_area.insert(start_pos, replace_str)
                    start_pos = self.text_area.search(find_str, end_pos, tk.END)

    def toggle_bold(self, *args):
        self.toggle_text_tag("bold")

    def toggle_italic(self, *args):
        self.toggle_text_tag("italic")

    def toggle_underline(self, *args):
        self.toggle_text_tag("underline")

    def increase_font_size(self, *args):
        current_size = int(self.text_area.cget("font").split(" ")[1])
        new_size = min(current_size + 2, 36)
        self.text_area.configure(font=("calibri", new_size))

    def decrease_font_size(self, *args):
        current_size = int(self.text_area.cget("font").split(" ")[1])
        new_size = max(current_size - 2, 6)
        self.text_area.configure(font=("calibri", new_size))

    def toggle_text_tag(self, tag):
        current_tags = self.text_area.tag_names(tk.SEL_FIRST)
        if tag in current_tags:
            self.text_area.tag_remove(tag, tk.SEL_FIRST, tk.SEL_LAST)
        else:
            self.text_area.tag_add(tag, tk.SEL_FIRST, tk.SEL_LAST)

    def bind_shortcuts(self):
        self.text_area.bind('<Command-n>', self.new_document)
        self.text_area.bind('<Command-o>', self.open_document)
        self.text_area.bind('<Command-s>', self.save)
        self.text_area.bind('<Command-S>', self.save_as)
        self.text_area.bind('<Key>', self.status_bar.update_status)

    def exit_application(self):
        if self.text_changed:
            confirmation = messagebox.askyesnocancel("Unsaved Changes", "Do you want to save the changes?")
            if confirmation is None:
                return
            elif confirmation:
                self.save()
        self.master.destroy()

    def update_word_count(self, *args):
        words = re.findall(r'\w+', self.text_area.get(1.0, tk.END))
        self.status_bar.word_count_var.set(f"Word Count: {len(words)}")

if __name__ == "__main__":
    master = tk.Tk()
    text_editor = CustomTextEditor(master)
    master.protocol("WM_DELETE_WINDOW", text_editor.exit_application)
    master.mainloop()
