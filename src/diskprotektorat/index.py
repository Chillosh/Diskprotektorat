import customtkinter
import pathlib
import string
from datetime import datetime
from ctypes import windll
customtkinter.set_appearance_mode("Dark")

frame = customtkinter.CTkFrame
font = "Arial"

def get_drives():
    drives = []
    bitmask = windll.kernel32.GetLogicalDrives()
    for letter in string.ascii_uppercase:
        if bitmask & 1:
            drives.append(f"{letter}:/")
        bitmask >>= 1
    return drives


def format_size(size):
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size < 1024: return f"{size:.1f} {unit}"
        size /= 1024
    return f"{size:.1f} TB"


class NavigationBar(frame):
    def __init__(self, master, callback, back_callback, add_tab_callback, **kwargs):
        super().__init__(master, fg_color="transparent", height=40, **kwargs)
        self.callback = callback
        customtkinter.CTkButton(self, text="home", width=30, command=lambda: self.callback(None)).pack(side="left", padx=2)
        customtkinter.CTkButton(self, text="back", width=30, command=back_callback).pack(side="left", padx=2)
        customtkinter.CTkButton(self, text="+ Tab", width=50, command=add_tab_callback).pack(side="left", padx=5)
        self.path_entry = customtkinter.CTkEntry(self, placeholder_text="C:/")
        self.path_entry.pack(side="left", fill="x", expand=True, padx=10, pady=5)
        self.path_entry.bind("<Return>", lambda e: self.callback(self.path_entry.get()))

class Sidebar(frame):
    def __init__(self, master, callback, **kwargs):
        super().__init__(master, width=200, corner_radius=0, **kwargs)
        self.callback = callback
        self.label = customtkinter.CTkLabel(self, text="Quick Access", font=(font, 12, "bold"))
        self.label.pack(pady=10)

        for drive in get_drives():
            btn = customtkinter.CTkButton(self, text=f"Disk {drive}", fg_color="transparent", anchor="w", command=lambda d=drive: self.callback(d))
            btn.pack(fill="x", padx=5)

        home = pathlib.Path.home()
        dirs = ["Downloads", "Documents", "Desktop", "Pictures", "Music"]
        for d_name in dirs:
            full_path = home / d_name
            if full_path.exists():
                customtkinter.CTkButton(self, text=d_name, fg_color="transparent", anchor="w", command=lambda p=full_path: self.callback(p)).pack(fill="x", padx=5)

class FileArea(customtkinter.CTkScrollableFrame):
    def __init__(self, master, callback, **kwargs):
        super().__init__(master, corner_radius=0, fg_color="#1a1a1a", **kwargs)
        self.callback = callback

    def refresh(self, path):
        for widget in self.winfo_children():
            widget.destroy()

        if path is None:
            for d in get_drives():
                self.render_item(pathlib.Path(d), True)
            return

        try:
            p = pathlib.Path(path)
            for item in p.iterdir():
                self.render_item(item)
        except Exception as e:
            customtkinter.CTkLabel(self, text=f"Error: {e}").pack()

    def render_item(self, item, is_drive=False):
        row = customtkinter.CTkFrame(self, fg_color="transparent")
        row.pack(fill="x", pady=1)

        try:
            s = item.stat()
            sz = format_size(s.st_size) if item.is_file() else "DIR"
            dt = datetime.fromtimestamp(s.st_mtime).strftime('%Y-%m-%d')
        except:
            sz, dt = "--", "--"

        color = "#1f538d" if item.is_dir() or is_drive else "#333333"
        display_name = item.name if not is_drive else f"Local Disk ({item})"

        btn = customtkinter.CTkButton(row, text=display_name, fg_color=color, anchor="w", width=350,
                                      command=lambda i=item: self.callback(i))
        btn.pack(side="left", padx=10, pady=2)

        customtkinter.CTkLabel(row, text=sz, width=80).pack(side="left", padx=5)
        customtkinter.CTkLabel(row, text=dt, width=120).pack(side="left", padx=5)


class Window(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("1100x700")
        self.title("Diskprotektorat")
        self.tab_map = {}

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.nav = NavigationBar(self, self.load_path, self.go_back, self.add_tab)
        self.nav.grid(row=0, column=0, columnspan=2, sticky="ew")

        self.sidebar = Sidebar(self, self.load_path)
        self.sidebar.grid(row=1, column=0, sticky="nsew")

        self.tabs = customtkinter.CTkTabview(self, command=self.update_ui_state)
        self.tabs.grid(row=1, column=1, sticky="nsew")

        self.add_tab()

    def add_tab(self):
        id = f"Tab {len(self.tab_map) + 1}"
        self.tabs.add(id)
        area = FileArea(self.tabs.tab(id), self.load_path)
        area.pack(fill="both", expand=True)
        self.tab_map[id] = {"area": area, "path": None}
        self.tabs.set(id)
        self.load_path(None)

    def go_back(self):
        active = self.tabs.get()
        curr = self.tab_map[active]["path"]
        if curr:
            parent = curr.parent
            self.load_path(None if parent == curr else parent)

    def update_ui_state(self):
        active = self.tabs.get()
        p = self.tab_map[active]["path"]
        self.nav.path_entry.delete(0, "end")
        self.nav.path_entry.insert(0, str(p) if p else "This PC")

    def load_path(self, path):
        active = self.tabs.get()
        if path in ["", "This PC", None]:
            p = None
        else:
            p = pathlib.Path(path)

        self.tab_map[active]["path"] = p
        self.tab_map[active]["area"].refresh(p)
        self.nav.path_entry.delete(0, "end")
        self.nav.path_entry.insert(0, str(p) if p else "This PC")
        self.tabs._segmented_button._buttons_dict[active].configure(text=p.name if p else "This PC")


def main():
    app = Window()
    app.mainloop()


if __name__ == "__main__":
    main()